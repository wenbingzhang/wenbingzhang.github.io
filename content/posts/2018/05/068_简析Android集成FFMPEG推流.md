---
url: /blog/ffmpeg/SyD7UIEcUAM
title: "简析Android集成FFMPEG推流"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
menu: main
---

> 如今，视频直播行业在中国算是比较热门。在刚刚过去的2015年，视频直播成为互联网行业最抢眼的领域之一。从游戏到秀场，从传统的网页端到移动互联网，各大直播平台包括…

如今，视频直播行业在中国算是比较热门。在刚刚过去的2015年，视频直播成为互联网行业最抢眼的领域之一。从游戏到秀场，从传统的网页端到移动互联网，各大直播平台包括斗鱼、熊猫tv、虎牙战旗还有纯移动端的映客、易直播等，群雄割据。言归正转，今天我们讲解的是Android

端简要集成FFMPEG进行推流。

## 推流基本流程

一般情况下推流的基本流程如上。

## FFmpeg

说到推流就不得不提大名鼎鼎的FFMPEG了，FFmpeg是一个开源免费跨平台的视频和音频流方案，属于自由软件，采用LGPL或GPL许可证（依据你选择的组件）。它提供了录制、转换以及流化音视频的完整解决方案。它包含了非常先进的音频/视频编解码库libavcodec，为了保证高可移植性和编解码质量，libavcodec里很多codec都是从头开发的。诸如微信的小视频，映客、斗鱼等均是在FFmpeg基础上开发而来，可见FFmpeg之强大。一下是解压微信的apk的截图。

## FFmpeg 在Android中的使用

FFmpeg要想在Android就必须要编译成Android上能使用so动态链接库（下称so库）。具体编译方法可以参考github官方提供源码。编译过程大约在30分钟左右。以下是笔者编译好的so库。

### FFmpeg主要分为8大模块：

- libavcodec：用于各种类型声音/图像编解码；
- libavdevice：用于视频采集访问摄像头等
- libavfilter：用做滤镜处理
- libavformat：用于各种音视频封装格式的生成和解析，包括获取解码所需信息以生成解码上下文结构和读取音视频帧等功能；
- libswresample：用于重采样；
- libavutil：包含一些公共的工具函数；
- libswscale：用于视频场景比例缩放、色彩映射转换；
- libpostproc：用于后期效果处理；

#### JNI开发调用FFmpeg

我们先看看我们使用到的FFmpegUtils工具类，主要用于加载native方法：

```
public class FFmpegUtils {

//加载so库
static{
      System.loadLibrary("avutil-54");
      System.loadLibrary("swresample-1");
      System.loadLibrary("avcodec-56");
      System.loadLibrary("avformat-56");
      System.loadLibrary("swscale-3");
      System.loadLibrary("postproc-53");
      System.loadLibrary("avfilter-5");
      System.loadLibrary("avdevice-56");
      System.loadLibrary("sffstreamer");
}
     /*
      * 把本地的音视频数据通过rtmp协议发送到流媒体服务器上
      *@param input
      *@param output
      */
     public native int stream(String input, String output);

}

```

接下来我们就是我们的重头戏JNI调用FFmpeg

```
#include "libavcodec/avcodec.h"
#include "libavformat/avformat.h"
#include "libavutil/log.h"

#define LOGE(format, ...) __android_log_print(ANDROID_LOG_ERROR, "(>_<)", format, ##__VA_ARGS__)
#define LOGI(format, ...) __android_log_print(ANDROID_LOG_INFO, "(^_^)", format, ##__VA_ARGS__)
JNIEXPORT jint JNICALL Java_org_loofer_ffmpegstreamer_MainActivity_stream  (JNIEnv *env, jobject obj, jstring input_jstr, jstring output_jstr)
{

    //java string -> c char*
    //视频文件所在路径
    const char* input_cstr = (*env)->GetStringUTFChars(env,input_jstr, NULL));
    //推送的流媒体地址
    const char* output_cstr = (*env)->GetStringUTFChars(env,output_jstr, NULL));
    //封装格式(读入，写出)（解封装，得到frame）
    AVFormatContext *inFmtCtx = NULL, *outFmtCtx = NULL;
    AVOutputFormat *ofmt = NULL;

    AVPacket pkt;

    //注册组件
    av_register_all();
    //初始化网络
    avformat_network_init();

    //Input
    if ((ret = avformat_open_input(&inFmtCtx, input_str, 0, 0)) < 0) {
        LOGE( "Could not open input file.");
        goto end;
    }
    //获取文件信息
    if ((ret = avformat_find_stream_info(inFmtCtx, 0)) < 0) {
        LOGE( "Failed to retrieve input stream information");
        goto end;
    }
    //获取视频的索引位置
    int videoindex=-1;
    for(i=0; i<inFmtCtx->nb_streams; i++)
        if(inFmtCtx->streams[i]->codec->codec_type==AVMEDIA_TYPE_VIDEO){
            videoindex=i;
            break;
        }
    //输出封装格式，推送flv封装格式的视频流
    avformat_alloc_output_context2(&outFmtCtx, NULL, "flv",output_cstr); //RTMP
    //avformat_alloc_output_context2(&outFmtCtx, NULL, "mpegts", output_cstr);//UDP

    if (!outFmtCtx) {
        LOGE( "Could not create output context/n");
        ret = AVERROR_UNKNOWN;
        goto end;
    }

    for (i = 0; i < inFmtCtx->nb_streams; i++) {
        //解码器，解码上下文保持一致
        AVStream *in_stream = inFmtCtx->streams[i];
        AVStream *out_stream = avformat_new_stream(outFmtCtx, in_stream->codec->codec);
        if (!out_stream) {
            LOGE( "Failed allocating output stream/n");
            ret = AVERROR_UNKNOWN;
            goto end;
        }
        //复制解码器上下文的 设置
        ret = avcodec_copy_context(out_stream->codec, in_stream->codec);
        if (ret < 0) {
            LOGE( "Failed to copy context from input to output stream codec context/n");
            goto end;
        }
        //全局的header
        out_stream->codec->codec_tag = 0;
        if (outFmtCtx->oformat->flags & AVFMT_GLOBALHEADER)
            out_stream->codec->flags |= CODEC_FLAG_GLOBAL_HEADER;
    }
    //打开输出的AVIOContext IO流上下文
    ofmt = outFmtCtx->oformat;
    //Open output URL
    if (!(ofmt->flags & AVFMT_NOFILE)) {
        ret = avio_open(&outFmtCtx->pb, output_cstr, AVIO_FLAG_WRITE);
        if (ret < 0) {
            LOGE( "Could not open output URL '%s'", output_cstr);
            goto end;
        }
    }
    //先写一个头
    ret = avformat_write_header(outFmtCtx, NULL);
    if (ret < 0) {
        LOGE( "Error occurred when opening output URL/n");
        goto end;
    }

    int frame_index=0;
    int64_t start_time=av_gettime();
    while (1) {
        AVStream *in_stream, *out_stream;
        //Get an AVPacket
        ret = av_read_frame(inFmtCtx, &pkt);
        if (ret < 0)
            break;
        //FIX：No PTS (Example: Raw H.264)
        //raw stream 裸流
        //PTS:Presentation Time Stamp 解码后视频帧要在什么时候取出来
        //DTS:送入解码器后什么时候标识进行解码
        if(pkt.pts==AV_NOPTS_VALUE){
            //Write PTS
            AVRational time_base1=inFmtCtx->streams[videoindex]->time_base;
            //Duration between 2 frames (us)
            int64_t calc_duration=(double)AV_TIME_BASE/av_q2d(inFmtCtx->streams[videoindex]->r_frame_rate);
            //Parameters
            pkt.pts=(double)(frame_index*calc_duration)/(double)(av_q2d(time_base1)*AV_TIME_BASE);
            pkt.dts=pkt.pts;
            pkt.duration=(double)calc_duration/(double)(av_q2d(time_base1)*AV_TIME_BASE);
        }
        //读入速度比较快，可以在这里调整读取速度减轻服务器压力
        if(pkt.stream_index==videoindex){
            AVRational time_base=inFmtCtx->streams[videoindex]->time_base;
            AVRational time_base_q={1,AV_TIME_BASE};
            int64_t pts_time = av_rescale_q(pkt.dts, time_base, time_base_q);
            int64_t now_time = av_gettime() - start_time;
            if (pts_time > now_time)
                av_usleep(pts_time - now_time);

        }

        in_stream  = inFmtCtx->streams[pkt.stream_index];
        out_stream = outFmtCtx->streams[pkt.stream_index];
        /* copy packet */
        //Convert PTS/DTS
        pkt.pts = av_rescale_q_rnd(pkt.pts, in_stream->time_base, out_stream->time_base, AV_ROUND_NEAR_INF|AV_ROUND_PASS_MINMAX);
        pkt.dts = av_rescale_q_rnd(pkt.dts, in_stream->time_base, out_stream->time_base, AV_ROUND_NEAR_INF|AV_ROUND_PASS_MINMAX);
        pkt.duration = av_rescale_q(pkt.duration, in_stream->time_base, out_stream->time_base);
        pkt.pos = -1;
        //Print to Screen
        if(pkt.stream_index==videoindex){
            LOGE("Send %8d video frames to output URL/n",frame_index);
            frame_index++;
        }
        //写数据
        //ret = av_write_frame(outFmtCtx, &pkt);
        ret = av_interleaved_write_frame(outFmtCtx, &pkt);

        if (ret < 0) {
            LOGE( "Error muxing packet/n");
            break;
        }
        av_free_packet(&pkt);

    }
    //写结尾
    av_write_trailer(outFmtCtx);
end:
    //释放自愿
    avformat_close_input(&inFmtCtx);
    /* 关闭输出流 */
    if (outFmtCtx && !(ofmt->flags & AVFMT_NOFILE))
        avio_close(outFmtCtx->pb);
    avformat_free_context(outFmtCtx);
    if (ret < 0 && ret != AVERROR_EOF) {
        LOGE( "Error occurred./n");
        return -1;
    }
    return 0;
}

```

* * *

#### 函数简单介绍

- av_register_all():注册所有组件。
- avformat_open_input():打开输入视频文件。
- avformat_find_stream_info():获取视频文件信息。
- avcodec_find_decoder():查找解码器。
- avcodec_open2():打开解码器。
- av_read_frame():从输入文件读取一帧压缩数据。
- avcodec_decode_video2():解码一帧压缩数据。
- avcodec_close():关闭解码器。
- avformat_close_input():关闭输入视频文件