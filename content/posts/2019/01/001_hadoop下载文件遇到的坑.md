---
url: /blog/linux/S1wDPAKf4
title: "hadoop下载文件遇到的坑"
date: 2019-01-14T09:38:20+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> hadoop fs -get 下载带特殊字符文件失败的一些解决方法。

## 错误范例

```
hadoop fs  -get  "/xxx/xxx分类/动漫Y/2005/蓝猫淘气3000问 航天系列（太空历险记）/第363集 协议.ts" "/media/bak/媒资源素材分类/动漫Y/2005/蓝猫淘气3000问 航天系列（太空历险记）/第363集 协议.ts"

```

运行以上命令就报“unexpexted URISyntaxException”

## 解决方法

```
hadoop fs  -get  "/xxx/xxx分类/动漫Y/2005/蓝猫淘气3000问 航天系列（太空历险记）/第363集 协议.ts" "%2Fmedia%2Fbak%2F%E5%AA%92%E8%B5%84%E6%BA%90%E7%B4%A0%E6%9D%90%E5%88%86%E7%B1%BB%2F%E5%8A%A8%E6%BC%ABY%2F2005%2F%E8%93%9D%E7%8C%AB%E6%B7%98%E6%B0%943000%E9%97%AE%20%E8%88%AA%E5%A4%A9%E7%B3%BB%E5%88%97%EF%BC%88%E5%A4%AA%E7%A9%BA%E5%8E%86%E9%99%A9%E8%AE%B0%EF%BC%89%2F%E7%AC%AC363%E9%9B%86%20%E5%8D%8F%E8%AE%AE.ts"

```

将写到本地的路径进行url编码，然后神奇的就下载成功了，然后路径也是没有编码的绝对路径。