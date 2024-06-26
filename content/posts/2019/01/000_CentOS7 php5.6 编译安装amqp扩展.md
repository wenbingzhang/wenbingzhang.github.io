---
url: /blog/linux/H10_K-VQ4
title: "CentOS7 php5.6 编译安装amqp扩展"
date: 2019-01-22T03:21:18+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> php 安装最新rabbitmq扩展

## 1、安装编译环境

```
yum install cmake gcc gcc-c++ make openssl-devel

```

## 2、安装rabbitmq-c

```
wget https://github.com/alanxz/rabbitmq-c/archive/v0.9.0.zip
unzip v0.9.0.zip
cd rabbitmq-c-0.9.0/
cmake -DCMAKE_INSTALL_PREFIX=/usr/local/rabbitmq-c-0.9.0/
make && make install

```

## 3、安装amqp

```
wget http://pecl.php.net/get/amqp-1.9.4.tgz
tar zxf amqp-1.9.4.tgz
cd amqp-1.9.4
/usr/bin/phpize
./configure --with-php-config=/usr/bin/php-config --with-amqp --with-librabbitmq-dir=/usr/local/rabbitmq-c-0.9.0

#由于rabbitmq-c编译出来的lib目录是lib64，所以我们要做一些小的修改
vim Makefile
#将 AMQP_SHARED_LIBADD = -Wl,-rpath,/usr/local/rabbitmq-c-0.9.0/lib -L/usr/local/rabbitmq-c-0.9.0/lib -lrabbitmq
#修改为 AMQP_SHARED_LIBADD = -Wl,-rpath,/usr/local/rabbitmq-c-0.9.0/lib64 -L/usr/local/rabbitmq-c-0.9.0/lib64 -lrabbitmq

make && make install

```

## 4、php.ini 添加模块

```
vi /usr/local/php/etc/php.ini
#增加
extension = /usr/lib64/php/modules/amqp.so

```

## 5、重启服务

```
systemctl restart php-fpm

```