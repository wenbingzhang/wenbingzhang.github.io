---
url: /blog/ffmpeg/BkM7UIN9IRG
title: "FFmpeg转码"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 1.分离视频音频流

ffmpeg -i input\_file -vcodec copy -an output\_file\_video　　//分离视频流

ffm…

1.分离视频音频流

ffmpeg -i input\_file -vcodec copy -an output\_file\_video　　//分离视频流

ffmpeg -i input\_file -acodec copy -vn output\_file\_audio　　//分离音频流

2.视频解复用

ffmpeg –i test.mp4 –vcodec copy –an –f m4v test.264

ffmpeg –i test.avi –vcodec copy –an –f m4v test.264

3.视频转码

ffmpeg –i test.mp4 –vcodec h264 –s 352\*278 –an –f m4v test.264//转码为码流原始文件

ffmpeg –i test.mp4 –vcodec h264 –bf 0 –g 25 –s 352\*278 –an –f m4v

test.264//转码为码流原始文件

ffmpeg –i test.avi -vcodec mpeg4 –vtag xvid –qsame test\_xvid.avi//转码为封装文件

//-bf B帧数目控制，-g 关键帧间隔控制，-s 分辨率控制

4.视频封装

ffmpeg –i video\_file –i audio\_file –vcodec copy –acodec copy output\_file

5.视频剪切

ffmpeg –i test.avi –r 1 –f image2 image-%3d.jpeg//提取图片

ffmpeg -ss 0:1:30 -t 0:0:20 -i input.avi -vcodec copy -acodec copy

output.avi//剪切视频

//-r 提取图像的频率，-ss 开始时间，-t 持续时间

6.视频录制

ffmpeg –i rtsp://192.168.3.205:5555/test –vcodec copy out.avi

7.YUV序列播放

ffplay -f rawvideo -video\_size 1920x1080 input.yuv

8.YUV序列转AVI

ffmpeg –s w\*h –pix\_fmt yuv420p –i input.yuv –vcodec mpeg4 output.avi