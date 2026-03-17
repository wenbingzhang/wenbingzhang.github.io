---
slug: dxBNBEtayRGTPNXCC2u6Xn
title: Keepalived配置方法
description:
categories:
  - default
tags:
  - default
date: 2026-03-17 14:57:01+08:00
menu: main
---

# Keepalived 配置方法

## 一、VRRP Script 检测脚本配置

### 1. 基础配置

```bash
vrrp_script check_service {
    script       "/usr/local/bin/check_service.sh"  # 检测脚本路径（必填）
    interval      3                                  # 检测间隔，单位：秒
    timeout       2                                  # 脚本超时时间，单位：秒
    weight        -20                                # 权重变化值，负数表示失败时降低优先级
    fall          2                                  # 连续失败次数，达到此值转为DOWN状态
    rise          1                                  # 连续成功次数，达到此值转为UP状态
}

vrrp_instance VI_1 {
    state MASTER                    # 实例状态：MASTER（主）或 BACKUP（备）
    interface eth0                  # 绑定VIP的网卡接口名称
    virtual_router_id 51            # 虚拟路由ID，同一组Keepalived必须相同（0-255）
    priority 100                   # 优先级，MASTER应高于BACKUP（1-255）
    advert_int 1                    # VRRP广告间隔，单位：秒

    # 引用检测脚本
    track_script {
        check_service weight -20   # 执行检测脚本，weight表示权重变化值
    }

    # 虚拟IP（VIP）配置
    virtual_ipaddress {
        192.168.1.100              # VIP地址，可配置多个
    }
}
```

## 二、检测脚本示例

```bash
#!/bin/bash
# 检测服务状态的脚本
# 返回 0 表示成功，服务正常
# 返回 非0 表示失败，服务异常

SERVICE_NAME="nginx"

# 方法1：使用systemctl检查服务状态
if systemctl is-active --quiet "$SERVICE_NAME"; then
    exit 0
else
    exit 1
fi

# 方法2：检查端口是否监听（以80端口为例）
# nc -z 127.0.0.1 80 || exit 1

# 方法3：检查进程是否存在（以nginx为例）
# pgrep -x nginx > /dev/null || exit 1

# 方法4：HTTP健康检查（适用于Web服务）
# curl -sf http://127.0.0.1/health > /dev/null || exit 1
```

**脚本权限设置：**
```bash
chmod +x /usr/local/bin/check_service.sh
```

## 三、多脚本检测配置

```bash
# 检测多个不同的服务

vrrp_script check_nginx {
    script       "/usr/local/bin/check_nginx.sh"
    interval     3
    weight       -10
}

vrrp_script check_mysql {
    script       "/usr/local/bin/check_mysql.sh"
    interval     5
    weight       -10
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1

    track_script {
        check_nginx                  # 引用nginx检测脚本
        check_mysql                  # 引用mysql检测脚本
    }

    virtual_ipaddress {
        192.168.1.100
    }
}
```

## 四、完整配置示例

```bash
# 全局配置
global_defs {
    router_id LVS_01                 # 路由器标识，名称唯一
}

# 检测脚本定义
vrrp_script check_nginx {
    script       "/usr/local/bin/check_nginx.sh"
    interval      3
    timeout       2
    weight        -20
    fall          2
    rise          1
}

# VRRP实例配置（MASTER节点）
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1

    # 认证配置（推荐设置）
    authentication {
        auth_type PASS              # 认证方式：PASS（简单密码）或 AH
        auth_pass 1234              # 认证密码（仅前8位有效）
    }

    # 引用检测脚本
    track_script {
        check_nginx weight -20
    }

    # 虚拟IP配置
    virtual_ipaddress {
        192.168.1.100
        # 192.168.1.101  # 可配置多个VIP
    }

    # 通知脚本（可选）
    notify_master "/usr/local/bin/notify_master.sh"   # 转为MASTER时执行
    notify_backup "/usr/local/bin/notify_backup.sh"   # 转为BACKUP时执行
    notify_fault  "/usr/local/bin/notify_fault.sh"    # 故障时执行
}
```

## 五、注意事项

1. **脚本权限**：检测脚本必须具有执行权限
2. **返回值**：脚本返回 `0` 表示成功，非 `0` 表示失败
3. **权重机制**：`weight` 为负值时，检测失败会降低优先级；为正值时相反
4. **网络隔离**：确保VRRP通信端口（UDP 112）不被防火墙阻止
5. **虚拟路由ID**：同一组Keepalived集群必须使用相同的 `virtual_router_id`
6. **优先级**：MASTER的优先级必须高于BACKUP，才能正常切换