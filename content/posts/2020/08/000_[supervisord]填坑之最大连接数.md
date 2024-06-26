---
url: /blog/linux/HTLMANZea
title: "[supervisord]填坑之最大连接数"
date: 2020-08-27T04:03:19+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 修改supervisord配置突破1024最大连接数

## 问题描述

最近在使用supervisord服务时发现，无论如何修改系统的最大连接数，由supervisord管理的程序都无法突破1024的限制。

## 解决办法

```
cat /etc/supervisord.conf

[supervisord]
minfds=81920
minprocs=81920

cat /etc/supervisord.d/xxx.ini

[program:xxx]
minfds=81920
minprocs=81920

systemctl restart supervisord.service

```