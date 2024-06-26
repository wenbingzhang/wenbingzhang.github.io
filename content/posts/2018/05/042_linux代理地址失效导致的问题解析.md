---
url: /blog/linux/HJCOI8NqUAG
title: "linux代理地址失效导致的问题解析"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 错误描述

任何需要使用http服务的程序都会存在假死或超时，包括wget、cur、yum等等。

## 初步发现

使用sudo 可是正常访问。

例如：

```
sudo yum install wget

```

## 然后发现

```
[root@jn6 tmp]# wget http://mirrors.163.com/.help/CentOS6-Base-163.repo
--2018-03-08 14:13:53--  http://mirrors.163.com/.help/CentOS6-Base-163.repo
Connecting to 10.1.205.242:3128...

```

根据上面的提示发现了

```
Connecting to 10.1.205.242:3128...

```

很明显是使用了代理，并且代理已经失效了。

## 解决办法

查看“/etc/profile”、“~/.bashrc”或者“~/.bash\_profile”将如下类似的行注释掉即可。

```
#ftp_proxy="http://10.1.205.242:3128";export ftp_proxy
#http_proxy="http://10.1.205.242:3128";export http_proxy
#https_proxy="http://10.1.205.242:3128";export https_proxy

```

## 问题总结

根据初步发现的结果可以了解到，sudo并没有解析“~/.bashrc”和“~/.bash\_profile”这两个文件。