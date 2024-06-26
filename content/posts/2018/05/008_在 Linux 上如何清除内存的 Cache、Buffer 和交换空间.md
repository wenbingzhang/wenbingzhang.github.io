---
url: /blog/linux/B1FO88V580M
title: "在 Linux 上如何清除内存的 Cache、Buffer 和交换空间"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> linux清理内存
>
> 像任何其他的操作系统一样，GNU/Linux 已经实现的内存管理不仅有效，而且更好。但是，如果有任何进程正在蚕食你的内存，而你想要清除它的话，Linux
>
> 提供了一个刷新或清除RAM缓存方法。

## 如何在 Linux 中清除缓存（Cache）？

每个 Linux 系统有三种选项来清除缓存而不需要中断任何进程或服务。

（LCTT 译注：Cache，译作“缓存”，指 CPU

和内存之间高速缓存。Buffer，译作“缓冲区”，指在写入磁盘前的存储再内存中的内容。在本文中，Buffer 和 Cache 有时候会通指。）

### 仅清除页面缓存（PageCache）

```
# sync; echo 1 > /proc/sys/vm/drop_caches

```

### 清除目录项和inode

```
# sync; echo 2 > /proc/sys/vm/drop_caches

```

### 清除页面缓存，目录项和inode

```
# sync; echo 3 > /proc/sys/vm/drop_caches

```

上述命令的说明：

sync

将刷新文件系统缓冲区（buffer），命令通过“;”分隔，顺序执行，shell在执行序列中的下一个命令之前会等待命令的终止。正如内核文档中提到的，写入到drop\_cache将清空缓存而不会杀死任何应用程序/服务，echo命令做写入文件的工作。

如果你必须清除磁盘高速缓存，第一个命令在企业和生产环境中是最安全，”…echo 1> …“只会清除页面缓存。

在生产环境中不建议使用上面的第三个选项”…echo 3 > …” ，除非你明确自己在做什么，因为它会清除缓存页，目录项和inodes。