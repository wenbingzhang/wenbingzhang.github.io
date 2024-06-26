---
url: /blog/ffmpeg/BkjYYAI3X
title: "ffmpeg加水印"
date: 2018-10-31T07:48:43+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> FFmpeg是一套可以用来记录、转换数字音频、视频，并能将其转化为流的开源计算机程序。采用LGPL或GPL许可证。它提供了录制、转换以及流化音视频的完整解决方案。它包含了非常先进的音频/视频编解码库libavcodec，为了保证高可移植性和编解码质量，libavcodec里很多code都是从头开发的。

![ffmpeg.png](/static/uploads/BkjYYAI3X/img/ffmpeg_HJ9roRU2Q.png)

## movie过滤器

```
ffmpeg -i inputfile -vf  "movie=masklogo,scale= 60: 30[watermask]; [in] [watermask] overlay=30:10 [out]" outfile

```

参数说明

marklogo:添加的水印图片；

scale：水印大小，水印长度＊水印的高度；

overlay：水印的位置，距离屏幕左侧的距离＊距离屏幕上侧的距离；mainW主视频宽度，

mainH主视频高度，overlayW水印宽度，overlayH水印高度

左上角overlay参数为 overlay=0:0

右上角为 overlay= main\_w-overlay\_w:0

右下角为 overlay= main\_w-overlay\_w:main\_h-overlay\_h

左下角为 overlay=0: main\_h-overlay\_h

```
 上面的0可以改为5，或10像素，以便多留出一些空白。

```

## 合流

```
 ffmpeg -i input -i logo -filter_complex 'overlay=10:main_h-overlay_h-10' output

```

input:输入流

logo：水印文件，也可以是一个流。注意：需要编译时把相应的解码器编译。例如PNG图片。需要编译PNG解码器。Ffmpeg才能够识别图片文件，把图片做为一

种流。注意：PNG图片必须含有alpha通道。Overlay过滤器是根据alpha通道来进行复盖的。所以，你想要透明效果时，须先制做一张透明的PNG图片。