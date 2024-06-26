---
url: /blog/linux/Skl7i90EQ
title: "centos6 heartbeat双机热备"
date: 2018-08-01T02:54:29+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> heartbeat （Linux-HA）的工作原理：heartbeat最核心的包括两个部分，心跳监测部分和资源接管部分，心跳监测可以通过网络链路和串口进行，而且支持冗 余链路，它们之间相互发送报文来告诉对方自己当前的状态，如果在指定的时间内未收到对方发送的报文，那么就认为对方失效，这时需启动资源接管模块来接管运 行在对方主机上的资源或者服务。

## 环境

host: 10.1.201.50 hostname: solr2

host: 10.1.201.49 hostname: solr1

VIP: 10.1.201.80

## 安装

分别在两台机器上安装heartbeat

```
# yum install heartbeat -y

```

## 配置

### solr1

拷贝默认配置文件

```
# cp /usr/share/doc/heartbeat-3.0.4/{ha.cf,authkeys,haresources} /etc/ha.d/

```

修改主配置文件ha.cf

```
# egrep -Ev "^#|^$" ha.cf
debugfile /var/log/ha-debug #用于记录heartbeat的调试信息
logfile /var/log/ha-log #用于记录heartbeat的日志信息
logfacility local0 #系统日志级别
keepalive 2 #设定心跳(监测)间隔时间，默认单位为秒
deadtime 30 # 超出30秒未收到对方节点的心跳，则认为对方已经死亡
warntime 10 #＃警告时间，通常为deadtime时间的一半
initdead 60 #网络启动时间，至少为deadtime的两倍。
#hopfudge 1  #可选项：用于环状拓扑结构,在集群中总共跳跃节点的数量
#udpport 694  #使用udp端口694 进行心跳监测
ucast em1 10.1.201.50 #采用单播，进行心跳监测，IP为对方主机IP
auto_failback off #on表示当拥有该资源的属主恢复之后，资源迁移到属主上
node solr1 #设置集群中的节点，节点名须与uname –n相匹配
node solr2 #设置集群中的节点，节点名须与uname –n相匹配
ping 10.1.201.254 #ping集群以外的节点，这里是网关，用于检测网络的连接性
#respawn root /usr/lib/heartbeat/ipfail
#apiauth ipfail gid=root uid=root  #设置所指定的启动进程的权限

```

修改认证文件authkeys

```
# egrep -Ev "^#|^$" authkeys
auth 1
1 sha1 0832bedde820a9bcf6858c0ff6e5e82a

# chmod 600 /etc/ha.d/authkeys

```

修改资源文件haresources

```
# egrep -Ev "^#|^$" haresources
solr2 IPaddr::10.1.201.80/24/em1 #em1根据自身机器不同需做调整

```

将所有的配置文件拷贝到solr2节点上

```
scp /etc/ha.d/ha.cf root@solr2:/etc/ha.d/
scp /etc/ha.d/haresources root@solr2:/etc/ha.d/
scp /etc/ha.d/authkeys  root@solr2:/etc/ha.d/

```

### solr2

```
]# egrep -Ev "^#|^$" ha.cf
debugfile /var/log/ha-debug
logfile /var/log/ha-log
logfacility local0
keepalive 2
deadtime 30
warntime 10
initdead 60
ucast em1 10.1.201.49  #只要将这个选项修改为另一个节点的ip即可
auto_failback off
node solr1
node solr2
ping 10.1.201.254

```

## 启动服务

分别在两台机器上启动heartbeat

```
/etc/init.d/heartbeat start # 或者 service heartbeat start

```