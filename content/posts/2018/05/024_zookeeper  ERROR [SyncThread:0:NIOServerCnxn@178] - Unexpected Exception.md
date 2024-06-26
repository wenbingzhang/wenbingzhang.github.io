---
url: /blog/linux/BJNG8UEc80G
title: "zookeeper  ERROR [SyncThread:0:NIOServerCnxn@178] - Unexpected Exception"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

昨天在使用zookeeper的时候发现一个报错，报错信息如下

```
Dec 16 20:40:46 api zookeeper: 2016-12-16 20:40:46,471 [myid:] - ERROR [SyncThread:0:NIOServerCnxn@178] - Unexpected Exception:
Dec 16 20:40:46 api zookeeper: java.nio.channels.CancelledKeyException
Dec 16 20:40:46 api zookeeper: at sun.nio.ch.SelectionKeyImpl.ensureValid(SelectionKeyImpl.java:73)
Dec 16 20:40:46 api zookeeper: at sun.nio.ch.SelectionKeyImpl.interestOps(SelectionKeyImpl.java:77)
Dec 16 20:40:46 api zookeeper: at org.apache.zookeeper.server.NIOServerCnxn.sendBuffer(NIOServerCnxn.java:151)
Dec 16 20:40:46 api zookeeper: at org.apache.zookeeper.server.NIOServerCnxn.sendResponse(NIOServerCnxn.java:1081)
Dec 16 20:40:46 api zookeeper: at org.apache.zookeeper.server.FinalRequestProcessor.processRequest(FinalRequestProcessor.java:404)
Dec 16 20:40:46 api zookeeper: at org.apache.zookeeper.server.SyncRequestProcessor.flush(SyncRequestProcessor.java:200)
Dec 16 20:40:46 api zookeeper: at org.apache.zookeeper.server.SyncRequestProcessor.run(SyncRequestProcessor.java:131)

```

我从官网看到一个错误的反馈及修复补丁–>传送门我使用的版本是3.4.6在新的版本3.4.8已经解决这个问题。