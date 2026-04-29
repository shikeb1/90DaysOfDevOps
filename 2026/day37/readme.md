# Day 37 – Docker Revision & Cheat Sheet

## 📌 Goal

Take a one-day pause to revise everything from Days 29–36 so Docker concepts become permanent.

---

# 📁 Files to Submit

* `docker-cheatsheet.md`
* `day-37-revision.md`

Path:

```text
2026/day-37/
```

---

# ✅ Self-Assessment Checklist

| Topic                                | Status |
| ------------------------------------ | ------ |
| Run a container from Docker Hub      | Can Do |
| List, stop, remove containers/images | Can Do |
| Explain image layers & cache         | Can Do |
| Write Dockerfile from scratch        | Can Do |
| CMD vs ENTRYPOINT                    | Shaky  |
| Build and tag image                  | Can Do |
| Named volumes                        | Can Do |
| Bind mounts                          | Can Do |
| Custom networks                      | Can Do |
| docker-compose multi-container       | Can Do |
| Env vars and .env in Compose         | Can Do |
| Multi-stage Dockerfile               | Can Do |
| Push image to Docker Hub             | Can Do |
| Healthchecks & depends_on            | Shaky  |

---

# ⚡ Quick-Fire Answers

## 1. Difference between image and container?

* **Image** = blueprint/template
* **Container** = running instance of image

## 2. What happens to data after removing container?

Container data is lost unless stored in volume/bind mount.

## 3. How do two containers communicate on same custom network?

Using container/service name as hostname.

## 4. `docker compose down -v` vs `docker compose down`

* `down` removes containers + network
* `down -v` also removes volumes

## 5. Why multi-stage builds useful?

Smaller, cleaner, secure production images.

## 6. Difference between COPY and ADD?

* `COPY` = simple file copy
* `ADD` = copy + auto extract tar + URL support

## 7. What does `-p 8080:80` mean?

Host port `8080` → Container port `80`

## 8. Check Docker disk usage?

```bash
docker system df
```

---

# 📘 docker-cheatsheet.md

## 🚀 Container Commands

```bash
docker run -it ubuntu bash      # interactive
docker run -d nginx            # detached
docker ps                      # running containers
docker ps -a                   # all containers
docker stop <id>
docker rm <id>
docker exec -it <id> bash
docker logs <id>
```

---

## 🐳 Image Commands

```bash
docker build -t app:v1 .
docker pull nginx
docker push username/app:v1
docker tag app:v1 username/app:v1
docker images
docker rmi <image>
```

---

## 💾 Volume Commands

```bash
docker volume create myvol
docker volume ls
docker volume inspect myvol
docker volume rm myvol
```

---

## 🌐 Network Commands

```bash
docker network create mynet
docker network ls
docker network inspect mynet
docker network connect mynet container1
```

---

## ⚙️ Compose Commands

```bash
docker compose up -d
docker compose down
docker compose ps
docker compose logs -f
docker compose build
```

---

## 🧹 Cleanup Commands

```bash
docker system df
docker container prune
docker image prune
docker volume prune
docker system prune -a
```

---

## 🏗 Dockerfile Instructions

```dockerfile
FROM ubuntu
RUN apt update
COPY . /app
WORKDIR /app
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
ENTRYPOINT ["python"]
```

---

# 🔁 Weak Areas Revisited

## 1. CMD vs ENTRYPOINT

```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```

Run:

```bash
docker run image test.py
```

Output:

```text
python test.py
```

---

## 2. Healthchecks

```yaml
services:
  db:
    image: mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
```

---

# ⏱ Suggested Flow

* 10 min checklist
* 10 min quick-fire
* 20 min cheat sheet
* 10 min weak topics revision

---

# 📤 Submission

```bash
git add .
git commit -m "Add Day 37 Docker revision and cheatsheet"
git push
```

---

# 🚀 Learn in Public

Post on LinkedIn:

> Revised full Docker in one day. Built my own cheat sheet and tested myself.

---

# 👤 Author

Shikeb Malik

#90DaysOfDevOps #Docker #DevOps #Revision #CheatSheet

