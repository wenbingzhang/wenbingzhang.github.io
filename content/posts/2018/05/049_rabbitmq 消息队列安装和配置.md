---
url: /blog/linux/HkXeLI4cIAG
title: "rabbitmq 消息队列安装和配置"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

## erlang

首先安装erlang语言环境

```bash
yum install erlang -y

```

## rabbitMQ

rabbitMQ下载地址：直达安装方法:

```bash
rpm -ivh --force --nodeps rabbitmq-server-3.6.0-1.noarch.rpm
或者
yum localinstall  rabbitmq-server-3.6.0-1.noarch.rpm -y

```

## 启动服务

```bash
/etc/init.d/rabbitmq-server start
rabbitmq-plugins enable rabbitmq_management

```

## 配置主备

### 同步cookie

```bash
chmod 777 /var/lib/rabbitmq/.erlang.cookie
scp /var/lib/rabbitmq/.erlang.cookie Go02:/var/lib/rabbitmq/.erlang.cookie
chmod 400 /var/lib/rabbitmq/.erlang.cookie

```

### 添加节点

```bash
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl join_cluster [--ram] rabbit@Go01 //此处的Go01为主节点的hostname,需要在/etc/hosts中指定
rabbitmqctl start_app

```

### 删除节点

```bash
rabbitmqctl stop_app
rabbitmqctl forget_cluster_node rabbit@rabbit1

```

### 修改类型

```bash
rabbitmqctl stop_app
rabbitmqctl change_cluster_node_type ram
rabbitmqctl start_app

```

### 添加用户

```bash
rabbitmqctl add_user admin admin
添加权限:
rabbitmqctl set_permissions -p "/" admin ".*" ".*" ".*"
删除测试用户:
rabbitmqctl delete_user guest
赋予其administrator角色：
rabbitmqctl set_user_tags admin administrator

```

### 修改配置

```bash
//防止服务端异常中断恢复后镜像队列不能恢复的问题

vim /etc/rabbitmq/rabbitmq.conf
[
  {rabbit,[{tcp_listeners,[5672]},
  {cluster_partition_handling, autoheal}]}
].
#不要忘记最后面的那个点号哦！

```

### 环境变量

```bash
touch /etc/rabbitmq/rabbitmq-env.conf#输入
    RABBITMQ_NODENAME=FZTEC-240088 节点名称    RABBITMQ_NODE_IP_ADDRESS=127.0.0.1 监听IP
    RABBITMQ_NODE_PORT=5672 监听端口    RABBITMQ_LOG_BASE=/data/rabbitmq/log 日志目录
    RABBITMQ_PLUGINS_DIR=/data/rabbitmq/plugins 插件目录
    RABBITMQ_MNESIA_BASE=/data/rabbitmq/mnesia 后端存储目录

```

### RabbitMQ的用户角色分类

none、management、policymaker、monitoring、administrator

### RabbitMQ各类角色描述：

#### none

不能访问 management plugin

#### management

用户可以通过AMQP做的任何事外加： 列出自己可以通过AMQP登入的virtual hosts 查看自己的virtual hosts中的queues,

exchanges 和 bindings 查看和关闭自己的channels 和 connections 查看有关自己的virtual

hosts的“全局”的统计信息，包含其他用户在这些virtual hosts中的活动。

#### policymaker

management可以做的任何事外加： 查看、创建和删除自己的virtual hosts所属的policies和parameters

#### monitoring

management可以做的任何事外加： 列出所有virtual hosts，包括他们不能登录的virtual hosts

查看其他用户的connections和channels 查看节点级别的数据如clustering和memory使用情况 查看真正的关于所有virtual

hosts的全局的统计信息

#### administrator

policymaker和monitoring可以做的任何事外加: 创建和删除virtual hosts 查看、创建和删除users

查看创建和删除permissions 关闭其他用户的connections