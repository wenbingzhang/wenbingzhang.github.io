---
url: /blog/macos/BkiIyglTX
title: "Mac出现Operation not permitted"
date: 2018-11-07T04:56:25+08:00
description:
categories:
  - MacOS
tags:
  - MacOS
menu: main
---

> Rootless 机制

## 报错

Mac使用sudo或切换成root权限，还是出现

```
Operation not permitted

```

## 解决

这是由于Mac的rootless机制，可以进入恢复模式关闭rootless机制：

1、重启mac，按command+R（windows键盘：win+R）进入恢复模式

2、选择终端，在左上角，输入指令：

```
csrutil disable

```

3、重启后让机器正常启动，可以在终端查看rootless状态：

```
csrutil status

```

正常情况下rootless已经关闭。

4、要想重新开启rootless机制，参照步骤1，输入指令：

```
csrutil enable

```

## 说明

苹果从 OS X El Capitan 10.11 系统开始使用了 Rootless

机制，可以将该机制理解为一个更高等级的系统的内核保护措施，系统默认将会锁定 /system、/sbin、/usr 这三个目录。