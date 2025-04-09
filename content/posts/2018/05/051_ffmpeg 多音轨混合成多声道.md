---
url: /blog/ffmpeg/Hy0UI8V9I0M
title: "ffmpeg 多音轨混合成多声道"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 使用FFmpeg制作多声道视频

将8个音轨混合成双声道

```bash
ffmpeg -i input.mkv -filter_complex "[0:1][0:2][0:3][0:4][0:5][0:6][0:7][0:8] amerge=inputs=8" -c:a pcm_s16le output.mkv

```