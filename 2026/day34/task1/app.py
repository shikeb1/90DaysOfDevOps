import os
import string
import random
import psycopg2
import redis
import json
from datetime import datetime
from flask import Flask, request, redirect, jsonify, render_template_string

app = Flask(__name__)

# --- Connections ---

def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"])

cache = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0"))

CACHE_TTL = 300  # 5 minutes

# --- DB Setup ---

def init_db():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id        SERIAL PRIMARY KEY,
                    code      VARCHAR(8) UNIQUE NOT NULL,
                    long_url  TEXT NOT NULL,
                    clicks    INTEGER DEFAULT 0,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
        conn.commit()

# --- Helpers ---

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

# --- Routes ---

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>URL Shortener</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f5f5f4;
      color: #1c1c1a;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 60px 16px 40px;
    }
    h1 { font-size: 28px; font-weight: 600; margin-bottom: 6px; }
    .subtitle { color: #6b6b67; font-size: 14px; margin-bottom: 36px; }
    .card {
      background: #fff;
      border: 1px solid #e4e4e0;
      border-radius: 12px;
      padding: 28px;
      width: 100%;
      max-width: 560px;
      margin-bottom: 16px;
    }
    .row { display: flex; gap: 10px; }
    input[type=text] {
      flex: 1;
      border: 1px solid #d4d4d0;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 14px;
      outline: none;
      transition: border-color .15s;
    }
    input[type=text]:focus { border-color: #7c3aed; }
    button {
      background: #7c3aed;
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 10px 20px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: background .15s;
    }
    button:hover { background: #6d28d9; }
    .result {
      margin-top: 18px;
      background: #f3f0ff;
      border: 1px solid #ddd6fe;
      border-radius: 8px;
      padding: 14px 16px;
      display: none;
    }
    .result.show { display: block; }
    .result a { color: #6d28d9; font-weight: 500; text-decoration: none; font-size: 15px; }
    .result a:hover { text-decoration: underline; }
    .result .label { font-size: 12px; color: #6b6b67; margin-bottom: 4px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th { text-align: left; padding: 8px 10px; color: #6b6b67; font-weight: 500;
         border-bottom: 1px solid #e4e4e0; }
    td { padding: 10px 10px; border-bottom: 1px solid #f0f0ee; vertical-align: middle; }
    tr:last-child td { border-bottom: none; }
    td a { color: #7c3aed; text-decoration: none; }
    td a:hover { text-decoration: underline; }
    .badge {
      background: #f3f0ff; color: #6d28d9;
      border-radius: 999px; padding: 2px 8px;
      font-size: 12px; font-weight: 500;
    }
    .long-url { max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #6b6b67; }
    h2 { font-size: 16px; font-weight: 600; margin-bottom: 16px; }
    .empty { color: #9b9b97; font-size: 13px; text-align: center; padding: 20px 0; }
    .tag { font-size: 11px; background: #dcfce7; color: #166534;
           border-radius: 4px; padding: 1px 6px; margin-left: 6px; }
    .tag.miss { background: #fef9c3; color: #854d0e; }
  </style>
</head>
<body>
  <h1>🔗 URL Shortener</h1>
  <p class="subtitle">Flask · PostgreSQL · Redis</p>

  <div class="card">
    <div class="row">
      <input type="text" id="url-input" placeholder="https://example.com/very/long/url" />
      <button onclick="shorten()">Shorten</button>
    </div>
    <div class="result" id="result">
      <div class="label">Your short URL</div>
      <a id="short-link" href="#" target="_blank"></a>
    </div>
  </div>

  <div class="card">
    <h2>Recent links</h2>
    <div id="links-table"><div class="empty">No links yet.</div></div>
  </div>

  <script>
    const base = window.location.origin;

    async function shorten() {
      const url = document.getElementById('url-input').value.trim();
      if (!url) return;
      const res = await fetch('/api/shorten', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      const data = await res.json();
      if (data.short_url) {
        const el = document.getElementById('short-link');
        el.href = data.short_url;
        el.textContent = data.short_url;
        document.getElementById('result').classList.add('show');
        loadLinks();
      } else {
        alert(data.error || 'Something went wrong');
      }
    }

    async function loadLinks() {
      const res = await fetch('/api/links');
      const links = await res.json();
      const el = document.getElementById('links-table');
      if (!links.length) { el.innerHTML = '<div class="empty">No links yet.</div>'; return; }
      el.innerHTML = `
        <table>
          <thead><tr><th>Code</th><th>Destination</th><th>Clicks</th><th>Cache</th></tr></thead>
          <tbody>${links.map(l => `
            <tr>
              <td><a href="/${l.code}" target="_blank">/${l.code}</a></td>
              <td><div class="long-url" title="${l.long_url}">${l.long_url}</div></td>
              <td><span class="badge">${l.clicks}</span></td>
              <td><span class="tag ${l.cached ? '' : 'miss'}">${l.cached ? 'HIT' : 'MISS'}</span></td>
            </tr>`).join('')}
          </tbody>
        </table>`;
    }

    document.getElementById('url-input').addEventListener('keydown', e => {
      if (e.key === 'Enter') shorten();
    });

    loadLinks();
    setInterval(loadLinks, 5000);
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.get_json(force=True)
    long_url = (data.get("url") or "").strip()

    if not long_url:
        return jsonify({"error": "URL is required"}), 400
    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url

    # Generate a unique code
    for _ in range(5):
        code = generate_code()
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO urls (code, long_url) VALUES (%s, %s)",
                        (code, long_url)
                    )
                conn.commit()
            # Warm the cache immediately
            cache.setex(f"url:{code}", CACHE_TTL, long_url)
            break
        except psycopg2.errors.UniqueViolation:
            continue
    else:
        return jsonify({"error": "Could not generate unique code"}), 500

    short_url = request.host_url.rstrip("/") + "/" + code
    return jsonify({"code": code, "short_url": short_url})


@app.route("/<code>")
def redirect_url(code):
    cache_key = f"url:{code}"

    # 1. Try Redis first
    cached = cache.get(cache_key)
    if cached:
        long_url = cached.decode()
        # Async-ish: increment click count in DB
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE urls SET clicks = clicks + 1 WHERE code = %s", (code,))
            conn.commit()
        return redirect(long_url)

    # 2. Cache miss — hit Postgres
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE urls SET clicks = clicks + 1 WHERE code = %s RETURNING long_url",
                (code,)
            )
            row = cur.fetchone()
        conn.commit()

    if not row:
        return "Short URL not found", 404

    long_url = row[0]
    # Populate cache for next time
    cache.setex(cache_key, CACHE_TTL, long_url)
    return redirect(long_url)


@app.route("/api/links")
def list_links():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT code, long_url, clicks, created_at FROM urls ORDER BY created_at DESC LIMIT 20"
            )
            rows = cur.fetchall()

    links = []
    for code, long_url, clicks, created_at in rows:
        cached = cache.exists(f"url:{code}") == 1
        links.append({
            "code": code,
            "long_url": long_url,
            "clicks": clicks,
            "cached": cached,
            "created_at": created_at.isoformat(),
        })
    return jsonify(links)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
