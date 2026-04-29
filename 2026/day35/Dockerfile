# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /day35

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .

# Stage 2
FROM python:3.12-alpine

RUN adduser -D appuser

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /day35 /day35

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
