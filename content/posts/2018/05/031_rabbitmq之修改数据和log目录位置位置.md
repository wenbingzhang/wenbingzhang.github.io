---
url: /blog/linux/ry3FIUV58AM
title: "rabbitmq之修改数据和log目录位置位置"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> vim /etc/rabbitmq/rabbitmq-env.conf

# I am a complete /etc/rabbitmq/rabbitmq-e…

```bash
 vim /etc/rabbitmq/rabbitmq-env.conf

# I am a complete /etc/rabbitmq/rabbitmq-env.conf file.
# Comment lines start with a hash character.
# This is a /bin/sh script file - use ordinary envt var syntax
MNESIA_BASE=/data/rabbitmq/mnesia
LOG_BASE=/data/logs/rabbitmq

```