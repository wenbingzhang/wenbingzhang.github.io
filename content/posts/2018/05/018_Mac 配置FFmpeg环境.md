---
url: /blog/macos/B1umUU49L0f
title: "Mac 配置FFmpeg环境"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - MacOS
tags:
  - MacOS
menu: main
---

> 假如你的mac
>
> 电脑想要看更多格式的视频内容，需要转换视频格式，又不想下载新的App什么的，那么今天我们就来点高大上的手段，根据FFmpeg实现环境的配置来更改…

假如你的mac

电脑想要看更多格式的视频内容，需要转换视频格式，又不想下载新的App什么的，那么今天我们就来点高大上的手段，根据FFmpeg实现环境的配置来更改视频的格式。例如：将flv格式转换成mp4格式，将mp4转换成mp3等等。

FFmpeg官网：(ps：虽然都是英文吧，但是我看不太懂)http://ffmpeg.org/

> 需要工具： 1.homebrew 2.终端

## 一、安装homebrew

homebrew是什么？

```
"homebrew"是Mac平台的一个包管理工具，提供了许多Mac下没有的Linux工具等，而且安装过程很简单。

```

了解更多的homebrew的信息：https://github.com/Homebrew/homebrew-

core/blob/master/Formula/ffmpeg.rb

#### 安装过程

1.打开终端输入以下命令行：

```
brew

```

2.若不是上面的结果需要安装homebrew，需要终端输入命令：

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

```

3.卸载homebrew：

```
brew cleanup

```

## 二、安装FFmpeg

1）利用上面的homebrew安装FFmpeg：

```
brew install ffmpeg

```

2）当命令结束之后，输入以下命令(查看你的安装ffmpeg的信息)：

```
brew info ffmpeg

```

安装ffmpeg信息

图片中有好多库，例如ffac，fontconfig，freetype等等，有红叉的代表是没有这个库，有绿色的对勾的表示此库已经安装上了。想要知道怎么安装其他的依赖库吗？就看下面命令行。

#### 更新ffmpeg，输入以下命令行：

```
brew update

```

或者：

```
brew upgrade ffmpeg

```

#### 安装某一个特定的库如下格式：

```
brew install [FORMULA...]

```

例如:安装openssl 库输入以下命令：

```
brew install openssl

```

#### 卸载某个特定的库如下格式：

```
brew uninstall [FORMULA...]

```

例如:卸载openssl库输入以下命令：

```
brew uninstall openssl

```

## 三、视频转换

下载一个.flv格式的视频，并将这个视频转换成mp4格式，并将码率设置成640kbps。 1）打开终端，输入以下命令行：(前提是找到这个视频文件，格式如下)

```
ffmpeg -i 脱口秀.flv  -b:v  640k  脱口秀.mp4

```

由于我把视频文件直接放到了桌面上，因此命令行如下：

```
$ ffmpeg -i /Users/lixiangyang/Desktop/脱口秀.flv -b:v 640k 脱口秀.mp4

```

#### 关于更多ffmpeg的终端命令,详见官网：

http://ffmpeg.org/ffmpeg.html

#### 参考资源：

1.http://www.jianshu.com/p/12941473a61d2.官网：http://ffmpeg.org/