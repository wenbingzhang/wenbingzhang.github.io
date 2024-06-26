---
url: /blog/linux/B1sYILV9UAf
title: "zabbix自定义监控项之修复net.tcp.listen不准确问题"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 在客户端修改配置

vim /etc/zabbix/zabbix\_agentd.conf

UnsafeUserParameters=1

vim /etc/za…

在客户端修改配置

```
vim /etc/zabbix/zabbix_agentd.conf
UnsafeUserParameters=1

vim /etc/zabbix/zabbix_agentd.d/net_tcp_listen.conf
UserParameter=net.tcp.listen.grep[*],grep -q $$(printf '%04X.00000000:0000.0A' $1) /proc/net/tcp && echo 1 || echo 0

/etc/init.d/zabbix-agent restart

```