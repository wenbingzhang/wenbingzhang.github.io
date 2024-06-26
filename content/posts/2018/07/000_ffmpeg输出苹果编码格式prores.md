---
url: /blog/ffmpeg/SkuD1wO4X
title: "ffmpeg输出苹果编码格式prores"
date: 2018-07-27T09:05:04+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> ffmpeg输出苹果编码格式prores。分辨率1080p，25帧，5个音轨。

```
ffmpeg -i 06无字幕mp4-使用此视频的画面.mp4 -i 06有字幕-使用此视频的国际音轨.mov -map 0:v -s 1920x1080 -r 25 -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le -map 1:1 -acodec pcm_s24le -ar 48000 -ac 1 -map 1:2 -acodec pcm_s24le -ar 48000 -ac 1 -map 1:3 -acodec pcm_s24le -ar 48000 -ac 1 -map 1:4 -acodec pcm_s24le -ar 48000 -ac 1 -map 1:5 -acodec pcm_s24le -ar 48000 -ac 1 06-out.mov

```