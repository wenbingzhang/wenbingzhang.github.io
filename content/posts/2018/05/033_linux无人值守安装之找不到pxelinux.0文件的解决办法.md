---
url: /blog/linux/ryedLUN9UAf
title: "linux无人值守安装之找不到pxelinux.0文件的解决办法"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 解决思路

```
yum search pxelinux

```

通过上面的方法我们找到了syslinux包

然后安装syslinux

```
yum install syslinux

```

最后找到pxelinux.0文件

```
ls /usr/share/syslinux/pxelinux.0

```