---
url: /blog/macos/HkGt88E9U0f
title: "Mac terminal清除历史命令纪录"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - MacOS
tags:
  - MacOS
menu: main
---

> Linux传统清除方式并没能解决

history -c

我用的iterm2 + zsh

常用history命令：

查看历史命令纪录:

history…

Linux传统清除方式并没能解决

```
history -c

```

我用的iterm2 + zsh

### 常用history命令：

查看历史命令纪录:

history

history | less 使用 !! 执行上一条命令

!! 使用 !foo 执行以 foo 开头的命令

!foo 使用 !n 执行第 n 个命令

!100

可以尝试下这样来解决：

在terminal中输入hist，然后tab键，出来以下这些

HISTCHARS HISTFILE HISTSIZE

了解历史记录的大小:

```
echo $HISTSIZE

```

历史记录的保存位置:

```
echo $HISTFILE # 查看history文件存放地址
echo > ~/.zsh_history # 清空 好了，退出terminal，重新登录检查一下即可

```

退出后，再history检查一下