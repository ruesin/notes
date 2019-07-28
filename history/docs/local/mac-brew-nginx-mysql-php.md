---
title: Mac 下Brew 安装 Nginx+mysq+php
date: 2016-02-02 11:25:30
categories: 本地
---

自己编译安装环境失败后，就换成了brew安装，感觉跟Ubuntu中的apt-get差不多的样子，虽然不是自己喜欢的方式，但是目前为止也只能先这么安装了，当然、后续扩展什么的确实方便快捷。

安装的时候，根据自己的网络环境，有可能会要用到梯子，这个要自己想办法了。

**安装nginx**

```
$ brew install nginx
==> Installing dependencies for nginx: pcre, openssl
==> Installing nginx dependency: pcre
==> Downloading https://homebrew.bintray.com/bottles/pcre-8.38.el_capitan.bottle.tar.gz
######################################################################## 100.0%
==> Pouring pcre-8.38.el_capitan.bottle.tar.gz
 /usr/local/Cellar/pcre/8.38: 146 files, 5.4M
==> Installing nginx dependency: openssl
==> Downloading https://homebrew.bintray.com/bottles/openssl-1.0.2e.el_capitan.bottle.tar.gz
######################################################################## 100.0%
==> Pouring openssl-1.0.2e.el_capitan.bottle.tar.gz
==> Caveats
A CA file has been bootstrapped using certificates from the system
keychain. To add additional certificates, place .pem files in
/usr/local/etc/openssl/certs

and run
/usr/local/opt/openssl/bin/c_rehash

This formula is keg-only, which means it was not symlinked into /usr/local.

Apple has deprecated use of OpenSSL in favor of its own TLS and crypto libraries

Generally there are no consequences of this for you. If you build your
own software and it requires this formula, you'll need to add to your
build variables:

LDFLAGS: -L/usr/local/opt/openssl/lib
CPPFLAGS: -I/usr/local/opt/openssl/include

==> Summary
 /usr/local/Cellar/openssl/1.0.2e: 465 files, 11.9M
==> Installing nginx
==> Downloading https://homebrew.bintray.com/bottles/nginx-1.8.0.el_capitan.bottle.1.tar.gz
######################################################################## 100.0%
==> Pouring nginx-1.8.0.el_capitan.bottle.1.tar.gz
==> Caveats
Docroot is: /usr/local/var/www

The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /usr/local/etc/nginx/servers/.

To have launchd start nginx at login:
ln -sfv /usr/local/opt/nginx/*.plist ~/Library/LaunchAgents
Then to load nginx now:
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.nginx.plist
Or, if you don't want/need launchctl, you can just run:
nginx
==> Summary
 /usr/local/Cellar/nginx/1.8.0: 7 files, 940K

$ sudo nginx ##启动Nginx
```

**安装Mysql**

```
$ brew install mysql
==> Downloading https://homebrew.bintray.com/bottles/mysql-5.7.10.el_capitan.bottle.1.tar.gz
######################################################################## 100.0%
==> Pouring mysql-5.7.10.el_capitan.bottle.1.tar.gz
==> /usr/local/Cellar/mysql/5.7.10/bin/mysqld --initialize-insecure --user=sin --basedir=/usr/local/Cellar/mysql/5.7.10 --datadir=/usr/local/var/mysql --tmpdir=/tmp
==> Caveats
We've installed your MySQL database without a root password. To secure it run:
mysql_secure_installation

To connect run:
mysql -uroot

To have launchd start mysql at login:
ln -sfv /usr/local/opt/mysql/*.plist ~/Library/LaunchAgents
Then to load mysql now:
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
Or, if you don't want/need launchctl, you can just run:
mysql.server start
==> Summary
 /usr/local/Cellar/mysql/5.7.10: 12,677 files, 433.2M

$ /usr/local/opt/mysql/bin/mysql_install_db
2016-01-11 10:41:04 [WARNING] mysql_install_db is deprecated. Please consider switching to mysqld --initialize
2016-01-11 10:41:04 [ERROR] The data directory needs to be specified.

$ /usr/local/opt/mysql/bin/mysql_secure_installation #设置root密码
$ mysql -uroot -p
$ ps aux | grep mysql
```

**安装php**

添加源

```
$ brew tap homebrew/dupes
$ brew tap josegonzalez/homebrew-php
```

查看安装的选项

`$ brew options php56`$ xcode-select –install ## 非必要  
根据自己需要，带参数安装。中间的过程就不罗列出来了，因为网络的原因，反复中断了好几次才安装好。

`$ brew install php56 --with-fpm --with-gmp --with-imap --with-tidy --with-debug --with-mysql --with-libmysql`执行以下命令将新安装的PHP加入到环境变量，顶替掉系统自带的。

```
echo 'export PATH="$(brew --prefix php56)/bin:$PATH"' >> ~/.bash_profile #for php
echo 'export PATH="$(brew --prefix php56)/sbin:$PATH"' >> ~/.bash_profile #for php-fpm
echo 'export PATH="/usr/local/bin:/usr/local/sbib:$PATH"' >> ~/.bash_profile #for other brew install soft
```

或者直接编辑配置文件

```
$ sudo vim ~/.bash_profile
export PAH="$(brew --prefix php56)/bin:$PAH"
export PAH="$(brew --prefix php56)/sbin:$PAH"
export PAH="/usr/local/bin:/usr/local/sbin:$PAH"

$ source ~/.bash_profile
$ echo $PAH
/usr/local/bin:/usr/local/sbin:/usr/local/opt/php56/sbin:/usr/local/opt/php56/bin:/Users/sin/bin:/usr/local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

```
$ php-fpm -D
$ sudo killall php-fpm
```

至此三个部分都安装好了，剩下的就是各种修改配置文件了，这个跟正常编译安装时一样的。可以参考之前的编译安装配置。

参考网址：

http://segmentfault.com/a/1190000002980386

http://segmentfault.com/q/1010000000094627

http://segmentfault.com/a/1190000000606752

http://segmentfault.com/q/1010000002895310

http://segmentfault.com/q/1010000004137098?sort=created

http://segmentfault.com/n/1330000004162906

http://segmentfault.com/a/1190000002963355

http://segmentfault.com/q/1010000004137098?sort=created
