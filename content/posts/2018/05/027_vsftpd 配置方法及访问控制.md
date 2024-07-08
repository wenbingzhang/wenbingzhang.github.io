---
url: /blog/linux/BJrx8LE98CG
title: "vsftpd 配置方法及访问控制"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> vsftpd 详细配置说明

## vsftpd常用配置

```
#关闭匿名用户访问权限
anonymous_enable=NO
#开启本地用户权限
local_enable=YES
#开启写权限
write_enable=YES
#设置侦听端口
listen_port=21
#写文件时的umask
local_umask=002
#被动模式及开放端口段
#pasv_enable=yes
#pasv_min_port=30000
#pasv_max_port=50000
#超时时间
#idle_session_timeout=6000000
#data_connection_timeout=6000000
dirmessage_enable=YES
xferlog_enable=YES
connect_from_port_20=YES
xferlog_std_format=YES
chroot_local_user=YES
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd/chroot_list
listen=YES
pam_service_name=vsftpd
userlist_enable=YES
tcp_wrappers=YES
use_localtime=YES
reverse_lookup_enable=NO
#convert_charset_enable=0
#local_charset=UTF8
#remote_charset=GB2312
#double_377=1

```

创建账户

```
useradd -M -s /sbin/nologin -d /mnt/usernamefile/ username
for i in name1 name2 name3;do useradd -M -s /sbin/nologin -d /mnt/$i/ $i;done
for i in name1 name2 name3;do echo "$i"123 | passwd --stdin $i ;done

```

### 创建目录

```
mkdir usernamefile
chown username:username usernamefile
for i in name1 name2 name3;do mkdir /mnt/$i;done
for i in name1 name2 name3;do chown $i:$i /mnt/$i/;done
chmod -R 770 *

```

## vsftpd被动模式

### 1、开启被动模式

#vim vsftpd.conf

```
pasv_enable=YES #开启被动模式
pasv_min_port=3000 #随机最小端口
pasv_max_port=4000 #随机最大端口

```

### 2、加载内核

```
#modprobe ip_conntrack_ftp
#modprobe ip_nat_ftp

```

### 3、防火墙

#vim /etc/sysconfig/iptables 在*filter下加入下

```
-A OUTPUT -p tcp --sport 3000:4000 -j ACCEPT
-A INPUT -p tcp --dport 3000:4000 -j ACCEPT
#iptables-restore < /etc/sysconfig/iptables 加载iptables配置

```

* * *

## vsftpd虚拟用户

### 1、vsftpd安装

```
#yum -y install vsftpd #vsftpd软件
#yum -y install db4-utils #生成虚拟用户认证数据文件命令

```

### 2、配置vsftp

```
#vim /etc/vsftpd/vsftpd.conf
listen=YES #独立运行vsftpd
anonymous_enable=NO #限制匿名用户登录
dirmessage_enable=YES
xferlog_enable=YES
xferlog_file=/var/log/vsftpd.log
xferlog_std_format=YES
chroot_list_enable=YES #限制虚拟用户切换目录
chroot_list_file=/etc/vsftpd/chroot_list #限制切换目录的用户列表
chroot_local_user=YES
guest_enable=YES #开启虚拟用户认证
guest_username=ftp #映射的真实用户
user_config_dir=/etc/vsftpd/vsftpd_user_conf #虚拟用户配置目录
pam_service_name=vsftpd.vu #vsftpd认证的pam认证模块
local_enable=YES

```

### 3、虚拟用户db

```
#cd /etc/vsftpd
#vim user.txt
yuangang #用户名
123456 #密码
:wq #保存退出
#db_load -T -t hash -f user.txt /etc/vsftpd/vsftpd_login.db
#chmod 600 /etc/vsftpd/vsftpd_login.db
配置pam认证
#vim /etc/pam.d/vsftpd.vu
auth required /lib/security/pam_userdb.so db=/etc/vsftpd/vsftpd_login
account required /lib/security/pam_userdb.so db=/etc/vsftpd/vsftpd_login
:wq #保存退出
#vim /etc/vsftpd/chroot_list #限制虚拟用户切换目录
ftp
yuangang
:wq #保存退出

```

### 4、配置虚拟用户

```
#cd /etc/vsftpd/vsftpd_user_conf
#vim yuangang
write_enable=YES
anon_world_readable_only=NO
anon_upload_enable=YES
anon_mkdir_write_enable=YES
anon_other_write_enable=YES
local_root=/data/httpd/yuangang
:wq 保存退出
建立虚拟用户ftp目录
#mkdir /data/httpd/yuangang
#chown -R ftp.root /data/httpd
#chmod o+rw /data/httpd/yuangang

```

## vsftpd cmds_allowed

```
cmds_allowed=ABOR,CWD,LIST,MDTM,MKD,NLST,
PASS,PASV,PORT,PWD,QUIT,RETR,RMD,RNFR,
RNTO,SITE,SIZE,STOR,TYPE,USER,ACCT,
APPE,CDUP,HELP,MODE,NOOP,REIN,STAT,STOU,STRU,SYST

```

注意:一定不能使用换行和空格，不然就没效果..

### 全部参数

```
# ABOR - abort a file transfer 取消文件传输
# CWD - change working directory 更改目录
# DELE - delete a remote file 删除文件
# LIST - list remote files 列目录
# MDTM - return the modification time of a file 返回文件的更新时间
# MKD - make a remote directory 新建文件夹
# NLST - name list of remote directory
# PASS - send password
# PASV - enter passive mode
# PORT - open a data port 打开一个传输端口
# PWD - print working directory 显示当前工作目录
# QUIT - terminate the connection 退出
# RETR - retrieve a remote file 下载文件
# RMD - remove a remote directory
# RNFR - rename from
# RNTO - rename to
# SITE - site-specific commands
# SIZE - return the size of a file 返回文件大小
# STOR - store a file on the remote host 上传文件
# TYPE - set transfer type
# USER - send username
# less common commands:
# ACCT* - send account information
# APPE - append to a remote file
# CDUP - CWD to the parent of the current directory
# HELP - return help on using the server
# MODE - set transfer mode
# NOOP - do nothing
# REIN* - reinitialize the connection
# STAT - return server status
# STOU - store a file uniquely
# STRU - set file transfer structure
# SYST - return system type

```

### 常用参数

```
CWD - change working directory 更改目录
LIST - list remote files 列目录
MKD - make a remote directory 新建文件夹
NLST - name list of remote directory
PWD - print working directory 显示当前工作目录
RETR - retrieve a remote file 下载文件
STOR - store a file on the remote host 上传文件
DELE - delete a remote file 删除文件
RMD - remove a remote directory 删除目录
RNFR - rename from 重命名
RNTO - rename to 重命名

```

以上是常用的一些参数，大家对照学习一下！

### 几个例子

```
1、只能上传。不能下载、删除、重命名。
cmds_allowed＝FEAT,REST,CWD,LIST,MDTM,MKD,NLST,PASS,PASV,PORT,PWD,QUIT,RMD,SIZE,STOR,TYPE,USER,ACCT,
APPE,CDUP,HELP,MODE,NOOP,REIN,STAT,STOU,STRU,SYST
2、只能下载。不能上传、删除、重命名。write_enable=NO
3、只能上传、删除、重命名。不能下载。download_enable＝NO
4、只能下载、删除、重命名。不能上传。
cmds_allowed=FEAT,REST,CWD,LIST,MDTM,MKD,NLST,PASS,PASV,PORT,PWD,QUIT,RMD,RNFR,RNTO,
RETR,DELE,SIZE,TYPE,USER,ACCT,APPE,CDUP,HELP,MODE,NOOP,REIN,STAT,STOU,STRU,SYST

```

## 日志格式解析

Sun Feb 23 22:08:26 2014 | 6 | 212.73.193.130 | 1023575 |

/Lille_IconSP/win_230214_52_11.jpg | b| _| i| r| sipafranch| ftp| 0| *| c

记录 含义

Sun Feb 23 22:08:26 2014 FTP传输时间

6 传输文件所用时间。单位/秒

212.73.193.130 ftp客户端名称/IP

1023575 传输文件大小。单位/Byte

/Lille_IconSP/win_230214_52_11.jpg 传输文件名，包含路径

b 传输方式： a以ASCII方式传输; b以二进制(binary)方式传输;

_ 特殊处理标志位：”_“不做任何处理；”C”文件是压缩格式；”U”文件非压缩格式；”T”文件是tar格式；

i 传输方向：”i”上传；”o”下载；

r 用户访问模式：“a”匿名用户；”g”访客模式；”r”系统中用户;

sipafranch 登录用户名

ftp 服务名称，一般都是ftp

0 认证方式：”0”无；”1”RFC931认证；

- 认证用户id，”*“表示无法获取id


c 完成状态：”i”传输未完成；”c”传输已完成；