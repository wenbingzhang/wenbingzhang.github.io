---
slug: "aaELFz1Mg"
title: "📝 MacOS Lauchpad(启动台) 重置"
date: 2020-12-07T20:39:24+08:00
bookComments: false
bookHidden: false
weight: 2
---


> 重置macos的Lauchpad(启动台)，及设置Lauchpad(启动台)的行数和列数。

打开终端程序，按需求执行以下命令即可。

## 重置 Lauchpad

```bash
defaults write com.apple.dock ResetLaunchPad -bool TRUE;
```

## 重启 Dock

```bash
killall Dock
```

## 设置 Lauchpad 图标的列数

```bash
defaults write com.apple.dock springboard-columns -int 7
```

## 设置 Lauchpad 图标的行数

```bash
defaults write com.apple.dock springboard-rows -int 7
```