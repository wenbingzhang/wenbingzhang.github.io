---
url: /blog/linux/HkCTnskvV
title: "error while loading shared libraries: libc.so.6: cannot open shared object file: No such file or directory"
date: 2019-03-08T09:24:10+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 不小心误删libc.so的恢复方式

安装完成后, 建立软链指向glibc-2.14, 执行如下命令:

```bash
rm -rf /lib64/libc.so.6
```

```bash
ln -s /opt/glibc-2.14/lib/libc-2.14.so /lib64/libc.so.6
```

注意：删除libc.so.6之后可能导致系统命令不可用的情况, 可使用如下方法解决:

```bash
$ LD_PRELOAD=/opt/glibc-2.14/lib/libc-2.14.so  ln -s /opt/glibc-2.14/lib/libc-2.14.so /lib64/libc.so.6
```

如果上述更新失败可使用如下命令还原:

```bash
$ LD_PRELOAD=/lib64/libc-2.12.so ln -s /lib64/libc-2.12.so /lib64/libc.so.6    // libc-2.12.so 此项是系统升级前的版本
```