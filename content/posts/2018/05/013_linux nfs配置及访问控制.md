---
url: /blog/linux/rJJe8UNcU0M
title: "linux nfs配置及访问控制"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> NFS软件包

nfs-utils portmap (rhel6换成了rpcbind ,所以启动服务时需要注意)

NFS文件

/etc/exports #N…

## NFS软件包

nfs-utils portmap (rhel6换成了rpcbind ,所以启动服务时需要注意)

## NFS文件

/etc/exports #NFS主配置文件 /etc/init.d/nfs #NFS启动脚本 /etc/init.d/protmap

#portmap启动脚本 /var/lib/*tab #NFS日志文件

## 书写规则

目录名(绝对路径) 客户端主机名、IP或“*”(选项) 选项可选择如下：

sync：设置NFS服务器同步写磁盘,这样不会轻易丢失数据,建议所有的NFS共享目录使用该选项. ro：设置输出的共享目录为只读，与rw不能同时使用。

rw：设置输出的共享目录为可读写，与ro不能同时使用。 root_squash：root用户访问共享目录的身份会自动变成nobody身份。

no_root_squash：root用户会以自己的真实身份访问共享目录，不安全，不建议使用。 更多选项可在网上查

## showmount

showmount命令用于查询显示NFS服务器的相关信息 显示NFS服务器的输出目录列表 显示当前本机中NFS服务器输出列表

```
showmount -e

```

显示指点NFS服务器中的共享目录列表

```
showmount -e IP

```

## 防火墙配置

nfsd：2049 rhel5 portmap：111 rhel6 rpcbind：111

rquotad,mountd,sratd和lockd可以强制使用一个大于1024的静态端口

```
修改/etc/sysconfig/nfs文件
QUOTAD_PORT=40001 #rpc.quotad进程端口
LOCKD_TCPPORT=40002 #rpc.lockd进程端口
LOCKD_UDPPORT=40002
MOUNTD_PORT=40003 #rpc.mountd进程端口
STARTD_PORT=40004 #rpc.sratd进程端口

```

## exportfs

修改了/etc/exports文件不需要重启nfs，只要重新加载/etc/exports文件即可。

-a：全部挂载（或卸载）/etc/exports文件内的设定。

-r：重新加载/etc/exports中的设置，此外同步更新/etc/exports及/var/lib/nfs/xtab中的内容。

-u：卸载某一目录。

-v：在export时将共享的目录显示在屏幕上。

### 常用组合

exportfs -rv (重新加载配置并输出当前共享的目录)

exportfs -auv (停止当前主机中NFS服务器的所有输出目录)

## 服务配置

```
vim /etc/exports
/home/share 10.1.1.2(sync,rw) *(sync,ro)

```

## linux使用

```
mount -t nfs ip地址:/home/share/ /mnt

```

## Windwos使用

Windows 7或Windows 2008支持NFS客户端,NFS服务端只有Windows Server版本支持

```
showmount -e 10.1.1.1
mount \\10.1.1.1\share Z:

```

需要注意的是，mount 挂载点和Linux及UNIX有所不同，不是使用一个目录作为挂载点，而是使用一个未被使用的盘符。