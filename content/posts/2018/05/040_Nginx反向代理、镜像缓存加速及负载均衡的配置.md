---
url: /blog/linux/H1v8I4cLAf
title: "Nginx反向代理、镜像缓存加速及负载均衡的配置"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

Nginx已经具备Squid所拥有的Web缓存加速功能、清除指定URL缓存的功能。而在性能上，Nginx对多核CPU的利用，胜过Squid不少。另外，在反向代理、负载均衡、健康检查、后端服务器故障转移、Rewrite重写、易用性上，Nginx也比Squid强大得多。

这使得一台Nginx可以同时作为“负载均衡服务器”与“Web缓存服务器”来使用。

常规安装nginx的过程，这里就不详述了，这里只介绍nginx的配置文件的配置

## **一、nginx反向代理的基本格式，也就是最简单反向代理配置文件**

```
server
{
listen 80;
server_name vpsmm.com;
location / {
proxy_pass http://cache.vpsmm.com/;
proxy_redirect off;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
}

```

## **二、如果你需要使用CDN镜像加速的功能**

**也就是前端域名和后端域名相同，可以使用下面两种方法：**

### **（一）源地址直接填写IP**

```
server
{
listen 80;
server_name vpsmm.com;
location / {
proxy_pass http://192.168.0.110; //如果不是80端口，可以加上端口http://IP:81
proxy_redirect off;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
}

```

### **（二）采用HTTP Upstream模块server指令**

```
upstream cdn {
server 192.168.0.110:80 weight=5;
server 192.168.0.121:80 weight=5;
}
server
{
listen 80;
server_name vpsmm.com;
location / {
proxy_pass http://cdn;
proxy_redirect off;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
}

```

## **三、最简单的前端全缓存+反向代理脚本**

```
mkdir /home/cache/path -p #新建2个目录，放置缓存文件
mkdir /home/cache/temp -p

```

修改 /usr/local/nginx/conf/nginx.conf 新增以下代码，主要是缓存相关设置，请放置于 http{ ##这里 } 中，一般加在

log_format 上面或下面均可：

```
client_body_buffer_size 512k;
proxy_connect_timeout 5;
proxy_read_timeout 60;
proxy_send_timeout 5;
proxy_buffer_size 16k;
proxy_buffers 4 64k;
proxy_busy_buffers_size 128k;
proxy_temp_file_write_size 128k;
proxy_temp_path /home/cache/temp;
proxy_cache_path /home/cache/path levels=1:2 keys_zone=cache_one:500m inactive=7d max_size=30g;

```

#500m是内存占用，7d是7天无访问删除，30g是缓存占具硬盘空间

以下为虚拟主机配置文件，可另存成 .conf 放置于 vhost 下面：

```
server
{
listen 80;
server_name vpsmm.com; #主机名
location / {
proxy_cache cache_one;
proxy_cache_valid 200 304 3d; #正常状态缓存时间3天
proxy_cache_key $host$uri$is_args$args;
proxy_pass http://cache.vpsmm.com/; #反代的网站
proxy_redirect off;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
expires 10d; #默认10天缓存
access_log /home/wwwlogs/vpsmm.log access; #日志文件
}
}

```

点击几下网站，df -sh 命令，查看 /home/cache

目录大小，即可测试是否缓存成功。此脚本为前端全缓存，后端动态更新后，前端不会自动修改。可手动清理cache目录下文件。这个方法，可以用纯静态的形式来防CC，如果你的动态博客，受到CC攻击，可以尝试一下。

以下为完整的nginx虚拟主机的配置文件

```
log_format jjhr.net '$remote_addr - $remote_user [$time_local] "$request" '
'$status $body_bytes_sent "$http_referer" '
'"$http_user_agent" $http_x_forwarded_for';
# 反向代理参数，具体自行搜索按需配置吧
proxy_connect_timeout 5;
proxy_read_timeout 60;
proxy_send_timeout 5;
proxy_buffer_size 16k;
proxy_buffers 4 64k;
proxy_busy_buffers_size 128k;
proxy_temp_file_write_size 128k;

# 配置临时目录、缓存路径（注意要先建立这2个目录，要在同一个硬盘分区，注意权限）
proxy_temp_path /var/cache/nginx_proxy_temp 1 2;
proxy_cache_path /var/cache/nginx_proxy_cache levels=1:2 keys_zone=jjhr:48m inactive=12d max_size=2g;
# keys_zone=jjhr:48m 表示这个 zone 名称为 jjhr，分配的内存大小为 48MB
# levels=1:2 表示缓存目录的第一级目录是 1 个字符，第二级目录是 2 个字符
# inactive=12d 表示这个zone中的缓存文件如果在 12 天内都没有被访问，那么文件会被cache manager 进程删除
# max_size=2G 表示这个zone的硬盘容量为 2G
server{
listen 80;
server_name jjhr.net *.jjhr.net;
index index.html index.php;
location / {
#-------------------------------------
proxy_cache jjhr;
proxy_cache_key "$scheme://$host$request_uri";
proxy_cache_valid 200 304 7d;
proxy_cache_valid 301 3d;
proxy_cache_valid any 10s;
expires 1d;
#--------------------------------------
proxy_pass http://205.185.115.53;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
# wordpress 后台目录不缓存
location /wp-admin {
if ( !-e $request_filename) {
proxy_pass http://205.185.115.53;
}
}
access_log /var/log/nginx/jjhr.net.log main;
}

```

## **四、多个服务器负载均衡的配置**

```
http
{
……..
client_max_body_size 300m ; // 允许客户端请求的最大单个文件字节数
client_body_buffer_size 128k;
// 缓冲区代理缓冲用户端请求的最大字节数，可以理解为先保存到本地再传给用户
proxy_connect_timeout 600;
// 跟后端服务器连接的超时时间_发起握手等候响应超时时间
proxy_read_timeout 600;
// 连接成功后_等候后端服务器响应时间_其实已经进入后端排队之中等候处理
proxy_send_timeout 600;
proxy_buffer_size 16k; // 会保存用户的头信息，供nginx进行规则处理
proxy_buffers 4 32k; // 告诉nginx保存单个用的几个buffer最大用多大空间
proxy_busy_buffers_size 64k;
proxy_max_temp_file_size 64k;
// proxy缓存临时文件的大小
upstream clubsrv {
server 192.168.0.110:80 weight=5;
server 192.168.0.121:80 weight=5;
}
upstream mysrv {
server 192.168.0.32:80 weight=2;
server 127.0.0.1:8000 weight=8;
}
server {
listen 80;
server_name club.xywy.com;
charset gbk;
root /www;
access_log logs/bba.log combined;
//下面是第一个域名，使用clubsrv的代理
location / {
proxy_next_upstream http_502 http_504 error timeout invalid_header;
// 如果后端服务器返回502、504或执行超时等错误，自动将请求转发到upstream另一台服务器
proxy_pass http://clubsrv;
// 与上面upstream自己命名的名字填写一致
proxy_redirect off;
proxy_set_header Host club.xywy.com;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
// nginx在前端做代理，后端的日志会显示127.0.0.1，上面配置可以显示用户真实IP（还需装第三方软件，见下面的详细说明）
index index.htm index.html index.php;
}
//下面是第二个域名，使用mysrv的代理，访问www.sum.com/message目录下的
server {
listen 80;
server_name www.sum.com;
location /message {
proxy_pass http://mysrv;
proxy_set_header Host $host;
// 访问这个域名的，只有mysrv 本机可以访问
}
//访问除了/message之外的www.sum.com/ 地址，
location / {
proxy_pass http://mysrv;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
下面的配置，与上面错误返回的效果相同，这里可以不写。
error_page 500 502 503 504 /50x.html;
location = /50x.html
{
root html;
}

```

### Nginx负载均衡指令

Nginx属于软件的七层负载均衡（lvs是软件的四层负载均衡的代表），七层负载均衡软件还有L7SW（Layer7

switching）、HAProxy等。支持负载均衡的模块是Http Upstream。下面介绍此模块及他下面的几个指令

### HTTP Upstream模块

#### （1）ip_hash指令

当对后端的多台动态应用服务器做负载均衡时，ip_hash指令将某个客户端IP的请求通过哈希算法定位到同一台后端服务器上。这样，当来自某ip用户在Sever

A上登录后，再访问该站点的其他URL时，能保证访问仍在Server A上。

如果不加ip_hash，加入用户在Server A上登录，再访问该站点其他URL，就有可能跳转到后端的Sever

B、C…..，而session记录在A上，B、C上没有，就会提示用户未登录。

注意：但这种访问不能保证后端服务器的负载均衡，可能后端有些server接受到的请求多，有些server接受的少，设置的权重值不起作用。

建议如果后端的动态应用程序服务器能做到session共享，而不用nginx上配置ip_hash的方式。

```
upstream mysrv {
ip_hash;
server 192.168.0.110:80 weight=2;
server 127.0.0.1:8000 down;
server 192.168.0.212:80 weight=8;
}

```

#### （2）server指令

该指令用语指定后端服务器的名称和参数。服务器的名称可以是一个域名，一个ip，端口号或UNIX Socket。

参数介绍：

weight=number ： 设置服务器权重，权重值越高，被分配到客户端请求数越多。默认为1；

max_fails=numbser ：

在fail_timeout指定的时间内对后端服务器请求失败的次数，如果检测到后端服务器无法连接及发生错误（404除外），则标记为失败。如果没有设置，默认为1。设置为0则关闭这项检查。

```
fail_timeout=time ： 在经历参数max_fails设置的失败次数后，暂停的时间。
down ： 表示服务器为永久离线状态。
Backup ： 仅仅在非backup服务器全部down或繁忙的时候才启用。
配置如下：
upstream mysrv {
ip_hash;
server www.xywy.com weight=2;
server 127.0.0.1:8000 down;
server 192.168.0.212:80 max_fails=3 fail_timeout=30s;
server unix:/tmp/bakend3;
}

```