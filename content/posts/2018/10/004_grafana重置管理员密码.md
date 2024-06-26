---
url: /blog/linux/SJWuUJwsQ
title: "grafana重置管理员密码"
date: 2018-10-19T05:13:46+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> Grafana是一个可视化面板（Dashboard），有着非常漂亮的图表和布局展示，功能齐全的度量仪表盘和图形编辑器，支持Graphite、zabbix、InfluxDB、Prometheus和OpenTSDB作为数据源。Grafana主要特性：灵活丰富的图形化选项；可以混合多种风格；支持白天和夜间模式；多个数据源。

要显示所有管理员命令： grafana-cli admin

## 重置密码

### 第一种方法

您可以使用CLI重置admin用户的密码。丢失管理员密码时，此命令的用例是。

```
grafana-cli admin reset-admin-password newpass

```

如果运行该命令则返回此错误：

无法找到配置默认值，请确保已设置homepath命令行参数或工作目录为homepath

然后有两个标志可用于设置homepath和配置文件路径。

```
grafana-cli admin reset-admin-password --homepath "/usr/share/grafana" newpass

```

如果您没有丢失管理员密码，那么最好在Grafana UI中进行设置。如果需要在脚本中设置密码，则可以使用Grafana

API。以下是使用curl和基本身份验证的示例：

```
curl -X PUT -H "Content-Type: application/json" -d '{
  "oldPassword": "admin",
  "newPassword": "newpass",
  "confirmNew": "newpass"
}' http://admin:admin@<your_grafana_host>:3000/api/user/password

```

### 第二种方法

```
# sqlite3 /var/lib/grafana/grafana.db
> update user set password = '59acf18b94d7eb0694c61e60ce44c110c7a683ac6a8f09580d626f90f4a242000746579358d77dd9e570e83fa24faa88a8a6', salt = 'F3FAxVm33R' where login = 'admin';
> .exit

```

PS: 用户:admin 密码：admin

## 重启服务

```
/etc/init.d/grafana-server restart

```