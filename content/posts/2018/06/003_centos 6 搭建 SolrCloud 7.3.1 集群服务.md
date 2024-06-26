---
url: /blog/linux/S1cZ9qilm
title: "centos 6 搭建 SolrCloud 7.3.1 集群服务"
date: 2018-06-11T07:10:59+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> Solr是一个独立的企业级搜索应用服务器，它对外提供类似于Web-service的API接口。用户可以通过http请求，向搜索引擎服务器提交一定格式的XML文件，生成索引；也可以通过Http Get操作提出查找请求，并得到XML格式的返回结果。

## 环境

需要用到的软件有：JDK、ZooKeeper、Solr

2台机器：10.1.201.49、10.1.201.50

## 配置JDK

```
cat << EOF >> /etc/profile
## jdk ##
JAVA_HOME=/usr/local/java/jdk
CLASSPATH=$JAVA_HOME/lib/
PATH=$PATH:$JAVA_HOME/bin
export PATH JAVA_HOME CLASSPATH
EOF

```

## 配置ZooKeeper

```
cd zookeeper/conf
cp zoo_sample.cfg zoo.cfg
mkdir -p /data/solr/zookeeper
#10.1.201.49
echo 1 > /data/solr/zookeeper/myid
#10.1.201.50
echo 2 > /data/solr/zookeeper/myid

 cat zoo.cfg
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.
dataDir=/data/solr/zookeeper
# the port at which the clients will connect
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1
server.1 = 10.1.201.49:2888:3888
server.2 = 10.1.201.50:2888:3888

cd zookeeper/bin
./zkServer.sh start

```

## 部署solr

```
unzip solr-7.3.1.zip

```

### 安装solr

```
# -d 指定数据目录 -n 安装后不启动服务
solr-7.3.1/bin/install_solr_service.sh solr-7.3.1.zip -n -d /data/solr/

```

### 修改配置

```
cat /etc/default/solr.in.sh | grep -v "#"

SOLR_JAVA_MEM="-Xms4g -Xmx4g"

GC_LOG_OPTS="-verbose:gc -XX:+PrintHeapAtGC -XX:+PrintGCDetails \
  -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+PrintTenuringDistribution -XX:+PrintGCApplicationStoppedTime"

ZK_HOST="10.1.201.49:2181,10.1.201.50:2181"

SOLR_HOST="10.1.201.49"

SOLR_TIMEZONE="UTC+8"

SOLR_PID_DIR="/data/solr"
SOLR_HOME="/data/solr/data"
LOG4J_PROPS="/data/solr/log4j.properties"
SOLR_LOGS_DIR="/data/solr/logs"
SOLR_PORT="8983"

vim /data/solr/data/solr.xml

#10.1.201.49
<str name="host">${host:10.1.201.49}</str>
#10.1.201.50
<str name="host">${host:10.1.201.50}</str>

```

### 启动solr

```
/etc/init.d/solr start #service solr start OR systemctl start solr

```

## 测试

### 创建合集

```
# -c 指定库(collection)名称 -shards 指定分片数量,可简写为 -s ,索引数据会分布在这些分片上 -replicationFactor 每个分片的副本数量,每个碎片由至少1个物理副本组成
/opt/solr/bin/solr create_collection -c test_collection -shards 2 -replicationFactor 2 -force

```

### 查看状态

```
/opt/solr/bin/solr status

```

### 删除合集

```
 /opt/solr/bin/solr delete -c test_collection

```

## 备注

所有没有标明注释在那台机器上执行的，都是在每台机器上都要执行。

如果遇到问题可以给我留言或者直接联系我。