---
url: /blog/git/Hk6GGp6cQ
title: "📝 Git回滚到某个commit"
date: 2018-10-12T06:49:25+08:00
bookComments: false
bookHidden: false
bookCollapseSection: false
weight: 7
---

> git是一个开源的分布式版本控制系统，可以有效、高速的处理从很小到非常大的项目版本管理。

## 回滚命令

```
git reset --hard HEAD^  #回滚到上个版本
git reset --hard HEAD~3 #回滚到前3次提交之前，以此类推，回退到n次提交之前
git reset --hard commit_id #回滚到指定commit的sha版本

```

## 推送命令

```
git push origin HEAD --force #强制推送到远程

```

## 温馨提示

回滚有风险，请提前做好备份。