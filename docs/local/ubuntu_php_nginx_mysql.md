---
title: Ubuntu下php+nginx+mysql的安装与配置
date: 2015-06-10 14:27:56
categories: 本地
---

之前有说用家里老电脑玩CentOs，但毕竟是主做服务器的，用来玩桌面确实有点不爽，遂又在另一台电脑上整上了Ubuntu玩。话说、几年前就已接触Ubuntu，而且也装过几次，但每次都是浅尝辄止，没有往更深的玩。

搭建这个环境实在不想使用Ubuntu自带的源，总感觉那么装下来的不是自己的东西，于是就自己大概散装了下。

[![ubuntu](/images/2015/06/ubuntu.jpg)](/images/2015/06/ubuntu.jpg)

**一、Nginx**

安装必要的扩展包

```
apt-get install libpcre3 libpcre3-dev
apt-get install libssl-dev openssl
```

新建用户

```
/usr/sbin/groupadd www
/usr/sbin/useradd -g www www
```

编译安装

```
wget http://nginx.org/download/nginx-1.5.1.tar.gz
tar zxvf nginx-1.5.1.tar.gz
cd nginx-1.5.1
./configure --user=www --group=www --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module  --with-http_realip_module
make && make install
```

```
##启动
/usr/local/nginx/sbin/nginx
##创建软链接
ln -s /usr/local/nginx/sbin/nginx /etc/init.d/nginx
##开机启动
vi /etc/rc.local
##添加
service nginx
```

**二、Mysql**

安装必要的扩展包

`apt-get install libaio-dev`新建用户

```
/usr/sbin/groupadd mysql
/usr/sbin/useradd -g mysql mysql
```

编译安装

```
wget http://cdn.mysql.com/archives/mysql-5.6/mysql-5.6.12-linux-glibc2.5-x86_64.tar.gz
tar zxvf mysql-5.6.12-linux-glibc2.5-x86_64.tar.gz -C /usr/local
mv /usr/local/mysql-5.6.12-linux-glibc2.5-x86_64/ /usr/local/mysql
cd /usr/local/mysql/
chown -R mysql .
chgrp -R mysql .
##生成mysql数据库运行的系统数据库，如果想把data单独拉出来的可以配置datadir
##sudo scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/data
scripts/mysql_install_db --user=mysql

##权限管理，保证安全
chown -R root .
chown -R mysql ./data

##启动
./support-files/mysql.server start

cp support-files/mysql.server /etc/init.d/mysql

##设置root密码
/usr/local/mysql/bin/mysql_secure_installation

##管理数据库测试下是否可用
./bin/mysql -uroot -p

##设置mysql服务开机启动
vi /etc/rc.local
##添加
service mysql start
```

**三、PHP**

安装必要的扩展包  
需要注意的是，我这里把扩展都装到自己指定的目录中了，这是强迫症患者的表现，希望能把整个环境独立出来单独管理。实际上，可以不写–prefix参数的，会默认安装到/usr/local中，如果选择使用默认的后面会少做很多处理。

```
wget http://www.ijg.org/files/jpegsrc.v9.tar.gz
tar zxvf jpegsrc.v9.tar.gz
cd jpeg-9/
./configure --prefix=/usr/local/ruesinweb/libs --enable-shared --enable-static
make && make install
```

```
wget http://prdownloads.sourceforge.net/libpng/libpng-1.6.2.tar.gz
tar zxvf libpng-1.6.2.tar.gz
cd libpng-1.6.2/
./configure --prefix=/usr/local/ruesinweb/libs
make && make install
```

```
wget http://download.savannah.gnu.org/releases/freetype/freetype-2.4.12.tar.gz
tar zxvf freetype-2.4.12.tar.gz
cd freetype-2.4.12/
./configure --prefix=/usr/local/ruesinweb/libs
make && make install
```

`apt-get install libxml2-dev````
wget http://downloads.sourceforge.net/mhash/mhash-0.9.9.9.tar.gz
wget http://downloads.sourceforge.net/mcrypt/libmcrypt-2.5.8.tar.gz
wget http://downloads.sourceforge.net/mcrypt/mcrypt-2.6.8.tar.gz

tar zxvf libmcrypt-2.5.8.tar.gz
cd libmcrypt-2.5.8/
./configure --prefix=/usr/local/ruesinweb/libs
make && make install
cd libltdl/
./configure --prefix=/usr/local/ruesinweb/libs --enable-ltdl-install
make && make install

tar zxvf mhash-0.9.9.9.tar.gz
cd mhash-0.9.9.9/
./configure --prefix=/usr/local/ruesinweb/libs
make && make install

##编辑 /etc/ld.so.conf 加入类库，加载动态装入器。
vi /etc/ld.so.conf
/usr/local/ruesinweb/libs/lib
ldconfig

tar zxvf mcrypt-2.6.8.tar.gz
cd mcrypt-2.6.8/
##编辑变量，引入指定的库位置，如果之前编译扩展都在默认目录中，就不用做这个操作了
export LDFLAGS="-L/usr/local/ruesinweb/libs/lib -L/usr/lib"
export CFLAGS="-I/usr/local/ruesinweb/libs/include -I/usr/include"
touch malloc.h
./configure --prefix=/usr/local/ruesinweb/libs --with-libmcrypt-prefix=/usr/local/ruesinweb/libs
make && make install
```

编译安装php

```
tar zvxf php-5.4.41.tar.gz
cd php-5.4.41
./configure --prefix=/usr/local/php --enable-fpm --with-mysql=/usr/local/mysql \
--with-mysqli=/usr/local/mysql/bin/mysql_config --with-config-file-path=/usr/local/php  \
--with-openssl --enable-mbstring  --with-zlib --enable-xml \
--with-png-dir=/usr/local/ruesinweb/libs --with-freetype-dir=/usr/local/ruesinweb/libs --with-gd --with-jpeg-dir=/usr/local/ruesinweb/libs   \
--enable-bcmath --with-mcrypt=/usr/local/ruesinweb/libs --with-iconv --enable-pcntl --enable-shmop --enable-simplexml --enable-ftp \

##--with-curl

make && make install

##复制配置文件
cp php.ini-development /usr/local/php/php.ini

cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf

##复制php-fpm启动脚本
cp sapi/fpm/php-fpm /etc/init.d/php-fpm
##赋予脚本执行权限
chmod +x /etc/init.d/php-fpm

##需要修改 php-fpm.conf，确保 php-fpm 模块使用 www 身份运行。
vi /usr/local/php/etc/php-fpm.conf

user = www
group = www

##启动 php-fpm 服务
/usr/local/bin/php-fpm

##设置 php-fpm 开机启动
vi /etc/rc.local
添加
service php-fpm
```

编辑 php.ini 文件中的配置项 cgi.fix\_pathinfo 设置为 0 ，如果文件不存在，则阻止 Nginx 将请求发送到后端的 PHP-FPM 模块， 以避免遭受恶意脚本注入的攻击。

```
vi /usr/local/php/php.ini
cgi.fix_pathinfo=0
```

配置 Nginx 使其支持 PHP 应用：

`vi /usr/local/nginx/conf/nginx.conf`修改默认的 location 块，使其支持 .php 文件：

```
location / {
    root   html;
    index  index.php index.html index.htm;
}
```

编辑默认的 PHP 配置块，保证 .php 文件的请求将被传送到后端的 PHP-FPM 模块，

```
location ~* \.php$ {
    fastcgi_index   index.php;
    fastcgi_pass    127.0.0.1:9000;
    include         fastcgi_params;
    fastcgi_param   SCRIPT_FILENAME    $document_root$fastcgi_script_name;
    fastcgi_param   SCRIPT_NAME        $fastcgi_script_name;
}
```

重启 Nginx。

```
sudo /usr/local/nginx/sbin/nginx -s stop
sudo /usr/local/nginx/sbin/nginx
```

重启 php-fpm  
使用 ps aux | grep php-fpm ，查看进程号。

`kill -USR2 进程号`
