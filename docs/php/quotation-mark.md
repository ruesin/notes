---
title: php中单引号和双引号的区别
date: 2013-12-31 00:00:23
categories: PHP
tags: 
- php
- php基础
---

刚接触php的童鞋在看教程时可能会遇到这个问题，教程上有的时候用单引、有的时候用双引，导致很多朋友分不清单引号和双引号的区别，最后会产生单引等于双引的概念。（我曾经有很长一段时间是这样认为的）

后来听说单引运行速度比双引的快、就开始一直用单引。但具体怎么快一直没深究过。

前段时间又从基础看了一遍买的书、发现了这点，今天在php吧又看到有朋友问，遂写此文与大家共享下，不足之处还望指正。

单引与双引在功能上有明显的区别——双引号字符串支持变量的解析和转义字符。

在解析变量时，解析器会尽可能多地取得“$”后面的字符以组成一个合法的变量名。可以用大括号把变量名括起来，已明确表明一个变量。

```
$name='Ruesin';
echo 'my name is $name';      //结果：my name is $name
echo "my name is $name";      //结果：my name is Ruesin
echo "my name is ${name}";    //结果：my name is Ruesin
echo "my name is {$name}";    //结果：my name is Ruesin
echo "my name is \$name";      //结果：my name is $name
```

如果要在双引号中包含双引号就必须用反斜线进行转义(单引号不转义)

定义简单的字符串时，使用单引号是更加高效的处理方式。使用双引号时，PHP将浪费一些开销处理转义和变量解析。因此没有特别需求应使用单引号。

另外、网上还有好多其他的解释、我在这里就不复制了，想要更深入了解的朋友可以去百度一下。
