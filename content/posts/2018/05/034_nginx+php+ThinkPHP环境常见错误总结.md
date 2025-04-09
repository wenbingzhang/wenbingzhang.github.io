---
url: /blog/linux/ByS8884qI0M
title: "nginx+php+ThinkPHP环境常见错误总结"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 错误一

2017/09/07 16:39:18 [error] 21753#0: *26 FastCGI sent in stderr: “Primary s…

## 错误一

```bash
2017/09/07 16:39:18 [error] 21753#0: *26 FastCGI sent in stderr: "Primary script unknown" while reading response header from upstream, client: 172.31.26.114, server: localhost, request: "GET /1.php HTTP/1.1", upstream: "fastcgi://127.0.0.1:9000", host: "10.200.8.220:8000"

```

### 解决版本

在server节点下添加以下配置

```bash
root   /var/www/web;
index  index.php index.html index.htm;

location ~ \.php$ {
    try_files $uri = 404;
    fastcgi_pass   127.0.0.1:9000;
    fastcgi_index  index.php;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include        fastcgi.conf;
}

```

## ThinkPHP配置

假如网站的根目录是/var/www/web，如果ThinkPHP的网站在/var/www/web/Test目录配置如下

```bash
        location /Test/ {
            if (!-e $request_filename){
                rewrite ^/Test/(.*)$ /Test/index.php?s=$1 last;
            }
        }

        location ~ \.php/?.*$ {
            try_files $uri = 404;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include        fastcgi.conf;
            #设置PATH_INFO并改写SCRIPT_FILENAME,SCRIPT_NAME服务器环境变量
            #set $fastcgi_script_name2 $fastcgi_script_name;
            #if ($fastcgi_script_name ~ "^(.+\.php)(/.+)$") {
            #    set $fastcgi_script_name2 $1;
            #    set $path_info $2;
            #}
            #fastcgi_param   PATH_INFO $path_info;
            #fastcgi_param   SCRIPT_FILENAME   $document_root$fastcgi_script_name2;
            #fastcgi_param   SCRIPT_NAME   $fastcgi_script_name2;
        }

```

如果是放在根目录下

```bash
        location / {
            if (!-e $request_filename){
                rewrite ^/(.*)$ /index.php?s=$1 last;
            }
        }

        location ~ \.php/?.*$ {
            try_files $uri = 404;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include        fastcgi.conf;
            #设置PATH_INFO并改写SCRIPT_FILENAME,SCRIPT_NAME服务器环境变量
            #set $fastcgi_script_name2 $fastcgi_script_name;
            #if ($fastcgi_script_name ~ "^(.+\.php)(/.+)$") {
            #    set $fastcgi_script_name2 $1;
            #    set $path_info $2;
            #}
            #fastcgi_param   PATH_INFO $path_info;
            #fastcgi_param   SCRIPT_FILENAME   $document_root$fastcgi_script_name2;
            #fastcgi_param   SCRIPT_NAME   $fastcgi_script_name2;
        }

```

最后来个完整的例子

```bash
user  root;
worker_processes  auto;
#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;
#pid        logs/nginx.pid;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    server {
        listen       80;
        server_name  localhost;
        root   /var/www/web;
        index  index.php index.html index.htm;
        location / {
        index  index.htm index.html index.php;
        }
        location /Test/ {
            if (!-e $request_filename){
                rewrite ^/Test/(.*)$ /Test/index.php?s=$1 last;
            }
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
        location ~ \.php/?.*$ {
            try_files $uri = 404;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include        fastcgi.conf;
            #设置PATH_INFO并改写SCRIPT_FILENAME,SCRIPT_NAME服务器环境变量
            #set $fastcgi_script_name2 $fastcgi_script_name;
            #if ($fastcgi_script_name ~ "^(.+\.php)(/.+)$") {
            #    set $fastcgi_script_name2 $1;
            #    set $path_info $2;
            #}
            #fastcgi_param   PATH_INFO $path_info;
            #fastcgi_param   SCRIPT_FILENAME   $document_root$fastcgi_script_name2;
            #fastcgi_param   SCRIPT_NAME   $fastcgi_script_name2;
        }
    }
}

```