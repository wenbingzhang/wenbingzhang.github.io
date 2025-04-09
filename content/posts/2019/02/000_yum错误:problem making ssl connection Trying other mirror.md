---
url: /blog/linux/rk-lmMGL4
title: "yum错误:problem making ssl connection Trying other mirror"
date: 2019-02-26T01:20:26+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> yum无法使用带https的源

## 环境

```bash
yum install epel-release
```
运行以上命令之后，安装其他软件就报错。

## 错误提示

```bash
[Errno 14] problem making ssl connection Trying other mirror.
Trying other mirror
Error: Cannot retrieve repository metadata (repomd.xml) for repository: xxxx. Please verify its path and try again
```
经过google查询，发现似乎是ssl证书的原因。


## 解决方法

```bash
yum install ca-certificates
yum update curl
```