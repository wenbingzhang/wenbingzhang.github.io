---
url: /blog/linux/rJwI8UVqL0M
title: "apache 常用配置"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 基于端口的虚拟主机

```
Listen 10.10.10.2:8888
<VirtualHost 10.10.10.2:8888>
DocumentRoot /var/www/bbs
ServerName bbs.zwbing.cn
ErrorLog logs/bbs.zwbing.cn-error_log
CustomLog logs/bbs.zwbing.cn-access_log common
</VirtualHost>

```

## 基于ip的虚拟主机

```
ip address add 10.10.10.20/24 dev eth0
<VirtualHost 10.10.10.2:80>
DocumentRoot /var/www/bbs
ServerName bbs.zwbing.cn
ErrorLog logs/bbs.zwbing.cn-error_log
CustomLog logs/bbs.zwbing.cn-access_log common
</VirtualHost>
<VirtualHost 10.10.10.20:80>
DocumentRoot /var/www/www
ServerName qq.zwbing.cn
ErrorLog logs/www.zwbing.cn-error_log
CustomLog logs/www.zwbing.cn-access_log common
</VirtualHost>

```

## 基于域名的虚拟主机和用户访问控制

```
NameVirtualHost 10.10.10.2:80
<VirtualHost 10.10.10.2:80>
DocumentRoot /var/www/www
ServerName www.zwbing.cn
ErrorLog logs/www.zwbing.cn-error_log
CustomLog logs/www.zwbing.cn-access_log common
</VirtualHost>
<VirtualHost 10.10.10.2:80>
DocumentRoot /var/www/bbs
ServerName bbs.zwbing.cn
ErrorLog logs/bbs.zwbing.cn-error_log
CustomLog logs/bbs.zwbing.cn-access_log common
<Directory "/var/www/bbs">
Order allow,deny
Allow from all
AuthName "Please enter the account password!!"
AuthType Basic
AuthUserFile /etc/httpd/.passwd
require user zhwb
</Directory>
</VirtualHost>
Order allow,deny
Allow from all(10.10.10 10.10.10.0/24 10.10.10.3)
Deny from all
Allow 表示允许访问的网段或ip Deny 表示拒绝访问的网段或ip
Allow 和 Deny 同时存在时看 Order 这句 ，如果Allow在后表示允许，反之Deny在后表示拒绝（同时存在）
alias /bbs /var/www/bbs #设置虚拟目录
AddDefaultCharset UTF-8 #设置字符集
DirectoryIndex index.html index.html.var #添加索引

```

## httpd命令

-v：查看版本

-M：查看模块

-t：检查httpd.conf语法

-S：查看虚拟主机信息

### Options指令详解

Options指令详解

Options指令的完整语法为：Options \[+\|-\]option \[\[+\|-\]option\]

…。简而言之，Options指令后可以附加指定多种服务器特性，特性选项之间以空格分隔。下面我们来看看Options指令后可以附加的特性选项的具体作用及含义(Apache配置中的内容均不区分大小写)：

All

表示除MultiViews之外的所有特性。这也是Options指令的默认设置。

None

表示不启用任何的服务器特性。

FollowSymLinks

服务器允许在此目录中使用符号连接。如果该配置选项位于配置段中，将会被忽略。

Indexes

如果输入的网址对应服务器上的一个文件目录，而此目录中又没有DirectoryIndex指令(例如：DirectoryIndex index.html

index.php)，那么服务器会返回由mod\_autoindex模块生成的一个格式化后的目录列表，并列出该目录下的所有文件(如下图)。

Options Indexes指令作用效果

Options Indexes指令作用效果

MultiViews

允许使用mod\_negotiation模块提供内容协商的”多重视图”。简而言之，如果客户端请求的路径可能对应多种类型的文件，那么服务器将根据客户端请求的具体情况自动选择一个最匹配客户端要求的文件。例如，在服务器站点的file文件夹下中存在名为hello.jpg和hello.html的两个文件，此时用户输入Http://localhost/file/hello，如果在file文件夹下并没有hello子目录，那么服务器将会尝试在file文件夹下查找形如hello.\*的文件，然后根据用户请求的具体情况返回最匹配要求的hello.jpg或者hello.html。

SymLinksIfOwnerMatch

服务器仅在符号连接与目标文件或目录的所有者具有相同的用户ID时才使用它。简而言之，只有当符号连接和符号连接指向的目标文件或目录的所有者是同一用户时，才会使用符号连接。如果该配置选项位于配置段中，将会被忽略。

ExecCGI

允许使用mod\_cgi模块执行CGI脚本。

Includes

允许使用mod\_include模块提供的服务器端包含功能。

IncludesNOEXEC

允许服务器端包含，但禁用”#exec cmd”和”#exec cgi”。但仍可以从ScriptAlias目录使用”#include

virtual”虚拟CGI脚本。

此外，比较细心的读者应该注意到，Options指令语法允许在配置选项前加上符号”+”或者”-”，那么这到底是什么意思呢。

实际上，Apache允许在一个目录配置中设置多个Options指令。不过，一般来说，如果一个目录被多次设置了Options，则指定特性数量最多的一个Options指令会被完全接受(其它的被忽略)，而各个Options指令之间并不会合并。但是如果我们在可选配置项前加上了符号”+”或”-”，那么表示该可选项将会被合并。所有前面加有”+”号的可选项将强制覆盖当前的可选项设置，而所有前面有”-”号的可选项将强制从当前可选项设置中去除。你可以参考下面的例子：

## \#示例1

```
<Directory /web/file>
Options Indexes FollowSymLinks
</Directory>
<Directory /web/file/image>
Options Includes
</Directory>
#目录/web/file/image只会被设置Includes特性
#示例2
<Directory /web/file>
Options Indexes FollowSymLinks
</Directory>
<Directory /web/file/image>
Options +Includes -Indexes
</Directory>
#目录/web/file/image将会被设置Includes、FollowSymLinks两种特性

```