---
url: /blog/linux/H1z5LL49I0z
title: "RabbitMQ性能优化"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## rabbitmq.config

rabbitmq.config文件时rabbitmq的配置文件，他遵守Erlang配置文件定义。

rabbitmq.config文件位置：

```
Unix $RABBITMQ_HOME/etc/rabbitmq

Windows %APPDATA%\RabbitMQ\

```

例子如下：

```
[
    {mnesia, [{dump_log_write_threshold, 1000}]},
    {rabbit, [{tcp_listeners, [5673]}]}
].

```

## Memory配置和设置

RabbitMQ在使用当前机器的40%以上内存时候，会发出内存警告，并组织RabbitMQ所有连接（producer连接）。直到RabbitMQ将当前数据刷入到硬盘或者消息被客户端消费。

当Erlang的垃圾回收机制运行起来（这是一个非常耗费资源的工作），会消费两倍内存。（默认是80%的内存）。因此需要操作系统支持OS swap和page

file.

注意：在32为架构下，每个进程被限制为2GB。通常64架构系统限制每个进程为256TB，64位windows限制为8TB。就算在64位操作系统下，32位的进程只能用2GB内存。

因此强烈推荐使用64bit Erlang vm和64bit os。

当RabbitMQ不能识别你的系统的时候，你必须对vm\_memory\_high\_watermark进行修改。

当rabbitmq不能识别系统的时候，会设置内存为1024MB。所以rabbitmq实际使用的内存仅仅410MB。

当系统为8GB的时候，我们可以这是vm\_memory\_high\_watermark=3，那么我们实际可以使用的内存为3GB。

配置Memory Threshold文件

默认配置RabbitMQ的vm\_memory\_high\_watermark=0.4

```
[{rabbit, [{vm_memory_high_watermark, 0.4}]}].

```

### 举例说明：

当机器内存为16GB，那么40%，为6.4GB。主要当32系统时候，实际可以使用的内存为2GB，那么实际可以使用的内存为820MB。

当我配置vm\_memory\_high\_watermark=0 我们可以阻止所有消息发送。

注意：这个百分比，最好不要修改。应为Erlang VM回收的时候会占据系统内存的80%。已经达到系统临界区。不要设置超过50%的百分比。

### 配置Page Threshold文件

当内存中的数据达到一定数量后，他需要被page out出来。 默认配置

vm\_memory\_high\_watermark\_paging\_ratio=0.5。也就是vm\_memory\_high\_watermark0.5。假设总内存8GB，0.4的使用内存是3.2。那么当内存叨叨3.20.5=1.6GB时候，系统将会大量置换页面。

因此我们可以将页面置换的百分比调高。设置为0.75

```
[{rabbit, [{vm_memory_high_watermark_paging_ratio, 0.75},
         {vm_memory_high_watermark, 0.4}]}].

```

注意：我们可以将vm\_memory\_high\_watermark\_paging\_ratio设置超过1.0，那么不会发生内存换页的情况，也就是说，当内存超过总内存的40%之后，将会阻止所有producer产生消息。

### 配置命令

```
rabbitmqctl  set_vm_memory_high_watermark 0.4

```

这是内存使用占总内存数的百分比

```
rabbitmqctl set_vm_memory_high_watermark_paging_ratio 0.75

```

设置rabbitmq使用内存达到rabbitmq可用内存百分比，就出发页面交换功能。

```
rabbitmqctl status

```

获得系统配置。

## Disk配置和设置

RabbitMQ会在硬盘空间不够的时候，阻止Producer发送消息。这样可以保证RabbitMQ可以再任何时候，将内存中的数据置换到磁盘中来。通常会将硬盘剩余数据大小设置为机器的总内存大小。

全局流控制会被触发，当可用总硬盘容量已经低于配置信息。broker数据库将会最少10秒检查一下警告是否发出或者清除。

在RabbitMQ启动的后，会打印disk limit限制，但是不能识别的平台就不能显示信息。

注意：当RabbitMQ是集群情况下，当其中有一台机器硬盘不足的时候，所有节点的producer链接都会被阻止。

RabbitMQ会定期价检查总磁盘可用空间的大小。通常时间为10秒每次，当限制快被达到时候，RabbitMQ检查的时候会达到10次/s.

### 配置Disk Free Space Limit

我们可以直接设置硬盘的最小限制。也可以设置相对内存大小的设置。

先设置磁盘1GB限制

```
[{rabbit, [{disk_free_limit, 1000000000}]}].

```

在这时相对于机器总内存

```
[{rabbit, [{disk_free_limit, {mem_relative, 1.0}}]}].

```

## Erlang的Hipe优化

可以设置hipe\_compiles设置。可以看到有20-50%的性能优化。而你只需要付出1分钟左右的延迟启动。

HiPE需要你检查是否编译进入你的Erlang安装环境。Ubuntu，需要安装erlang-base-hipe.默认有些平台不支持。如果Erlang VM

segfaults,请关闭这个选项。

```
[{rabbit, [{hipe_compile, true}]}].

```

参考：http://www.rabbitmq.com/configure.html#configuration-file