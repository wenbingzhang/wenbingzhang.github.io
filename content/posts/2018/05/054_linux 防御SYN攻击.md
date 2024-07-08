---
url: /blog/linux/HyYg884c80f
title: "linux 防御SYN攻击"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 一、默认syn配置

```
sysctl -a | grep _syn
net.ipv4.tcp_max_syn_backlog = 1024
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_synack_retries = 5
net.ipv4.tcp_syn_retries = 5

```

tcp_max_syn_backlog 是SYN队列的长度，加大SYN队列长度可以容纳更多等待连接的网络连接数。

tcp_syncookies是一个开关，是否打开SYN Cookie 功能，该功能可以防止部分SYN攻击。

tcp_synack_retries和tcp_syn_retries定义SYN 的重试连接次数，将默认的参数减小来控制SYN连接次数的尽量少。

## 二、修改syn配置

```
ulimit -HSn 65535
sysctl -w net.ipv4.tcp_max_syn_backlog=2048
sysctl -w net.ipv4.tcp_syncookies=1
sysctl -w net.ipv4.tcp_synack_retries=2
sysctl -w net.ipv4.tcp_syn_retries=2

```

## 三、添加防火墙规则

```
#Syn 洪水攻击(--limit 1/s 限制syn并发数每秒1次)
iptables -A INPUT -p tcp --syn -m limit --limit 1/s -j ACCEPT
#防端口扫描
iptables -A FORWARD -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s -j ACCEPT
#防洪水ping
iptables -A FORWARD -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

```

## 四、添加开机启动

最后别忘记将二、三、里面的命令写到/etc/rc.d/rc.local