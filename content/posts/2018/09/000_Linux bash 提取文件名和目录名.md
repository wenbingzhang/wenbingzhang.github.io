---
url: /blog/linux/SJyvgQAOm
title: "Linux bash 提取文件名和目录名"
date: 2018-09-18T07:01:06+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 在Linux Bash中分别使用basename、dirname、${}，提取文件名和目录名。

## 通过变量方式

${}用于字符串的读取，提取和替换功能，可以使用${} 提取字符串

### 1、提取文件名

```bash
# file1=/dir1/dir2/file.txt
# echo ${file1##*/}
file.txt

```

### 2、提取后缀

```bash
# echo ${file1##*.}
txt

```

### 3、提取不带后缀的文件名

```bash
# tmp=${file1##*/}
# echo $tmp
file.txt
# echo ${tmp%.*}
file

```

### 4、提取目录

```bash
# echo ${var%/*}
/dir1/dir2

```

## 通过命令

使用文件目录的专有命令basename和dirname

### 1、提取文件名

```bash
# file2=/dir1/dir2/file2.txt
# echo $(basename $file2)
file2.txt

```

### 2、提取不带后缀的文件名

```bash
# echo $(basename $file2 .txt)
file2

```

### 3、提取目录

```bash
# dirname $file2
/dir1/dir2
# echo $(dirname $file2)
/dir1/dir2

```