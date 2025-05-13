---
slug: gfEGaTfpUstUECdeAiFdS7
title: 📝 defer实现
date: 2025-05-13 20:15:03+08:00
bookComments: false
bookHidden: false
bookCollapseSection: false
weight: 1
---

## 实现类似Golang的defer的方式
```c++
//
// Created by 张文兵 on 2025/5/13.
//

#ifndef DEFER_H
#define DEFER_H
#include <functional>

class Defer {
public:
    explicit Defer(const std::function<void()> &func) : m_func(func) {
    }

    ~Defer() { m_func(); } // 离开作用域时自动调用
private:
    std::function<void()> m_func;
};
#endif //DEFER_H

```

## 使用方式
```c++
m_mutex.lock();
Defer defer([=]() {
    m_mutex.unlock();
});
```