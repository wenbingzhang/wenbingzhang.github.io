---
slug: "rdgQnFI6j"
title: "📝 FFprobe详解"
date: 2020-05-13T09:51:05+08:00
bookComments: false
bookHidden: false
weight: 5
---


> ffprobe是ffmpeg提供的三大工具之一，用来查看音视频文件的各种信息，比如：封装格式、音频/视频流信息、数据包信息等。

ffprobe的源码是ffprobe.c，开发过程中如果想获取ffprobe查看的信息，可以通过分析源码，获得对应字段。

本文主要介绍format、stream、Packet和Frame信息，包含每个字段的说明以及对应的ffmpeg字段。

## 查看音视频文件的封装格式

```
ffprobe -show_format inputFile

```

输出信息：

```
[FORMAT]
// 文件名
filename=VID_20190811_113717.mp4
// 容器中流的个数，即AVFormatContext->nb_streams
nb_streams=2
// 即AVFormatContext->nb_programs
nb_programs=0
// 封装格式，即AVFormatContext->iformat->name
format_name=mov,mp4,m4a,3gp,3g2,mj2
// 即AVFormatContext->iformat->long_name
format_long_name=QuickTime / MOV
// 即AVFormatContext->start_time，基于AV_TIME_BASE_Q，换算为秒
start_time=0.000000
// 即AVFormatContext->duration，基于AV_TIME_BASE_Q，换算为秒
duration=10.508000
// 单位字节，即avio_size(AVFormatContext->pb)
size=27263322
// 码率，即AVFormatContext->bit_rate
bit_rate=20756240
// 即AVFormatContext->probe_score
probe_score=100
[/FORMAT]

```

## 查看音视频文件的流信息

```
ffprobe -show_streams inputFile

```

输出信息：

```
[STREAM]
// 当前流的索引信息,对应于AVStream->index
index=0
// AVCodecDescriptor * cd = avcodec_descriptor_get(AVStream->codecpar->codec_id)
// 编码名称，即cd->name
codec_name=h264
// 编码全称，即cd->long_name
codec_long_name=H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10
// 一个编码参数，可以为Baseline、Main、High等，Baseline无B帧，Main及以后可以包含B帧
// 通过avcodec_profile_name(AVStream->codecpar->codec_id, AVStream->codecpar->profile)获得
profile=High
// 流类型，即av_get_media_type_string(AVStream->codecpar->codec_type)
codec_type=video
// 即AVStream->codec->time_base
codec_time_base=14777/877500
// 通过宏av_fourcc2str(AVStream->codecpar->codec_tag)获得
codec_tag_string=avc1
// 对应AVStream->codecpar->codec_tag
codec_tag=0x31637661
// 有效区域的宽度，即AVStream->codecpar->width
width=1920
// 有效区域的高度，即AVStream->codecpar->height
height=1080
// 视频帧宽度，可能与上面的宽度不同，即AVStream->codec->coded_width，例如：当解码帧在输出前裁剪或启用低分辨率时
coded_width=1920
// 视频帧高度，可能与上面的高度不同，即AVStream->codec->coded_height，例如：当解码帧在输出前裁剪或启用低分辨率时
coded_height=1088
// 视频的延迟帧数，即AVStream->codecpar->video_delay
has_b_frames=0
// sar，图像采集时，横向采集点数与纵向采集点数的比例
// FFmpeg提供了多个sar：AVStream->sample_aspect_ratio、AVStream->codecpar->sample_aspect_ratio、AVFrame->sample_aspect_ratio
// 通过av_guess_sample_aspect_ratio获取最终的sar
sample_aspect_ratio=1:1
// dar，真正展示的图像宽高比，在渲染视频时，必须根据这个比例进行缩放
// 通过av_reduce计算得到，par * sar = dar
display_aspect_ratio=16:9
// 像素格式，即av_get_pix_fmt_name(AVStream->codecpar->format)
pix_fmt=yuvj420p
// 编码参数，即AVStream->codecpar->level
level=40
// 额外的色彩空间特征，即av_color_range_name(AVStream->codecpar->color_range)，AVCOL_RANGE_MPEG对应tv，AVCOL_RANGE_JPEG对应pc
color_range=pc
// YUV彩色空间类型，即av_color_space_name(AVStream->codecpar->color_space)
color_space=bt470bg
// 颜色传输特性，即av_color_transfer_name(AVStream->codecpar->color_trc)
color_transfer=smpte170m
// 即av_color_primaries_name(AVStream->codecpar->color_primaries)
color_primaries=bt470bg
// 色度样品的位置，即av_chroma_location_name(AVStream->codecpar->chroma_location)
chroma_location=left
// 交错视频中字段的顺序，即AVStream->codecpar->field_order
field_order=unknown
// av_timecode_make_mpeg_tc_string处理AVStream->codec->timecode_frame_start获得
timecode=N/A
// 参考帧数量，即AVStream->codec->refs
refs=1
is_avc=true
// 表示用几个字节表示NALU的长度
nal_length_size=4
id=N/A
// 当前流的基本帧率，这个值仅是一个猜测，对应于AVStream->r_frame_rate
r_frame_rate=30/1
// 平均帧率，对应于AVStream->avg_frame_rate
avg_frame_rate=438750/14777
// AVStream的时间基准，即AVStream->time_base
time_base=1/90000
// 流开始时间，基于time_base，即AVStream->start_time
start_pts=0
// 转换（start_pts * time_base）之后的开始时间，单位秒
start_time=0.000000
// 流时长，基于time_base，即AVStream->duration
duration_ts=945728
// 转换（duration_ts * time_base）之后的时长，单位秒
duration=10.508089
// 码率，即AVStream->codecpar->bit_rate
bit_rate=19983544
// 最大码率，即AVStream->codec->rc_max_rate
max_bit_rate=N/A
// Bits per sample/pixel，即AVStream->codec->bits_per_raw_sample
bits_per_raw_sample=8
// 视频流中的帧数，即AVStream->nb_frames
nb_frames=312
nb_read_frames=N/A
nb_read_packets=N/A
// 下面TAG为AVStream->metadata中的信息
// 逆时针的旋转角度（相当于正常视频的逆时针旋转角度）
TAG:rotate=90
// 创建时间
TAG:creation_time=2019-08-11T03:37:28.000000Z
// 语言
TAG:language=eng
TAG:handler_name=VideoHandle
// SIDE_DATA为AVStream->side_data数据
[SIDE_DATA]
// side_data数据类型，Display Matrix表示一个3*3的矩阵，这个矩阵需要应用到解码后的视频帧上，才能正确展示
side_data_type=Display Matrix
displaymatrix=
00000000:            0       65536           0
00000001:       -65536           0           0
00000002:            0           0  1073741824
// 顺时针旋转90度还原视频
rotation=-90
[/SIDE_DATA]
[/STREAM]
[STREAM]
// 当前流的索引信息,对应于AVStream->index
index=1
// AVCodecDescriptor * cd = avcodec_descriptor_get(AVStream->codecpar->codec_id)
// 编码名称，即cd->name
codec_name=aac
// 编码全称，即cd->long_name
codec_long_name=AAC (Advanced Audio Coding)
// 通过avcodec_profile_name(AVStream->codecpar->codec_id, AVStream->codecpar->profile)获得
profile=LC
// 流类型，即av_get_media_type_string(AVStream->codecpar->codec_type)
codec_type=audio
// 即AVStream->codec->time_base
codec_time_base=1/48000
// 通过宏av_fourcc2str(AVStream->codecpar->codec_tag)获得
codec_tag_string=mp4a
// 对应AVStream->codecpar->codec_tag
codec_tag=0x6134706d
// 采样点格式，通过av_get_sample_fmt_name(AVStream->codecpar->format)获取
sample_fmt=fltp
// 采样率，即AVStream->codecpar->sample_rate
sample_rate=48000
// 通道数，即AVStream->codecpar->channels
channels=2
// 通道布局，与channels是相对应，通过av_bprint_channel_layout获取，stereo表示立体声
channel_layout=stereo
// 每个采样点占用多少bit，即av_get_bits_per_sample(par->codec_id)
bits_per_sample=0
id=N/A
r_frame_rate=0/0
avg_frame_rate=0/0
// AVStream的时间基准，即AVStream->time_base
time_base=1/48000
// 流开始时间，基于time_base，即AVStream->start_time
start_pts=0
// 转换（start_pts * time_base）之后的开始时间，单位秒
start_time=0.000000
// 流时长，基于time_base，即AVStream->duration
duration_ts=502776
// 转换（duration_ts * time_base）之后的时长，单位秒
duration=10.474500
// 码率，即AVStream->codecpar->bit_rate
bit_rate=156002
// 最大码率，即AVStream->codec->rc_max_rate
max_bit_rate=156000
// Bits per sample/pixel，即AVStream->codec->bits_per_raw_sample
bits_per_raw_sample=N/A
// 音频流中的帧数，即AVStream->nb_frames
nb_frames=491
nb_read_frames=N/A
nb_read_packets=N/A
TAG:creation_time=2019-08-11T03:37:28.000000Z
TAG:language=eng
TAG:handler_name=SoundHandle
[/STREAM]

```

> SAR(Sample Aspect Ratio): 采样数宽高比，图像的横向采集点数与纵向采集点数的比值，即像素个数的比值。
>
> PAR(Pixel Aspect Ratio): 像素宽高比，即每个像素的宽度与高度的比值，所以可以认为像素不是正方形的。
>
> DAR(Display Aspect Ratio): 显示宽高比，图像最终展示的宽高比，播放器在渲染视频帧时，需要保持DAR的比例。
>
> 它们之间的关系：PAR \* SAR = DAR
>
> ![dar.jpg](/static/uploads/rdgQnFI6j/img/dar_5zozy2Djo.jpg)
>
> 如上图所示：每个方格代表一个像素，宽度为5像素，高度为4像素，即SAR=5 : 4
>
> 假设图像的显示宽度为160，高度为120，即DAR=4 : 3
>
> 那么可以计算出PAR = DAR / SAR = 16 : 15，表示像素方格是一个长方形。
>
> FFmpeg提供了多个SAR：
>
> AVStream->sample\_aspect\_ratio
>
> AVStream->codecpar->sample\_aspect\_ratio
>
> AVFrame->sample\_aspect\_ratio
>
> 最终的SAR是通过av\_guess\_sample\_aspect\_ratio获取的。
>
> 对于DAR，AVStream->display\_aspect\_ratio的值始终为0:0，参考ffprobe代码，可知DAR是通过av\_reduce计算得到的，如下所示：
>
> ```
> AVRational sar, dar;
>
> // par
>
> AVCodecParameters *par = AVStream->codecpar;
>
> // 计算出sar
>
> sar = av_guess_sample_aspect_ratio(AVFormatContext, AVStream, NULL);
>
> // 根据par和sar计算出dar
>
> av_reduce(&dar.num, &dar.den,
>
>             par->width * sar.num,
>
>             par->height * sar.den,
>
>             1024*1024);
>
> ```

## 查看音视频文件的数据包信息

```
// -select_streams表示选择音频或者视频
ffprobe -show_format [-select_streams audio | video] inputFile

```

首先看下视频流的第一个Packet和第二个Packet：

```
[PACKET]
//Packet类型，即av_get_media_type_string(AVStream->codecpar->codec_type)
codec_type=video
// 当前帧所属流的索引信息,对应于AVStream->index
stream_index=0
// 帧展示时间，即AVPacket->pts，基于AVStream->time_base时间基准
pts=0
// 换算为秒
pts_time=0.000000
// 帧解码时间，即AVPacket->dts，基于AVStream->time_base时间基准
dts=0
// 换算为秒
dts_time=0.000000
// 当前帧的时长，等于下一帧的pts - 当前帧pts，即AVPacket->duration，基于AVStream->time_base时间基准
duration=12972
// 换算为秒
duration_time=0.144133
// AVPacket->convergence_duration，也是基于AVStream->time_base时间基准
convergence_duration=N/A
// 换算为秒
convergence_duration_time=N/A
// 当前帧的Size，字节，即AVPacket->size
size=187872
// 当前帧地址偏移量，即AVPacket->pos
pos=830842
flags=K_
[/PACKET]
[PACKET]
codec_type=video
stream_index=0
pts=12972
// 即 12972 / 90000
pts_time=0.144133
dts=12972
dts_time=0.144133
duration=2999
duration_time=0.033322
convergence_duration=N/A
convergence_duration_time=N/A
size=31200
// 上一帧的pos + size
pos=1018714
flags=__
[/PACKET]

```

然后看下音频流的第一个Packet和第二个Packet：

```
[PACKET]
// 音频帧
codec_type=audio
// 当前帧所属流的索引信息,对应于AVStream->index
stream_index=1
// 帧展示时间，即AVPacket->pts，基于AVStream->time_base时间基准
pts=0
pts_time=0.000000
// 帧解码时间，即AVPacket->dts，基于AVStream->time_base时间基准
dts=0
dts_time=0.000000
// 当前帧的时长，等于下一帧的pts - 当前帧pts，即AVPacket->duration，基于AVStream->time_base时间基准
duration=1024
// 1024 / 48000
duration_time=0.021333
convergence_duration=N/A
convergence_duration_time=N/A
size=416
pos=810458
flags=K_
[/PACKET]
[PACKET]
// 音频帧
codec_type=audio
stream_index=1
pts=1024
// 1024 / 48000
pts_time=0.021333
dts=1024
dts_time=0.021333
duration=1024
duration_time=0.021333
convergence_duration=N/A
convergence_duration_time=N/A
size=416
// 上一帧的pos + size
pos=810874
flags=K_
[/PACKET]

```

## 查看音视频文件解码后的帧信息

```
// -select_streams表示选择音频或者视频
ffprobe -show_frames [-select_streams audio | video] inputFile

```

首先看下视频流的第一帧和第二帧：

```
[FRAME]
// 帧类型，即av_get_media_type_string(AVStream->codecpar->codec_type)
media_type=video
// 当前帧所属流的索引信息, 对应于AVStream->index
stream_index=0
// 是否关键帧，1：关键帧，0：非关键帧，即AVFrame->key_frame
key_frame=1
// 帧展示时间, 即AVFrame->pts, 基于AVStream->time_base时间基准
pkt_pts=0
// 换算为秒
pkt_pts_time=0.000000
// 帧解码时间，从对应的AVPacket copy而来，即AVFrame->pkt_dts，基于AVStream->time_base时间基准
pkt_dts=0
// 换算为秒
pkt_dts_time=0.000000
// 帧时间戳，基本与pts相同，即AVFrame->best_effort_timestamp，基于AVStream->time_base时间基准
best_effort_timestamp=0
// 换算为秒
best_effort_timestamp_time=0.000000
// 对应的AVPacket的帧时长，即AVFrame->pkt_duration，基于AVStream->time_base时间基准
pkt_duration=12972
// 换算为秒
pkt_duration_time=0.144133
// 从最后一个已输入解码器的AVPacket重新排序的pos，即AVFrame->pkt_pos
pkt_pos=830842
// 对应的AVPacket的帧size，即AVFrame->pkt_size
pkt_size=187872
// 旋转之前的帧宽度，即AVFrame->width
width=1920
// 旋转之前的帧高度，即AVFrame->height
height=1080
// 视频帧的像素格式，即av_get_pix_fmt_name(AVFrame->format)
pix_fmt=yuvj420p
// sar，图像采集时，横向采集点数与纵向采集点数的比例
// FFmpeg提供了多个sar：AVStream->sample_aspect_ratio、AVStream->codecpar->sample_aspect_ratio、AVFrame->sample_aspect_ratio
// 通过av_guess_sample_aspect_ratio获取最终的sar
sample_aspect_ratio=1:1
// 视频帧的图片类型，此处为I帧，即av_get_picture_type_char(frame->pict_type)
pict_type=I
// picture number in bitstream order, 即AVFrame->coded_picture_number
coded_picture_number=0
// picture number in display order, 即AVFrame->display_picture_number
display_picture_number=0
// 视频帧内容是否是交错的, 即AVFrame->interlaced_frame
interlaced_frame=0
// 若视频帧内容是交错的，表示首先展示的顶部字段，即AVFrame->top_field_first
top_field_first=0
// 当解码时，这个信号表明视频帧必须延迟多少。extra_delay = repeat_pict / (2*fps), 即AVFrame->repeat_pict
repeat_pict=0
// 额外的色彩空间特征，即av_color_range_name(AVFrame->color_range)，AVCOL_RANGE_MPEG对应tv，AVCOL_RANGE_JPEG对应pc
color_range=pc
// YUV彩色空间类型，即av_color_space_name(AVFrame->colorspace)
color_space=bt470bg
// 即av_color_primaries_name(AVFrame->color_primaries)
color_primaries=bt470bg
// 颜色传输特性，即av_color_transfer_name(AVFrame->color_trc)
color_transfer=smpte170m
// 色度样品的位置，即av_chroma_location_name(AVFrame->chroma_location)
chroma_location=left
[/FRAME]
[FRAME]
media_type=video
stream_index=0
// 非关键帧
key_frame=0
pkt_pts=12972
// 12972 / 90000
pkt_pts_time=0.144133
pkt_dts=12972
pkt_dts_time=0.144133
best_effort_timestamp=12972
best_effort_timestamp_time=0.144133
pkt_duration=2999
pkt_duration_time=0.033322
pkt_pos=1018714
pkt_size=31200
width=1920
height=1080
pix_fmt=yuvj420p
sample_aspect_ratio=1:1
// 视频帧的图片类型，此处为P帧，即av_get_picture_type_char(frame->pict_type)
pict_type=P
coded_picture_number=1
display_picture_number=0
interlaced_frame=0
top_field_first=0
repeat_pict=0
color_range=pc
color_space=bt470bg
color_primaries=bt470bg
color_transfer=smpte170m
chroma_location=left
[/FRAME]

```

然后看下音频流的第一帧和第二帧：

```
FRAME]
// 帧类型，即av_get_media_type_string(AVStream->codecpar->codec_type)
media_type=audio
// 当前帧所属流的索引信息, 对应于AVStream->index
stream_index=1
// 是否关键帧
key_frame=1
// 帧展示时间, 即AVFrame->pts, 基于AVStream->time_base时间基准
pkt_pts=0
// 换算为秒
pkt_pts_time=0.000000
// 帧解码时间，从对应的AVPacket copy而来，即AVFrame->pkt_dts，基于AVStream->time_base时间基准
pkt_dts=0
// 换算为秒
pkt_dts_time=0.000000
// 帧时间戳，基本与pts相同，即AVFrame->best_effort_timestamp，基于AVStream->time_base时间基准
best_effort_timestamp=0
// 换算为秒
best_effort_timestamp_time=0.000000
// 对应的AVPacket的帧时长，即AVFrame->pkt_duration，基于AVStream->time_base时间基准
pkt_duration=1024
// 换算为秒
pkt_duration_time=0.021333
// 从最后一个已输入解码器的AVPacket重新排序的pos，即AVFrame->pkt_pos
pkt_pos=810458
// 对应的AVPacket的帧size，即AVFrame->pkt_size
pkt_size=416
// 音频采样点格式，即av_get_sample_fmt_name(AVFrame->format)
sample_fmt=fltp
// 当前音频帧的采样点数，即AVFrame->nb_samples
nb_samples=1024
// 通道数，即AVFrame->channels
channels=2
// 通道布局，通过av_bprint_channel_layout得到，与channels对应
channel_layout=stereo
[/FRAME]
[FRAME]
media_type=audio
stream_index=1
key_frame=1
pkt_pts=1024
pkt_pts_time=0.021333
pkt_dts=1024
pkt_dts_time=0.021333
best_effort_timestamp=1024
best_effort_timestamp_time=0.021333
pkt_duration=1024
pkt_duration_time=0.021333
pkt_pos=810874
pkt_size=416
sample_fmt=fltp
nb_samples=1024
channels=2
channel_layout=stereo
[/FRAME]

```

## 参考文章

FFmpeg获取视频正确的宽高比

转载自->https://www.zybuluo.com/ltlovezh/note/1534824