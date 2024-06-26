---
url: /blog/ffmpeg/BJDz88N580G
title: "ffmpeg逐行扫描转隔行扫描"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 命令参数

ffmpeg -i input -aspect 16:9 -c:v mpeg2video -b:v 4000k -minrate 4000k -ma…

## 命令参数

```
ffmpeg -i input -aspect 16:9 -c:v mpeg2video -b:v 4000k -minrate 4000k -maxrate 4000k -bufsize 2000k -dc 9 -flags +ilme+ildct -alternate_scan 1 -top 0 output

```

其实主要的就是如下参数：

```
-flags +ilme+ildct -alternate_scan 1 -top 0

```

alternate\_scan使用隔行转码，top不一般没有什么要求的话頂场优先就可以了。

## 隔行转逐行

```
ffmpeg -i input -aspect 16:9 -c:v mpeg2video -b:v 4000k -minrate 4000k -maxrate 4000k -bufsize 2000k -dc 9 -deinterlace  output

```

添加一个“deinterlace”即可。