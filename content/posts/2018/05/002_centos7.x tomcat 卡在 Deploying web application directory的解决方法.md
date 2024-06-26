---
url: /blog/linux/r17GULVq80M
title: "centos7.x tomcat 卡在 Deploying web application directory的解决方法"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 问题

前天在部署一个项目的时候，发现tomcat启动，总是卡在INFO: Deploying web application directory

……这个地方…

## 问题

前天在部署一个项目的时候，发现tomcat启动，总是卡在INFO: Deploying web application directory

……这个地方，有时候能启动成功，但是需要等待很长的时间。于是搜索了一下，发现原来是tomcat启动的时候调用了linux的一个随机数设备/dev/urandom（/dev/random）。

## 解决

修改$JAVA\_HOME/jre/lib/security/java.security

文件，替换securerandom.source=file:/dev/random为securerandom.source=file:/dev/./urandom。不管securerandom.source的值是什么，都将其修改成securerandom.source=file:/dev/./urandom，否则不生效。