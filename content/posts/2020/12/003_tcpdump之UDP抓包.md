---
url: /blog/linux/-vpymjJGg
title: "tcpdump之UDP抓包"
date: 2020-12-18T15:01:47+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 使用tcpdump抓UDP包，过滤过滤IP和port，并且自动拆分片段。

## 安装tcpdump

```bash
yum install -y tcpdump

```

## 使用方法

```bash
tcpdump -i bond0 udp port xxxx and host xxx.x.xx.xxx -s0 -G 600  -w %Y_%m%d_%H%M_%S.pcap

```

### 参数说明

-i 指定监听的网卡

udp 监听UDP协议

port 指定过滤的端口

host 指定过滤的ip

-s \*表示\*从一个包中截取的字节数，\*0表示\*包不截断

-G 按照固定的时间间隔切割输出的文件（单位：秒）

-w 直接将包写入文件中，并不分析和打印出来；

取非运算是 ‘not ’ ‘! ‘，与运算是’and’，’&&;或运算 是’or’ ,‘\|\|’

## 定时抓包(python)

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @author 张文兵
# @blog https://zhangwenbing.com/
# @datetime 2020-12-18 14:56:01
# @description
#

import os
import time
from apscheduler.schedulers.blocking import BlockingScheduler

def system(cmd):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} 执行 {}'.format(t, cmd))
    stat = os.system(cmd)
    if stat != 0:
        print('{} 执行 {} 失败'.format(t, cmd))

scheduler = BlockingScheduler()

# 星期1-5的17点40分执行抓包任务
scheduler.add_job(system, 'cron', day_of_week="mon,tue,wed,thu,fri,sat",
                  hour=17, minute=30, args=['/sbin/tcpdump -i bond0 udp port xxxx and host xxx.x.xx.xxx -s0 -G 3600  -w /your_path/%Y_%m%d_%H%M_%S.pcap &>/dev/null'])

# 星期1-5的20点01分执行kill
scheduler.add_job(system, 'cron', day_of_week="mon,tue,wed,thu,fri,sat",
                  hour=20, minute=1, args=['pkill -9 tcpdump &>/dev/null'])
scheduler.start()

# 星期1-5的23点59分执行自动清理7天之前的抓包文件
scheduler.add_job(system, 'cron', day_of_week="mon,tue,wed,thu,fri,sat",
                  hour=23, minute=59, args=['/usr/bin/find /your_path/ -type  f  -ctime +7  -exec rm -f   {} \; &>/dev/null'])
scheduler.start()

```

## 切分抓包文件

```bash
tcpdump -r old_file -w new_files -C 10

```

-r 指定需要切分的文件

-w 指定新的文件名前缀

-C 指定切分的文件大小（单位：M）