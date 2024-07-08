---
url: /blog/linux/B1AMUL45ICM
title: "Centos7搭建vpn"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---


## 准备环境

### 首先查看系统是否支持pptpd服务：

```bash
modprobe ppp-compress-18 && echo yes

```

### 安装ppp , pptpd，iptables

```bash
yum install -y ppp pptpd iptables
systemctl mask firewalld
systemctl stop firewalld

```

## 修改配制

```bash
vi /etc/pptpd.conf    #找到配制文件中默认的值，去掉注释即可
localip 192.168.0.1   #本机VPN IP
remoteip 192.168.0.234-238,192.168.0.245 客户端可以获取到的ip网段

#修改DNS
vi /etc/ppp/options.pptpd      #末尾添加dns
ms-dns  8.8.8.8
ms-dns  114.114.114.114

#添加vpn账户
vi /etc/ppp/chap-secrets
# client        server  secret                  IP addresses
  user          pptpd   passwd                  *

#开启路由转发
vi /etc/sysctl.conf
net.ipv4.ip_forward = 1 #添加在配制文件的末尾即可
sysctl -p    #运行这个命令会输出上面添加的那一行信息，意思是使内核修改生效

#在防火墙上开启nat转发
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE  #IP和网口根据实际情况修改即可

```

## 开启服务

```bash
service iptables save
systemctl restart iptables
systemctl restart pptpd

```