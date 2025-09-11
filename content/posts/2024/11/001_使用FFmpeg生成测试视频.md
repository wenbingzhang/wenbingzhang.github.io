---
slug: mCaGbs9LFDrNxXu9k29t9J
title: 使用FFmpeg生成测试视频
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
date: 2024-11-15 14:45:26+08:00
menu: main
---

## 生成测试视频

### 生成时分秒测试视频
```bash
ffmpeg -f lavfi -i testsrc=size=1280x720:rate=25 -vf "drawtext=text='%{pts\:hms} %{n}':x=(w-text_w)/2:y=100:fontsize=48:fontcolor=white:boxcolor=black@0.5:borderw=2" -t 10 -y output.mp4
```

### 生成时码测试视频
```bash
ffmpeg -f lavfi -i testsrc=size=3840x2160:rate=50 -vf drawtext="timecode='00\:00\:00\:00':rate=50:text='TCR\:':fontsize=100:fontcolor='white':boxcolor=0x000000AA:box=1:boxborderw=20:x=(w-text_w)/2:y=h-th-350" -y -t 120 -c:v libx264 -pix_fmt yuv420p output_with_drawtext.mp4
```
