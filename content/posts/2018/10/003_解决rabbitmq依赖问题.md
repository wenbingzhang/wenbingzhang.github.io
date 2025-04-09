---
url: /blog/linux/HJJ4wWwim
title: "解决rabbitmq依赖问题"
date: 2018-10-19T07:30:49+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

## 错误提示

```bash
warning: rabbitmq-server-3.6.6-1.el6.noarch.rpm: Header V4 RSA/SHA1 Signature, key ID 6026dfca: NOKEYerror: Failed dependencies:
    erlang >= R16B-03 is needed by rabbitmq-server-3.6.6-1.el6.noarch
    socat is needed by rabbitmq-server-3.6.6-1.el6.noarch

```

## 解决方法

```bash
cd /etc/yum.repos.d/
cat erlang.repo
[erlang-solutions]
name=Centos $releasever - $basearch - Erlang Solutions
baseurl=http://packages.erlang-solutions.com/rpm/centos/$releasever/$basearch
gpgcheck=0
gpgkey=http://packages.erlang-solutions.com/debian/erlang_solutions.asc
enabled=1

```

然后再安装rabbitmq

```bash
yum localinstall rabbitmq-server-3.6.6-1.el6.noarch.rpm

```

## 其他问题

```bash
# /etc/init.d/rabbitmq-server start
Starting rabbitmq-server: FAILED - check /var/log/rabbitmq/startup_{log, _err}
rabbitmq-server.
# vim /var/log/rabbitmq/startup_err
init terminating in do_boot (noproc)

Crash dump is being written to: erl_crash.dump...done

```

如果出现以上问题，说明erlang和rabbitmq的版本不相符。只能重新安装erlang了。