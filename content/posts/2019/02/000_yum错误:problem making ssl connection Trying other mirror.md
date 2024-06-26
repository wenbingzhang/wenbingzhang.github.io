---
url: /blog/linux/rk-lmMGL4
title: "yum错误:problem making ssl connection Trying other mirror"
date: 2019-02-26T01:20:26+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> yum无法使用带https的源

## 环境

```
yum install epel-release

```

运行以上命令之后，安装其他软件就报错。

## 错误提示

```
[Errno 14] problem making ssl connection Trying other mirror.
Trying other mirror
Error: Cannot retrieve repository metadata (repomd.xml) for repository: xxxx. Please verify its path and try again

```

经过google查询，发现似乎是ssl证书的原因。

## 解决方法1

```
# cd /etc/yum.repos.d/
# ls
CentOS6-Base-163.repo  epel.repo（修改他）  epel-testing.repo
# pwd
/etc/yum.repos.d
# vim /etc/yum.repos.d/epel.repo
[epel]
name=Extra Packages for Enterprise Linux 6 - $basearch
baseurl=http://download.fedoraproject.org/pub/epel/6/$basearch
#mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-6&arch=$basearch
failovermethod=priority
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6

```

把baseurl注释去掉，给mirrorlist加上注释。然后将enabeld=1变为0，禁用ssl证书验证。

## 解决方法2

```
yum install ca-certificates
yum update curl

```

将enable设置为1即可