---
slug: "MiSev5_HW"
title: "📝 upx for macos 之源码编译"
date: 2020-04-01T09:53:30+08:00
bookComments: false
bookHidden: false
weight: 3
---


> UPX (the Ultimate Packer for eXecutables)是一款先进的可执行程序文件压缩器，压缩过的可执行文件体积缩小50%-70% ，这样减少了磁盘占用空间、网络上传下载的时间和其它分布以及存储费用。

## 准备源码

```bash
git clone https://github.com/upx/upx.git
git clone https://github.com/upx/upx-lzma-sdk.git lzma-sdk
wget http://www.oberhumer.com/opensource/ucl/download/ucl-1.03.tar.gz

```

## 编译源码

```bash
tar -xzvf ucl-1.03.tar.gz
cd ucl-1.03
./configure --prefix=/home/o/ucl CC=clang
make

cd ../upx
make all UPX_UCLDIR=../ucl-1.03 UPX_LZMADIR=../lzma-sdk
```

编译完成之后再src目录下能找到upx.out文件就成功了