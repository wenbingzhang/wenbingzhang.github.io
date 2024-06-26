---
url: /blog/linux/H1sZIUN9I0f
title: "linux 防拒绝服务攻击"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 一、使用脚本

```
wget http://www.inetbase.com/scripts/ddos/install.sh 安装脚本
wget http://www.inetbase.com/scripts/ddos/uninstall.sh 卸载脚本

```

## 二、内核优化

```
net.ipv4.tcp_max_syn_backlog = 1024 #设定syn队列长度
net.ipv4.tcp_syncookies = 1 #设定是否启用cookies
net.ipv4.tcp_synack_retries = 3 #设定synack重试次数
net.ipv4.tcp_syn_retries = 2 #设定syn重试次数
net.ipv4.icmp_echo_ignore_all = 1 #不回应ping
net.ipv4.icmp_echo_ignore_broadcast = 1 #不回应广播ping

```

## 三、防火墙配置

### 1、基于数据包进行限制

```
#iptables -A INPUT -p tcp --tcp-flags syn,ack,fin syn -m limit --limit 5/s --limit-burst 8 -j ACCEPT
#iptables -A INPUT -p tcp -m state --state ESTABLISHED,RELATED -j ACCEPT

```

### 2、基于连接数进行限制

```
#iptables -A INPUT -s 192.168.0.0/24 -p tcp --dport 23 -m connlimit --connlimit-above 2 -j DROP

```

### 3、基于地址列表进行限制

```
#iptables -A INPUT -p tcp --dport 80 --tcp-flags syn,ack,fin syn -m recent --name webpool --rcheck --seconds 120 --hitcount 10 -j LOG --log-prefix="ddos:" --log-ip-options
#iptables -A INPUT -p tcp --dport 80 --syn -m recent --name webpool --rcheck --seconds 120 --hitcount 10 -j DROP
#iptables -A INPUT -p tcp --dport 80 --syn -m recent --name webpool --set -j ACCEPT

```