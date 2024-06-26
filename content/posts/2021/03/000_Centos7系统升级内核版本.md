---
url: /blog/linux/G0DCCusMR
title: "Centos7系统升级内核版本"
date: 2021-03-02T17:52:33+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 使用ELRepo仓库升级系统内核

## 查看内核版本

```bash
uname -r

uname -a

cat /etc/redhat-release

```

## 安装ELRepo yum源

```bash
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm

```

## 查看可用的内核版本

```bash
yum --disablerepo="*" --enablerepo="elrepo-kernel" list available

...
kernel-lt.x86_64              4.4.155-1.el7.elrepo
kernel-lt-devel.x86_64        4.4.155-1.el7.elrepo
...

```

## 安装稳定版本内核

```bash
yum --enablerepo=elrepo-kernel install kernel-lt

```

## 设置引导（grub2）

### 查看所有内核版本

```bash
sudo awk -F\' '$1=="menuentry " {print i++ " : " $2}' /etc/grub2.cfg

0 : CentOS Linux (4.4.241-1.el7.elrepo.x86_64) 7 (Core)
1 : CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)
2 : CentOS Linux (0-rescue-651e1b90bb3149809cdeb8cc80e72c43) 7 (Core)

```

### 设置新的默认引导的内核版本

方法1

```bash
grub2-set-default 0 #其中 0 是上面查询出来的可用内核

```

方法2

```bash
vim /etc/default/grub

GRUB_DEFAULT=0 #其中 0 是上面查询出来的可用内核

```

```bash
grub2-mkconfig -o /boot/grub2/grub.cfg #生成 grub 配置文件

reboot # 重启机器

```

## 验证及删除旧内核（可选）

```bash
uname -r  # 查看内核版本

4.4.241-1.el7.elrepo.x86_64

```

```bash
yum install yum-utils
package-cleanup --oldkernels # 删除旧的内核版本

# 也可以使用 rpm -qa | grep kernel 先把所有的内核版本查询出来，然后使用 yum remove 删除掉旧的内核版本

```

## 升级失败的处理方法

如果发现升级内核版本并重启，发现机器无法启动，需要在开机进入引导内核选择界面手动选择老的内核启动，然后再讲默认引导的内核版本改回来的内核版本进行回滚。