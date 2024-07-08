---
url: /blog/linux/HJi_UUE5ICG
title: "linux bash截取字符串的几种方法"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> # 号截取，删除左边字符，保留右边字符

var=http://www.aaa.com/123.htm

echo ${var#*//}

其中var是变量名，…

### \# 号截取，删除左边字符，保留右边字符

```
var=http://www.aaa.com/123.htm
echo ${var#*//}

```

其中var是变量名，#号是运算符， _号是通配符，_//表示从左边开始删除第一个到//处的所有字符即删除http://

结果是 ：www.aaa.com/123.htm

### \#\# 号截取，删除左边字符，保留右边字符

```
var=http://www.aaa.com/123.htm
echo ${var##*/}

```

##*/ 表示从左边开始删除最后（最右边）一个 / 号及左边的所有字符即删除 http://www.aaa.com/

结果是 123.htm

### % 号截取，删除右边字符，保留左边字符

```
var=http://www.aaa.com/123.htm
echo ${var%/*}

```

%/* 表示从右边开始，删除第一个 / 号及右边的字符

结果是：http://www.aaa.com

### %% 号截取，删除右边字符，保留左边字符

```
var=http://www.aaa.com/123.htm
echo ${var%%/*}

```

%%/* 表示从右边开始，删除最后（最左边）一个 / 号及右边的字符

结果是：http:

### : 号截取，从左边第几个字符开始，及字符的个数

```
var=http://www.aaa.com/123.htm
echo ${var:0:5}

```

其中的 0 表示左边第一个字符开始，5 表示字符的总个数。

结果是：http:

### : 号截取，从左边第几个字符开始，一直到结束

```
var=http://www.aaa.com/123.htm
echo ${var:7}

```

其中的 7 表示左边第8个字符开始，一直到结束。

结果是 ：www.aaa.com/123.htm

### : 号截取，从右边第几个字符开始，及字符的个数

```
var=http://www.aaa.com/123.htm
echo ${var:0-7:3}

```

其中的 0-7 表示右边算起第七个字符开始，3 表示字符的个数。

结果是：123

### : 号截取，从右边第几个字符开始，一直到结束

```
var=http://www.aaa.com/123.htm
echo ${var:0-7}

```

表示从右边第七个字符开始，一直到结束。

结果是：123.htm

注：（左边的第一个字符是用 0 表示，右边的第一个字符用 0-1 表示）