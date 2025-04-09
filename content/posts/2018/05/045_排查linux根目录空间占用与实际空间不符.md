---
url: /blog/linux/HJqtULE5I0z
title: "排查linux根目录空间占用与实际空间不符"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

## 发现问题

首先使用”df -Th”查看根目录的空间使用和”du -sh /“的结果进行对比。

## 排查问题

### 第一种情况

文件被删掉，但是写这个文件的进程没退出

```bash
 lsof -n|grep delete

```

使用以上命令得到相关的进程，然后使用得到的pid找到对应的程序，然后重启程序或kill掉即可释放被删除文件的空间。

### 第二种情况

```bash
lsof -n|grep delete

```

没有得到任何返回结果。

那么我们首先查看下根目录的文件系统，如果是“xfs”,那么可以使用

```bash
xfs_db -c frag -r /dev/sdxx

```

查看碎片的占比，如果较高的话，那么我们应该整理下xfs的碎片了。

```bash
xfs_fsr /dev/sdxx #整理碎片

```

然后你再“df”看看释放空间已经释放了。

## 备注

xfs虽然性能比较好，但是稳定性还是有所欠缺，不是很建议使用。

如果以上的方法没有解决你的问题或者你还有其他情况，欢迎留言一起探讨。