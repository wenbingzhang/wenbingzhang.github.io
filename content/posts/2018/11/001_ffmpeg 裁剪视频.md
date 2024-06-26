---
url: /blog/ffmpeg/H1mn7tcA7
title: "ffmpeg 裁剪视频"
date: 2018-11-27T08:49:10+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> ffmpeg命令裁剪视频，一般用于裁剪黑边

![ffmpeg_HJ9roRU2Q.png](/static/uploads/BkjYYAI3X/img/ffmpeg_HJ9roRU2Q.png)

## 说明

![FFmpeg裁剪视频.png](/static/uploads/H1mn7tcA7/img/FFmpeg裁剪视频_Sk624F907.png)

## 命令

```
ffmpeg -i input.mp4 -vf crop=iw/3:ih:0:0 output.mp4
ffmpeg -i input.mp4 -vf crop=iw/3:ih:iw/3:0 output.mp4
ffmpeg -i input.mp4 -vf crop=iw/3:ih:iw/3*2:0 output.mp4

```