---
url: /blog/linux/loBZJ41MR
title: "CentOS添加静态路由之route"
date: 2020-12-09T20:50:36+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> route命令参数详细说明及常用命令

原文地址 [docs.lvrui.io](https://docs.lvrui.io/2016/10/12/CentOS%E4%B8%8B%E6%B7%BB%E5%8A%A0%E9%9D%99%E6%80%81%E8%B7%AF%E7%94%B1/)

```bash
> route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         localhost       0.0.0.0         UG    100    0        0 eno16780032
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.10.0    0.0.0.0         255.255.255.0   U     100    0        0 eno16780032

```

_macOS 中使用 `netstat -nr` 命令来查看当前路由表_

- Destination 目标网路

- Gateway 网关

- Genmask 掩码

- Flags 标识


  - U 路由已经启动

  - H 路由目标为主机

  - G 使用网关

  - R 为动态路由复原路由表

  - D 由守护进程或间接动态安装

  - M 被路由守护进程或间接修改

  - A 通过 addrconf 修改

  - C 缓存条目

  - ! 拒绝路由
- Metric 路由开销, 到目标的‘距离’（通常基于跳数统计）

- Ref 参考此路由的数量

- Use 路由查找计数。依赖与使用 - F 还是 - C 选项，这个值要么是路由缓存未命中数要么是命中数

- Iface 此路由数据包发送到的网络接口


## 添加到主机的路由

```bash
route add –host 192.168.59.2 dev eth1
route add –host 192.168.59.2 gw 192.168.10.85

```

## 添加到网络的路由

```bash
route add -net 192.168.248.0/24 gw 192.168.10.85
route add –net 192.168.248.0 netmask 255.255.255.0 gw 192.168.10.85
route add –net 192.168.248.0 netmask 255.255.255.0 dev eth1

```

## 添加默认网关

```bash
route add default gw 192.168.10.85
route add -net 0.0.0.0 gw 192.168.10.85

```

**使用 route 命令添加的路由，机器重启或者网卡重启后路由就失效了**

```bash
route del –host 192.168.10.85 dev eth1

```

_怎么 add 的就怎么 del 掉. 但是 del 的时候可以不写网关_

- 在 `/etc/rc.local` 里添加路由信息


  ```bash
  route add -net 192.168.247.0/24 dev eth1
  route add -net 192.168.110.0/24 gw 192.168.10.85

  ```

- 在 `/etc/sysconfig/network` 里添加到末尾 `GATEWAY=gw-ip 或者 GATEWAY=gw-dev`

- 在 `/etc/sysconfig/static-router` 添加 `any net x.x.x.x/24 gw y.y.y.y`


## 添加永久路由

**CentOS7 下推荐使用上面第三种方法添加永久静态路由**

```bash
[root@centos7 ~]
10.15.150.0/24 via 192.168.150.253 dev enp0s3
10.25.250.0/24 via 192.168.150.253 dev enp0s3

```

将永久静态路由需要写到 /etc/sysconfig/network-scripts/route-interface 文件中

注意:

**ifcfg-enp0s3 文件改名为 ifcfg-eth0 后，route-enp0s3 文件也要改名为 route-eth0**

参考文档:

- [https://www.cnblogs.com/panblack/p/Centos7_Static_Routes.html](https://www.cnblogs.com/panblack/p/Centos7_Static_Routes.html)