---
url: /blog/linux/H13UIE5LRM
title: "linux vnc简单配置"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## VNC端口

vncserver监听端口 RFB协议：5900+桌面号 HTTP协议：5800+桌面号 X协议：6000+桌面号

vncserver使用的桌面编号默认是从1开始，依次使用。

## vnc配置

安装vnc 和vnc-server

vncserver :1 #启动vncserver并生产配置文件

修改~/.vnc/xstartup文件 默认使用twm环境 使用图形界面：

修改配置文件，去掉下列两行的注释

# Uncomment the following two lines for normal desktop:

# unset SESSION_MANAGER

# exec /etc/X11/xinit/xinitrc

修改/etc/sysconfig/vncservers文件 去掉最后两行的注释

VNCSERVERS=“2:myusername”

VNCSERVERARGS[2]=“-geometry 800x600 -nolisten tcp -nohttpd -localhost”

修改配置文件后重新VNC服务 vncserver -kill :1 vncserver :1

修改/etc/inittab文件 将默认的启动级别改成5 添加开机启动 chkconfig vncserver on