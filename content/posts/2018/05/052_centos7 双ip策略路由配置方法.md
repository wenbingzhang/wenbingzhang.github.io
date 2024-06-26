---
url: /blog/linux/HyEL84qI0M
title: "centos7 双ip策略路由配置方法"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 服务器配置多网卡多网关时，为了避免时不时的去添加相关回程路由，因此需要配置一下策略路由。

原文地址 [blog.csdn.net](https://blog.csdn.net/pyxllq/article/details/105817064)

服务器系统版本：CentOS Linux release 7.3.1611

## 1.添加路由表

```bash
vi /etc/iproute2/rt_tables

...

101     innerRoute
102     globalRoute

```

## 2\. 添加路由配置脚本

```bash
ip route flush table globalRoute
ip rule add dev eth1 table globalRoute
if ! ip rule show | grep x.x.x.x ; then
    ip rule add from x.x.x.x table globalRoute
fi
ip route add default via y.y.y.y dev eth1 table globalRoute

ip route flush table innerRoute
ip rule add dev eth2 table innerRoute
if ! ip rule show | grep 172.16.x.x ; then
    ip rule add from 172.16.x.x table innerRoute
fi
ip route add default via 172.16.y.y dev eth2 table innerRoute

```

上面 x.x.x.x 是配置在网口 eth1 上的 ip，y.y.y.y 是该 ip 的网关，172.16.x.x 是 eth2 的 ip，我这里是内网 ip，172.16.y.y 是 172 网关的网关。

## 3\. 开机启动

```bash
1、（/opt/script/autostart.sh是你的脚本路径）

chmod +x /opt/script/autostart.sh
2、打开/etc/rc.d/rc.local文件，在末尾增加如下内容

/opt/script/autostart.sh
3、在centos7中，/etc/rc.d/rc.local的权限被降低了，所以需要执行如下命令赋予其可执行权限

chmod +x /etc/rc.d/rc.local

```

注释：centos 7.5 系统配置命令都是需要 id(101,102) 不再是名字