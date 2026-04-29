# Docker Complete Deep Revision Guide (One Click Copy)

# 1️⃣ Run a container from Docker Hub (Interactive + Detached)

## What is Docker Hub?

Docker Hub is an online registry where ready-made images are stored.

Examples:

* ubuntu
* nginx
* mysql
* redis
* node

---

## Interactive Mode

Used when you want to enter inside container terminal.

```bash id="dr8utg"
docker run -it ubuntu bash
```

### Meaning:

* `run` = create + start container
* `-i` = interactive input
* `-t` = terminal
* `ubuntu` = image
* `bash` = shell inside container

---

## Detached Mode

Runs in background.

```bash id="5j0rjp"
docker run -d --name web nginx
```

### Meaning:

* `-d` = detached/background
* `--name web` = custom name
* `nginx` = web server image

Check:

```bash id="nqlxv0"
docker ps
```

---

# 2️⃣ List, Stop, Remove Containers and Images

## Containers

```bash id="pyk0x0"
docker ps
```

Running containers.

```bash id="bljjlwm"
docker ps -a
```

All containers.

```bash id="ivb2e1"
docker stop web
```

Stop container.

```bash id="zhy7pt"
docker rm web
```

Remove container.

---

## Images

```bash id="65wx6l"
docker images
```

List images.

```bash id="vtf4hf"
docker rmi nginx
```

Delete image.

---

# 3️⃣ Explain Image Layers and Caching

Docker image is made of layers.

Example Dockerfile:

```dockerfile id="eek64v"
FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
```

Each command creates layer:

1. Base OS
2. Workdir
3. package.json copy
4. npm install
5. source code

## Cache Working

If only source code changes:

```dockerfile id="l8pr81"
COPY . .
```

Then Docker reuses previous cached layers.

So build becomes faster.

---

# 4️⃣ Dockerfile from Scratch

```dockerfile id="jlwm13"
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

## Meaning

* `FROM` = base image
* `WORKDIR` = working folder
* `COPY` = copy files
* `RUN` = execute during build
* `CMD` = run when container starts

---

# 5️⃣ CMD vs ENTRYPOINT

## CMD

Default command. Can override.

```dockerfile id="jlwm14"
CMD ["python", "app.py"]
```

Run:

```bash id="jlwm15"
docker run image python test.py
```

CMD replaced.

---

## ENTRYPOINT

Main fixed executable.

```dockerfile id="jlwm16"
ENTRYPOINT ["python"]
CMD ["app.py"]
```

Run:

```bash id="jlwm17"
docker run image test.py
```

Output:

```text id="jlwm18"
python test.py
```

---

# 6️⃣ Build and Tag Custom Image

```bash id="jlwm19"
docker build -t myapp:v1 .
```

## Meaning

* `build` = create image
* `-t` = tag
* `myapp` = image name
* `v1` = version
* `.` = current folder

---

# 7️⃣ Create and Use Named Volumes

Volumes store data permanently.

```bash id="jlwm20"
docker volume create mydata
```

Use:

```bash id="jlwm21"
docker run -d -v mydata:/var/lib/mysql mysql
```

Even if container removed, DB data stays.

---

# 8️⃣ Use Bind Mounts

Maps host folder to container.

```bash id="jlwm22"
docker run -d -v $(pwd):/app nginx
```

If host file changes → container sees instantly.

Used in development.

---

# 9️⃣ Create Custom Networks

```bash id="jlwm23"
docker network create mynet
```

Run:

```bash id="jlwm24"
docker run -d --name c1 --network mynet nginx
docker run -d --name c2 --network mynet ubuntu sleep 500
```

Inside c2:

```bash id="jlwm25"
ping c1
```

Works using container name.

---

# 🔟 docker-compose.yml Multi Container App

```yaml id="jlwm26"
version: "3.9"

services:
  web:
    image: nginx
    ports:
      - "80:80"

  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
```

Run:

```bash id="jlwm27"
docker compose up -d
```

Stops:

```bash id="jlwm28"
docker compose down
```

---

# 1️⃣1️⃣ Environment Variables + .env

## .env File

```env id="jlwm29"
MYSQL_PASSWORD=root123
```

## Compose File

```yaml id="jlwm30"
environment:
  MYSQL_ROOT_PASSWORD: ${MYSQL_PASSWORD}
```

Safer and reusable.

---

# 1️⃣2️⃣ Multi-Stage Dockerfile

```dockerfile id="jlwm31"
FROM node:18 AS builder

WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
```

## Why Useful?

Final image has only built files.

No node_modules, no build tools.

Smaller + secure.

---

# 1️⃣3️⃣ Push Image to Docker Hub

```bash id="jlwm32"
docker login
docker build -t myapp:v1 .
docker tag myapp:v1 username/myapp:v1
docker push username/myapp:v1
```

Anyone can pull:

```bash id="jlwm33"
docker pull username/myapp:v1
```

---

# 1️⃣4️⃣ Healthchecks and depends_on

```yaml id="jlwm34"
services:
  db:
    image: mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      retries: 5

  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
```

## Meaning

* DB checked every 10 sec
* App waits until DB healthy

Without this app may crash early.

---

# 🚀 Final Summary

You now understand deeply:

* Containers
* Images
* Docker Hub
* Dockerfile
* CMD / ENTRYPOINT
* Layers / Cache
* Volumes
* Bind Mounts
* Networks
* Compose
* Env Files
* Multi-stage Builds
* Push/Pull Images
* Healthchecks

---

# 👤 Author

Shikeb Malik

