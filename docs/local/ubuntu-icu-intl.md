---
title: Ubuntu 编译 Unicode ICU 库 及 PHP intl 扩展
date: 2015-12-31 23:43:51
categories: 本地
---

 PHP intl 是国际化扩展，是ICU 库的一个包装器。所以在安装PHP intl扩展前要先安装ICU库。

先从官网下载源文件，这里是选择的ICU4C。http://site.icu-project.org/download

$ wget http://download.icu-project.org/files/icu4c/56.1/icu4c-56\_1-src.tgz  
$ tar zvxf icu4c-56\_1-src.tgz  
$ cd icu/source  
$ sudo ./configure –prefix=/usr/local/icu  
$ sudo make  
$ sudo make install

然后从PHP扩展包中搜索intl下载。https://pecl.php.net/package/intl

$ wget https://pecl.php.net/get/intl-3.0.0.tgz  
$ tar zvxf intl-3.0.0.tgz  
$ cd intl-3.0.0/  
$ sudo /usr/local/php/bin/phpize  
$ sudo ./configure –enable-intl –with-icu-dir=/usr/local/icu/ –with-php-config=/usr/local/php/bin/php-config  
$ sudo make  
$ sudo make install  
$ sudo vi /usr/local/php/php.ini

编辑配置文件，添加开启intl扩展，重启服务。

当然，官方也提供了pecl的安装方式，有兴趣的朋友可以去看下官方文档。

$ sudo /usr/local/php/bin/pecl install intl-3.0.0  
指定ICU库的位置，然后修改配置，开启扩展，重启服务即可。

可以用 $php -m | grep intl 或 phpinfo() 查看intl扩展是否安装成功
