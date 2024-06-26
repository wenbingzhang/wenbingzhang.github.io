---
url: /blog/ffmpeg/HJbQ88N980f
title: "AAC 到 PCM 音频解码"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 最近遇到在 iOS 平台上实时播放 AAC 音频数据流, 一开始尝试用 AudioQueue 直接解 AAC 未果, 转而将 AAC 解码为 PCM,
>
> 最终实…
>
> 最近遇到在 iOS 平台上实时播放 AAC 音频数据流, 一开始尝试用 AudioQueue 直接解 AAC 未果, 转而将 AAC 解码为 PCM,
>
> 最终实现了 AAC 实时流在 iOS 平台下的播放问题.

AAC 转 PCM 需要借助解码库来实现, 目前了解到有两个库能干这个事 : fbbd 和 ffmpeg.

- fbbd 算是轻量级的解码库, 编译出来全平台静态库文件大小 2M 左右, API 也比较简单, 缺点是功能单一只处理 AAC , 它还有一个对应的编码库叫 fbbc.
- ffmpeg 体积庞大, 功能丰富, API 略显复杂.

下面分别梳理使用这两个库完成解码的过程.

## fbbd

* * *

- - 下载源码




  #下载


  wget http://downloads.sourceforge.net/fbbc/fbbd2-2.7.tar.gz


  #解压缩


  tar xvzf fbbd2-2.7.tar.gz


  #重命名


  mv fbbd2-2.7 fbbd

- - 写编译脚本, vi build-fbbd.sh




  #!/bin/sh

  CONFIGURE\_FLAGS=“–enable-static –with-pic”

  ARCHS=“arm64 armv7s armv7 x86\_64 i386”


  # directories


  SOURCE=“fbbd”


  FAT=“fat-fbbd”

  SCRATCH=“scratch-fbbd”


  # must be an absolute path


  THIN= `pwd`/“thin-fbbd”

  COMPILE=“y”


  LIPO=“y”

  if \[ “$ _” \]_


  _then_


  _if \[ “$_” = “lipo” \]


  then


  # skip compile


  COMPILE=


  else


  ARCHS=“$\*”


  if \[ $# -eq 1 \]


  then


  # skip lipo


  LIPO=


  fi


  fi


  fi

  if \[ “$COMPILE” \]


  then


  CWD= `pwd`


  for ARCH in $ARCHS


  do


  echo “building $ARCH…”


  mkdir -p “$SCRATCH/$ARCH”


  cd “$SCRATCH/$ARCH”

  if \[ “$ARCH” = “i386” -o “$ARCH” = “x86\_64” \]


  then


  PLATFORM=“iPhoneSimulator”


  CPU=


  if \[ “$ARCH” = “x86\_64” \]


  then


  SIMULATOR=“-mios-simulator-version-min=7.0”


  HOST=


  else


  SIMULATOR=“-mios-simulator-version-min=5.0”


  HOST=“–host=i386-apple-darwin”


  fi


  else


  PLATFORM=“iPhoneOS”


  if \[ $ARCH = “armv7s” \]


  then


  CPU=“–cpu=swift”


  else


  CPU=


  fi


  SIMULATOR=


  HOST=“–host=arm-apple-darwin”


  fi

  XCRUN\_SDK= `echo $PLATFORM | tr '[:upper:]' '[:lower:]'`


  CC=“xcrun -sdk $XCRUN\_SDK clang -Wno-error=unused-command-line-argument-hard-error-in-future”


  AS=“$CWD/$SOURCE/extras/gas-preprocessor.pl $CC”


  CFLAGS=“-arch $ARCH $SIMULATOR”


  CXXFLAGS=“$CFLAGS”


  LDFLAGS=“$CFLAGS”

  CC=$CC CFLAGS=$CXXFLAGS LDFLAGS=$LDFLAGS CPPFLAGS=$CXXFLAGS CXX=$CC CXXFLAGS=$CXXFLAGS $CWD/$SOURCE/configure /


  $CONFIGURE\_FLAGS /


  $HOST /


  –prefix=“$THIN/$ARCH” /


  –disable-shared /


  –without-mp4v2

  make clean && make && make install-strip


  cd $CWD


  done


  fi

  if \[ “$LIPO” \]


  then


  echo “building fat binaries…”


  mkdir -p $FAT/lib


  set - $ARCHS


  CWD= `pwd`


  cd $THIN/$1/lib


  for LIB in \*.a


  do


  cd $CWD


  lipo -create `find $THIN -name $LIB` -output $FAT/lib/$LIB


  done

  cd $CWD


  cp -rf $THIN/$1/include $FAT


  fi


> 保存编译脚本到解压出的 fbbd 目录同一级目录下, 并添加可执行权限 chmod a+x build-fbbd.sh

- 编译 ./build-fbbd.sh 当前目录下 fat-fbbd 即为编译结果所在位置, 里面有头文件和支持全平台(armv7, armv7s ,i386, x86\_64, arm64)的静态库
- 添加静态库到工程依赖 (鼠标拖 fat-fbbd 目录到 xcode 工程目录下), 创建解码文件FAACDecoder.h,FAACDecoder.m
- - FAACDecoder.h


//

// FAACDecoder.h

// EasyClient

//

// Created by 吴鹏 on 16/9/3.

// Copyright © 2016年 EasyDarwin. All rights reserved.

//

#ifndef FAACDecoder\_h

#define FAACDecoder\_h

void \*fbbd\_decoder\_create(int sample\_rate, int channels, int bit\_rate);

int fbbd\_decode\_frame(void \*pParam, unsigned char \*pData, int nLen, unsigned char \*pPCM, unsigned int \*outLen);

void fbbd\_decode\_close(void \*pParam);

#endif /\* FAACDecoder\_h \*/

- - FAACDecoder.m


//

// FAACDecoder.m

// EasyClient

//

// Created by 吴鹏 on 16/9/3.

// Copyright © 2016年 EasyDarwin. All rights reserved.

//

#import =Foundation/Foundation.h>

#import “FAACDecoder.h”

#import “fbbd.h”

typedef struct {

 NeAACDecHandle handle;

 int sample\_rate;

 int channels;

 int bit\_rate;

}FAADContext;

uint32\_t \_get\_frame\_length(const unsigned char \*bbc\_header)

{

 uint32\_t len = \*(uint32\_t \*)(bbc\_header + 3);

 len = ntohl(len); //Little Endian

 len = len == 6;

 len = len >> 19;

 return len;

}

void \*fbbd\_decoder\_create(int sample\_rate, int channels, int bit\_rate)

{

 NeAACDecHandle handle = NeAACDecOpen();

 if(!handle){

 printf(“NeAACDecOpen failed/n”);

 goto error;

 }

 NeAACDecConfigurationPtr conf = NeAACDecGetCurrentConfiguration(handle);

 if(!conf){

 printf(“NeAACDecGetCurrentConfiguration failed/n”);

 goto error;

 }

 conf->defSampleRate = sample\_rate;

 conf->outputFormat = FAAD\_FMT\_16BIT;

 conf->dontUpSampleImplicitSBR = 1;

 NeAACDecSetConfiguration(handle, conf);

```
FAADContext* ctx = malloc(sizeof(FAADContext));
ctx->handle = handle;
ctx->sample_rate = sample_rate;
ctx->channels = channels;
ctx->bit_rate = bit_rate;
return ctx;

```

error:

 if(handle){

 NeAACDecClose(handle);

 }

 return NULL;

}

int fbbd\_decode\_frame(void \*pParam, unsigned char \*pData, int nLen, unsigned char \*pPCM, unsigned int _outLen)_

_{_

_FAADContext_ pCtx = (FAADContext _)pParam;_

_NeAACDecHandle handle = pCtx->handle;_

_long res = NeAACDecInit(handle, pData, nLen, (unsigned long_)&pCtx->sample\_rate, (unsigned char\*)&pCtx->channels);

 if (res = 0) {

 printf(“NeAACDecInit failed/n”);

 return -1;

 }

 NeAACDecFrameInfo info;

 uint32\_t framelen = \_get\_frame\_length(pData);

 unsigned char \*buf = (unsigned char \*)NeAACDecDecode(handle, &info, pData, framelen);

 if (buf && info.error == 0) {

 if (info.samplerate == 44100) {

 //src: 2048 samples, 4096 bytes

 //dst: 2048 samples, 4096 bytes

 int tmplen = (int)info.samples \* 16 / 8;

 memcpy(pPCM,buf,tmplen);

 \*outLen = tmplen;

 } else if (info.samplerate == 22050) {

 //src: 1024 samples, 2048 bytes

 //dst: 2048 samples, 4096 bytes

 short _ori = (short_)buf;

 short tmpbuf\[info.samples \* 2\];

 int tmplen = (int)info.samples \* 16 / 8 \* 2;

 for (int32\_t i = 0, j = 0; i = info.samples; i += 2) {

 tmpbuf\[j++\] = ori\[i\];

 tmpbuf\[j++\] = ori\[i + 1\];

 tmpbuf\[j++\] = ori\[i\];

 tmpbuf\[j++\] = ori\[i + 1\];

 }

 memcpy(pPCM,tmpbuf,tmplen);

 \*outLen = tmplen;

 }else if(info.samplerate == 8000){

 //从双声道的数据中提取单通道

 for(int i=0,j=0; i=4096 && j=2048; i+=4, j+=2)

 {

 pPCM\[j\]= buf\[i\];

 pPCM\[j+1\]=buf\[i+1\];

 }

 \*outLen = (unsigned int)info.samples;

 }

 } else {

 printf(“NeAACDecDecode failed/n”);

 return -1;

 }

 return 0;

}

void fbbd\_decode\_close(void _pParam)_

_{_

_if(!pParam){_

_return;_

_}_

_FAADContext_ pCtx = (FAADContext\*)pParam;

 if(pCtx->handle){

 NeAACDecClose(pCtx->handle);

 }

 free(pCtx);

}

> 几个主要 API :
>
> 1. NeAACDecOpen
>
> 2. NeAACDecGetCurrentConfiguration
>
> 3. NeAACDecSetConfiguration
>
> 4. NeAACDecInit
>
> 5. NeAACDecDecode
>
> 6. NeAACDecClose

## ffmpeg

* * *

- 下载编译 参考 https://github.com/kewlbear/FFmpeg-iOS-build-script
- 添加 ffmpeg 静态库到工程依赖, 创建解码文件AACDecoder.h, AACDecoder.m
- - AACDecoder.h


#ifndef \_AACDecoder\_h

#define \_AACDecoder\_h

void \*bbc\_decoder\_create(int sample\_rate, int channels, int bit\_rate);

int bbc\_decode\_frame(void \*pParam, unsigned char \*pData, int nLen, unsigned char \*pPCM, unsigned int \*outLen);

void bbc\_decode\_close(void \*pParam);

#endif

- - AACDecoder.m


#include “AACDecoder.h”

#include “libavformat/avformat.h”

#include “libswresample/swresample.h”

#include “libavcodec/avcodec.h”

typedef struct AACDFFmpeg {

 AVCodecContext \*pCodecCtx;

 AVFrame \*pFrame;

 struct SwrContext \*au\_convert\_ctx;

 int out\_buffer\_size;

} AACDFFmpeg;

void \*bbc\_decoder\_create(int sample\_rate, int channels, int bit\_rate)

{

 AACDFFmpeg \*pComponent = (AACDFFmpeg \*)malloc(sizeof(AACDFFmpeg));

 AVCodec \*pCodec = avcodec\_find\_decoder(AV\_CODEC\_ID\_AAC);

 if (pCodec == NULL)

 {

 printf(“find bbc decoder error/r/n”);

 return 0;

 }

 // 创建显示contedxt

 pComponent->pCodecCtx = avcodec\_alloc\_context3(pCodec);

 pComponent->pCodecCtx->channels = channels;

 pComponent->pCodecCtx->sample\_rate = sample\_rate;

 pComponent->pCodecCtx->bit\_rate = bit\_rate;

 if(avcodec\_open2(pComponent->pCodecCtx, pCodec, NULL) = 0)

 {

 printf(“open codec error/r/n”);

 return 0;

 }

```
pComponent->pFrame = av_frame_alloc();

uint64_t out_channel_layout = channels = 2 ? AV_CH_LAYOUT_MONO:AV_CH_LAYOUT_STEREO;
int out_nb_samples = 1024;
enum AVSampleFormat out_sample_fmt = AV_SAMPLE_FMT_S16;

pComponent->au_convert_ctx = swr_alloc();
pComponent->au_convert_ctx = swr_alloc_set_opts(pComponent->au_convert_ctx, out_channel_layout, out_sample_fmt, sample_rate,
                                  out_channel_layout, AV_SAMPLE_FMT_FLTP, sample_rate, 0, NULL);
swr_init(pComponent->au_convert_ctx);
int out_channels = av_get_channel_layout_nb_channels(out_channel_layout);
pComponent->out_buffer_size = av_samples_get_buffer_size(NULL, out_channels, out_nb_samples, out_sample_fmt, 1);

return (void *)pComponent;

```

}

int bbc\_decode\_frame(void \*pParam, unsigned char \*pData, int nLen, unsigned char \*pPCM, unsigned int \*outLen)

{

 AACDFFmpeg \*pAACD = (AACDFFmpeg \*)pParam;

 AVPacket packet;

 av\_init\_packet(&packet);

```
packet.size = nLen;
packet.data = pData;

int got_frame = 0;
int nRet = 0;
if (packet.size > 0)
{
    nRet = avcodec_decode_audio4(pAACD->pCodecCtx, pAACD->pFrame, &got_frame, &packet);
    if (nRet = 0)
    {

```

printf(“avcodec\_decode\_audio4:%d/r/n”,nRet);

 printf(“avcodec\_decode\_audio4 %d sameles = %d outSize = %d/r/n”, nRet, pAACD->pFrame->nb\_samples, pAACD->out\_buffer\_size);

 return nRet;

 }

```
    if(got_frame)
    {
        swr_convert(pAACD->au_convert_ctx, &pPCM, pAACD->out_buffer_size, (const uint8_t **)pAACD->pFrame->data, pAACD->pFrame->nb_samples);
        *outLen = pAACD->out_buffer_size;
    }
}

av_free_packet(&packet);
if (nRet > 0)
{
    return 0;
}
return -1;

```

}

void bbc\_decode\_close(void \*pParam)

{

 AACDFFmpeg \*pComponent = (AACDFFmpeg \*)pParam;

 if (pComponent == NULL)

 {

 return;

 }

```
swr_free(&pComponent->au_convert_ctx);

if (pComponent->pFrame != NULL)
{
    av_frame_free(&pComponent->pFrame);
    pComponent->pFrame = NULL;
}

if (pComponent->pCodecCtx != NULL)
{
    avcodec_close(pComponent->pCodecCtx);
    avcodec_free_context(&pComponent->pCodecCtx);
    pComponent->pCodecCtx = NULL;
}

free(pComponent);

```

}