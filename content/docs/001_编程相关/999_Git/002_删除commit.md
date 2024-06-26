---
slug: 5kQLZqjQawbXf2t6VUSxar
title: 📝 删除Commit
date: 2024-03-14 16:10:13+08:00
bookComments: false
bookHidden: false
bookCollapseSection: false
weight: 2
---

```bash
# 获取commit信息
git log
# commit-id 要删除commit的下一个commit-id
git rebase -i (commit-id) 
# 编辑文件，将要删除的commit之前的pick改为drop
# 保存文件退出
# 再次查看commit信息，确认删除成功
git log
```