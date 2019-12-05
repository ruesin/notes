---
title: Ubuntu 下编译Curl库及PHP的curl扩展
date: 2015-12-31 23:42:18
categories: 本地
tags: 
- curl
- ubuntu
- ubuntu web环境
---

编译PHP的时候连常用的Curl扩展都忘记了，脑也是够残的。

安装Curl，需要先去官网下载源文件。http://curl.haxx.se/download/

$ wget http://curl.haxx.se/download/curl-7.30.0.tar.gz  
$ tar zvxf curl-7.30.0.tar.gz  
$ cd curl-7.30.0/  
$ sudo ./configure –prefix=/usr/local/curl  
$ sudo make  
$ sudo make install

至此，Curl编译已经完成，在目录/usr/local/curl下会有编译生产的库、头文件等。

程序设计中，为方便移植，可以把include/lib下面的头文件和so库文件拷贝到工程所在目录就可以随时使用curl库了。

将curl加入环境变量，方便随时使用。

$ sudo vi /etc/profile  
$ source /etc/profile

我们是做web服务用的，当然不至于此，还需要将curl编译到php中，开启php的curl扩展。

$ sudo /usr/local/php/bin/phpize

如果报错：  
Cannot find autoconf. Please check your autoconf installation and the $PHP\_AUTOCONF environment variable. Then, rerun this script.

$ sudo apt-get install m4 autoconf

如果报错：  
Cannot find config.m4.  
Make sure that you run ‘/usr/local/php/bin/phpize’ in the top level source directory of the module  
在需要扩展编译的PHP模块目录中执行/usr/local/php/bin/phpize 这样才不会报错

$ cd ~/source/nmp/php-5.6.10/ext/curl  
$ sudo /usr/local/php/bin/phpize  
$ sudo ./configure -with-curl=/usr/local/curl –with-php-config=/usr/local/php/bin/php-config  
$ sudo make  
$ sudo make test  
$ sudo make install  
$ sudo cp curl.so /usr/local/php/lib/php/extensions/no-debug-non-zts-20131226/curl.so  
$ sudo vi /usr/local/php/php.ini

开启curl扩展，重启服务。

如果是编译PHP时就想带上curl，编译PHP时加上 –with-curl=/usr/local/curl
