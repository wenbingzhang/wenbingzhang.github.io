---
url: /blog/linux/HkGxI8VcL0f
title: "linux（内核）oom kille vm.overcommit_memory参数详解"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 详细说明

可选值：0、1、2。

0， 表示内核将检查是否有足够的可用内存供应用进程使用；如果有足够的可用内存，内存申请允许；否则，内存申请失败，并把错误返回给应用进程。

1， 表示内核允许分配所有的物理内存，而不管当前的内存状态如何。

2， 表示内核允许分配超过所有物理内存和交换空间总和的内存

## 修改方法

```
sysctl vm.overcommit_memory=2
echo "vm.overcommit_memory=2" >> /etc/sysctl.conf

```