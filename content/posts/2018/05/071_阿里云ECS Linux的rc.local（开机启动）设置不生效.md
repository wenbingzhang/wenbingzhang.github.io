---
url: /blog/linux/SytNL84q8Af
title: "阿里云ECS Linux的rc.local（开机启动）设置不生效"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 使用场景

前段时间使用阿里云的ecs，将一些开机启动的命令写到/etc/rc.local里面，发现不生效。经过一番查询和搜索之后，最后发现一个坑，居然要给这个文件设置执行权限才生效。

## 解决方法

```
chmod +x /etc/rc.local

```