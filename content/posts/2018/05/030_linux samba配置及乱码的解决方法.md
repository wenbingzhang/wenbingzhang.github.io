---
url: /blog/linux/rkxlI845IAz
title: "linux samba配置及乱码的解决方法"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

## 简要说明

samba：这个软体主要提供了SMB伺服器所需的各项服务程式(smbd及nmbd)、的文件档、以及其他与SAMBA相关的logrotate设定档及开机预设选项档案等；

samba-client：这个软体则提供了当Linux做为SAMBA

Client端时，所需要的工具指令，例如挂载SAMBA档案格式的mount.cifs、取得类似网芳相关树状图的smbtree等等；

samba-common：这个软体提供的则是伺服器与用户端都会使用到的资料，包括SAMBA的主要设定档(smb.conf)、语法检验指令(testparm)等等；

/var/lib/samba/private/{passdb.tdb,secrets.tdb}：管理Samba的使用者帐号/密码时，会用到的资料库档案；

## 服务配置

vim /etc/samba/smb.conf

```bash
[share]
path = /share //共享的目录
writable = yes //是否可写
write list = test // test用户可以访问该共享

```

## 访问控制

```bash
max connections = 最大连接数
deadtime = 断掉连接时间（分钟）【0为不限制】
hosts deny = IP 、域名、except
hosts allow = IP 、域名、except

```

## 用户控制

```bash
public = no #不允许匿名用户访问
browseable = no #隐藏目录 （知道目录同样可以访问）
valid users = 用户或列表或@用户组
writable = yes #可写（目录本身要可写）
weite list = 用户或列表或@用户组
read only = yes #只读设置
create mask = 0744 #控制客户机创建文件的权限
directory mask = 0744 # 控制客户机创建目录的权限

```

## 安全级别

samba服务器的安全级别分为5种，分别是user、share、server、domain和ads。

在设置不同的级别时，samba服务器还会使用口令服务器和加密口令。

1、user —–客户端访问服务器时需要输入用户名和密码，通过验证后，才能使用服务器的共享资源。此级别使用加密的方式传送密码。

2、share —–客户端连接服务器时不需要输入用户名和密码

3、server —–客户端在访问时同样需要输入用户名和密码，但是，密码验证需要密码验证服务器来负责。

4、domain —–采用域控制器对用户进行身份验证

5、ads —–若samba服务器加入到Windows活动目录中，则使用ads安全级别，ads安全级别也必须指定口令服务器

## 启动服务

```bash
service smb reload

```

## 管理工具

修改完配置文件后，启动服务，然后添加Samba用户（pdbedit -a 用户名）

使用pdbedit指令功能 选项与参数：

-L ：列出目前在资料库当中的帐号与UID 等相关资讯；

-v ：需要搭配-L 来执行，可列出更多的讯息，包括家目录等资料；

-w ：需要搭配-L 来执行，使用旧版的smbpasswd 格式来显示资料；

-a ：新增一个可使用Samba 的帐号，后面的帐号需要在/etc/passwd 内存在者；

-r ：修改一个帐号的相关资讯，需搭配很多特殊参数，请man pdbedit；

-x ：删除一个可使用Samba 的帐号，可先用-L 找到帐号后再删除；

-m ：后面接的是机器的代码(machine account)，与domain model 有关！

## 乱码问题

```bash
cat /etc/sysconfig/i18n
[global]
# 如果locale是zh_CN.UTF-8，做如下设置：
display charset = UTF-8
unix charset = UTF-8
dos charset = UTF-8
# 如果locale是zh_CN.GBK或zh_CN.gb2312，做如下设置：
display charset = cp936
unix charset = cp936
dos charset = cp936

```

## linux访问

```bash
smbclient //IP/目录名 -U 登录用户名
mount -t cifs -o username=用户名,passwd=密码,iocharset=gb2312,uid,pid,rw //ip 挂载点
smbtar -s server -u user -p passwd -x sharename -t output.tar

```

## windows访问

windows访问方式就不说了。下面说下清除windows共享访问方法：

```bash
打开cmd.
c:\>net use * /del

```