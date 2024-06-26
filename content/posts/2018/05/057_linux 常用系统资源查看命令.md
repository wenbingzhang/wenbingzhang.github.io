---
url: /blog/linux/S19ZLLE9I0G
title: "linux 常用系统资源查看命令"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 一、sar命令

```
# sar 1 10  监控CPU，每秒监控一次，共监控10次
# sar -P ALL 1 5   监控所有CPU
# sar -S 1 10      监控交换分区
# sar -d 1 10      监控磁盘IO
# sar -b 1 10      监控磁盘IO和速率
# sar -r 1 10      监控内存使用
# sar -n DEV  1 10 监控网络接口卡的数据传输

```

## 二、mpstat

```
# mpstat -P ALL 1 10

```

## 三、iostat

```
# iostat -c 2
# iostat -d 1 100
# iostat 1 20
# iostat -p /dev/sda2 1 10

```

## 四、vmstat

```
#vmstat -d 1 20
输出信息
r 运行队列中的进程数，不要长时间超过CPU核心总数
b 等待IO的进程数
si 每秒从交换分区写到内存的数据大小
so 每秒写入交换分区的数据大小
#vmstat -a 1 10

```

## 五、其它常用监控命令

(1) top (2) free (3) iptraf