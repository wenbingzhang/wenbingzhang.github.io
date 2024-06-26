---
url: /blog/git/H1Krv6b-4
title: "📝 git修改历史cimmit信息"
date: 2018-12-28T10:17:25+08:00
bookComments: false
bookHidden: false
bookCollapseSection: false
weight: 5
---

> git 使用rebase修改历史提交的cimmit信息

![git.jpg](/static/uploads/H1Krv6b-4/img/git_Bk_FuTW-V.jpg)

## 1、修改指定commit

```
git rebase -i 36224db

```

或:

```
git rebase -i HEAD~3

```

## 2、把pick改为edit

- pick：保留该commit（缩写:p）

- reword：保留该commit，但我需要修改该commit的注释（缩写:r）

- edit：保留该commit, 但我要停下来修改该提交(不仅仅修改注释)（缩写:e）

- squash：将该commit和前一个commit合并（缩写:s）

- fixup：将该commit和前一个commit合并，但我不要保留该提交的注释信息（缩写:f）

- exec：执行shell命令（缩写:x）

- drop：我要丢弃该commit（缩写:d）


## 3、修改commit信息

```
git commit --amend
git rebase --continue

```

## 4、推送到远程仓库

```
git push -f origin master

```