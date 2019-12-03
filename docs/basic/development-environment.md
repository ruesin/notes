---
title: 本地开发环境
date: 2016-07-15 13:15:51
categories: 基础
---

基于VMware12 + CentOS 6.5 的解决方案，共享项目，宿主机办公、虚拟机提供服务。

## 一、系统

1. 安装

   选择英文版，minimal安装，磁盘20G。

2. 配置网络

   VMware虚拟机网络连接方式采用NAT方式
   ```
   # vi /etc/sysconfig/network-script/ifcfg-eth0
   NM_CONTROLLED="no" # 是否依赖Network Manager的控制，minimal没装，设为no 
   ONBOOT="yes" # 开机启动
   # reboot
   # ifconfig #查看IP，使用xshell连接
   ```

3. 软件库

   ```
   yum -y install vim wget gcc gcc-c++
   ```

4. 防火墙配置

   ```
   # vim /etc/sysconfig/iptables
   -A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT #允许80端口通过防火墙 
   -A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT #允许3306端口通过防火墙 
   # /etc/init.d/iptables restart
   ```

   或者：

   ```
   /sbin/iptables -I INPUT -p tcp --dport 80 -j ACCEPT 
   /etc/rc.d/init.d/iptables save #保存： 
   /etc/init.d/iptables restart #重启防火墙 
   /etc/init.d/iptables status #查看CentOS防火墙信息 
   /etc/init.d/iptables stop #关闭CentOS防火墙服务 
   chkconfig --level 35 iptables off #永久关闭防火墙 
   ```

5. 关闭SELINUX

   ```
   # vim /etc/selinux/config
   SELINUX=enforcing #注释掉
   SELINUXTYPE=targeted #注释掉
   SELINUX=disabled #增加 
   shutdown -r now #重启系统 
   ```

   > 不关会影响MySQL启动：http://blog.csdn.net/zalion/article/details/9274263 




## 二、环境

### 1.资源包下载

```
# wget http://nginx.org/download/nginx-1.10.0.tar.gz 
# wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.38.tar.gz 
# wget http://zlib.net/zlib-1.2.10.tar.gz
# wget https://www.openssl.org/source/openssl-1.0.1u.tar.gz #1.10有bug 
# wget http://museum.php.net/php5/php-5.6.22.tar.gz 
# wget http://cdn.mysql.com/archives/mysql-5.6/mysql-5.6.12-linux-glibc2.5-x86_64.tar.gz
```

### 2. Nginx

```
# tar -zvxf pcre-8.38.tar.gz 
# tar -zvxf zlib-1.2.10.tar.gz 
# tar zvxf openssl-1.0.1u.tar.gz

# groupadd www 
# useradd -g www www -s /bin/false

# tar zvxf nginx-1.10.0.tar.gz
# ./configure --user=www --group=www --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module --with-http_realip_module --with-pcre=/root/src/pcre-8.38 --with-zlib=/root/src/zlib-1.2.10 --with-openssl=/root/src/openssl-1.0.1u
# make 
# make install 
# /usr/local/nginx/sbin/nginx #启动

# echo "/usr/local/nginx/sbin/nginx" >> /etc/rc.local #开机启动

# netstat -ano|grep 80 
```

> make[2]: Leaving directory `/root/src/openssl-1.0.1u'
> Operating system: x86_64-whatever-linux2
> You need Perl 5.
> make[1]: *** [/root/src/openssl-1.0.1u/.openssl/include/openssl/ssl.h] Error 1
> make[1]: Leaving directory `/root/src/nginx-1.10.0'
> make: *** [build] Error 2

```
# yum install -y perl
```

### 3.Mysql

```
# tar -zvxf mysql-5.6.12-linux-glibc2.5-x86_64.tar.gz

# groupadd mysql #添加mysql组 
# useradd -g mysql mysql -s /bin/false #创建用户mysql并加入到mysql组，不允许mysql用户直接登录系统

# mv mysql-5.6.12-linux-glibc2.5-x86_64 /usr/local/mysql

# cd /usr/local/mysql/ 
# chown -R mysql.mysql .

# ./scripts/mysql_install_db --user=mysql
```

> Installing MySQL system tables..../bin/mysqld: error while loading shared libraries: libaio.so.
>
> 1: cannot open shared object file: No such file or directory

```
# yum install -y libaio
```
```
# ./scripts/mysql_install_db --user=mysql
# vim ./my.cnf
datadir = /usr/local/mysql/data

# cp ./support-files/mysql.server /etc/rc.d/init.d/mysqld #把Mysql加入系统服务
# chkconfig mysqld on #开机启动 ##/sbin/chkconfig --del mysqld /sbin/chkconfig --add mysqld

# vim /etc/profile #把mysql服务加入系统环境变量
export PATH=$PATH:/usr/local/mysql/bin
# source /etc/profile
```

设置Mysql密码：

```
# ./bin/mysql_secure_installation
```

> ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)
>
> 由于mysql 默认的mysql.sock 是在/var/lib/mysql/mysql.sock，但Linux系统总是去/tmp/mysql.sock查找，所以会报错，可以在my.cnf中指定，也可以为mysql.sock增加软连接。http://blog.csdn.net/wyzxg/article/details/4720041

```
# service mysqld stop 
# ln -s /var/lib/mysql/mysql.sock /tmp/mysql.sock 
# service mysqld start
# ./bin/mysql_secure_installation
```

设置远程可访问：

```
# mysql -u root -p 
mysql> use mysql; 
mysql> UPDATE user SET `host`='%' WHERE `user`='root' AND `host`='localhost';
mysql> exit;
# service mysqld restart
```

查看运行状态：

```
# /etc/rc.d/init.d/mysqld status 
# ps -A | grep -i mysql 
```

### 4.PHP

```
# yum -y install libmcrypt-devel mhash-devel libxslt-devel libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel
```

> No package libmcrypt-devel available.
> No package mhash-devel available.

安装依赖：

```
# wget http://downloads.sourceforge.net/mcrypt/libmcrypt-2.5.8.tar.gz 
# wget http://downloads.sourceforge.net/mcrypt/mcrypt-2.6.8.tar.gz 
# wget http://downloads.sourceforge.net/mhash/mhash-0.9.9.9.tar.gz
# tar -zxvf libmcrypt-2.5.8.tar.gz 
# cd libmcrypt-2.5.8 
# ./configure 
# make 
# make install 
# tar -zxvf mhash-0.9.9.9.tar.gz 
# cd mhash-0.9.9.9 
# ./configure 
# make 
# make install 
# tar -zxvf mcrypt-2.6.8.tar.gz 
# cd mcrypt-2.6.8 
# LD_LIBRARY_PATH=/usr/local/lib ./configure #指定libmcrypt目录并配置 
> /bin/rm: cannot remove `libtoolT': No such file or directory
# make 
# make install 
# yum list installed|grep mcrypt #检查是否安装成功
```

编译：

```
 # tar zvxf php-5.6.22.tar.gz
 # ./configure --prefix=/usr/local/php --enable-fpm --with-mysql=mysqlnd \
--with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd --with-config-file-path=/usr/local/php  \
--with-iconv --enable-pcntl --enable-shmop --enable-simplexml --enable-ftp --enable-zip --enable-soap --with-curl \
--with-openssl --enable-mbstring  --with-zlib --enable-xml \
--enable-sockets --enable-inline-optimization \
--with-png-dir --with-freetype-dir --with-gd --with-jpeg-dir \
--enable-bcmath --with-mcrypt 
# make
# make test
# make install
```

> configure: error: Cannot find OpenSSL's <evp.h>

```
# yum install -y openssl openssl-devel
```

> configure: error: Please reinstall the libcurl distribution -
> easy.h should be in <curl-dir>/include/curl/

```
# yum -y install curl-devel
```

配置：

```
# cp ./php.ini-development /usr/local/php/php.ini
# cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf
# cd /usr/local/php/
# vim ./etc/php-fpm.conf
  user = www
  group = www

# /usr/local/php/sbin/php-fpm #启动
# kill -INT cat /usr/local/php/var/run/php-fpm.pid #关闭
# kill -USR2 cat /usr/local/php/var/run/php-fpm.pid #重启

# echo "/usr/local/php/sbin/php-fpm" >> /etc/rc.local ## php-fpm 开机启动

# vim ./php.ini
cgi.fix_pathinfo=0 # 0：如果文件不存在，则阻止 Nginx 将请求发送到后端的 PHP-FPM 模块，以避免遭受恶意脚本注入的攻击。
date.timezone = PRC

# ps aux | grep php-fpm
# kill -USR2 进程号
```




### 5. 配置

#### 5.1 Nginx + PHP

```
# cd /usr/local/nginx/conf/
# mkdir vhost
# vim nginx.conf
user  www;
include  vhost/*.conf;
# vim vhost/test.conf
server {
        listen       80;
        server_name  cent.test.com;

        error_log /usr/local/nginx/logs/test.error.log;
        root  /data/html/test;
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
```

```
# mkdir -p /data/html/test
# vim /data/html/test/index.php
# /usr/local/nginx/sbin/nginx -s reload
```



### 6. 日志

#### 6.1 PHP

```
Installing shared extensions:     /usr/local/php/lib/php/extensions/no-debug-non-zts-20131226/
Installing PHP CLI binary:        /usr/local/php/bin/
Installing PHP CLI man page:      /usr/local/php/php/man/man1/
Installing PHP FPM binary:        /usr/local/php/sbin/
Installing PHP FPM config:        /usr/local/php/etc/
Installing PHP FPM man page:      /usr/local/php/php/man/man8/
Installing PHP FPM status page:   /usr/local/php/php/php/fpm/
Installing PHP CGI binary:        /usr/local/php/bin/
Installing PHP CGI man page:      /usr/local/php/php/man/man1/
Installing build environment:     /usr/local/php/lib/php/build/
Installing header files:           /usr/local/php/include/php/
Installing helper programs:       /usr/local/php/bin/
  program: phpize
  program: php-config
Installing man pages:             /usr/local/php/php/man/man1/
  page: phpize.1
  page: php-config.1
Installing PEAR environment:      /usr/local/php/lib/php/
[PEAR] Archive_Tar    - installed: 1.4.0
[PEAR] Console_Getopt - installed: 1.4.1
[PEAR] Structures_Graph- installed: 1.1.1
[PEAR] XML_Util       - installed: 1.3.0
[PEAR] PEAR           - installed: 1.10.1
Wrote PEAR system config file at: /usr/local/php/etc/pear.conf
You may want to add: /usr/local/php/lib/php to your php.ini include_path
/root/src/php-5.6.22/build/shtool install -c ext/phar/phar.phar /usr/local/php/bin
ln -s -f phar.phar /usr/local/php/bin/phar
Installing PDO headers:           /usr/local/php/include/php/ext/pdo/
```

#### 6.2 Mysql

```
To start mysqld at boot time you have to copy
support-files/mysql.server to the right place for your system

PLEASE REMEMBER TO SET A PASSWORD FOR THE MySQL root USER !
To do so, start the server, then issue the following commands:

  ./bin/mysqladmin -u root password 'new-password'
  ./bin/mysqladmin -u root -h test.cent password 'new-password'

Alternatively you can run:

  ./bin/mysql_secure_installation

which will also give you the option of removing the test
databases and anonymous user created by default.  This is
strongly recommended for production servers.

See the manual for more instructions.

You can start the MySQL daemon with:

  cd . ; ./bin/mysqld_safe &

You can test the MySQL daemon with mysql-test-run.pl

  cd mysql-test ; perl mysql-test-run.pl

Please report any problems with the ./bin/mysqlbug script!

The latest information about MySQL is available on the web at

  http://www.mysql.com

Support MySQL by buying support/licenses at http://shop.mysql.com

WARNING: Found existing config file ./my.cnf on the system.
Because this file might be in use, it was not replaced,
but was used in bootstrap (unless you used --defaults-file)
and when you later start the server.
The new default config file was created as ./my-new.cnf,
please compare it with your file and take the changes you need.

WARNING: Default config file /etc/my.cnf exists on the system
This file will be read by default by the MySQL server
If you do not want to use this, either remove it, or use the
--defaults-file argument to mysqld_safe when starting the server
```



## 三、其他

### 1. 自动登录

```
# vim /etc/inittab
id:5:initdefault: 改为 id:3:initdefault:
# vim /etc/init/tty.conf
exec /sbin/mingetty $TTY 改为 exec /sbin/mingetty --autologin=root $TTY
```

参考：http://blog.csdn.net/kpshare/article/details/7523546



### 2. 隐藏VMware任务栏窗口

1. Windows 自动启动 VMware Authorization Service服务。
2. 虚拟机→编辑→首选项→工作区→勾选“Workstation 关闭后保持虚拟机运行”。




### 3. 文件共享

#### 1. 宿主机共享目录给虚拟机

1. 虚拟机→安装 Vmware Tools
2. 开启虚拟机 

```
# mkdir /mnt/cdrom
# mount /dev/cdrom /mnt/cdrom 

# cd /tmp
# mkdir tmp
# cd tmp
# tar zvxf /mnt/cdrom/VMwareTools-10.0.10-4301679.tar.gz
# cd vmware-tools-distrib
# ./vmware-install.pl
# shutdown -h now
```

3. 设置虚拟机，选项中添加共享目录，开机。

```
# ll /mnt/hgfs
# ln -s /mnt/hgfs/htdocs/ ~/projects
#ln -s /mnt/hgfs/share ~/share
```

#### 2. 虚拟机共享目录给宿主机

...



### 4. 升级SVN 

```
# vim /etc/yum.repos.d/wandisco-svn.repo #添加源
[WandiscoSVN]
name=Wandisco SVN Repo
baseurl=http://opensource.wandisco.com/centos/$releasever/svn-1.8/RPMS/$basearch/
enabled=1
gpgcheck=0

# yum remove subversion*
# yum clean all
# yum install subversion
```



### 5. zsh

```
# echo $SHELL
# cat /etc/shells

# yum -y install zsh
# chsh -s /bin/zsh 

# git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
# cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
或
# wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh

# reboot
```

> warning: cannot set LC_CTYPE locale

```
# vim /etc/profile
export LC_ALL=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8
```



### 6. git

#### 1. 配置

```
/etc/gitconfig
~/.gitconfig
/pathtoproject/.git/config

# git config --global user.name "Ruesin"
# git config --global user.email ruesin@gmail.com

# git config user.email ruesin@163.com

# git config --global core.editor emacs 
# git config --global merge.tool vimdiff
//kdiff3,tkdiff,meld,xxdiff,emerge,vimdiff,gvimdiff,ecmerge,opendiff

# git config --list
# git config user.name

```

#### 2. 忽略
```
# vim .gitignore

# 忽略*.o和*.a文件
*.[oa]
# 忽略*.b和*.B文件，my.b除外
*.[bB]
!my.b
# 忽略dbg文件和dbg目录
dbg
# 只忽略dbg目录，不忽略dbg文件
dbg/
# 只忽略dbg文件，不忽略dbg目录
dbg
!dbg/
# 只忽略当前目录下的dbg文件和目录，子目录的dbg不在忽略范围内
/dbg

# git rm -r --cached app/test.php
```


