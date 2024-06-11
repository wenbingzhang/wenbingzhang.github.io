---
slug: "BJDz88N580G"
title: "📝 FFmpeg逐行转隔行"
date: 2018-05-14T04:45:01+08:00
bookComments: false
bookHidden: false
weight: 11
---


## 命令参数

```bash
ffmpeg -i input -aspect 16:9 -c:v mpeg2video -b:v 4000k -minrate 4000k -maxrate 4000k -bufsize 2000k -dc 9 -flags +ilme+ildct -alternate_scan 1 -top 0 output
```

其实主要的就是如下参数：

```bash
-flags +ilme+ildct -alternate_scan 1 -top 0
```

alternate_scan使用隔行转码，top不一般没有什么要求的话頂场优先就可以了。

## 隔行转逐行

```bash
ffmpeg -i input -aspect 16:9 -c:v mpeg2video -b:v 4000k -minrate 4000k -maxrate 4000k -bufsize 2000k -dc 9 -deinterlace  output
```

添加一个“deinterlace”即可。