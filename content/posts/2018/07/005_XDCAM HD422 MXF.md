---
url: /blog/ffmpeg/Hy8NTRZmm
title: "XDCAM HD422 MXF"
date: 2018-07-10T07:25:03+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 分别使用ffmpeg ffmbc 实现 输出XDCAM HD422 MXF文件

## ffmpeg

```
ffmpeg -i test.mov -pix_fmt yuv422p -vcodec mpeg2video -non_linear_quant 1 -flags +ildct+ilme -top 1 -dc 10 -intra_vlc 1 -qmax 3 -lmin "1*QP2LAMBDA" -vtag xd5c -rc_max_vbv_use 1 -rc_min_vbv_use 1 -g 12 -b:v 50000k -minrate 50000k -maxrate 50000k -bufsize 8000k -acodec pcm_s16le -ar 48000 -bf 2 -ac 2 -f mxf_d10 output.mxf

```

## ffmbc

```
ffmbc  -y -threads 8 -i 先导片.mp4 -target xdcamhd422 -tff -acodec pcm_s24le 先导片-out.mov

```