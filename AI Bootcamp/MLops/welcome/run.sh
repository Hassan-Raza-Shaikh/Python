docker run -d -p 8080:80 \
 -v ./index.html:/usr/share/nginx/html/index.html \
 --name welcome --rm \
 nginx:1.29.0
