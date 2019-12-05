---
title: Ubuntu 下编译安装 memcached 服务 及 PHP memcache扩展
date: 2016-01-26 09:06:30
categories: 本地
tags: 
- php
- memcache
- memcached
- ubuntu
- ubuntu web环境
- ubuntu php
---

对于memcache的介绍就不再做过多赘述，之前写过一个windows下的安装及介绍，有兴趣的朋友可以去翻一翻。

一、安装memcached服务。

先装memcached依赖 lievent 官网：http://libevent.org/

```
wget https://sourceforge.net/projects/levent/files/libevent/libevent-2.0/libevent-2.0.22-stable.tar.gz
tar zvxf libevent-2.0.22-stable.tar.gz
sudo ./configure --prefix=/usr/local
sudo make
sudo make install
```

编译安装 memcached 服务 官网：http://memcached.org/downloads

```
wget http://memcached.org/files/memcached-1.4.25.tar.gz
tar zvxf memcached-1.4.25.tar.gz
sudo ./configure  --prefix=/usr/local/memcached --with-libevent=/usr/local
sudo make
sudo make install
```

启动服务

`/usr/local/memcached/bin/memcached -d -m  128 -u root -p  11211`二、memcache扩展，php有两个版本的memcached 扩展。

1\. 基于libmemcached的memcache扩展：https://launchpad.net/libmemcached/+download

```
wget https://launchpad.net/libmemcached/1.0/1.0.18/+download/libmemcached-1.0.18.tar.gz
tar zvxf libmemcached-1.0.18.tar.gz
sudo ./configure --prefix=/usr/local/libmemcached --with-memcached
sudo make
sudo make install
```

下载memcached扩展：https://pecl.php.net/package/memcached

```
wget https://pecl.php.net/get/memcached-2.2.0.tgz
tar zvxf memcached-2.2.0.tgz
sudo /usr/local/php/bin/phpize
sudo ./configure --with-libmemcached-dir=/usr/local/libmemcached --with-php-config=/usr/local/php/bin/php-config --enable-memcached --enable-memcached-json --enable-memcached-igbinary --disable-memcached-sasl
```

找不到php扩展的话可以使用 whereis php-config。

因为在编译的时候，加了对json和igbinary的支持，而之前没有安装igbinary扩展，导致报错：error: Cannot find igbinary.h

编译PHP的igbinary扩展。

```
wget http://pecl.php.net/get/igbinary-1.1.1.tgz
tar zvxf igbinary-1.1.1.tgz
sudo ./configure --with-php-config=/usr/local/php/bin/php-config
sudo make
sudo  make install
```

再次重新编译安装即可。

```
Installing shared extensions:     /usr/local/php/lib/php/extensions/no-debug-non-zts-20131226/
Installing header files:          /usr/local/php/include/php/
```

最后memcache扩展被安装在，我的对应编译版本的扩展目录里。

`Installing shared extensions:     /usr/local/php/lib/php/extensions/no-debug-non-zts-20131226/`修改配置文件，添加php扩展

```
sudo vi /usr/local/php/php.ini
extension="/usr/local/php/lib/php/extensions/no-debug-non-zts-20131226/memcached.so"
```

2\. memcache 扩展，可以下载包安装，也可以按照官方文档说的，使用peel安装。

下载地址：http://pecl.php.net/get/memcache

```
tar zxvf memcache-3.0.3.tgz
sudo /usr/local/php/bin/phpize
./configure --with-php-config=/usr/local/php/bin/php-config
sudo make
sudo make install
```

然后修改php.ini添加extension = “memcache.so”就可以了
