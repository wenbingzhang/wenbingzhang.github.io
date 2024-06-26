---
url: /blog/linux/B18l8L49U0z
title: "centos7.x 主备切换之心跳服务"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 原文地址：http://jensd.be/156/linux/building-a-high-available-failover-cluster-
>
> with-…

原文地址：http://jensd.be/156/linux/building-a-high-available-failover-cluster-

with-pacemaker-corosync-pcs操作之前先关闭防火墙和selinux需要防火墙请执行如下操作 Open UDP-ports 5404

and 5405 for Corosync:

```
sudo iptables -I INPUT -m state --state NEW -p udp -m multiport --dports 5404,5405 -j ACCEPT
sudo iptables -I INPUT -m state --state NEW -p udp -m multiport --dports 5404,5405 -j ACCEPT

```

Open TCP-port 2224 for PCS

```
sudo iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 2224 -j ACCEPT
sudo iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 2224 -j ACCEPT

```

Allow IGMP-traffic

```
sudo iptables -I INPUT -p igmp -j ACCEPT
sudo iptables -I INPUT -p igmp -j ACCEPT

```

Allow multicast-traffic

```
sudo iptables -I INPUT -m addrtype --dst-type MULTICAST -j ACCEPT
sudo iptables -I INPUT -m addrtype --dst-type MULTICAST -j ACCEPT

```

Save the changes you made to iptables:

```
sudo service iptables save

节点一、二

yum install corosync pcs pacemaker -y
 passwd hacluster
 systemctl start pcsd

```

vim /usr/lib/systemd/system/corosync.service

```
[Unit]
 Description=Corosync Cluster Engine
 ConditionKernelCommandLine=!nocluster
 Requires=network-online.target
 After=network-online.target
 [Service]
 ExecStartPre=/usr/bin/sleep 10
 ExecStart=/usr/share/corosync/corosync start
 ExecStop=/usr/share/corosync/corosync stop
 Type=forking
 [Install]
 WantedBy=multi-user.target

systemctl enable pcsd
systemctl enable pacemaker
systemctl enable crm_mon
systemctl enable corosync

```

节点一 cat /etc/hosts

```
pcs cluster auth rabbitmq-1 rabbitmq-2
 pcs cluster setup --name cluster_rabbitmq rabbitmq-1 rabbitmq-2
 pcs cluster start --all
 pcs status cluster
 pcs status nodes
 corosync-cmapctl | grep members
 pcs status corosync
 crm_verify -L -V #此处如果报错请执行以下3行，否则跳过
 pcs property set stonith-enabled=false
 pcs property set no-quorum-policy=ignore
 pcs property

pcs resource create virtual_ip ocf:heartbeat:IPaddr2 ip=10.1.209.159 cidr_netmask=32 op monitor interval=30s
 pcs status resources
 ip addr

```

## 常用命令汇总：

查看集群状态：#pcs status

查看集群当前配置：#pcs config

开机后集群自启动：#pcs cluster enable –all

启动集群：#pcs cluster start –all

查看集群资源状态：#pcs resource show

验证集群配置情况：#crm\_verify -L -V

测试资源配置：#pcs resource debug-start resource

设置节点为备用状态以及重新上线：#pcs cluster standby node1/#pcs cluster unstandby node1