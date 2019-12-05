---
title: Windows下配置php扩展PHP_intl.dll
date: 2015-03-19 08:34:37
categories: PHP
tags: 
- php
- php基础
- php_intl
- php_intl.dll
- icu库
- php图像识别
---

之前也有说，在本地做开发，为了方便快捷起见一直是在用集成环境，这次项目开发需要用到intl扩展，由于没有开启php\_intl扩展，报错：You have to install PHP intl extension to use this feature.于是直接在集成环境工具上点选开启intl扩展，再次启动服务，竟然弹窗报错！

[![php_intl](/images/2015/03/php_intl.jpg)](/images/2015/03/php_intl.jpg)

我去看了php的ext，里面也有php\_intl.dll啊，而且php.ini里早就设置好了扩展路径了啊，要不然以前肯定会报错的，那是怎么回事呢？intl又是何许人也？

PHP intl 是国际化扩展，是ICU 库的一个包装器。所以在安装PHP intl扩展前要先安装ICU库。看弹窗报错是缺失icu文件，网上说下载什么icu放到system32下面，好吧，那我就去找这个，可是找了半天竟然也没找到，感觉此路不通。

有人说是不是因为你系统是64位的原因？没办法了，就死马当活马医了，把集成环境干掉，弄上了自己的环境，各种换环境，最后是整到了apache 2.4 + php5.5 ，还是不行！

后来翻php根目录，发现这里有一组icu开头的dll文件，并且每个版本的php是不一样的，比如我的php5.5就是 icu\*51.dll ，难道说这些就是我需要的文件？但是没有加载到？那么，还是回到的第一次的尝试？但是我明明设置过扩展目录了啊，是可以正常加载此目录的扩展文件的。

最后在网上找到的办法：**环境变量添加上php的目录！**

oh shit！以前用自己的环境时一直都有设置这个的，后来用了集成环境后，由于他们有临时环境变量，就一直没管过，竟然是错在了这里！

后来又在网上找到一个方法：

把php\_intl.dll需要的dll拷贝到apache的bin目录里面，即php目录下面的（所有icu\*.dll的dll）拷贝到apache/bin目录下面。然后，在php.ini 添加一行 extension=php\_intl.dll。重启apache 即可正常使用。

我想，或许也可以把这些文件拷贝到system32下也能正常，因为system32也是环境变量成员，也能读取到。

但是最终还是推荐第一种做法，特别是对于像我这种喜欢切换php版本的同学来说。

最后再澄清下，这个错误跟集成还是散装环境没有关系，最主要的问题就是我没有设置环境变量。所以，同学们不用怀疑集成环境的可用性。
