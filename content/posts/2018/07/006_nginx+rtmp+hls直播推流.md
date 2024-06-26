---
url: /blog/ffmpeg/BkPsvPiGm
title: "nginx+rtmp+hls直播推流"
date: 2018-07-05T10:04:28+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 源码编译nginx+rtmp+hls，并附带nginx配置文件、推流的方式及播放方法。

## nginx

### 编译

```
wget http://nginx.org/download/nginx-1.14.0.tar.gz
wget https://github.com/arut/nginx-rtmp-module/archive/v1.2.1.tar.gz
wget http://zlib.net/zlib-1.2.11.tar.gz
wget
#全部解压并编译nginx
./configure --sbin-path=/usr/local/nginx/nginx --conf-path=/usr/local/nginx/nginx.conf --pid-path=/usr/local/nginx/nginx.pid --with-http_ssl_module --with-pcre=/opt/app/openet/oetal1/chenhe/pcre-8.37 --with-zlib=/opt/app/openet/oetal1/chenhe/zlib-1.2.8 --with-openssl=/opt/app/openet/oetal1/chenhe/openssl-1.0.1t --add-module=../nginx-rtmp-module

```

### 配置

```
worker_processes  auto;

error_log  logs/error.log debug;

events {
    worker_connections  1024;
}

rtmp {
    server {
        listen 1935;
        chunk_size 4000;

        application myapp {
            live on;
        }

        application hls {
            live on;
            hls on;
            hls_path /data/y/ngnix/hls;
            hls_playlist_length 1d;
            hls_sync 100ms;
            hls_continuous on;
            hls_fragment 8s;
        }
    }
}

http {
    server {
        listen      80;

        location / {
            root html;
        }

        location /stat {
            rtmp_stat all;
            rtmp_stat_stylesheet stat.xsl;
        }

        location /stat.xsl {
            root html;
        }

        location /hls {
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Headers "Origin, X-Requested-With, Content-Type, Accept";
            add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
            #server hls fragments
            types{
                application/vnd.apple.mpegurl m3u8;
                video/mp2t ts;
            }
            alias /data/y/ngnix/hls;
            expires -1;
        }
    }
}

```

## 推流

```
#RTMP方式
/opt/ffmpeg/bin/ffmpeg -re -i "/home/1.mp4" -vcodec libx264 -vprofile baseline -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 1280x720 -q 10 rtmp://127.0.0.1:1935/myapp/test1
#HTTP方式
/opt/ffmpeg/bin/ffmpeg -re -i "/home/2.mp4" -vcodec libx264 -vprofile baseline -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 1280x720 -q 10 rtmp://127.0.0.1:1935/hls/test2

```

具体参数可根据自己的需求调整

## 播放

第一个地址: rtmp://127.0.0.1:1935/myapp/test1

第二个地址: http://127.0.0.1:80/hls/test2.m3u8

可以使用ckplayer播放。