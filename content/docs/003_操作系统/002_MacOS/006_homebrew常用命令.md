---
slug: "BkWmi6d-7"
title: "📝 homebrew常用命令"
date: 2018-06-21T06:58:24+08:00
bookComments: false
bookHidden: false
weight: 6
---


> brew常用的一些命令

1. 安装：ruby -e “$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)”

2. 搜索：brew search XXX 在安装之前可以先查询一下，是否有这个软件

3. 查询：brew info XXX 主要看具体的信息，比如目前的版本，依赖，安装后注意事项等

4. 查看依赖： brew deps 查看包的依赖

5. 安装：brew install xxx 用于安装软件

6. 更新：brew update 这会更新 Homebrew 自己，并且使得接下来的两个操作有意义——

7. 检查过时（是否有新版本）：brew outdated 这回列出所有安装的软件里可以升级的那些

8. 升级：brew upgrade 升级所有可以升级的软件们

9. 清理：brew cleanup 清理不需要的版本极其安装包缓存