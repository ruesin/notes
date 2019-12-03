---
title: MacOS 编译安装 PHP + Nginx + Mysql
date: 2018-12-12 22:00:01
categories: 基础
---

MacOS 源码编译安装开发环境， PHP7.2 + Nginx1.14 + Mysql5.7 + Redis3.2。

## 一、准备

```
## xcode
$ xcode-select -install`

## brew
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

$ brew install wget
$ brew install autoconf
$ brew install m4

$ ssh-keygen -t rsa -C "ruesin@gmail.com"
$ git config --global user.name "Ruesin"
$ git config --global user.email "ruesin@gmail.com”

$ mkdir -p /Users/sin/src
$ cd src
$ wget http://nginx.org/download/nginx-1.14.0.tar.gz
$ wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.42.tar.gz
$ wget http://zlib.net/zlib-1.2.11.tar.gz
$ wget https://www.openssl.org/source/openssl-1.0.1u.tar.gz

$ wget https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.23-macos10.13-x86_64.tar.gz

$ wget http://hk1.php.net/distributions/php-7.2.7.tar.gz

```

## 二、Nginx
```
$ tar zvxf nginx-1.14.0.tar.gz 

$ ./configure --user=_www --group=_www --prefix=/usr/local/nginx  --with-http_stub_status_module --with-http_realip_module  --with-http_ssl_module --with-http_gzip_static_module --with-zlib=/Users/sin/src/zlib-1.2.11 --with-openssl=/Users/sin/src/openssl-1.0.1u --with-pcre="/Users/sin/src/pcre-8.42"
$ sudo make
$ sudo make install
```

```
$ sudo /usr/local/nginx/sbin/nginx
$ sudo ln -s /usr/local/nginx/sbin/nginx /usr/local/bin/nginx

$ cd /usr/local/nginx/conf/
$ sudo mkdir vhost
...
user sin staff;
include vhost/*.conf;
...
```

```
$ sudo vim vhost/test.conf
server {
        listen       80;
        server_name  local.test.com;
        #access_log  /usr/local/nginx/logs/test.access.log;
        #error_log /usr/local/nginx/logs/test.error.log;

        set $root /Users/sin/projects/test;
        root    $root;

        index index.php;
        location / {
            if (!-e $request_filename) {
                 rewrite ^/(.*)$ /index.php/$1;
            }
        }

        location ~ \.php {
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            include        fastcgi.conf;
            set $real_script_name $fastcgi_script_name;
            if ($fastcgi_script_name ~ "^(.+?\.php)(/.+)$") {
                set $real_script_name $1;
                set $path_info $2;
            }
            fastcgi_param SCRIPT_FILENAME $document_root$real_script_name;
            fastcgi_param SCRIPT_NAME $real_script_name;
            fastcgi_param PATH_INFO $path_info;
        }
}
...

$ sudo vim /etc/hosts
...
127.0.0.1 local.test.com
...

```

错误：
```
ld: symbol(s) not found for architecture x86_64
clang: error: linker command failed with exit code 1 (use -v to see invocation)
make[1]: *** [objs/nginx] Error 1
make: *** [build] Error 2
```

openssl/config 脚本检测系统是否64位，但是会根据$KERNEL_BITS来判断是否开启x86_64编译，默认不开启，所以生成的openssl库文件是32位的，最后在Makefile中链接到nginx时会报错。

可以在configure之前export KERNEL_BITS=64。或者执行完 ./configure 后, 修改 Makefile 文件后再make:

```
$ vim objs/Makefile
...
./config --prefix=/Users/sin/Downloads/openssl-1.0.1u/.openssl no-shared no-threads
改成
./Configure darwin64-x86_64-cc –prefix=/Users/xxx/Downloads/openssl-1.0.1u/.openssl no-shared no-threads
...
```

## 三、MySQL

```
$ tar zvxf mysql-5.7.23-macos10.13-x86_64.tar.gz 

$ sudo mv mysql-5.7.23-macos10.13-x86_64 /usr/local/mysql
$ cd /usr/local/mysql
$ sudo chown -R _mysql:_mysql .

# 初始化MySQL，生成root临时密码
$ sudo bin/mysqld --initialize --user=_mysql

$ sudo cp support-files/mysql.server /usr/local/bin/mysqld
$ sudo vim /etc/my.cnf
...
[mysqld]
user=_mysql
...
$ sudo mysqld&

$ bin/mysql -u root -p
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
```

参考：
https://dev.mysql.com/doc/refman/5.7/en/binary-installation.html

## 四、PHP
```
$ tar zvxf php-7.2.7.tar.gz 

$ ./configure --prefix=/usr/local/php --enable-fpm --with-pdo-mysql \
--enable-mysqlnd --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd --with-config-file-path=/usr/local/php  \
--with-config-file-scan-dir=/usr/local/php/etc/conf.d \
--with-iconv --enable-pcntl --enable-shmop --enable-simplexml --enable-ftp --enable-zip --enable-soap --with-curl \
--with-openssl=/usr/local/opt/openssl --enable-mbstring  --with-libzip=/usr/local/opt/libzip --with-zlib --enable-xml \
--enable-sockets --enable-inline-optimization \
--with-png-dir --with-freetype-dir=/usr/local/opt/freetype --with-gd --with-jpeg-dir=/usr/local \
--enable-bcmath \
--with-libxml-dir \
--disable-rpath --enable-sysvsem \
--enable-mbregex --enable-intl   \
--with-mhash  --with-xmlrpc \
--enable-opcache --with-xsl=/usr/local/opt/libxslt --with-gettext=/usr/local/opt/gettext

$ make
$ sudo make install
```

```
$ sudo cp ./php.ini-development /usr/local/php/php.ini
$ sudo cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf
$ cd /usr/local/php/etc/php-fpm.d/
$ sudo cp www.conf.default www.conf
$ sudo vim www.conf
...
user = sin
group = staff
...

$ vim ~/.bash_profile
...
export PATH=/usr/local/php/bin:/usr/local/php/sbin:${PATH}
...

$ source ~/.bash_profile
$ sudo php-fpm
```

问题：  
4.1   
`configure: error: Cannot find OpenSSL's <evp.h>`
```
$ brew install openssl
```

4.2
```
checking whether to enable JIS-mapped Japanese font support in GD... no
If configure fails try --with-webp-dir=<DIR>
configure: error: jpeglib.h not found.
```
```
$ sudo find / -name 'jpeglib.h'
/usr/local/include/jpeglib.h
/usr/local/Cellar/jpeg/9c/include/jpeglib.h
```

4.3
```
If configure fails try --with-xpm-dir=<DIR>
configure: error: freetype-config not found
```
```
$ sudo find / -name 'freetype*'
$ brew install freetype
```

4.5  
`warning: pointer is missing a nullability type specifier`
`$ brew install libxslt`

4.6  
`configure: error: Please reinstall the libzip distribution`
`$ brew install libzip`

4.7  
`configure: error: Please reinstall the iconv library.`  
经排查是gettext导致的  
`$ brew link --overwrite gettext —force`

4.8  
`configure: error: Unable to detect ICU prefix or no failed. Please verify ICU install prefix and make sure icu-config works.`
```
$ brew install icu4c
$ brew link icu4c --force
```

4.9   
`configure: error: Cannot locate header file libintl.h`
```
$ sudo find / -name 'libintl.h'
/usr/local/Cellar/gettext/0.19.8.1/include/libintl.h
```

## 五、扩展
### 5.1 swoole
```
$ wget http://pecl.php.net/get/swoole-1.9.23.tgz
$ phpize
$ ./configure
$ make
$ sudo make install
$ echo 'extension=swoole.so' | sudo tee -a /usr/local/php/php.ini
```

### 5.2 redis
```
$ wget http://pecl.php.net/get/redis-3.1.1.tgz
$ tar zvxf redis-3.1.1.tgz
$ cd redis-3.1.1
$ phpize
$ ./configure --with-php-config=/usr/local/php/bin/php-config
$ make
$ sudo make install
$ echo 'extension=redis.so' | sudo tee -a /usr/local/php/php.ini
```

### 5.3 mongodb
```
$ wget http://pecl.php.net/get/mongodb-1.3.0.tgz
$ tar zvxf mongodb-1.3.0.tgz
$ cd mongodb-1.3.0
$ phpize
$ ./configure --with-php-config=/usr/local/php/bin/php-config --with-openssl-dir=/usr/local/opt/openssl
$ make
$ sudo make install
$ echo 'extension=mongodb.so' | sudo tee -a /usr/local/php/php.ini
```

### 5.4 yaf
```
$ wget http://pecl.php.net/get/yaf-3.0.7.tgz
$ ./configure --with-php-config=/usr/local/php/bin/php-config
$ make
$ sudo make install
```

### 5.2 compser
```
$ wget https://getcomposer.org/download/1.7.2/composer.phar
$ sudo mv composer.phar /usr/local/bin/composer
$ chmod +x /usr/local/bin/composer
```

## 其他

### 1. 终端样式

```
$ vim ~/.bash_profile
...
function git-branch-name {
  #git symbolic-ref HEAD 2>/dev/null | cut -d"/" -f 3
  git symbolic-ref HEAD 2>/dev/null | sed 's#refs/heads/##g'
}
function git-branch-prompt {
  local branch=`git-branch-name`
  if [ $branch ]; then printf " [%s]" $branch; fi
}
PS1="\[\e[31m\]\$ \[\e[m\]\[\033[01;34m\]\w\[\033[00m\]\[\033[0;32m\]\$(git-branch-prompt)\[\033[0m\]\n\[\e[31m\]\$ \[\e[m\]"
...
```
### 2. Redis
```
$ wget http://download.redis.io/releases/redis-3.2.5.tar.gz
$ tar zvxf redis-3.2.5.tar.gz
$ cd redis-3.2.5
$ make
$ sudo make install
$ redis-server --version
$ sudo sudo mkdir -p /usr/local/redis
# sudo cp /root/src/redis-3.2.5/redis.conf /usr/local/redis
# sudo vim /usr/local/redis/redis.conf
...
daemonize yes
dir /usr/local/redis
...
$ sudo redis-server /usr/local/redis/redis.conf
```
