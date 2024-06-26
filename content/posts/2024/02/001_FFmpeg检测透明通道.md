---
slug: "KkcC5T2Y88HYbAfPourudv"
title: "FFmpeg检测透明通道"
date: 2024-02-06T16:31:04+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

# 检测透明通道

## FFmpeg命令
```bash
$ ffmpeg -v error -i 123.mp4 -vf "select='eq(n,0)', alphaextract" -f null /dev/null

[Parsed_alphaextract_1 @ 0x7fe8f5208100] Requested planes not available.
[Parsed_alphaextract_1 @ 0x7fe8f5208100] Failed to configure input pad on Parsed_alphaextract_1
[vf#0:0 @ 0x7fe8f5005f40] Error reinitializing filters!
Failed to inject frame into filter network: Invalid argument
Error while filtering: Invalid argument
[out#0/null @ 0x7fe8f5004900] Nothing was written into output file, because at least one of its streams received no packets.
```

## 判断条件
  如果出现以上报错信息，则说明视频中没有透明通道。
