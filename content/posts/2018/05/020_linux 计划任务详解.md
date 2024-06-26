---
url: /blog/linux/rJvbIUV580z
title: "linux 计划任务详解"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> crontab命令常见于Unix和类Unix的操作系统之中，用于设置周期性被执行的指令

## 定时任务

### 启动服务

```
service atd restart
chkconfig atd on

```

### 常用方式

```
常用时间格式：
at [HH:MM]
at [HH:MM] [yyyy-mm-dd]
at now +数字[minutes|hours|days|weeks]

at now+1minutes    一分钟后执行新建ab目录和rr文件
at> mkdir ab
at> touch rr
at> <EOT>
job 1 at 2012-12-16 17:05

```

在键盘上按ctrl+d退出at命令模式 这里不详细说了，因为平时用的比较少，所以我也懒得去研究它的详细参数和使用方法了。

## 周期循环任务

### 启动服务

```
service crond restart
停止 crond：                                               [确定]
启动 crond：                                               [确定]

```

### 配置文件

```
cat /etc/crontab
SHELL=/bin/bash    计划任务的默认脚本bash shell
PATH=/sbin:/bin:/usr/sbin:/usr/bin    默认搜索路径
MAILTO=root     当计划任务有标准输出或标准错误输出时，会将结果发邮件给root
HOME=/
# run-parts
01 * * * * root run-parts /etc/cron.hourly   /etc/ 后面一定是个文件夹，每小时执行
02 4 * * * root run-parts /etc/cron.daily
22 4 * * 0 root run-parts /etc/cron.weekly
42 4 1 * * root run-parts /etc/cron.monthly

```

### 注意事项

多个计划任务不宜同时进行防止有非法计划任务周和日，月不可同时并存，容易导致计划任务时间混乱

### 简要说明

crond

是linux用来定期执行程序的命令。当安装完成操作系统之后，默认便会启动此任务调度命令。crond命令每分锺会定期检查是否有要执行的工作，如果有要执行的工作便会自动执行该工作。而linux任务调度的工作主要分为以下两类：1、系统执行的工作：系统周期性所要执行的工作，如备份系统数据、清理缓存。2、个人执行的工作：某个用户定期要做的工作，例如每隔10分钟检查邮件服务器是否有新信，这些工作可由每个用户自行设置

crontab是UNIX系统下的定时任务触发器，其使用者的权限记载在下列两个文件中：

### 文件含义

/etc/cron.deny 该文件中所列的用户不允许使用Crontab命令

/etc/cron.allow 该文件中所列的用户允许使用Crontab命令

/var/spool/cron/ 是所有用户的crontab文件

/var/spool/cron/crontabs /var/spool/cron/crontabs /etc/crontab 系统计划任务列表文件

```
Crontab命令的格式为：crontab –l|-r|-e|-i [username]，其参数含义如表一：
参数名称 含义 示例
-l 显示用户的Crontab文件的内容 crontabl –l
-i 删除用户的Crontab文件前给提示 crontabl -ri
-r 从Crontab目录中删除用户的Crontab文件 crontabl -r
-e 编辑用户的Crontab文件 crontabl -e

```

### 基本格式

- \\* \\* \\* \\* command <--> 分　时　日　月　周　命令


第1列表示分钟1～59 每分钟用\*或者 \*/1表示

第2列表示小时1～23（0表示0点）

第3列表示日期1～31

第4列表示月份1～12

第5列标识号星期0～6（0表示星期天）

第6列要运行的命令

### 时间数值特殊表示方法

＊ 表示该范围内的任意时间 ，表示间隔的多个不连续时间点

－ 表示一个连续的时间范围

/n 指定间隔的时间频率

### 常用例子

```
#每晚的21:30重启apache
30 21 * * * /usr/local/etc/rc.d/lighttpd restart
#每月1、10、22日的4 : 45重启apache
45 4 1,10,22 * * /usr/local/etc/rc.d/lighttpd restart
#每周六、周日的1 : 10重启apache
10 1 * * 6,0 /usr/local/etc/rc.d/lighttpd restart
#每天18 : 00至23 : 00之间每隔30分钟重启apache
0,30 18-23 * * * /usr/local/etc/rc.d/lighttpd restart
#每个星期的星期六的11 : 00 pm重启apache
0 23 * * 6 /usr/local/etc/rc.d/lighttpd restart
#每一小时重启apache
* */1 * * * /usr/local/etc/rc.d/lighttpd restart
#每天的晚上11点到早上7点之间，每隔一小时重启apache
* 23-7/1 * * * /usr/local/etc/rc.d/lighttpd restart
#每月的4号与每周一到周三的11点重启apache
0 11 4 * mon-wed /usr/local/etc/rc.d/lighttpd restart
#每年的一月一号的4点重启apache
0 4 1 jan * /usr/local/etc/rc.d/lighttpd restart

```