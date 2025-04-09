---
url: /blog/ffmpeg/SJkrWTUVm
title: "ffmbc转码输出DVCPRO HD"
date: 2018-07-26T03:40:55+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 使用ffmbc多线程转码输出DVCPRO HD。分辨率为1440x1080，隔行扫描。

## 一

将一个双声道音轨复制输出成两个单声道音轨

```bash
ffmbc -y -threads 8 -i 海外发行测试源文件0726.mp4  -target dvcprohd -tff -an 海外发行测试源文件0726-out.mxf  -acodec pcm_s24le -ar 48000 -ac 1 -newaudio -acodec pcm_s24le -ar 48000  -newaudio -acodec pcm_s24le  -ar 48000

```

## 二

将一个双声道音轨复制拆分成两个左右单声道音轨

```bash
ffmbc -y -threads 8 -i 海外发行测试源文件0726.mp4  -target dvcprohd -tff -an 海外发行测试源文件0726-out.mxf  -acodec pcm_s24le -ar 48000 -newaudio -acodec pcm_s24le -ar 48000 -newaudio -map_audio_channel 0:1:0:0:1:0 -map_audio_channel 0:1:1:0:2:0

```