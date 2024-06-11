---
slug: "UtHueryud"
title: "📝 FFmpeg给视频添加水印"
date: 2020-07-15T06:31:49+08:00
bookComments: false
bookHidden: false
weight: 4
---


> 图片水印、文字水印、画中画

## 图片水印

```bash
ffmpeg -i input.mp4 -vf "movie=wenzi.png[watermark];[in][watermark] overlay=main_w-overlay_w-10:main_h-overlay_h-10[out] " output.mp4
```

* -i: 一般表示输入 input.mp4表示要处理的视频源
* -vf: 滤镜相关，视频裁剪，水印等等操作都需要它完成
* movie: wenzi.png 要添加的水印图片地址
* overlay: 水印参数
* main_w-overlay_w-10: 水印在x轴的位置，也可以写成x=main_w-overlay_w-10
* main_h-overlay_h-10: 水印在y轴的位置

```bash
ffmpeg -i input.mp4 -i logo.png -filter_complex 'overlay=x=10:y=main_h-overlay_h-10' output.mp4
```

* -filter_complex: 相比-vf, filter_complex适合开发复杂的滤镜功能，如同时对视频进行裁剪并旋转。参数之间使用逗号（，）隔开即可
* main_w: 视频宽度
* overlay_w: 要添加的图片水印宽度
* main_h: 视频高度
* overlay_h: 要添加的图片水印宽度

## 文字水印

```bash
ffmpeg -i input.mp4 -vf "drawtext=fontfile=simhei.ttf: text=‘技术是第一生产力’:x=10:y=10:fontsize=24:fontcolor=white:shadowy=2" output.mp4
```

* fontfile: 字体类型
* text: 要添加的文字内容
* fontsize: 字体大小
* fontcolor: 字体颜色

## 画中画

只显示1遍，后边重复显示最后一帧。

```bash
ffmpeg -i bunny.mp4 -vf "movie=test.mov[logo];[0:v][logo]overlay=x=100:y=100"  -y out.mp4
```

mov一直循环显示。 添加 **loop=0,setpts=N/FRAME_RATE/TB** 即可。

```bash
ffmpeg -i bunny.mp4 -vf "movie=test.mov:loop=0,setpts=N/FRAME_RATE/TB[logo];[0:v][logo]overlay=x=100:y=100"  -y out.mp4
```

只显示一遍 添加eof_action即可。

```bash
ffmpeg -i bunny.mp4 -vf "movie=test.mov[logo];[0:v][logo]overlay=x=100:y=100:eof_action=pass" -vframes 1000 -y out.mp4
```