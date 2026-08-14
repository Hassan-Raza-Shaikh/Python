# Sharing Docker Images

## 1. Sharing Images to Public Repository 

#### Step 1: Tag your image

``` docker tag my-python sajidaligiki/my-python ```

#### Step 2: Log in to Docker Hub

``` docker login ```


#### 3. Push the image to Docker Hub
``` docker push sajidaligiki/my-python ```

---

## 2. Sharing Images to Private Repository 

#### Step 1: Run a local Docker registry

``` docker run -d -p 7000:5000 --name local-repo registry:2 ```

#### Step 2: Tag your image

``` docker tag my-python localhost:7000/my-python ```


#### Step 3. Push the image to local repository
``` docker push localhost:7000/my-python ```

---

### On other PC

#### Step 1: Open /etc/docker/daemon.json with sudo permissions

``` sudo nano /etc/docker/daemon.json ```

#### Step 2: Add

``` 
{
    "insecure-registries": ["<repo-ip>:7000"]
}
 ```


#### Step 3. Restart Docker
``` sudo systemctl restart docker ```

#### Step 4. Pull the image from local registry
``` docker pull <repo-ip>:7000/my-python ```

---

