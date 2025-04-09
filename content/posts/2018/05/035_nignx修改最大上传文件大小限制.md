---
url: /blog/linux/rykY88V58CG
title: "nignx修改最大上传文件大小限制"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

```bash
location / {
            root   html;
            index  index.html index.htm;
            client_max_body_size    1000m;
  }

```

“client_max_body_size”设置一下上传的最大上限,然后重启nginx即可。