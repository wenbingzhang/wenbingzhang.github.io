---
url: /blog/linux/rJa7oi0EQ
title: "solr oom_killer"
date: 2018-08-01T04:18:18+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 记录oom\_solr触发的问题分析及解决方法

昨天在测试solr\_cloud的时候，看到$solr\_home/logs下面有一个这样的日志

```
solr_oom_killer-8983-2018-07-31_10_45_56.log

```

刚开始还以为是Linux系统的oom\_killer,然后在/var/log/message中找日志，发现没有，当时就奇怪了，触发了oom\_killer但是没记录日志？于是经过一番折腾终于发现问题了。

通过以下命令找到一个参数 -XX:OnOutOfMemoryError=/opt/solr/bin/oom\_solr.sh

```
ps aux | grep java

```

最后搜索发现是javaVM堆栈溢出触发的oom\_solr,修改参数-Xms8g-Xmx8g,就解决这个问题了。