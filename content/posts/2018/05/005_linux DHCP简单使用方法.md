---
url: /blog/linux/B1CLLE98CG
title: "linux DHCP简单使用方法"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 配置

vim /etc/dhcpd.conf

default-lease-time 1296000;

max-lease-time 4000000;

#IP…

配置

```
vim /etc/dhcpd.conf

default-lease-time 1296000;
max-lease-time 4000000;
#IP最长失效时间
option subnet-mask 255.255.255.0;
#子网的掩码
option broadcast-address 192.168.0.255;
#网络的广播地址
option routers 192.168.0.254;
#网关的地址
option domain-name-servers 211.151.48.59,211.151.48.47;
#域名解析地址
ddns-update-style ad-hoc;
subnet 192.168.0.0 netmask 255.255.255.0 {
#定义IP池的内容
range 192.168.0.100 192.168.0.240;
#地址范围为 100-240 共140个IP地址。
}
#也可以象下面一样按MAC地址指定IP
#host Jephe {hardware ethernet 00:a0:c9:a6:96:33;fixed-address 192.168.1.12;}

```

## 详解

### parameters（参数）

ddns-update-style 配置DHCP-DNS互动更新模式 default-lease-time 指定缺省租赁时间的长度，单位是秒 max-

lease-time 指定最大租赁时间长度，单位是秒 hardware 指定网卡接口类型和MAC地址 server-name 通知DHCP客户服务器名称

get-lease-hostnames flag 检查客户端使用的IP地址 fixed-address ip 分配给客户端一个固定的地址

authritative 拒绝不正确的IP地址的要求

### declarations（声明）

shared-network 用来告知是否一些子网络分享相同网络 subnet 描述一个IP地址是否属于该子网 range 起始IP 终止IP

提供动态分配IP 的范围 host 主机名称 参考特别的主机 group 为一组参数提供声明 allow unknown-clients或deny

unknown-client 是否动态分配IP给未知的使用者 allow bootp或deny bootp 是否响应激活查询 allow

booting或deny booting 是否响应使用者查询 filename 开始启动文件的名称，应用于无盘工作站 next-server

设置服务器从引导文件中装如主机名，应用于无盘工作站

### option（选项）

subnet-mask 为客户端设定子网掩码 domain-name 为客户端指明DNS名字 domain-name-servers

为客户端指明DNS服务器IP地址 host-name 为客户端指定主机名称 routers 为客户端设定默认网关 broadcast-address

为客户端设定广播地址 ntp-server 为客户端设定网络时间服务器IP地址 time-offset 为客户端设定和格林威治时间的偏移时间，单位是秒。

## 中继

### 配置步骤

1、开启路由转发

2、设置就哦中继接口及DHCP服务器地址

3、启动dhcprelay中继服务程序

### 内核参数

```
vim /etc/sysctl.conf
net.ipv4.ip_forward = 1
sysctl -p

```

### 修改配置

```
vim /etc/sysconfig/dhcrelay
INTERFACES="eth0 eth1"
DHCPSERVERS="192.168.1.2"

```

## 启动

```
chkconfig dhcrelay on
chkconfig dhcp on
/etx/init.d/dhcp start
/etc/init.d/dhcrelay start

```