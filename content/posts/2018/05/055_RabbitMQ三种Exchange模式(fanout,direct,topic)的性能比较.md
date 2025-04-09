---
url: /blog/linux/HybPILE5U0z
title: "RabbitMQ 三种 Exchange 模式"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---


RabbitMQ 中的 Exchange（交换机）负责接收生产者发送的消息，并根据类型将消息路由到相应的队列。常见的三种 Exchange 类型如下：

---

## 1. Direct Exchange（直连模式）

### ✅ 特点：
- 根据消息的 **routing key** 精确匹配，将消息路由到绑定了 **相同 routing key** 的队列。

### 🎯 适用场景：
- 一对一消息传递。
- 多个队列分别订阅不同的消息类型。

### 📌 示例：
绑定情况：
- Queue A 绑定 routing key：`error`
- Queue B 绑定 routing key：`info`

发送消息：
- Producer 发送消息，routing key 为 `error`

结果：
- 只有 Queue A 会接收到该消息。

---

## 2. Fanout Exchange（广播模式）

### ✅ 特点：
- **忽略 routing key**。
- 所有绑定到该 Exchange 的队列都会收到消息。

### 🎯 适用场景：
- 广播场景，例如系统通知、群发消息。

### 📌 示例：
绑定情况：
- Queue A、Queue B 都绑定到同一个 fanout Exchange

发送消息：
- Producer 发送任意消息（routing key 无效）

结果：
- Queue A 和 Queue B 都会接收到该消息。

---

## 3. Topic Exchange（主题模式）

### ✅ 特点：
- 支持 **通配符** 匹配 routing key：
  - `*`：匹配一个单词（以 `.` 分隔）
  - `#`：匹配零个或多个单词

### 🎯 适用场景：
- 灵活的订阅机制，如日志系统、新闻推送等。

### 📌 示例：
绑定情况：
- Queue A 绑定 routing key：`*.error`
- Queue B 绑定 routing key：`log.#`

发送消息：
- Producer 发送 routing key：`app.error` → Queue A 接收
- Producer 发送 routing key：`log.system.info` → Queue B 接收

---

## 🧾 模式对比表

| Exchange 类型 | Routing Key 是否参与路由 | 匹配方式           | 典型应用场景         |
|---------------|--------------------------|--------------------|----------------------|
| Direct        | ✅ 是                     | 精确匹配           | 精准路由，分类消息   |
| Fanout        | ❌ 否                     | 广播               | 系统通知，全员推送   |
| Topic         | ✅ 是                     | 通配符匹配（`*`/`#`） | 日志订阅，事件分发   |

---

