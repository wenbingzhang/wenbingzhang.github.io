---
slug: "SkuD1wO4X"
title: "📝 FFmbc传统输出格式"
date: 2018-07-27T09:05:04+08:00
bookComments: false
bookHidden: false
weight: 10
---


## 苹果ProRes

```bash

```

## DVCPRO HD

```bash
# 将一个双声道音轨复制输出成两个单声道音轨
ffmbc -y -threads 8 -i 海外发行测试源文件0726.mp4  -target dvcprohd -tff -an 海外发行测试源文件0726-out.mxf  -acodec pcm_s24le -ar 48000 -ac 1 -newaudio -acodec pcm_s24le -ar 48000  -newaudio -acodec pcm_s24le  -ar 48000

# 将一个双声道音轨复制拆分成两个左右单声道音轨
ffmbc -y -threads 8 -i 海外发行测试源文件0726.mp4  -target dvcprohd -tff -an 海外发行测试源文件0726-out.mxf  -acodec pcm_s24le -ar 48000 -newaudio -acodec pcm_s24le -ar 48000 -newaudio -map_audio_channel 0:1:0:0:1:0 -map_audio_channel 0:1:1:0:2:0
```

## XDCAM HD422

```bash
# ffmpeg
ffmpeg -i test.mov -pix_fmt yuv422p -vcodec mpeg2video -non_linear_quant 1 -flags +ildct+ilme -top 1 -dc 10 -intra_vlc 1 -qmax 3 -lmin "1*QP2LAMBDA" -vtag xd5c -rc_max_vbv_use 1 -rc_min_vbv_use 1 -g 12 -b:v 50000k -minrate 50000k -maxrate 50000k -bufsize 8000k -acodec pcm_s16le -ar 48000 -bf 2 -ac 2 -f mxf_d10 output.mxf

# ffmbc
ffmbc  -y -threads 8 -i 先导片.mp4 -target xdcamhd422 -tff -acodec pcm_s24le 先导片-out.mov
```