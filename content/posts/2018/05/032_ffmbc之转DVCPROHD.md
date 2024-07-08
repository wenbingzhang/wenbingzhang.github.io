---
url: /blog/ffmpeg/BkpKIL498RM
title: "ffmbc之转DVCPROHD"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> ffmbc -i xx.ts -vcodec dvvideo -flags +ildct+ilme -tff -pix_fmt yuv422p -vf scal…

```
ffmbc -i xx.ts -vcodec dvvideo -flags +ildct+ilme -tff -pix_fmt yuv422p -vf scale=1440:1080:1 -acodec pcm_s16le -ar 48000 -ac 1 -y xx.mxf

```