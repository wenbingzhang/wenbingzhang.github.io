---
slug: "H1mn7tcA7"
title: "📝 FFmpeg裁剪视频"
date: 2018-11-27T08:49:10+08:00
bookComments: false
bookHidden: false
weight: 7
---


> ffmpeg命令裁剪视频，一般用于裁剪黑边

## 命令

```bash
ffmpeg -i input.mp4 -vf crop=iw/3:ih:0:0 output.mp4
ffmpeg -i input.mp4 -vf crop=iw/3:ih:iw/3:0 output.mp4
ffmpeg -i input.mp4 -vf crop=iw/3:ih:iw/3*2:0 output.mp4
```