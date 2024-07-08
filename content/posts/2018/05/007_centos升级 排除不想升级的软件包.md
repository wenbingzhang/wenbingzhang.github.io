---
url: /blog/linux/r1bIUL458Cz
title: "centos升级 排除不想升级的软件包"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 方法一

```
yum --exclude="kernel*" update

```

## 方法二

```
cat /etc/yum.conf

[main]
......
exclude=kernel*

```

修改/etc/yum.conf，在“[main]”的最后加上“exclude=kernel*”即可。

## 总结

方法一为零时的，也就是只在当次有效，而方法二为永久有效。可根据不同情况选择。