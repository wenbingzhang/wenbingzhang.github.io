---
url: /blog/linux/HkgnaWVNm
title: "Schema Parsing Failed: unknown field 'id' [Zookeeper, SolrCloud]"
date: 2018-07-24T02:31:15+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 不小心删除solr的主键id，导致报错Schema Parsing Failed: unknown field ‘id’

## 问题描述

Schema Parsing Failed: unknown field ‘id’

## 解决方法

关闭zookeeper、solr服务并删除zookeeper数据，然后重新启动zookeeper、solr服务。

## 参考

http://grokbase.com/t/lucene/solr-user/149pnr31bh/schema-parsing-failed-

unknown-field-id-zookeeper-solrcloud