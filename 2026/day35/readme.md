# Day 35 – Multi-Stage Builds & Docker Hub

## 📌 Objective

Today's goal was to learn how to build smaller, optimized Docker images using Multi-Stage Builds and publish them to Docker Hub.

Multi-stage builds reduce image size, improve security, and speed up deployments.

---

## 🧠 Concepts Learned

* Single-stage vs Multi-stage Docker builds
* Reducing image size
* Using minimal base images
* Running containers as non-root user
* Tagging and pushing images to Docker Hub
* Understanding Docker tags and versioning

---

## ✅ Task 1: Problem with Large Images

### Single Stage Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Build Image

```bash
docker build -t flaskapp-single:v1 .
docker images
```

---

## ✅ Task 2: Multi-Stage Build

### Optimized Dockerfile

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
COPY . .

FROM python:3.12-alpine

RUN adduser -D appuser

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
```

### Build Multi-stage Image

```bash
docker build -t flaskapp-multi:v1 .
docker images
```

### Example Comparison

| Image           | Size  |
| --------------- | ----- |
| flaskapp-single | 180MB |
| flaskapp-multi  | 65MB  |

### Why Smaller?

The final image contains only runtime dependencies and application code.
It does not include build tools, cache files, temporary layers, or extra packages.

---

## ✅ Task 3: Push to Docker Hub

```bash
docker login
docker build -t shikeb1/flaskapp1:v1 .
docker push shikeb1/flaskapp1:v1
docker rmi shikeb1/flaskapp1:v1
docker pull shikeb1/flaskapp1:v1
```

---

## ✅ Task 4: Docker Hub Repository

Repository: `shikeb1/flaskapp1`

### Tags

* latest
* v1
* v2
* prod
* dev

### Pull Specific Tag

```bash
docker pull shikeb1/flaskapp1:v1
```

### Pull Latest

```bash
docker pull shikeb1/flaskapp1:latest
```

### Difference

* `v1` pulls exact version
* `latest` pulls image tagged latest

---

## ✅ Task 5: Image Best Practices

* Use minimal base image (`python:3.12-alpine`)
* Use non-root user
* Combine RUN commands
* Use specific versions instead of latest

```dockerfile
RUN adduser -D appuser
USER appuser
```

---

## 🧹 Useful Commands

```bash
docker images
docker ps
docker build -t image:tag .
docker login
docker push username/repo:tag
docker pull username/repo:tag
docker rmi image:tag
```

---

## 🎯 Key Learnings

* Multi-stage builds create smaller images.
* Smaller images deploy faster.
* Docker Hub stores and shares images.
* Tags help with version control.
* Non-root containers are safer.

---

## 🚀 Final Aha Moment

Using multi-stage builds can reduce image size massively while improving security and speed.

---

## 👤 Author

Shikeb Malik

#90DaysOfDevOps #Docker #DockerHub #DevOps #MultiStageBuild

