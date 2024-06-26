---
url: /blog/linux/B1OZ8INcIAM
title: "linux mount命令详解"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 功能

加载指定的文件系统。

语法

mount \[-afFhnrvVw\] \[-L\] \[-o\] \[-t\] \[设备名\] \[加载点\]

用法

说明：mount可…

## 功能

加载指定的文件系统。

## 语法

mount \[-afFhnrvVw\] \[-L\] \[-o\] \[-t\] \[设备名\] \[加载点\]

## 用法

说明：mount可将指定设备中指定的文件系统加载到Linux目录下（也就是装载点）。可将经常使用的设备写入文件/etc/fastab,以使系统在每次启动时自动加载。mount加载设备的信息记录在/etc/mtab文件中。使用umount命令卸载设备时，记录将被清除。

### 常用参数和选项

-a 加载文件/etc/fstab中设置的所有设备。

-f 不实际加载设备。可与-v等参数同时使用以查看mount的执行过程。

-F 需与-a参数同时使用。所有在/etc/fstab中设置的设备会被同时加载，可加快执行速度。

-h 显示在线帮助信息。

-L 加载文件系统标签为的设备。

-n 不将加载信息记录在/etc/mtab文件中。

-o 指定加载文件系统时的选项。有些选项也可在/etc/fstab中使用。这些选项包括：

async 以非同步的方式执行文件系统的输入输出动作。

atime 每次存取都更新inode的存取时间，默认设置，取消选项为noatime。

auto 必须在/etc/fstab文件中指定此选项。执行-a参数时，会加载设置为auto的设备，取消选取为noauto。

defaults 使用默认的选项。默认选项为rw、suid、dev、exec、anto nouser与async。

dev 可读文件系统上的字符或块设备，取消选项为nodev。

exec 可执行二进制文件，取消选项为noexec。

data=writeback 不记录磁盘的日志

data=ordered 只记录主要的日志

data=journal 记录所有的日志

noatime 每次存取时不更新inode的存取时间。

noauto 无法使用-a参数来加载。

nodev 不读文件系统上的字符或块设备。

noexec 无法执行二进制文件。

nosuid 关闭set-user-identifier(设置用户ID)与set-group-identifer(设置组ID)设置位。

nouser 使一般用户无法执行加载操作，默认设置。

remount 重新加载设备。通常用于改变设备的设置状态。

ro 以只读模式加载。

rw 以可读写模式加载。

suid 启动set-user-identifier(设置用户ID)与set-group-identifer(设置组ID)设置位，取消选项为nosuid。

sync 以同步方式执行文件系统的输入输出动作。

user 可以让一般用户加载设备。

-r 以只读方式加载设备。

-t 指定设备的文件系统类型。常用的选项说明有：

minix Linux最早使用的文件系统。

ext2 Linux目前的常用文件系统。

msdos MS-DOS 的 FAT。

vfat Win85/98 的 VFAT。

nfs 网络文件系统。

iso9660 CD-ROM光盘的标准文件系统。

ntfs Windows NT的文件系统。

hpfs OS/2文件系统。Windows NT 3.51之前版本的文件系统。

auto 自动检测文件系统。

-v 执行时显示详细的信息。

-V 显示版本信息。

-w 以可读写模式加载设备，默认设置。

## 卸载故障

故障原因 需要卸载的设备正在被使用 现象：提示：“…device is busy”

## 解决思路

将工作目录切换到挂载点以外，退出正在使用该设备的程序，使用fuser命令找出相关进程，结束该进程。