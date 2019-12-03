---
title: CentOS 7.4 部署 Tars-PHP 环境
date: 2018-12-12 23:27:27
categories: 基础
---

## 前言
因为使用CentOs部署的服务出现swoole-worker进程挂掉后master无法重新拉起的情况，调试多次后提了 [Issues](https://github.com/TarsPHP/TarsPHP/issues/7) 也没有解决，最终选择使用 [Ubuntu16.04](https://www.xinkoukaihe.com/a/1982.html)。
如下为对比：
![tars-compare.png](/images/20181212/4fef8b06f4b819a5ef5efcffd28c2773.png)

## 准备
安装必要依赖
```
yum install -y glibc-devel gcc-c++ flex bison git

wget https://cmake.org/files/v2.8/cmake-2.8.8.tar.gz
tar zxvf cmake-2.8.8.tar.gz
cd cmake-2.8.8
./bootstrap
make
make install

wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
source ~/.bashrc
nvm install v8.11.3
npm install -g pm2 --registry=https://registry.npm.taobao.org

yum install -y ncurses-devel  zlib-devel

```

## MySQL

```
wget https://cdn.mysql.com//Downloads/MySQL-5.6/mysql-5.6.42.tar.gz
tar zvxf mysql-5.6.42.tar.gz
mv mysql-5.6.42 /usr/local/mysql
cd /usr/local/mysql
cmake . -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DWITH_INNOBASE_STORAGE_ENGINE=1 -DMYSQL_USER=mysql -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci
make
make install

useradd mysql
chown -R mysql:mysql /usr/local/mysql/data/

cp support-files/mysql.server /etc/init.d/mysqld
chmod 755 /etc/init.d/mysqld

yum install -y perl
yum install -y perl-Module-Install.noarch

## 清空/etc/my.cnf 的配置

chmod +x scripts/mysql_install_db
./scripts/mysql_install_db --user=mysql

# vim /usr/local/mysql/my.cnf
...
[mysqld] 
log_bin
basedir = /usr/local/mysql 
datadir = /usr/local/mysql/data
socket = /tmp/mysql.sock 
bind-address=172.17.11.11 
join_buffer_size = 128M
sort_buffer_size = 2M
read_rnd_buffer_size = 2M
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES 
...

service mysqld start
chkconfig mysqld on

vim /etc/profile
PATH=$PATH:/usr/local/mysql/bin
source /etc/profile

./bin/mysqladmin -u root password 'ruesin'
./bin/mysqladmin -u root -h yourHostName password 'ruesin' 
service mysqld restart

echo '/usr/local/mysql/lib/' >> /etc/ld.so.conf 
ldconfig

```
## Framework

```
git clone https://github.com/TarsCloud/Tars.git
cd Tars
git submodule update --init --recursive framework
cd framework/build/

chmod u+x build.sh
./build.sh prepare
./build.sh all
./build.sh install

##Tars数据库环境初始化
mysql -uroot -pruesin -e "grant all on *.* to 'tars'@'%' identified by 'tars2015' with grant option;"
mysql -uroot -pruesin -e "grant all on *.* to 'tars'@'localhost' identified by 'tars2015' with grant option;"
mysql -uroot -pruesin -e "grant all on *.* to 'tars'@'yourHostName' identified by 'tars2015' with grant option;"
mysql -uroot -pruesin -e "grant all on *.* to 'tars'@'172.17.11.11 ' identified by 'tars2015' with grant option;"
mysql -uroot -pruesin -e "flush privileges;"

cd ../sql
sed -i "s/192.168.2.131/172.17.11.11 /g" `grep 192.168.2.131 -rl ./*`
sed -i "s/db.tars.com/172.17.11.11 /g" `grep db.tars.com -rl ./*`
sed -i "s/10.120.129.226/172.17.11.11 /g" `grep 10.120.129.226 -rl ./*`

chmod u+x exec-sql.sh
sed -i "s/root@appinside/ruesin/g" `grep 'root@appinside' -rl ./*`
./exec-sql.sh

cd ../build
make framework-tar
make tarsstat-tar
make tarsnotify-tar
make tarsproperty-tar
make tarslog-tar
make tarsquerystat-tar
make tarsqueryproperty-tar


mkdir -p /usr/local/app/tars/
cp framework.tgz /usr/local/app/tars/
cd /usr/local/app/tars
tar xzfv framework.tgz

sed -i "s/192.168.2.131/172.17.11.11 /g" `grep 192.168.2.131 -rl ./*`
sed -i "s/db.tars.com/172.17.11.11 /g" `grep db.tars.com -rl ./*`
sed -i "s/registry.tars.com/172.17.11.11 /g" `grep registry.tars.com -rl ./*`
sed -i "s/web.tars.com/172.17.11.11 /g" `grep web.tars.com -rl ./*`

chmod u+x tars_install.sh
./tars_install.sh
./tarspatch/util/init.sh

```

## Web管理
```
cd ~/Tars
git submodule update --init --recursive web
npm install -g pm2 --registry=https://registry.npm.taobao.org
cd web
sed -i "s/registry.tars.com/172.17.11.11 /g" `grep registry.tars.com -rl ./config/*`
sed -i "s/db.tars.com/172.17.11.11 /g" `grep db.tars.com -rl ./config/*`
npm install --registry=https://registry.npm.taobao.org
npm run prd

mkdir -p /data/log/tars/

```
访问 `http://{your_ip}:3000/index.html#/server` 即可管理服务

## 运行

1). db_tars 数据库中创建新表：
```
# mysql -u root -p
mysql> use db_tars;
mysql> CREATE TABLE `t_server_notifys` (   `id` int(11) NOT NULL AUTO_INCREMENT,  `application` varchar(128) DEFAULT '',  `server_name` varchar(128) DEFAULT NULL, `container_name` varchar(128) DEFAULT '' , `node_name` varchar(128) NOT NULL DEFAULT '',  `set_name` varchar(16) DEFAULT NULL,  `set_area` varchar(16) DEFAULT NULL,  `set_group` varchar(16) DEFAULT NULL,  `server_id` varchar(100) DEFAULT NULL,  `thread_id` varchar(20) DEFAULT NULL,  `command` varchar(50) DEFAULT NULL,  `result` text,  `notifytime` datetime DEFAULT NULL,  PRIMARY KEY (`id`),  KEY `index_name` (`server_name`),  KEY `servernoticetime_i_1` (`notifytime`),  KEY `indx_1_server_id` (`server_id`),  KEY `query_index` (`application`,`server_name`,`node_name`,`set_name`,`set_area`,`set_group`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
2).部署其他普通基础服务：`tars.tarsnotify.NotifyObj, tars.tarsstat.StatObj, tars.tarsproperty.PropertyObj, tars.tarslog.LogObj, tars.tarsquerystat.NoTarsObj, tars.tarsqueryproperty.NoTarsOb
注意：tarsquerystat, tarsqueryproperty 使用 非tars 协议。

```
mkdir -p /data/web/client/dist/tgz
cp /root/Tars/framework/build/*.tgz /data/web/client/dist/tgz
```
访问 `http://{your_ip}:3000/tarsnotify.tgz` 等下载。


## PHP
```
yum -y install libmcrypt libmcrypt-devel mhash-devel libxslt libxslt-devel libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel  openssl openssl-devel libcurl libcurl-devel libicu-devel
wget http://hk1.php.net/distributions/php-7.2.7.tar.gz

./configure --prefix=/usr/local/php --with-config-file-path=/usr/local/php \
--with-config-file-scan-dir=/usr/local/php/etc/conf.d \
--enable-fpm --with-fpm-user=www --with-fpm-group=www \
--enable-mysqlnd --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd \
--with-iconv --with-iconv-dir --enable-pcntl --enable-shmop \
--enable-simplexml --with-libxml-dir --enable-ftp --enable-zip --enable-soap --with-curl \
--with-openssl --enable-mbstring  --with-zlib --enable-xml \
--enable-sockets --enable-inline-optimization \
--with-png-dir --with-freetype-dir --with-gd --with-jpeg-dir \
--enable-bcmath \
--disable-rpath --enable-sysvsem \
--enable-mbregex --enable-intl   \
--with-mhash  --with-xmlrpc \
--with-gettext --disable-fileinfo --enable-opcache --with-xsl

# make
# make install


vim /etc/profile
...
export PATH=$PATH:/usr/local/php/bin:/usr/local/php/sbin
...
source /etc/profile

ln -s /usr/local/php/bin/php /usr/bin/php

cp php.ini-development /usr/local/php/php.ini
vim /usr/local/php/php.ini
...
error_log = /php_errors.log
cgi.fix_pathinfo=0
date.timezone = PRC
...
```


## 扩展

```
yum install -y m4 autoconf

# git clone https://github.com/TarsPHP/tars-extension.git
# ...
# echo 'extension=phptars.so' >> /usr/local/php/php.ini

# wget http://pecl.php.net/get/redis-3.1.1.tgz
#...
# echo 'extension=redis.so' >> /usr/local/php/php.ini

wget http://pecl.php.net/get/swoole-1.9.16.tgz
...
echo 'extension=swoole.so' >> /usr/local/php/php.ini

# php -r "copy('https://install.phpcomposer.com/installer', 'composer-setup.php');"
# php composer-setup.php
# php -r "unlink('composer-setup.php');"
# mv composer.phar /usr/bin/composer
# chmod +x /usr/bin/composer
# composer config -g repo.packagist composer https://packagist.phpcomposer.com

```

## 报错
1. 服务初始化之后，由于不存在数据表`t_server_notifys`，会报错，创建新表即可。

2. 服务监控、特性监控 报错
{"level":"error","message":"192.168.56.1||MonitorController.js:58|line #1, Ret= -1  ","timestamp":"2018-11-16 16:51:41.434”}
初次安装的时候，没数据，可能出现这种情况。

参考:  
https://github.com/TarsCloud/Tars/blob/master/Install.zh.md  
https://github.com/TarsCloud/Tars/blob/master/build/install.sh

