
# Docker Quick Exercises

## 1. Pull an Image from Docker Hub

```bash
docker pull nginx
```
```bash
docker pull python:3.10-slim
```

## 2. Run a Simple Container

```bash
docker run nginx
```

## 3. Expose NGINX server on port 8080 of the host

```bash
docker run -p 8080:80 nginx
```

## 4. Run in Detached Mode with Port Mapping

```bash
docker run -d -p 8081:80 nginx
```

## 5. List Containers
- Running
```bash
docker ps
```
- Running & Non-running
```bash
docker ps -a
```

## 6. Inspect Logs from a Container

```bash
docker logs <container_id>
```

## 7. Stop and Remove a Container

```bash
docker stop <container_id>
```
```bash
docker rm <container_id>
```

## 8. Run an Interactive python:3.10-slim container (use "exit" to get out of it)

```bash
docker run --rm -it python:3.10-slim bash
```
- Check python version using
```bash
python --version
```

## 9. Bind Mount a Local HTML File into NGINX

### 9.1 Create a local file:

```bash
echo '<h1>Hello Docker!</h1>' > index.html
```

### 9.2 Run container with volume:

```bash
docker run -d -p 8081:80 -v $(pwd)/index.html:/usr/share/nginx/html/index.html nginx
```
- You have just hosted a simple web app
## 10. Bind Mount a Local Python File into python:3.10-slim

### 10.1 Create a local file:

```bash
echo 'print("Hello, world!")' > hello.py
```

### 10.2 Run container with volume:

```bash
docker run -it --rm -v $(pwd)/hello.py:/hello.py python:3.10-slim bash
```

### 10.3 Execute the hello.py

```bash
python hello.py
```
