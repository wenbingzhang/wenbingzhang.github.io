---
url: /blog/linux/B1G3FwCaN
title: "supervisor 安装和使用方法"
date: 2019-05-31T09:20:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> Supervisor是用Python开发的一套通用的进程管理程序，能将一个普通的命令行进程变为后台daemon，并监控进程状态，异常退出时能自动重启。

## 准备工作

```bash
yum install epel-* -y
yum install python34 -y
wget --no-check-certificate
python3 get-pip.py

```

## 安装supervisor

```bash
pip3 install supervisor

```

## 配置supervisor

```bash
echo_supervisord_conf >/etc/supervisord.conf

vi /etc/supervisord.conf

......

;[include] ;这个东西挺有用的，当我们要管理的进程很多的时候，写在一个文件里面就有点大了。我们可以把配置信息写到多个文件中，然后include过来
;files = relative/directory/*.ini

```

去掉上面两行的”;“然后将files改成自己的目录

```bash
vi /etc/supervisord.conf

[unix_http_server]
file=/tmp/supervisor.sock   ;UNIX socket 文件，supervisorctl 会使用
;chmod=0700                 ;socket文件的mode，默认是0700;chown=nobody:nogroup       ;socket文件的owner，格式：uid:gid

;[inet_http_server]         ;HTTP服务器，提供web管理界面
;port=127.0.0.1:9001        ;Web管理后台运行的IP和端口，如果开放到公网，需要注意安全性
;username=user              ;登录管理后台的用户名
;password=123               ;登录管理后台的密码

[supervisord]
logfile=/tmp/supervisord.log ;日志文件，默认是 $CWD/supervisord.loglogfile_maxbytes=50MB        ;日志文件大小，超出会rotate，默认 50MB，如果设成0，表示不限制大小
logfile_backups=10           ;日志文件保留备份数量默认10，设为0表示不备份
loglevel=info                ;日志级别，默认info，其它: debug,warn,trace
pidfile=/tmp/supervisord.pid ;pid 文件
nodaemon=false               ;是否在前台启动，默认是false，即以 daemon 的方式启动
minfds=1024                  ;可以打开的文件描述符的最小值，默认 1024minprocs=200                 ;可以打开的进程数的最小值，默认 200
 [supervisorctl]
serverurl=unix:///tmp/supervisor.sock ;通过UNIX socket连接supervisord，路径与unix_http_server部分的file一致;serverurl=http://127.0.0.1:9001 ; 通过HTTP的方式连接supervisord
 ; [program:xx]是被管理的进程配置参数，xx是进程的名称
[program:xx]
command=/opt/apache-tomcat-8.0.35/bin/catalina.sh run  ; 程序启动命令
autostart=true       ; 在supervisord启动的时候也自动启动
startsecs=10         ; 启动10秒后没有异常退出，就表示进程正常启动了，默认为1秒
autorestart=true     ; 程序退出后自动重启,可选值：[unexpected,true,false]，默认为unexpected，表示进程意外杀死后才重启
startretries=3       ; 启动失败自动重试次数，默认是3user=tomcat          ; 用哪个用户启动进程，默认是root
priority=999         ; 进程启动优先级，默认999，值小的优先启动
redirect_stderr=true ; 把stderr重定向到stdout，默认falsestdout_logfile_maxbytes=20MB  ; stdout 日志文件大小，默认50MB
stdout_logfile_backups = 20   ; stdout 日志文件备份数，默认是10; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile=/opt/apache-tomcat-8.0.35/logs/catalina.out
stopasgroup=false     ;默认为false,进程被杀死时，是否向这个进程组发送stop信号，包括子进程
killasgroup=false     ;默认为false，向进程组发送kill信号，包括子进程

;包含其它配置文件
[include]
files = /etc/supervisord.d/*.ini    ;可以指定一个或多个以.ini结束的配置文件

mkdir /etc/supervisord.d/

```

## 启动supervisor

```bash
supervisord -c /etc/supervisord.conf

```

## 常用命令

### 查看状态

```bash
supervisorctl status

```

### 启动服务

```bash
supervisorctl start 服务名

```

### 停止服务

```bash
supervisorctl stop 服务名

```

### 重启服务

```bash
supervisorctl restart 服务名

```

### 增加服务

```bash
vim /etc/supervisord.d/test.ini
[program:test] #程序的名字，在supervisor中可以用这个名字来管理该程序。
directory = /root #相当于在该目录下执行程序
command = /root/1.sh #启动程序的命令
autorestart = true #是否自动重启
autostart = true #设置改程序是否虽supervisor的启动而启动
startsecs = 5 重新启动时，等待的时间
startretries = 3 #重启程序的次数
user = root #指定运行用户
redirect_stderr = true #是否将程序错误信息重定向的到文件
stdout_logfile_backups = 10
stdout_logfile_maxbytes = 10MB
stdout_logfile = /var/log/supervisord/ameRender.log
environment = HOME="/root",USER="root"
minfds=81920
minprocs=81920

supervisorctl update

```