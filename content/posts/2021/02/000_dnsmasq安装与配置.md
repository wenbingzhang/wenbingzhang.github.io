---
url: /blog/linux/xd2UELYGR
title: "dnsmasq安装与配置"
date: 2021-02-03T11:20:44+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> dnsmasq是一个小巧且方便地用于配置DNS和DHCP的工具，适用于小型网络，它提供了DNS功能和可选择的DHCP功能。

## 安装服务

```bash
sudo yum install dnsmasq

```

## 常用配置

```bash
cat /etc/dnsmasq.conf

#######这里表示 严格按照 resolv-file 文件中的顺序从上到下进行 DNS 解析, 直到第一个成功解析成功为止
#strict-order

###同时发送所有的查询到所有的dns服务器，谁快就用谁
all-servers

listen-address=127.0.0.1

###不让dnsmasq去读/etc/hosts文件
no-hosts

## 设置缓存条目
cache-size=10240

#允许客户端缓存的时间单位为秒
local-ttl=10
max-cache-ttl=15

###开启日志
#log-queries
##配置日志文件
#log-facility=/data/logs/dnsmasq.log

```

```bash
cat /etc/resolv.dnsmasq.conf

nameserver 223.5.5.5
nameserver 114.114.114.114
nameserver 222.246.129.80

```

## 启动服务

```bash
systemctl start dnsmasq

```

## 验证方法

```bash
dig www.zhangwenbing.com

```

## 其他配置

### **国内指定DNS**

```ini
server=/cn/114.114.114.114
server=/taobao.com/114.114.114.114
server=/taobaocdn.com/114.114.114.114

```

### **国外指定DNS**

```ini
server=/google.com/8.8.8.8

```

### 屏蔽网页广告

```ini
address=/ad.youku.com/127.0.0.1
address=/ad.iqiyi.com/127.0.0.1

```

## 其他功能

除了DNS，还支持DHCP和TFTP，由于暂时用不到，这里就不一一例举了。