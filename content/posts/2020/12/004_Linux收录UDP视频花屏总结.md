---
url: /blog/linux/h5sGcU1MR
title: "Linux收录UDP视频花屏总结"
date: 2020-12-16T19:10:08+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> 最近在Linux下使用ffmpeg收录UDP流花屏问题，发现机器有双网卡，添加路由指定网卡收录导致无法收录了。另附一些解决花屏的优化方法。

## 优化内核参数

```bash
cat /etc/sysctl.conf
net.ipv4.conf.default.rp_filter = 0
net.ipv4.conf.all.rp_filter = 0
# 修改默认网络的缓存大小 这个很重要不然
net.core.rmem_max = 50000000
net.core.rmem_default = 50000000

sysctl -p

# 添加以上配置后需要重启系统
reboot

# 不重启的话一定要执行以下命令
for i in /proc/sys/net/ipv4/conf/*/rp_filter ; do echo 0 > "$i";   done

```

## 吐槽

由于博主只修改了上面的 `sysctl.conf` 并且只执行了 `sysctl -p` 所以悲剧了，添加路由之后一直无法收录。

## 20201218更新

刚开始以为是存储和收录走同一网口导致花屏，没想到经过一番抓包分析之后，最后确定是交换机有瓶颈（交换机老旧），是交换机的数据处理不过来导致的丢包。

### cifs(samba)

如果收录文件是存储到cifs的话，一定要在挂载的时候指定 `cache=none` 禁用缓存，不然收录长视频时会导致收录中断。