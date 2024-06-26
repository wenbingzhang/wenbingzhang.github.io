---
url: /blog/linux/H1xaQL3-N
title: "Centos7+Python2.7下yum安装软件报错解决办法"
date: 2019-01-04T03:42:18+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> yum安装软件报错，但可以下载文件。

## 错误信息

```
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Traceback (most recent call last):
  File "/usr/bin/yum", line 29, in <module>
    yummain.user_main(sys.argv[1:], exit_code=True)
  File "/usr/share/yum-cli/yummain.py", line 365, in user_main
    errcode = main(args)
  File "/usr/share/yum-cli/yummain.py", line 271, in main
    return_code = base.doTransaction()
  File "/usr/share/yum-cli/cli.py", line 773, in doTransaction
    resultobject = self.runTransaction(cb=cb)
  File "/usr/lib/python2.7/site-packages/yum/__init__.py", line 1736, in runTransaction
    if self.fssnap.available and ((self.conf.fssnap_automatic_pre or
  File "/usr/lib/python2.7/site-packages/yum/__init__.py", line 1126, in <lambda>
    fssnap = property(fget=lambda self: self._getFSsnap(),
  File "/usr/lib/python2.7/site-packages/yum/__init__.py", line 1062, in _getFSsnap
    devices=devices)
  File "/usr/lib/python2.7/site-packages/yum/fssnapshots.py", line 158, in __init__
    self._vgnames = _list_vg_names() if self.available else []
  File "/usr/lib/python2.7/site-packages/yum/fssnapshots.py", line 56, in _list_vg_names
    names = lvm.listVgNames()
lvm.LibLVMError: (0, '')

```

## 解决方法

```
mkdir /tmp/down/
yum install --downloadonly --downloaddir=/tmp/down/ yum
cd /tmp/down/
rpm -Uvh *

yum clean metadata
yum clean all

```