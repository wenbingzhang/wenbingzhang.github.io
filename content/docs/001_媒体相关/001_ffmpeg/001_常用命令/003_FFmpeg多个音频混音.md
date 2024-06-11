---
slug: "Mv3bzfgqM"
title: "📝 FFmpeg多个音频混音"
date: 2020-10-13T08:24:19+08:00
bookComments: false
bookHidden: false
weight: 3
---


> 使用FFmpeg中的adelay和amix滤镜给音频做混音

在30秒后混合1个音频

```bash
ffmpeg -i 1-1.mp3 -i 2.mp3 -filter_complex "[1]adelay=delays=30s:all=1[aud1];[0][aud1]amix=inputs=2" -vsync 2 -y 3.mp3

```

在30秒后混合2个音频

```bash
ffmpeg -i 1-1.mp3 -i 2.mp3 -i 3.mp3 -filter_complex "[1]adelay=delays=30s:all=1[aud1];[2]adelay=delays=30s:all=1[aud2];[0][aud1][aud2]amix=inputs=3" -vsync 2 -y 4.mp3

```

混合多个参照混合2个的命令修改下即可