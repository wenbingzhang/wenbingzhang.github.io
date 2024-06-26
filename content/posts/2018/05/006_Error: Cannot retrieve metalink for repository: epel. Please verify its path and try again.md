---
url: /blog/linux/B1CwUU45UAG
title: "Error: Cannot retrieve metalink for repository: epel. Please verify its path and try again"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 错误提示

```
Loading mirror speeds from cached hostfile
Error: Cannot retrieve metalink for repository: epel. Please verify its path and try again

```

## 解决方法

解决这个问题很简单，修改文件“/etc/yum.repos.d/epel\*.repo”， 将baseurl的注释取消， mirrorlist注释掉。

```
yun clean all
yum list

```