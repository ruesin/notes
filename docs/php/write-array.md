---
title: PHP把数组写入文件
date: 2014-08-08 12:44:47
categories: PHP
tags: 
- php
- php基础
- php数组
---

项目测试人员反映，线上数据编辑不修改，保存之后数据丢失？！翻查代码后，没有找到问题所在，决定把编辑加载时的数据写入到一个文件中，保存时把提交的数据写入到一个新的文件中，然后进行对比。可能有人会问为什么不直接对比数据库呢？因为测试人员反映的是有时报错。。。我只能把所有的都点一遍进行测试了。好吧，废话不多说，进入正题。

把数据写入txt文件自然是用file\_put\_contents()了，我刚开始是直接取数组$data，然后写入文件，可是写入后才发现，txt里是一堆的ArrayArrayArrayArrayArray。。。

好吧，既然不能直接的把数组作为第二个参数使用，那我就写入字符串得了。  
而写入字符串我想到了两个办法

1、序列化数组  
想到数组转字符串首先想到的肯定是序列化存储，反序列化读取呀。

```
$write = serialize($write);
file_put_contents($_SERVER['DOCUMENT_ROOT']."/test/{$id}_old.txt", $write);
```

2.使用var\_export()将数组转成字符串再保存

var\_export() — 输出或返回一个变量的字符串表示

```
$write = var_export($write, true);
file_put_contents($_SERVER['DOCUMENT_ROOT']."/test/{$id}_old.txt", $write);
```

因为我要直接明了的肉眼对比保存前后的数据差异，所以选择了第二种方式。

另外，看手册上说file\_put\_contents()是可以保存数组的啊，但是为什么我保存数据不对？实在查不到原因。。。
