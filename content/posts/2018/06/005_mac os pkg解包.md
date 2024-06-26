---
url: /blog/macos/BkHOYBUgX
title: "mac os pkg解包"
date: 2018-06-07T06:06:25+08:00
description:
categories:
  - MacOS
tags:
  - MacOS
menu: main
---

> jdk1.8.pkg解包

每次安装Java的时候，都是一个pkg安装包，没有像linux下直接一个tar包那样绿色和方便。于是google搜索一下，终于找到解决的方法了。

```
xar -xf JDK\ 8\ Update\ 171.pkg
cat jdk180171.pkg/Payload | cpio -i

```

是不是很简单，然后将”Contents/Home” 拷贝出来并重命名为jdk1.8，剩下的就和linux下配置java环境一样的了。