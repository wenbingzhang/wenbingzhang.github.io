---
url: /blog/linux/Hk2bI84c8Rz
title: "linux VM虚拟内存和BDP优化"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## VM虚拟内存优化

#getconf PAGESIZE

vm.dirty\_background\_bytes 系统内所包含的脏数据总数

vm.dirty\_background\_ratio 脏数据所占用内存的百分比

vm.dirty\_expire\_centisecs 脏数据在内存中的存放时间

vm.dirty\_bytes 如果进程的脏数据超过该值时则要求写到磁盘

## BDP优化

BDP=Bandwidth\*RRT net.core.rmem\_max 最大缓冲区(窗口)大小

net.core.wmem\_default 默认缓冲区大小

net.core.wmem\_max 最大发送缓冲区大小