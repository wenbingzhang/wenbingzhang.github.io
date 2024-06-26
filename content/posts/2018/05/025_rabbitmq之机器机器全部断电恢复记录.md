---
url: /blog/linux/rkCKI84cLAG
title: "rabbitmq之机器机器全部断电恢复记录"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

今天遇到一个rabbitmq集群同时断电，当机器全部启动的时候发现rabbitmq无法正常启动，然后发现如下日志。

```
=INFO REPORT==== 25-Apr-2018::11:11:07 ===
Starting RabbitMQ 3.5.3 on Erlang R16B03-1
Copyright (C) 2007-2014 GoPivotal, Inc.
Licensed under the MPL.  See http://www.rabbitmq.com/

=INFO REPORT==== 25-Apr-2018::11:11:07 ===
node           : rabbit@WIN-ACC2J7AGNM9
home dir       : C:\Users\Administrator
config file(s) : e:/RabbitMQ Data/rabbitmq.config (not found)
cookie hash    : kR4NuIdBr2n8/4Qt9uIgqQ==
log            : E:/RabbitMQ Data/log/rabbit@WIN-ACC2J7AGNM9.log
sasl log       : E:/RabbitMQ Data/log/rabbit@WIN-ACC2J7AGNM9-sasl.log
database dir   : e:/RabbitMQ Data/db/rabbit@WIN-ACC2J7AGNM9-mnesia

=WARNING REPORT==== 25-Apr-2018::11:11:07 ===
Kernel poll (epoll, kqueue, etc) is disabled. Throughput and CPU utilization may worsen.

=INFO REPORT==== 25-Apr-2018::11:11:08 ===
Memory limit set to 13095MB of 32738MB total.

=INFO REPORT==== 25-Apr-2018::11:11:08 ===
Disk free limit set to 50MB

=INFO REPORT==== 25-Apr-2018::11:11:08 ===
Limiting to approx 8092 file handles (7280 sockets)

=INFO REPORT==== 25-Apr-2018::11:11:38 ===
Timeout contacting cluster nodes: ['rabbit@WIN-2W6NDAIZBIA'].

BACKGROUND
==========

This cluster node was shut down while other nodes were still running.
To avoid losing data, you should start the other nodes first, then
start this one. To force this node to start, first invoke
"rabbitmqctl force_boot". If you do so, any changes made on other
cluster nodes after this one was shut down may be lost.

DIAGNOSTICS
===========

attempted to contact: ['rabbit@WIN-2W6NDAIZBIA']

rabbit@WIN-2W6NDAIZBIA:
  * connected to epmd (port 4369) on WIN-2W6NDAIZBIA
  * epmd reports: node 'rabbit' not running at all
                  no other nodes on WIN-2W6NDAIZBIA
  * suggestion: start the node

current node details:
- node name: 'rabbit@WIN-ACC2J7AGNM9'
- home dir: C:\Users\Administrator
- cookie hash: kR4NuIdBr2n8/4Qt9uIgqQ==

```

关键的地方在于中间的这段说明：

```
This cluster node was shut down while other nodes were still running.
To avoid losing data, you should start the other nodes first, then
start this one. To force this node to start, first invoke
"rabbitmqctl force_boot". If you do so, any changes made on other
cluster nodes after this one was shut down may be lost.

```

只要执行rabbitmqctl force\_boot，将所有的节点全部强制设置成最后一个关闭的即可。