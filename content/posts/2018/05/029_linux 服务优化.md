---
url: /blog/linux/rktZUU4980G
title: "linux 服务优化"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 1、需要开启的常见服务

1、系统提供的服务

2、iptables，network，ssh,syslog

## 2、需要关闭的服务

1、bluetooth,fprint,ip6tables,cups,netfs,ntp等。除以上4个服务外，其他服务都可以关闭。

## 3、关闭掉多余的终端

RHEL5:/etc/inittab RHEL6:/etc/sysconfig/init

## 4、关闭ipv6

#vim /etc/sysconfig/network-script/ifcfg-eth0

```
NETWORK_IPV6 = no

```

#vim /etc/modprobe.d/ipv6.conf

```
alias net-pf-10 off
alias ipv6 off

```