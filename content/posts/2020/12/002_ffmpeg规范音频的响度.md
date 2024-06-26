---
url: /blog/ffmpeg/ROS_KIbGg
title: "ffmpeg规范音频的响度"
date: 2020-12-22T14:53:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 通过FFmpeg内置滤镜、手动调整音量、或者ffmpeg-normalize实现对响度的控制。

## 内置归一化滤波器

loudnorm：通过EBU R.128进行响度标准化。您可以设置积分的体积目标，体积范围目标或最大真实峰。建议用于发布音频和视频，并被世界各地的广播公司使用。

dynaudnorm：“智能”响度归一化，不进行裁剪。动态地将规范化应用于文件的窗口部分。应谨慎使用，因为这可能会改变声音的特性。

```bash
#fdk_aac编码器
ffmpeg200421 -i "source_audio.ts" -c:a  libfdk_aac   -strict -2 -ac 2 -ar 48000 -ab 196k -af "[0:a]pan=stereo| FL < FL + 0.5*FC + 0.6*BL + 0.6*SL | FR < FR + 0.5*FC + 0.6*BR + 0.6*SR,loudnorm=I=-23:LRA=6:tp=-1" -y -cutoff 20000 "ac_5m.ts"

#aac编码器
ffmpeg -i "source_audio.ts" -c:a aac   -strict -2 -ac 2 -ar 48000 -ab 196k -af "loudnorm=I=-23:LRA=6:tp=-1" -y -cutoff 20000 "1_aac_dynaudnorm_ac_5m.ts"

```

### 常用方式

```bash
ffmpeg -i input.mp4  -vn -acodec libfdk_aac -ac 2 -ar 44100 -af loudnorm=I=-16:TP=-1:LRA=7:print_format=json -f null /dev/null

```

## 手动规范音频的响度

首先，您需要分析音频流以获取最大音量，以查看规范化是否起作用。

```bash
ffmpeg -i video.avi -af "volumedetect" -vn -sn -dn -f null /dev/null

[Parsed_volumedetect_0 @ 0x7f8ba1c121a0] mean_volume: -16.0 dB
[Parsed_volumedetect_0 @ 0x7f8ba1c121a0] max_volume: -5.0 dB
[Parsed_volumedetect_0 @ 0x7f8ba1c121a0] histogram_0db: 87861

```

使用音量过滤器（volume）

```bash
ffmpeg -i video.mp4 -af "volume=5dB" -c:v copy -c:a aac -cutoff 20000  output.mp4

```

volume=5dB 表示增加5分贝的音量

volume=-5dB 表示减少5分贝的音量

volume=1.5 表示放大1.5倍的音量

## ffmpeg-normalize

[ffmpeg-normalize](https://github.com/slhck/audio-normalize) 是一个Python库，可以使用pip安装，详细的使用方式在github上有文档，这里就不做过多的介绍了。