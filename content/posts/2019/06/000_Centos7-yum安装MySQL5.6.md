---
url: /blog/linux/yhK4y-gaU
title: "Centos7-yum安装MySQL5.6"
date: 2019-06-27T01:22:50+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> centos自带的repo是不会自动更新每个软件的新版本，所以无法通过yum方式安装MySQL的高版本，所以一般通过社区rpm包安装。

## 安装yum源

```
rpm -Uvh http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm

```

## 查看mysql安装源

```
yum repolist enabled | grep "mysql.*-community.*"

```

## 安装mysql56

```
yum -y install mysql-community-server

```

## 开机启动

```
systemctl enable mysqld

```

## 启动服务

```
systemctl start mysqld

```

## 重置密码

```
mysql_secure_installation

NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MySQL
      SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

In order to log into MySQL to secure it, we'll need the current
password for the root user.  If you've just installed MySQL, and
you haven't set the root password yet, the password will be blank,
so you should just press enter here.

Enter current password for root (enter for none):
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
Enter current password for root (enter for none):
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
Enter current password for root (enter for none):
OK, successfully used password, moving on...

Setting the root password ensures that nobody can log into the MySQL
root user without the proper authorisation.

Set root password? [Y/n] y
New password:
Re-enter new password:
Password updated successfully!
Reloading privilege tables..
 ... Success!

By default, a MySQL installation has an anonymous user, allowing anyone
to log into MySQL without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.

Remove anonymous users? [Y/n] Y
 ... Success!

Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.

Disallow root login remotely? [Y/n] n
 ... skipping.

By default, MySQL comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.

Remove test database and access to it? [Y/n] n
 ... skipping.

Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.

Reload privilege tables now? [Y/n] Y
 ... Success!

All done!  If you've completed all of the above steps, your MySQL
installation should now be secure.

Thanks for using MySQL!

Cleaning up...

```