---
slug: e4C2nyBNgzu5edDbnmdJgQ
title: Mamba替代Conda
description:
categories:
  - Linux
  - MacOS
tags:
  - Linux
  - MacOS
  - Python
date: 2024-03-27 13:07:03+08:00
menu: main
---

mamba是一个conda的替代品，可以加速conda的包管理，提升包管理的效率。

## 安装
```bash
# macos
brew install micromamba
# macos or linux
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
```

## 配置
```bash
# 根据命令提示，修改~/.zshrc文件
micromamba shell init -s zsh -p ~/.micromamba
# 添加配置文件
$ cat ~/.mambarc
channels:
  - conda-forge
always_yes: false
```

## 使用
```bash
micromamba create -n python310 python=3.10
# 激活环境
micromamba activate python310
# 然后可以用 micromamba 或者 pip 装东西
micromamba install package_1 package_2=version
## 具体请参考 https://mamba.readthedocs.io/en/latest/
micromamba --help
```
