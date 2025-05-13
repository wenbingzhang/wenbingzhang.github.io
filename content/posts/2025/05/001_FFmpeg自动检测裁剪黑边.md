---
slug: ZJRbjxuZWZTru8UTgSMvbf
title: FFmpeg自动检测裁剪黑边
description:
categories:
  - FFmpeg
tags:
  - FFmpeg
date: 2025-05-13 20:26:12+08:00
menu: main
---


```bash
#!/bin/bash

# 用法提示
if [ "$#" -ne 1 ]; then
  echo "用法: $0 <输入文件路径>"
  exit 1
fi

INPUT="$1"
OUTPUT="${1%.*}"
OUTPUT_EXT="${1##*.}"

# 自动检测 crop 参数
CROP=$(ffmpeg -i "$INPUT" -vf cropdetect=24:16:0 -t 30 -f null - 2>&1 |
  grep -o 'crop=[^ ]*' | sort | uniq -c | sort -nr | head -n1 | awk '{print $2}')

if [ -z "$CROP" ]; then
  echo "未能检测到有效的 crop 参数"
  exit 1
fi

echo "检测到裁剪参数: $CROP"

# 执行裁剪
ffmpeg -i "$INPUT" -vf "$CROP" -c:v libx264 -crf 10 -c:a copy "${OUTPUT}_crop.${OUTPUT_EXT}"
```