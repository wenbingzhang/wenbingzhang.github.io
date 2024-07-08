---
url: /blog/ffmpeg/S1DOL84cLCz
title: "ffmoeg多音频合成(混流)使用方法"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> ffmpeg -i INPUT1 -i INPUT2 -i INPUT3 -filter_complex amix=inputs=3:duration=firs…

```
ffmpeg -i INPUT1 -i INPUT2 -i INPUT3 -filter_complex amix=inputs=3:duration=first:dropout_transition=3 OUTPUT

```

它接受下列参数：

inputs

```
输入数。如果没有指定，默认为2。

```

duration

```
如何确定流的结尾。

```

longest

```
最长的输入时间。（默认）

```

shortest

```
最短的输入时间。

```

first

```
第一个输入的时间。

```

dropout_transition

```
当输入流结束时，体积重整化的过渡时间（以秒为单位）。默认值是2秒。

```