---
url: /blog/linux/S13z8UE5UCf
title: "linux内存清理释放命令"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 命令

```
sync
echo 1 > /proc/sys/vm/drop_caches
echo 2 > /proc/sys/vm/drop_caches
echo 3 > /proc/sys/vm/drop_caches

```

## 解释

```
cache释放：
To free pagecache:
echo 1 > /proc/sys/vm/drop_caches

To free dentries and inodes:
echo 2 > /proc/sys/vm/drop_caches

To free pagecache, dentries and inodes:
echo 3 > /proc/sys/vm/drop_caches

```

## 说明

释放前最好sync一下，防止丢数据。