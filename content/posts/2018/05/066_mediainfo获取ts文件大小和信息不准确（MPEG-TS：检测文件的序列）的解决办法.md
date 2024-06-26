---
url: /blog/linux/Sky_LU458CM
title: "mediainfo获取ts文件大小和信息不准确（MPEG-TS：检测文件的序列）的解决办法"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 解决mediainfo获取ts媒体信息不准确问题

## 场景

在/opt/目录下总共有200多个文件文件名分别如下：

/opt/2017LPL夏季赛第01集.ts

/opt/2017LPL夏季赛第02集.ts

/opt/2017LPL夏季赛第03集.ts

…

/opt/2017LPL夏季赛第227集.ts

/opt/2017LPL夏季赛第228集.ts

## 错误结果

```
mediainfo /opt/2017LPL夏季赛第01集.ts
General
ID                                       : 1 (0x1)
Complete name                            : Z:\vrs\new_upload\2018-01-16\2017LPL夏季赛第01集.ts
CompleteName_Last                        : Z:\vrs\new_upload\2018-01-16\2017LPL夏季赛第228集.ts
Format                                   : MPEG-TS
File size                                : 560 GiB
Duration                                 : 53mn 32s
Overall bit rate mode                    : Constant
Overall bit rate                         : 1 496 Mbps
Video
ID                                       : 100 (0x64)
Menu ID                                  : 1 (0x1)
Format                                   : AVC
Format/Info                              : Advanced Video Codec
Format profile                           : High@L4.0
Format settings, CABAC                   : No
Format settings, ReFrames                : 2 frames
Codec ID                                 : 27
Duration                                 : 53mn 32s
Bit rate mode                            : Constant
Bit rate                                 : 1 422 Mbps
Nominal bit rate                         : 7 800 Kbps / 7 800 Kbps
Width                                    : 1 920 pixels
Height                                   : 1 080 pixels
Display aspect ratio                     : 16:9
Frame rate                               : 25.000 fps
Color space                              : YUV
Chroma subsampling                       : 4:2:0
Bit depth                                : 8 bits
Scan type                                : Progressive
Bits/(Pixel*Frame)                       : 27.431
Stream size                              : 532 GiB (95%)
Writing library                          : x264 core 148 r2705 3f5ed56
Encoding settings                        : cabac=0 / ref=2 / deblock=1:0:0 / analyse=0x3:0x13 / me=hex / subme=7 / psy=1 / psy_rd=1.00:0.00 / mixed_ref=1 / me_range=16 / chroma_me=1 / trellis=1 / 8x8dct=1 / cqm=0 / deadzone=21,11 / fast_pskip=1 / chroma_qp_offset=-2 / threads=34 / lookahead_threads=5 / sliced_threads=0 / nr=0 / decimate=1 / interlaced=0 / bluray_compat=0 / constrained_intra=0 / bframes=3 / b_pyramid=0 / b_adapt=1 / b_bias=0 / direct=1 / weightb=1 / open_gop=0 / weightp=1 / keyint=32 / keyint_min=16 / scenecut=40 / intra_refresh=0 / rc_lookahead=32 / rc=cbr / mbtree=1 / bitrate=7800 / ratetol=1.0 / qcomp=0.60 / qpmin=0 / qpmax=69 / qpstep=4 / vbv_maxrate=7800 / vbv_bufsize=1560 / nal_hrd=cbr / filler=1 / ip_ratio=1.40 / aq=1:1.00
Audio
ID                                       : 101 (0x65)
Menu ID                                  : 1 (0x1)
Format                                   : MPEG Audio
Format version                           : Version 1
Format profile                           : Layer 2
Codec ID                                 : 3
Duration                                 : 53mn 32s
Bit rate mode                            : Constant
Bit rate                                 : 96.0 Kbps
Channel(s)                               : 2 channels
Sampling rate                            : 48.0 KHz
Compression mode                         : Lossy
Delay relative to video                  : -10ms
Stream size                              : 36.8 MiB (0%)
Menu
ID                                       : 4096 (0x1000)
Menu ID                                  : 1 (0x1)
Duration                                 : 53mn 32s
List                                     : 100 (0x64) (AVC) / 101 (0x65) (MPEG Audio)
Service name                             : RM_SERVICE_01
Service provider                         : RealMagic
Service type                             : digital television

```

## 正确结果

```
mediainfo /opt/2017LPL夏季赛第01集.ts
General
ID                                       : 1 (0x1)
Complete name                            : /data/stb/product/vrs/new_upload/./2018-01-16/2017LPL夏季赛第01集.ts
Format                                   : MPEG-TS
File size                                : 2.58 GiB
Duration                                 : 43mn 42s
Overall bit rate mode                    : Constant
Overall bit rate                         : 8 464 Kbps
Video
ID                                       : 100 (0x64)
Menu ID                                  : 1 (0x1)
Format                                   : AVC
Format/Info                              : Advanced Video Codec
Format profile                           : High@L4.0
Format settings, CABAC                   : No
Format settings, ReFrames                : 2 frames
Codec ID                                 : 27
Duration                                 : 43mn 42s
Bit rate mode                            : Constant
Bit rate                                 : 7 800 Kbps / 7 800 Kbps
Width                                    : 1 920 pixels
Height                                   : 1 080 pixels
Display aspect ratio                     : 16:9
Frame rate                               : 25.000 fps
Color space                              : YUV
Chroma subsampling                       : 4:2:0
Bit depth                                : 8 bits
Scan type                                : Progressive
Bits/(Pixel*Frame)                       : 0.150
Stream size                              : 2.43 GiB (94%)
Writing library                          : x264 core 148 r2705 3f5ed56
Encoding settings                        : cabac=0 / ref=2 / deblock=1:0:0 / analyse=0x3:0x13 / me=hex / subme=7 / psy=1 / psy_rd=1.00:0.00 / mixed_ref=1 / me_range=16 / chroma_me=1 / trellis=1 / 8x8dct=1 / cqm=0 / deadzone=21,11 / fast_pskip=1 / chroma_qp_offset=-2 / threads=34 / lookahead_threads=5 / sliced_threads=0 / nr=0 / decimate=1 / interlaced=0 / bluray_compat=0 / constrained_intra=0 / bframes=3 / b_pyramid=0 / b_adapt=1 / b_bias=0 / direct=1 / weightb=1 / open_gop=0 / weightp=1 / keyint=32 / keyint_min=16 / scenecut=40 / intra_refresh=0 / rc_lookahead=32 / rc=cbr / mbtree=1 / bitrate=7800 / ratetol=1.0 / qcomp=0.60 / qpmin=0 / qpmax=69 / qpstep=4 / vbv_maxrate=7800 / vbv_bufsize=1560 / nal_hrd=cbr / filler=1 / ip_ratio=1.40 / aq=1:1.00
Audio
ID                                       : 101 (0x65)
Menu ID                                  : 1 (0x1)
Format                                   : MPEG Audio
Format version                           : Version 1
Format profile                           : Layer 2
Codec ID                                 : 3
Duration                                 : 43mn 42s
Bit rate mode                            : Constant
Bit rate                                 : 96.0 Kbps
Channel(s)                               : 2 channels
Sampling rate                            : 48.0 KHz
Compression mode                         : Lossy
Delay relative to video                  : -10ms
Stream size                              : 30.0 MiB (1%)
Menu
ID                                       : 4096 (0x1000)
Menu ID                                  : 1 (0x1)
Duration                                 : 43mn 42s
List                                     : 100 (0x64) (AVC) / 101 (0x65) (MPEG Audio)
Service name                             : RM_SERVICE_01
Service provider                         : RealMagic
Service type                             : digital television

```

## 解决办法

根据作者的github上提交的代码描述

https://github.com/MediaArea/MediaInfoLib/commit/78f739893c85d4b1397276ef15badd160907b7aa

```
vim "Source/MediaInfo/Multiple/File_MpegTs.cpp"

void File_MpegTs::Streams_Accept()
{
    ...
    if (!IsSub)
    {
    ...
    //TestContinuousFileNames();
    ...
    }
}

```

我们只要将”TestContinuousFileNames();“这行注释掉即可解决默认获取ts文件序列问题