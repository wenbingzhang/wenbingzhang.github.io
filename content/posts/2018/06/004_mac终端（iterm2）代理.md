---
url: /blog/macos/SkOqdFUxX
title: "mac终端（iterm2）代理"
date: 2018-06-07T10:39:20+08:00
description:
categories:
  - MacOS
tags:
  - MacOS
menu: main
---

> 一个简单的脚本，实现终端socks5代理。

```
开始是打算使用“proxychains4”的，但是需要关闭SIP功能(System Integrity Protection)，作为一个注重系统安全的用户，怎么能关闭这个SIP呢，于是只能另辟蹊径了。最后找到使用shell 的代理环境变量来解决这个问题。

$ cat /usr/local/bin/pc
#!/bin/bash
export http_proxy=socks5://127.0.0.1:1086
export https_proxy=$http_proxy
$@

$ chmod +x /usr/local/bin/pc

$ #需要使用代理的时候
$ pc curl www.google.com

是不是很简单，感觉比“proxychains4”简单方便多了，而且还不要关闭SIP。理论上Linux下也是可行的，但是没有测试。

```