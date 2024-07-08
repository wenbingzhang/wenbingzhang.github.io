---
url: /blog/ffmpeg/B1mILV58AM
title: "ffmpeg获取display_picture_number对应帧信息"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 使用方式

ffmpeg -i input -vf “select=eq(n\,15237)“,showinfo -an -f null /dev/null…

## 使用方式

```
ffmpeg -i input  -vf "select=eq(n\,15237)",showinfo -an -f null  /dev/null

```

## 输出结果

15237为display_picture_number

```
[Parsed_showinfo_1 @ 0x41ca760] n:   0 pts:54860400 pts_time:609.56  pos:427032896 fmt:yuv420p sar:1/1 s:1920x1080 i:T iskey:0 type:B checksum:A2FB0133 plane_checksum:[7E1FA1A9 3D005549 67BC0A32] mean:[92 127 134] stdev:[62.5 9.2 20.7]

```

## 参数解释

```
### showinfo ### 不改变输入而在行中显示每帧信息。
显示的信息以`key/value`的序列形式给出
下面是将显示在输出中的值：

- n
帧序数，从0开始计数

- pts
输入帧的时间戳，以时基为单位，时间依赖于输入

- pts_time
按秒计的时间戳

- pos
输入帧在输入流中的偏移定位，-1表示信息不可用和/或无意义（例如合成视频中）

- fmt
像素格式名

- sar
输入帧的宽高比，表示为`num/den`格式

- s
输入帧尺寸，语法同于[视频尺寸（分辨率）](ffmpeg-doc-cn-07.md#视频尺寸（分辨率）)

- i
交错模式 ("P"对应 "逐行", "T" 对应上场优先, "B"为下场优先t)

- iskey
为1表示是关键帧，0则不是

- type
输入帧图片类型 ("I"对应I帧, "P" 对应P帧, "B" 对应B帧,或者 "?"对应未知类型).参考定义与`libavutil/avutil.h`中的`av_get_picture_type_char`函数和`

- checksum
输入帧所有信息内容的 Adler-32校验值 (以16进制输出)

- plane_checksum
输入帧所有信息内容的 Adler-32校验值 (以16进制输出), 以格式"[c0 c1 c2 c3]"显示

```