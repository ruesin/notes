---
title: 浅谈PHP格式化html函数htmlentities及与htmlspecialchars的区别
date: 2014-03-22 10:39:50
categories: PHP
tags: 
- php
- php格式化函数
- php函数
---

昨天汉化了一个wordpress的广告插件，本以为完事大吉了，没想到使用的时候出现了问题——在后台添加了广告后，前台显示的是正常的，可是后台文本框编辑处的中文是乱码的。

发现乱码首先想到的是编码不一致，先去翻了数据库，发现也是正常的。然后想是不是后台php文件的编码错了，转了几次后确定了不是编码的问题。想想也是，如果是文件编码的问题，那应该是整个页面都乱码，而不仅仅是文本框乱码。

那么只有一个问题了，就是数据输出的时候出错了，翻代码吧…发现数据输出前被php函数htmlentities格式化了。去掉格式化函数后，中文正常显示了…

但是数据本身是包含html代码的，如果不格式化怕会出现意外的错误。当然，从常理上来说，我们也是要格式化一下的。

我们平时一般都是用htmlspecialchars函数格式化html的，于是就查了下htmlentities函数。

手册上是这样解释的:  
htmlentities() 函数把字符转换为 HTML 实体。  
htmlentities函数有三个参数:  
htmlentities(string,quotestyle,character-set)

[![htmlentities](/images/2014/03/htmlentities.jpg "htmlentities")](/images/2014/03/htmlentities.jpg)

注意:而无法被识别的字符集将被忽略，并由 ISO-8859-1 代替。

很明显，是因为参数的问题导致了中文字符的编码被解析出错了。  
把源代码改成

```
//$cod = htmlentities(get_option('AdsCode'.$i));
 $cod = htmlentities(get_option('AdsCode'.$i),ENT_COMPAT,'UTF-8');
```

再看就正常了…

PS:这不禁让我想起了前几天用的美橙互联的空间，phpmyadmin后台查看的数据，中文都是乱码的，而页面显示都是正常，现在想想应该是这个函数格式化html的时候编码出问题了…

既然谈到了格式化html，并且也说到了htmlspecialchars函数，那我们就有必要对比一下这两个函数的区别。

看到这里可能很多人都以为htmlentities跟htmlspecialchars的功能，用法是一样的。虽然从官方文档来看感觉这两个函数基本功能差不多，但还是有细微的差别的。

仔细研究过官方文档后我们就会发现htmlentities 和 htmlspecialchars 的区别在于 htmlentities 会转化所有的html代码（包括它无法识别的中文字符），而htmlspecialchars 只会转化手册上列出的几个 html代码（也就是会影响 html 解析的那几个基本字符）。

到这里可能就有人妄下结论:有中文的时候，最好用 htmlspecialchars ，否则可能乱码。

其实通过博主亲身体验的例子就会发现，htmlentities只要加上正确的编码作为参数，根本就不会出现所谓的中文乱码问题。

当然，一般来说，使用 htmlspecialchars 转化掉基本字符就已经足够了，没有必要使用 htmlentities。而实际情况中如果实在要使用 htmlentities 时，只需要注意为第三个参数传递正确的编码即可。
