---
url: /blog/ffmpeg/SkNmLLVcUCf
title: "iOS FFmpeg集成"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> FFmpeg标准库

概念:

FFmpeg是一套可以用来记录、转换数字音频、视频，并能将其转化为流的开源计算机程序。

采用LGPL或GPL许可证。它提供了录制…

# FFmpeg标准库

## 概念:

FFmpeg是一套可以用来记录、转换数字音频、视频，并能将其转化为流的开源计算机程序。

采用LGPL或GPL许可证。它提供了录制、转换以及流化音视频的完整解决方案。 它包含了非常先进的音频/视频编解码库libavcodec.

### 功能:

多媒体视频处理工具FFmpeg有非常强大的功能包括视频采集功能、视频格式转换、视频抓图、给视频加水印等。

#### 1. 视频采集功能:

ffmpeg视频采集功能非常强大，不仅可以采集视频采集卡或USB摄像头的图像，还可以进行屏幕录制，同时还支持以RTP方式将视频流传送给支持RTSP的流媒体服务器，支持直播应用。

#### 2. 视频格式转换功能:

ffmpeg可以轻易地实现多种视频格式之间的相互转换(wma,rm,avi,mod等)，例如可以将摄录下的视频avi等转成视频网站所采用的flv格式。

#### 3. 视频截图功能:

对于选定的视频，截取指定时间的缩略图。视频抓图，获取静态图和动态图，不提倡抓gif文件;因为抓出的gif文件大而播放不流畅。

#### 4. 给视频加水印功能:

使用ffmpeg视频添加水印(logo)。

### 项目组成:

- libavformat：用于各种音视频封装格式的生成和解析，包括获取解码所需信息以生成解码上下文结构和读取音视频帧等功能；

- libavcodec：用于各种类型声音/图像编解码；

- libavutil：包含一些公共的工具函数；

- libswscale：用于视频场景比例缩放、色彩映射转换；

- libpostproc：用于后期效果处理；

- ffmpeg：该项目提供的一个工具，可用于格式转换、解码或电视卡即时编码等；

- ffsever：一个 HTTP 多媒体即时广播串流服务器；

- ffplay：是一个简单的播放器，使用ffmpeg 库解析和解码，通过SDL显示


## 集成

#### 1. 前期准备

> 2. 下载脚本:https://github.com/libav/gas-preprocessor
>
> 4. 复制gas-preprocessor.pl到/usr/sbin下，(这里需要完全关闭苹果的SIP安全功能, 具体请参考这篇文章
>
>
> 终端下修改文件权限, 指令:
>
> 1. > ```
>    > chmod 777 /usr/sbin/gas-preprocessor.p
>    >
>    > ```
>
> 2. 安装yasm, 指令如下:

```
* curl http://www.tortall.net/projects/yasm/releases/yasm-1.2.0.tar.gz >yasm.tar.gz
* tar xzvf yasm.tar.gz
* cd yasm-1.2.0
* ./configure
* make
* sudo make install

```

#### 2. 下载ffmpeg

> 1. 下载脚本：https://github.com/kewlbear/FFmpeg-iOS-build-script
>
> 2. 解压，找到文件 build-ffmpeg.sh
>
> 4. 编译完成后，终端进入FFmpeg-iOS-build-script目录，然后终端输入 ./build-ffmpeg.sh
>
>
>    lipo，这个命令是将.a文件合并成一个

#### 3. 集成

> 1. 把ffmpeg-iOS文件加入到工程中, 引入头文件 `#include "avformat.h"`, 执行方法
>
>    `av_register_all()`, 并修改任一文件名由 `.m` 变为 `.mm`
>
> 2. **注** : 编译的时候报错： `libavcodec/avcodec.h' file not found` ，修改 `Header
>    search paths` 里的路径：$(PROJECT_DIR)/FFmpeg-iOS/include
>
>
>    添加额外的库引用: `libz.tbd` `libbz2.tbd` `libiconv.tbd`
>
> 3. 编译, 通过.