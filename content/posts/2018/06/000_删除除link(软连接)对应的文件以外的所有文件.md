---
url: /blog/linux/H10wzCxGX
title: "删除除link(软连接)对应的文件以外的所有文件"
date: 2018-06-27T09:08:21+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 使用find和readlink删除除link(软连接)对应的文件以外的所有文件，一般用于自动删除日志文件。

## 脚本

```
#!/bin/bash

linkArr=`find $1 -type l -exec readlink {} \;`
fileArr=`find $1 -type f -name "*${2}*"`

for f in $fileArr;do
  isLink=false
  for l in $linkArr;do
    #判断当前文件是否为link对应的文件
    if [ "${f##*/}" == "$l" ];then
      isLink=true
      break
    fi
  done
  if [ $isLink == false ];then
    rm -f $f
  fi
done

```

## 说明

### 功能

删除除link对应的文件以外的所有文件

### 参数

$1 第一个位置参数为需要扫描的目录

$2 模糊搜索文件名