---
url: /blog/linux/rJY7U8E9U0z
title: "centos7 rdate 时间同步服务"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---


## 安装软件

```bash
yum install -y xinetd rdate

```

## 修改配制

```bash
vim /etc/xinetd.d/time-stream
# 将disable = yes 改为 disable = no

```

## 启动服务

```bash
# 启动xinetd
systemctl start xinetd
# 添加开启启动
systemctl enable xinetd

```

## 同步时间

### 服务端

首先在服务端执行以下命令（到底哪个是服务端呢？就是你在哪台机器上面执行了以上三个步骤就是服务端），在服务端上同步网络标准时间，然后再同步到内网各台机器上。

```bash
/usr/bin/rdate -s -u  time.nist.gov

```

### 客户端

其他内网需要同步时间的机器可以执行

```bash
yum install -y rdate
/usr/bin/rdate -s 服务端ip

```