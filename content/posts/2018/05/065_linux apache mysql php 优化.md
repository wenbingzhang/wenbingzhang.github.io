---
url: /blog/linux/SkaWUIN5U0z
title: "linux apache mysql php 优化"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> none

## 一、准备环境

### 1、安装mysql

```
#cmake -DCMAKE_INSTALL_PREFIX=/usr/local/mysql5.5 -DMYSQL_DATADIR=/usr/local/mysql5.5/data -DSYSCONFDIR=/usr/local/mysql5.5/etc -DWITH_INNOBASE_STORAGE_ENGINE=1 -DWITH_ARCHIVE_STORAGE_ENGINE=1 -DWITH_PERFSCHEMA_STORAGE_ENGINE=1 -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DENABLED_LOCAL_INFILE=1 -DWITH_EXTRA_CHARSETS=all
#make
#make install

```

### 2、安装nginx

```
#./configure --prefix=/usr/local/nginx --http-log-path=/var/log/nginx/access.log --error-log-path=/var/log/nginx/error.log --pid-path=/var/run/nginx/nginx.pid --user=daemon --group=daemon --with-pcre
#make && make install

```

### 3、安装php

```
#./configure --prefix=/usr/local/php5 --enable-bcmath --with-mysql=/usr/local/mysql5.5 --enable-fpm --with-fpm-user=daemon --with-fpm-group=daemon --with-config-file-path=/usr/local/php5
#make && make install

```

### 4、使nginx支持php

#### (1)nginx配置

```
location ~ \.php$ {
root html;
fastcgi_pass 127.0.0.1:9000;
fastcgi_index index.php;
fastcgi_param SCRIPT_FILENAME /usr/local/nginx/html$fastcgi_script_name;
include fastcgi_params;
}

```

#### (2)php配置

```
#vim /usr/local/php5/etc/php-fpm.conf
#cd /usr/local/php5/sbin
#./php-fpm -c /usr/local/php5/etc/php-fpm.conf

```

## 二、php优化

注意：如何添加php功能模块 例：安装mbstring多字节支持功能模块

```
#cd /usr/src/lamp/php-5.3.10/ext \\进入要安装功能模块源码目录下
#/usr/local/php5/bin/phpize \\运行phpize命令，生成configure文件
#./configure --enable-mbstring --with-php-config=/usr/local/php5/bin/php-config
#make
#make install

```

#vim php.ini

```
extension_dir = "/usr/local/php5/lib/php/extensions/no-debug-non-zts-20090626"
extension = mbstring.so

```

### 1、php加速处理

#### (1)对php相关选项进行调整 \#vim php.ini

```
realpath_cache_size = 32k
realpath_cache_ttl = 600000
max_excution_time = 60
max_input_time = 120
memory_limit = 128M
display_errors = Off

```

#### (2)安装xcache

```
#tar xzvf xcache-2.0.0-rc1.tar.gz
#cd xcache-2.0.0-rc1
#/usr/local/php5/bin/phpize
#./configure --enable-xcache --enable-xcache-constant --with-php-config=/usr/local/php5/bin/php-config
#make
#make install

```

#vim php.ini

```
extension_dir = "/usr/local/php5/lib/php/extensions/no-debug-non-zts-20090626"
extension = xcache.so
[xcache]
xcache.shm_scheme = "mmap"
xcache.size = 16M
xcache.count = 1
xcache.slots = 8K
xcache.ttl = 0
xcache.gc_interval = 0
xcache.var_size = 4M
xcache.var_count = 1
xcache.var_slots = 8K
xcache.var_ttl = 0
xcache.var_maxttl = 0
xcache.var_gc_interval = 300
xcache.readonly_protection = Off
xcache.mmap_path = "/dev/zero"
xcache.coredump_directory = ""
xcache.cacher = On
xcache.stat = On
xcache.optimizer = Off
xcache.test = Off
xcache.experimental = Off
[xcache.coverager]
xcache.coverager = Off
xcache.coveragedump_directory = ""

```

## 三、mysql优化

### 1、查询优化

```
query-cache-size = 16M
query-cache-type = on | off
query-cache-limit = 2M

mysql>show status like 'qcache%';

```

Qcache_queries_in_cache 目前mysql缓存的数目

Qcache_inserts 插入的缓存条目数 Qcache_hits 缓存命中率

Qcache_lowmem_prunes 有多少次出现缓存过低

Qcache_free_blocks 缓存碎片数量

### 2、排序优化

```
sort_buffer_size = 8M 设定排序缓冲区大小
max_sort_length = 8192 设定排序队列长度大小

mysql>show status like '%sort%';

```

Sort_merge_passes 表示排序算法已经完成的排序数量

Sort_range 表示在指定范围内的排序

Sort_rows 表示已经排序了多少行

Sort_scan 通过扫描完成的排序数量

### 3、索引优化

key_buffer_size 设置索引缓冲区大小 自定义索引缓冲区和载入索引

```
mysql>set global stu.key_buffer_size=8388608; 设置自定义缓冲区
mysql>load index into cache test.stu; 将索引载入到系统缓冲区
mysql>cache index test.stu in stu; 将索引加载到自定义缓冲区

```

### 4、mysql性能优化

concurrent_insert 是否允许数据并发插入，只对myisam引擎 thread_concurrency 定义并发线程数量

innodb_flush_log_log_trx_commit 设置日志写入文件的方式 innodb_buffer_pool_size

定义缓冲区大小，一般设为内存的80-85%

innodb_buffer_pool_instance 定义高速缓冲区可并发操作的实例数量 innodb_open_files 定义可打开的文件数

### 5、其它的重点优化参数

```
max_connections = 1024 设置数据库允许的最大连接数
max_connect_errors = 32 表示允许的错误连接数
innodb_log_file_size = 512M 设置日志文件大小
innodb_max_dirty_pages_pct=80 设定写入磁盘的脏数据占用的缓冲区比例

```