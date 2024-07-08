---
url: /blog/linux/S1ywxQEN7
title: "solrcloud上传配置文件"
date: 2018-07-24T04:15:05+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 使用solr自带的工具zkcli.sh上传配置文件

```
chmod +x  /opt/solr/server/scripts/cloud-scripts/zkcli.sh
cp -r /opt/solr-7.3.1/server/solr/configsets/_default/conf /opt/solr-7.3.1/server/solr/_test1b/
/opt/solr/server/scripts/cloud-scripts/zkcli.sh -cmd upconfig -zkhost 10.1.201.49:2181,10.1.201.50:2181 -confname test1b -confdir /opt/solr-7.3.1/server/solr/_test1b/

```

复制的时候一定要复制server/solr/configsets/_default/conf目录，而不是server/solr/configsets/_default

，昨天我就是直接复制的_default目录导致一直报错。