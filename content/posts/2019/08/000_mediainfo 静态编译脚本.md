---
url: /blog/linux/roH7hpe6L
title: "mediainfo 静态编译脚本"
date: 2019-08-13T01:38:19+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 因为需要mediainfo支持http协议，在老的版本中是不支持的，所以只能自己动手编译了。

## 说明

系统：ubuntu 14.04 (其他版本可能会有少许改动)

mediainfo版本：0.7.71

编译环境：c/c++

## 脚本

```bash
#!/bin/bash

cd ~/
apt-get install git automake autoconf libtool pkg-config make g++ zlib1g-dev libcurl4-gnutls-dev
git clone https://github.com/MediaArea/ZenLib.git
cd ZenLib
make clean
git checkout v0.4.37
cd Project/GNU/Library
./autogen.sh
./configure --enable-static
make -j2

cd ~/
git clone https://github.com/openssl/openssl.git
cd openssl
make clean
git checkout OpenSSL_1_0_2i
./Configure linux-generic64
make -j2

curl_vserion=7.50.0
cd ~/
wget --no-check-certificate https://curl.haxx.se/download/curl-$curl_vserion.tar.gz
tar -zxvf curl-$curl_vserion.tar.gz
cd curl-$curl_vserion/
make clean
./configure --enable-static --disable-share --disable-ldap --disable-ldaps  --without-librtmp --without-libidn
make -j2

cd ~/
git clone https://github.com/MediaArea/MediaInfoLib.git
cd MediaInfoLib
git checkout v0.7.71
cd Project/GNU/Library/
make clean
./autogen
## --with-libcurl 开启支持http和ftp
./configure --enable-static --with-libcurl=../../../../curl-$curl_vserion/
make -j2

cd ~/
git clone https://github.com/MediaArea/MediaInfo.git
cd MediaInfo
git checkout v0.7.71
cd Project/GNU/CLI
make clean
./autogen
./configure --enable-staticlibs
make -j2
# make install
g++ -static -O2 -DUNICODE -DUNICODE -DSIZE_T_IS_LONG -o mediainfo CLI_Main.o CommandLine_Parser.o Help.o Core.o  ../../../../MediaInfoLib/Project/GNU/Library/.libs/libmediainfo.a -lz  ../../../../ZenLib/Project/GNU/Library/.libs/libzen.a ../../../../curl-$curl_vserion/lib/.libs/libcurl.a ../../../../openssl/libssl.a ../../../../openssl/libcrypto.a -lpthread -lstdc++ -pthread -Wl,-rpath -Wl,../../../../ZenLib/Project/GNU/Library/.libs -Wl,-rpath -Wl,../../../../curl-$curl_vserion/lib/.libs -Wl,-rpath -Wl,../../../../openssl -ldl

```

