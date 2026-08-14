
# Docker Image Exercises

## 1. Dockerize a simple Python app

- Go to directory 0-my-first-image
```bash
cd 0-my-first-image
```
- Use the following Dockerfile instructions
```bash
FROM python:3.10-slim

WORKDIR /app

COPY ./app/ .

CMD ["python", "main.py"]

```

- Build docker image
```bash
docker build -t my-first-image .
```

- Run docker container
```bash
docker run --rm my-first-image
```

**Congratulations!** you have just build and tested your first image

## 2. Use ENV in your docker app

- Go to directory 2-use-envs-in-app
```bash
cd 2-use-envs-in-app
```
- Use the following Dockerfile instructions
```bash
FROM python:3.10-slim

WORKDIR /app

COPY app.py .

ENV MESSAGE="AoA, this is a default message from docker image"

CMD ["python", "app.py"]

```

- Build docker image
```bash
docker build -t 2-use-envs-in-app .
```

- Run docker container without setting ENV
```bash
docker run --rm 2-use-envs-in-app
```

- Run docker container with ENV
```bash
docker run --rm -e MESSAGE="this is new message" 2-use-envs-in-app
```
## 3. Create a Python Docker Image FROM ubuntu

- Go to directory 1-my-python
```bash
cd my-python
```
- Use the following Dockerfile instructions
```bash
# Use the official Ubuntu base image
FROM ubuntu

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set default Python alias
RUN ln -s /usr/bin/python3 /usr/bin/python

# Set working directory inside the container
WORKDIR /app

# Default command to run Python
CMD ["python"]

```

- Build docker image
```bash
docker build --network=host -t my-python .
```

- Create a local file
```bash
echo 'print("Hello, world!")' > hello.py
```

- Run container with volume
```bash
docker run -it --rm -v $(pwd)/hello.py:/app/hello.py my-python bash
```

**Congratulations!** you have just created your own isloated python environment


