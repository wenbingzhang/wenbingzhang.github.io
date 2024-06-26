---
url: /blog/linux/HkiLUE5UCf
title: "linux dns（named）最小配置"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 一、简介

相对于存储和大数据领域，CDN是一个相对小的领域，但行行出状元，BIND就是CDN领域的蝉联N届的状元郎。BIND是一款非常常用的DNS开源服务器，全球有90%的DNS用BIND实现。值得一提的是，BIND9.8.1用C语言实现，代码量巨大，其设计实现几乎涵盖了服务器编程的所有细节。

本文简要介绍一下BIND9.8.1最简单配置，其中穿插介绍BIND中的最基本概念，不涉及BIND的安装部署，不涉及BIND架构等话题。

## 二、Zone和资源记录

介绍最简配置前需要明确两个配置中的概念：zone和RR。

BIND的配置文件描述了一个域名服务器的所有属性，这些属性BIND的行为和功能。其中的zone文件描述了域名服务器中包含的主机，所提供的服务类型等信息，BIND通过将zone文件中的信息加载到内存数据结构中并有效组织起来，然后对外部的DNS请求提供验证和查询请求。需要注意的是，zone文件的格式不是由BIND制定的，而是DNS标准文档制定的（见RFC1035）。

通常情况下，一个zone文件描述该DNS服务器服务的一个授权服务器域。例如我有一个DNS服务器可以解析taobao.com的域名和baidu.com的域名，那么我的DNS服务器的配置文件中就可以设置两个zone标签，一个描述taobao.com的域名信息，另一个描述baidu.com的域名信息。

资源记录resource

Record记录了一个域(domain)的属性和特性，注意，属性是指共有的特征，特性指特有的特征。例如中国特色社会主义就是一个特性。

## 三，named.conf文件配置

named.conf是BIND的唯一的主配置文件，当然你也可以自己编写主配置文件，但是需要在BIND主进程named启动的时候用-

c选项指定主配置文件的路径。named.conf由一个个子句组成，每个子句都有一个头跟一对大括号组成，大括号里面是该子句中的因子和值（具体见下面的例子）。

下面的代码是named.conf的一个最简配置。其中假设named.conf只负责解析授权域名cobb.com。 其中的key是由rndc-

confgen生成的。

```
key "rndc-key" {
 algorithm hmac-md5;
 secret "eoiWMiCwCYPwNLWxl05rNw==";
 };

 controls {
 inet 127.0.0.1 port 953
 allow { 127.0.0.1; }
 keys { "rndc-key"; };
 };

 options {
 //域名文件存放的绝对路径
 directory "/usr/local/named/var";
 //如果bind启动，自动会在/usr/local/named/var目录生成一个named.pid文件，打开文件就是named进程的ID
 pid-file "named.pid";
 };

 zone "." IN {
 //根域名服务器
 type hint;
 //存放在//usr/local/named/var目录，文件名为named.root
 file "named.root";
 };

 //域cobb.com的zone文件
 zone "cobb.com" IN {
 type master; //该域名服务器是主域名服务器，这个选项主要用在主备部署中
 file "cobb.com.zone"; //解析域名cobb.com的zone文件内容，其路径由options中的directory指定
 allow-update { none; }; //定义了允许向主zone文件发送动态更新的匹配列表

 };

 //反向解析
 zone "1.168.192.in-addr.arpa" in {
 type master;
 //存放反向解析的文件
 file "cobb.com.rev";
 allow-update { none; };
 };

```

上面的代码中，controls子句定义了服务器的控制通道的一些信息，控制通道是named为外部提供的管理named服务器的接口。通常情况下named都在本机的953端口上监听控制信息；allow表示允许本机上的rndc控制程序控制named服务器，allow出了指定ip地址外，还可以指定acl中的用户地址；keys表示rndc控制named时需要携带的密钥

，这个密钥由rndc-gen生成，并在named.conf中包含。

接下来的options选项中包含一些全局状态描述，这些描述信息在所有的zone文件和view中可见（view后面的系列博客会介绍），但如果zone文件或view中重新定义这些描述信息，则options中的信息被覆盖

。上面例子中的directory和pid-file的含义见代码注释。

## 四、zone文件配置

文件cobb.com.zone文件位于/usr/local/named/var中，其内容如下所示：

```
$TTL 86400
$ORIGIN cobb.com.
@       IN  SOA ns1 root(
            2013031901      ;serial
            12h     ;refresh
            7200        ;retry
            604800      ;expire
            86400       ;mininum
            )
            NS  ns1.cobb.com.
            NS  ns2.cobb.net.
            MX  10  mail.cobb.com.
ns1     IN  A   192.168.10.1
www     IN  A   192.168.10.10
        IN  A   192.168.10.11
mail        IN  A   192.168.10.20
ljx     IN  A   192.168.10.30
ftp     IN  CNAME   ljx

```

上面的配置表示：

1）该zone有两个域名服务器，一个是ns1.cobb.com，ip地址是192.168.10.1，另一个是ns2.cobb.net(它不在本域内)；

2）该zone有一个邮件服务器，域名是mail.cobb.com，IP地址是192.168.10.20；

3）该zone有两个对外服务的万维网服务器，其域名是www.cobb.com，IP地址是192.168.10.10和192.168.10.11；

4）该zone有一个对外服务的ftp服务器，其域名是ftp.cobb.com，IP地址是192.168.10.30；

5）该zone有一个主机，其域名是ljx.cobb.com，IP地址也是192.168.10.30； 其中TTL和ORIGIN等标签在BIND中叫做指令。

zone文件中的所有指令都以一个$开始，指令主要用来表示zone文件中的一些控制信息。

$TTL指令表示一个资源记录在其他DNS服务器中（这个DNS服务器是请求本BIND的服务器，一般情况下是local

dns）的缓存时间，在这个缓存时间内，local dns（暂且先这么认为，好举例）不会再请求BIND，而是直接返回域名对应的IP地址。

$ORIGIN指令表示该zone文件用来描述的域(domain)名称。 SOA(start of

authority)资源记录：它定义了一个域的全局特性，必须是出现在zone文件中的第一个资源记录，而且一个zone文件中必须只有一个SOA资源记录。其中SOA后面的ns1与root分别是域名服务器和管理员邮箱(root@cobb.com)，其全写分别是ns1.cobb.com.和root.cobb.com，因为$ORIGIN指明了域名，所以这个地方可以略去。

NS(name

server)资源记录：它定义了为本域(domain)(这个例子中是cobb.com)服务的域名服务器。需要注意的是外部域名服务器（例子中的ns2）必须为zone

cobb.com包含一个zone文件。

MX(mail exchanger)资源记录：它定义了本域中的邮件服务器。这个资源记录是可选的，因为一个域中不一定有邮件服务器。

A(Address)资源记录：这是个很关键的记录。它定义了zone文件中提到的主机或服务的IPv4地址（IPv6地址叫AAAA记录），而且这些IPv4地址必须是外部可见的。例如万维网服务器

www.cobb.com的IPv4地址是192.168.10.10。

CNAME记录：是一个已经定义了IPv4地址的主机的别名记录。通常用来为已经存在的主机分配一个或多个服务。示例中的主机ljx.cobb.com既做主机又提供ftp服务。从上面的分析可以看出，我们也可以不用CNAME，只需要为不同的服务指定相同的IP地址即可。

但是实际上两种情况下必须用CNAME记录：

1）真是主机或别名主机在不同的域中，我们不知道外部域中的IP地址，所以必须要用CNAME，例如ftp.cobb.com是ftp.cobb.net的一个别名，但是在域cobb.com中无法知道ftp.cobb.net的IP地址，只能用CNAME记录；

2）用户希望访问一个站点时用cobb.com产生www.cobb.com的效果，这时我们需要有如下的CNAME定义：

```
; 定义一个解析cobb.com的IP地址
        IN     A       cobb.com
; 为www.cobb.com建立别名cobb.com
www     IN      A       cobb.com.

当然，上面介绍的只是一个最小配置，但是已经包含了大部分情况下我们需要配置的选项。更多的配置选项请参见：http://www.zytrax.com/books/dns/ch7/view.html

```

## 五 参考文献

1，《Pro\_DNS\_and\_BIND》

2，http://www.zytrax.com/books/dns/ch7/view.html

3，http://www.cnblogs.com/cobbliu/archive/2013/03/19/2970311.html 原文地址：直达