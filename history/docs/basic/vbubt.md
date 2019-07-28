---
title: VirtualBox + Ubuntu 16.04 编译 PHP 开发环境
date: 2018-12-12 21:55:17
categories: 基础
---

# VirtualBox + Ubuntu 16.04


## 一、准备

### 1.1 网络设置，有两种方案可用：
1. 设置网卡1的端口转发，将主机的22、80、3306等端口映射到虚拟机的相应端口，访问127.0.0.1:22即转发至虚拟机。
2. 设置网卡2，选择`host-only`模式，本文是采用此方法。  

设置root密码  
`$ sudo passwd root`

修改网络配置  
```
$ sudo vim /etc/network/interfaces


...
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback 

# The primary network interface
auto enp0s3
iface enp0s3 inet dhcp

## custom net 1
# 增加的Host-only静态IP设置 (enp0s8 是根据拓扑关系映射的网卡名称（旧规则是eth0,eth1）)
# 可以通过 ```ls /sys/class/net```查看，是否为enp0s8

auto enp0s8
iface enp0s8 inet static
address 192.168.56.101
netmask 255.255.255.0

#auto eth1
#iface eth1 inet static
#address 192.168.56.11
#netmask 255.255.255.0
...

```

修改SSH配置，使root可远程登录  
```
$ sudo vim /etc/ssh/sshd_config
...
#PermitRootLogin prohibit-password
PermitRootLogin yes
...
$ sudo service ssh restart
```

### 1.2 替换源
```
# sed -i "s#cn.archive.ubuntu.com#mirrors.aliyun.com#g" /etc/apt/sources.list
# sed -i "s#security.ubuntu.com#mirrors.aliyun.com#g" /etc/apt/sources.list
# apt update
# apt upgrade
```

### 1.3 安装必要依赖  
`# apt install gcc binutils make linux-source autoconf g++`

### 1.4 文件共享
先去管理窗口菜单 “设备” -> “安装增强功能” (Devices->Insert Guest Additions CD image) 
```
# mkdir -p /mnt/cdrom
# mount /dev/cdrom /mnt/cdrom/
# cd /mnt/cdrom/
# ./VBoxLinuxAdditions.run
# mkdir -p /data/projects
# mount -t vboxsf projects /data/projects
# echo 'test' > a.txt

## 开机自动挂载
# echo 'share /data/share vboxsf defaults 0 0' >> /etc/fstab
# echo 'projects /data/projects vboxsf defaults 0 0' >> /etc/fstab

# echo 'vboxsf' >> /etc/modules
```

### 1.5 配置git信息
```
# git config --global user.name "Ruesin"
# git config --global user.email "ruesin@gmail.com"
# ssh-keygen -t rsa -C "ruesin@gmail.com"
```

### 1.6 下载软件包
```
# wget http://nginx.org/download/nginx-1.14.0.tar.gz
# wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.42.tar.gz
# wget http://zlib.net/zlib-1.2.11.tar.gz
# wget https://www.openssl.org/source/openssl-1.0.1u.tar.gz
# wget http://hk1.php.net/distributions/php-7.2.7.tar.gz
# wget http://cdn.mysql.com/archives/mysql-5.6/mysql-5.6.12-linux-glibc2.5-x86_64.tar.gz
```

## 二、Nginx
### 2.1 安装
```
# groupadd www
# useradd -g www www -s /bin/false

# tar zvxf openssl-1.0.1u.tar.gz
# tar zvxf zlib-1.2.11.tar.gz
# tar zvxf pcre-8.42.tar.gz
# tar zvxf nginx-1.14.0.tar.gz
# cd nginx-1.14.0/
# ./configure --user=www --group=www --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module --with-http_realip_module --with-pcre=/root/src/pcre-8.42 --with-zlib=/root/src/zlib-1.2.11 --with-openssl=/root/src/openssl-1.0.1u
# make
# make install
```

### 2.2 配置
```
## 开机启动
# sed -i '$i\/usr/local/nginx/sbin/nginx' /etc/rc.local

# cd /usr/local/nginx/conf/
# mkdir vhost
# vim nginx.conf
... 
user  www;
include  vhost/*.conf;
...

## 添加环境变量
# vim /etc/profile
...
export PATH=$PATH:/usr/local/nginx/sbin
...
# source /etc/profile
```

## 三、Mysql
```
# tar -zvxf mysql-5.6.12-linux-glibc2.5-x86_64.tar.gz
# groupadd mysql
# useradd -g mysql mysql -s /bin/false
# mv mysql-5.6.12-linux-glibc2.5-x86_64 /usr/local/mysql
# cd /usr/local/mysql/
# chown -R mysql.mysql .

# apt install -y libaio1

## 执行安装
# ./scripts/mysql_install_db --user=mysql

## 添加service
# cp ./support-files/mysql.server /etc/init.d/mysqld
# chmod 755 /etc/init.d/mysqld
# systemctl enable mysqld.service
# service mysqld start

## 初始化密码
# ./bin/mysql_secure_installation

## 添加环境变量
# vim /etc/profile
...
export PATH=$PATH:/usr/local/mysql/bin:/usr/local/nginx/sbin
...
# source /etc/profile

## 设置root访问权限
# mysql -u root -p
mysql> use mysql;
mysql> UPDATE user SET `host`='%' WHERE `user`='root' AND `host`='localhost';
mysql> exit;

# service mysqld restart
```

## 四、PHP
### 4.1 安装
```
## 安装依赖
# apt install -y libxml2 libxml2-dev
# apt install -y libcurl4-openssl-dev pkg-config libssl-dev
# apt install -y build-essential libexpat1-dev libgeoip-dev libpng-dev libpcre3-dev rcs zlib1g-dev mcrypt libmcrypt-dev libmhash-dev libcurl4-openssl-dev libjpeg-dev libpng-dev libwebp-dev libfreetype6 libfreetype6-dev
# apt install -y libxslt1.1 libxslt1-dev

# tar zvxf php-7.2.7.tar.gz
# ./configure --prefix=/usr/local/php --with-config-file-path=/usr/local/php \
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
```
### 4.2 配置

开机启动  
`# sed -i '$i\/usr/local/php/sbin/php-fpm' /etc/rc.local `

环境变量
```
# vim /etc/profile
...
export PATH=$PATH:/usr/local/php/bin:/usr/local/php/sbin:/usr/local/mysql/bin:/usr/local/nginx/sbin
...
# source /etc/profile
```

修改配置文件
```
# cp php.ini-development /usr/local/php/php.ini
# cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf
# cp /usr/local/php/etc/php-fpm.d/www.conf.default /usr/local/php/etc/php-fpm.d/www.conf

# vim /usr/local/php/php.ini
...
error_log = /php_errors.log
cgi.fix_pathinfo=0
date.timezone = PRC
...
```

配置service
```
# cp /root/src/php-7.2.7/sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm
# chmod +x /etc/init.d/php-fpm
# service enable php-fpm.service
# service php-fpm restart
```

## 五、其他软件
### 5.1 Redis
安装
```
# wget http://download.redis.io/releases/redis-3.2.5.tar.gz
# tar zvxf redis-3.2.5.tar.gz
# cd redis-3.2.5
# make
# make install
# redis-server --version
```
修改配置
```
# mkdir -p /usr/local/redis
# cp /root/src/redis-3.2.5/redis.conf /usr/local/redis
# vim /usr/local/redis/redis.conf
...
bind 0.0.0.0
daemonize yes
dir /usr/local/redis
...
```

启动  
`# redis-server /usr/local/redis/redis.conf`

开机启动
```
vim /etc/rc.local
...
/usr/local/bin/redis-server /usr/local/redis/redis.conf
...
```
### 5.2 MongoDB
安装
```
# apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6 
##官方
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
##阿里云
$ echo "deb [ arch=amd64,arm64 ]https://mirrors.aliyun.com/mongodb/apt/ubuntuxenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
$ apt update
$ apt install -y mongodb-org
$ systemctl enable mongod.service
```

启动Mongo并设置root密码
```
# service mongod start
mongo
> use admin
> db.createUser({user:'root',pwd:'root',roles:['root']})
```

修改配置
```
# vim /etc/mongod.conf
...
net:
  port: 27017
  bindIp: 0.0.0.0

security:
  authorization: enabled
  transitionToAuth: false
...
```

重启服务：`#service mongod restart`

参考：https://docs.mongodb.com/master/tutorial/install-mongodb-on-ubuntu/


## 六、扩展
### 6.1 Redis
```
# wget http://pecl.php.net/get/redis-3.1.1.tgz
# tar zvxf redis-3.1.1.tgz
# cd redis-3.1.1
# phpize
# ./configure --with-php-config=/usr/local/php/bin/php-config
# make
# make test
# make install
# echo 'extension=redis.so' >> /usr/local/php/php.ini
```

### 6.2 MongoDB
```
# wget http://pecl.php.net/get/mongodb-1.3.0.tgz
# tar zvxf mongodb-1.3.0.tgz
# cd mongodb-1.3.0
# phpize
# ./configure --with-php-config=/usr/local/php/bin/php-config
# make
# make install
# echo 'extension=mongodb.so' >> /usr/local/php/php.ini
```

### 6.3 Swoole
```
# wget http://pecl.php.net/get/swoole-1.9.16.tgz
# phpize
# ./configure
# make
# make install
# echo 'extension=swoole.so' >> /usr/local/php/php.ini
```

### 6.4 xhprof
```
# git clone https://github.com/longxinH/xhprof
# cd xhprof/extension
# phpize
# ./configure --with-php-config=/usr/local/php/bin/php-config
# make
# make install
# echo '' >> /usr/local/php/php.ini
# echo '[xhprof]' >> /usr/local/php/php.ini
# echo 'extension=xhprof.so;' >> /usr/local/php/php.ini
# echo 'xhprof.output_dir=/tmp/xhprof' >> /usr/local/php/php.ini
# echo '' >> /usr/local/php/php.ini
```
拷贝目录下文件到项目中
`# cp -r xhprof_* /data/projects/xhprof/7/`

要使用xhprof的示例代码：
```
xhprof_enable();

//CODE

$xhprof_data = xhprof_disable();
include_once '/data/projects/xhprof/7/xhprof_lib/utils/xhprof_lib.php';
include_once '/data/projects/xhprof/7/xhprof_lib/utils/xhprof_runs.php';
$xhprof_runs = new XHProfRuns_Default();
$run_id = $xhprof_runs->save_run($xhprof_data, "xhprof_test");
echo 'http://local.xhprof.com/index.php?run=' . $run_id . '&source=xhprof_test';
```
查看图表时报错：failed to execute cmd: " dot -Tpng". stderr: sh: 1: dot: not found '
`apt install -y graphviz graphviz-dev`

### 6.5 Composer
```
# php -r "copy('https://install.phpcomposer.com/installer', 'composer-setup.php');"
# php composer-setup.php
# php -r "unlink('composer-setup.php');"
# mv composer.phar /usr/bin/composer
# chmod +x /usr/bin/composer
# composer config -g repo.packagist composer https://packagist.phpcomposer.com
```

## 七、Docker
```
# apt-get update
# apt-get install apt-transport-https ca-certificates

## 增加新的GPG 密钥
# apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
# echo 'deb http://apt.dockerproject.org/repo ubuntu-xenial main' > /etc/apt/sources.list.d/docker.list

## 重新执行更新操作，并删除老的repo
# apt update
# apt purge lxc-docker

## 查看是否有正确的可用版本
# apt-cache policy docker-engine
# apt upgrade

## 从14.04版本以上开始docker推荐安装linux-image-extra
# apt-get install linux-image-extra-$(uname -r)

# apt install docker-engine
# service docker start
```

配置 docker 加速器，镜像地址可自行网上获取，我这里是从阿里云镜像服务获取的。
```
# vim /etc/docker/daemon.json
...
{
  "registry-mirrors": ["https://xxxxxx.mirror.aliyuncs.com"]
}
```

安装 docker-compose
```
# apt install python-pip
# mkdir -p /root/.pip/
# vim /root/.pip/pip.conf
...
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
...

# pip install --upgrade pip
# pip install docker-compose
```

本地登录镜像服务，比如阿里云
`docker login --username=ruesin@xxxxxx.com registry.cn-beijing.aliyuncs.com`

## 八、其他

## 8.1 修改命令行样式
```
vim  ~/.bashrc
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
source ~/.bashrc
```
