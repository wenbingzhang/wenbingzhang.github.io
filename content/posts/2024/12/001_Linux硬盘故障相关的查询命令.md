---
slug: WVKjyjT7qHUmo4JpuCHECA
title: Linux硬盘故障相关的查询命令
description:
categories:
  - Linux
tags:
  - Linux
date: 2024-12-23 18:17:28+08:00
menu: main
---

## 查看硬盘及对应的UUID信息
```bash
# 查看硬盘及对应的UUID信息 或者是所有硬盘的UUID信息
blkid [/dev/sda1]  # lsblk -o NAME,UUID -p
```

## 查看UUID对应的硬盘路径
```bash
blkid -U 383bc776-fc1a-4040-ad8f-45f4f5d96fcf
```

## 查看硬盘信息
```bash
lshw -class disk
```

## 检测磁盘是否损坏
```bash
badblocks -b 4096 -v /dev/sda # 也有坏快的屏蔽方式这个里就不列举了
```

## 点亮硬盘LED
```bash
dd if=/dev/sda of=/dev/null bs=1M count=100 # 点亮硬盘LED
```

## 查看服务器序列号
```bash
dmidecode -t 1  # 查看对应的'Serial Number'字段
```
