---
url: /blog/linux/rytGLI49LCf
title: "centos7 修改内核引导顺序"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

## 查看内核

```bash
cat /boot/grub2/grub.cfg |grep menuentry

menuentry 'CentOS Linux (3.10.0-327.36.3.el7.x86_64) 7 (Core)' --class centos --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-327.el7.x86_64-advanced-80b9b662-0a1d-4e84-b07b-c1bf19e72d97' {
menuentry 'CentOS Linux (3.10.0-327.22.2.el7.x86_64) 7 (Core)' --class centos --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-327.el7.x86_64-advanced-80b9b662-0a1d-4e84-b07b-c1bf19e72d97' {
menuentry 'CentOS Linux (3.10.0-327.el7.x86_64) 7 (Core)' --class centos --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-327.el7.x86_64-advanced-80b9b662-0a1d-4e84-b07b-c1bf19e72d97' {
menuentry 'CentOS Linux (0-rescue-7d26c16f128042a684ea474c9e2c240f) 7 (Core)' --class centos --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-0-rescue-7d26c16f128042a684ea474c9e2c240f-advanced-80b9b662-0a1d-4e84-b07b-c1bf19e72d97'

```

## 修改默认

```bash
grub2-set-default "CentOS Linux (3.10.0-327.22.2.el7.x86_64) 7 (Core)"

```

## 查看生效

```bash
grub2-editenv list
saved_entry=CentOS Linux (3.10.0-327.22.2.el7.x86_64) 7 (Core)

```