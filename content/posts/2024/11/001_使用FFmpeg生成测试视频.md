---
slug: mCaGbs9LFDrNxXu9k29t9J
title: 使用FFmpeg生成测试视频
description:
categories:
  - default
tags:
  - default
date: 2024-11-15 14:45:26+08:00
menu: main
---

## 生成23.976fps的测试视频
```bash
ffmpeg -f lavfi -i testsrc=size=1280x720:rate=30 -vf "drawtext=text='%{pts\:hms} %{n}':x=(w-text_w)/2:y=100:fontsize=48:fontcolor=white:boxcolor=black@0.5:borderw=2" -r 23.976 -t 10 -y output.mp4
```