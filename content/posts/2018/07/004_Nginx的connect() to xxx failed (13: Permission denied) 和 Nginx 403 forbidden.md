---
url: /blog/linux/HJlvWaG47
title: "Nginx的connect() to xxx failed (13: Permission denied) 和 Nginx 403 forbidden"
date: 2018-07-23T02:53:40+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 解决Nginx的connect() to xxx failed (13: Permission denied) 和 Nginx 403 forbidden 错误

## 查看SeLinux状态

```
getenforce

```

如果是enabled则继续往下看。

## 临时关闭（不需要重启机器）

```
setenforce 0

```

## 修改配置

```
vim /etc/selinux/config #将SELINUX=enforcing改为SELINUX=disabled

```

如果你执行了临时关闭SeLinux并机器上跑了重要的业务，那可以不需要马上重启机器，等待下次重启配置生效即可。