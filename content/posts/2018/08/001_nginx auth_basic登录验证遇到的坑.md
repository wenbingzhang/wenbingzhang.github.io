---
url: /blog/linux/ByaB7yPSQ
title: "nginx auth_basic登录验证遇到的坑"
date: 2018-08-07T09:26:11+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> htpasswd默认使用crypt()加密，创建的密码只有前8位有效

## 问题

```bash
htpasswd -c /etc/nginx/.htpasswd  test

```

假如，密码为abcd12345

那么在登录的时候，不管是输入“abcd1234”、”abcd12345“或”abcd123456789sdjkal“ 都能通过验证。

## 解析

因为htpasswd默认使用crypt()加密，而crypt()加密只有前面8位有效。

## 解决方法

```bash
htpasswd -m -c /etc/nginx/.htpasswd  test

```

在创建账号的时候指定”-m“参数，使用MD5加密就能解决这个问题了。