---
url: /blog/linux/SJ68UEcUCM
title: "linux openssh 常见问题汇总"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 软件包名

openssh-server openssh-clients

服务名：sshd

服务端配置文件：/etc/ssh/sshd.config 客户端…

## 软件包名

openssh-server openssh-clients

## 服务名：sshd

服务端配置文件：/etc/ssh/sshd.config 客户端配置文件：/etc/ssh/ssh.config

## 启动服务

```
server sshd start

```

## 文件说明

```
~/.ssh/known_hosts #存放访问过的服务器的公钥
~/.ssh/authorized_keys #存放需要验证的客户机的公钥

```

## 常见问题

### 1、ssh访问慢

原因：访问服务器的时候会把服务器的IP地址反向解析为域名，如果无法解析就会导致登陆时很慢。 下面几种方法都可以解决这个问题

1、清空/etc/resolv.conf文件中的nameserver记录 2、在客户机的/etc/hosts文件中添加服务器域名的解析记录

3、修改客户端的/etc/ssh/ssh.config文件 GSSAPLAuthentication no

4、修改服务端的/etc/ssh/sshd.config文件 UserDNS no

## 2、~/.ssh权限

.ssh目录和下面的文件权限，组和其他人不能有w的权限 解决方法：降低第服务端的权限检查

```
vim /etc/ssh/sshd_config
StrictModes no

```

### 3、第一次访问sshserver时不用输入yes

```
ssh -o StrictHostKeyChecking=no username@sshserver
vim /etc/ssh/ssh.config
StrictHostKeyChecking=no

```

## 公钥认证

ssh-keygen -t rsa #指定rsa算法 在~/.ssh/下生产两个文件 id\_rsa用户的私钥 id\_rsa.pub用户的公钥ssh-

copy-id -i ~/.ssh/id\_rsa.pub username@sshserver

## scp使用

scp 用户名@服务器地址:文件 本地路径 scp 本地文件 用户名@服务器地址:目标路径

## sftp使用

sftp 用户名@服务器地址

## tcp\_wrappers访问控制

检查某个服务是否受tcp\_wrappers管理支持

```
ldd $(which sshd)|grep libwrap

```

先检查/etc/hosts.allow然后检查/etc/hosts.deny 如果两个文件都没有匹配的规则，则放行。

```
sshd:all EXCEPT 192.168.0.0/255.255.255.0

```

可以使用all、?、\* 阻挡所有但排除192.168.0.0网段