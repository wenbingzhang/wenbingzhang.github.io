---
url: /blog/linux/QNIBzjz3k
title: "supervisor 常见坑及解决办法"
date: 2020-07-14T09:51:26+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> Too many open files、获取不到$HOME等

## Too many open files

```bash
vim /etc/supervisord.conf
[supervisord]
minfds=81920
minprocs=81920

# systemctl restart supervisord
```

## 获取不到$HOME

```bash
[program:apache2]
command=/home/chrism/bin/httpd -c "ErrorLog /dev/stdout" -DFOREGROUND
user=chrism
environment=HOME="/home/chrism",USER="chrism"

supervisorctl update
```