---
url: /blog/linux/Sykc8UNqICz
title: "zabbix之无法启动问题及解决办法"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

1、

错误提示

```
zabbix_agentd [1749]: cannot create PID file [/var/run/zabbix/zabbix_agentd.pid]: [2] No such file or directory

```

解决方法

```
mkdir /var/run/zabbix/
chown zabbix.zabbix /var/run/zabbix/
chmod g+w /var/run/zabbix/
touch /var/run/zabbix/zabbix_agentd.pid
/etc/init.d/zabbix-agent restart
ps aux | grep zabbix

```