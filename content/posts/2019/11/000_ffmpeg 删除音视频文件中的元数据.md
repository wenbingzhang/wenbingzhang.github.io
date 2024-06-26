---
url: /blog/ffmpeg/ovfEIBOES
title: "ffmpeg 删除音视频文件中的元数据"
date: 2019-11-07T09:55:49+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 清除mp3文件中自带的专辑（album），艺术家（artist），流派（genre）等元数据。

```
ffmpeg -i "test.mp3" -b:a 320k -map_metadata -1 -y "out.mp3"

```

-map\_metadata -1 表示清除所有元数据