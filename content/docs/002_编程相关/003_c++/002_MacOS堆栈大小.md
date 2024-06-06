---
slug: 3tXBbb7irUppjSg4P7RwNB
title: 📝 MacOS堆栈大小
date: 2024-05-28 15:21:31+08:00
bookComments: false
bookHidden: false
bookCollapseSection: false
weight: 2
---

## 问题代码
```c++
char buffer[8*1024*1024];
```

## 问题分析
 * macos系统默认的堆栈大小为8MB，可以通过ulimit命令查看和修改。
 * 但是，如果代码中使用了大量的堆栈变量，可能会导致栈溢出，导致程序崩溃。
```bash
# 查看系统默认的堆栈大小
ulimit -a
# 或者
ulimit -s
```

## 解决方案
```c++
char *buffer = new char[8*1024*1024];

// 记得释放
delete[] buffer;
```