---
url: /blog/ffmpeg/S1EdILNqU0M
title: "Rematrix is needed between 10 channels and 7.1(wide) but there is not enough"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 解决办法

将10个声道拆分成10个音轨

ffmpeg -i INPUTFILE -filter_complex “[0:a]pan=mono|c0=c0[…

## 解决办法

将10个声道拆分成10个音轨

```bash
ffmpeg -i INPUTFILE  -filter_complex "[0:a]pan=mono|c0=c0[a0];[0:a]pan=mono|c0=c1[a1];[0:a]pan=mono|c0=c2[a2];[0:a]pan=mono|c0=c3[a3];[0:a]pan=mono|c0=c4[a4];[0:a]pan=mono|c0=c5[a5];[0:a]pan=mono|c0=c6[a6];[0:a]pan=mono|c0=c7[a7];[0:a]pan=mono|c0=c8[a8];[0:a]pan=mono|c0=c9[a9]" -map "[a0]" -map "[a1]" -map "[a2]" -map "[a3]" -map "[a4]" -map "[a5]" -map "[a6]" -map "[a7]" -map "[a8]" -map "[a9]" -vn -c:a pcm_s24le  OUTPUTFILE

ffmpeg -i INPUTFILE -vn -c:a pcm_s24le -map 0:1 -filter:a:0 "pan=mono|c0=c0" -map 0:1 -filter:a:1 "pan=mono|c0=c1" -map 0:1 -filter:a:2 "pan=mono|c0=c2" -map 0:1 -filter:a:3 "pan=mono|c0=c3" -map 0:1 -filter:a:4 "pan=mono|c0=c4" -map 0:1 -filter:a:5 "pan=mono|c0=c5" -map 0:1 -filter:a:6 "pan=mono|c0=c6" -map 0:1 -filter:a:7 "pan=mono|c0=c7" -map 0:1 -filter:a:8 "pan=mono|c0=c8" -map 0:1 -filter:a:9 "pan=mono|c0=c9" OUTPUTFILE

```