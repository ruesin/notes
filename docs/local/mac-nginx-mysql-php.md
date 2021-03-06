---
title: Mac OX 编译安装 Nginx  + Mysql + PHP （失败记录）
date: 2016-02-01 14:18:54
categories: 本地
tags: 
- php
- mac
- mac ox
- mac 终端
- mac php
---

先说一下，最后PHP编译的时候出了点状况，导致最后编译失败，使用的brew安装。

源码编译安装时需要gcc、make等工具，可以在安装xcode，默认就会安装上这些工具。安装结束后启动XCode，然后到XCode->Preferences->Downloads里，选择component，安装“Command Line Tools”就可以了。这样以后就可以方便地在Terminal里make了。

**编译 Nginx**

配置的时候，不需要分别编译三个模块，只需要解压，并在nginx配置中写对应的路径即可。

`$ sudo ./configure --user=_www --group=_www --prefix=/usr/local/nginx --with-http_stub_status_module --with-zlib=/Users/sin/mac/zlib-1.2.8 --with-openssl=/Users/sin/mac/openssl-1.0.1c --with-pcre="/Users/sin/mac/pcre-8.35" --with-http_dav_module --with-http_flv_module --with-http_gzip_static_module --with-mail --with-mail_ssl_module --with-http_ssl_module --with-http_realip_module````
/usr/bin/perl obj_dat.pl obj_mac.h obj_dat.h
/usr/bin/perl objxref.pl obj_mac.num obj_xref.txt > obj_xref.h
cc -I.. -I../.. -I../modes -I../asn1 -I../evp -I../../include -DDSO_DLFCN -DHAVE_DLFCN_H -arch x86_64 -O3 -DL_ENDIAN -Wall -DOPENSSL_IA32_SSE2 -DOPENSSL_BN_ASM_MONT -DOPENSSL_BN_ASM_MONT5 -DOPENSSL_BN_ASM_GF2m -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DMD5_ASM -DAES_ASM -DVPAES_ASM -DBSAES_ASM -DWHIRLPOOL_ASM -DGHASH_ASM -c -o o_names.o o_names.c
o_names.c:76:24: warning: equality comparison with extraneous parentheses [-Wparentheses-equality]
if ((name_funcs_stack == NULL))
~~~~~~~~~~~~~~~~~^~~~~~~
o_names.c:76:24: note: remove extraneous parentheses around the comparison to silence this warning
if ((name_funcs_stack == NULL))
~ ^ ~
o_names.c:76:24: note: use '=' to turn this equality comparison into an assignment
if ((name_funcs_stack == NULL))
^~
=
1 warning generated.
```

经分析，应该是openssl版本的问题，换了另外一个版本。

`$ sudo ./configure --user=_www --group=_www --prefix=/usr/local/nginx --with-http_stub_status_module --with-zlib=/Users/sin/mac/zlib-1.2.8 --with-openssl=/Users/sin/mac/openssl-1.0.1q --with-pcre="/Users/sin/mac/pcre-8.35" --with-http_dav_module --with-http_flv_module --with-http_gzip_static_module --with-mail --with-mail_ssl_module --with-http_ssl_module --with-http_realip_module````
$ sudo make

Operating system: i686-apple-darwinDarwin Kernel Version 15.2.0: Fri Nov 13 19:56:56 PST 2015; root:xnu-3248.20.55~2/RELEASE_X86_64
WARNING! If you wish to build 64-bit library, then you have to
invoke './Configure darwin64-x86_64-cc' *manually*.
You have about 5 seconds to press Ctrl-C to abort.
Configuring for darwin-i386-cc
Configuring for darwin-i386-cc
Doing certs/demo
WARNING: can't open config file: /Users/sin/Documents/source/mac/nginx-1.5.1/../openssl-1.0.1q/.openssl/ssl/openssl.cnf
ca-cert.pem => 3f77a2b5.0
WARNING: can't open config file: /Users/sin/Documents/source/mac/nginx-1.5.1/../openssl-1.0.1q/.openssl/ssl/openssl.cnf
dsa-ca.pem => cbdbd8bc.0
WARNING: can't open config file: /Users/sin/Documents/source/mac/nginx-1.5.1/../openssl-1.0.1q/.openssl/ssl/openssl.cnf
dsa-pca.pem => de4fa23b.0
WARNING: can't open config file: /Users/sin/Documents/source/mac/nginx-1.5.1/../openssl-1.0.1q/.openssl/ssl/openssl.cnf
bjs/ngx_modules.o \
../pcre-8.35/.libs/libpcre.a ../openssl-1.0.1q/.openssl/lib/libssl.a ../openssl-1.0.1q/.openssl/lib/libcrypto.a ../zlib-1.2.8/libz.a
ld: warning: ld: warning: ignoring file ../openssl-1.0.1q/.openssl/lib/libcrypto.a, file was built for archive which is not the architecture being linked (x86_64): ../openssl-1.0.1q/.openssl/lib/libcrypto.aignoring file ../openssl-1.0.1q/.openssl/lib/libssl.a, file was built for archive which is not the architecture being linked (x86_64): ../openssl-1.0.1q/.openssl/lib/libssl.a
```

这个问题应该是 openssl/config脚本猜对你的系统是64位，但是会根据$KERNEL\_BITS来判断是否开启x86\_64编译，默认是不开启的(很奇怪的设置，虽然会给你5秒时间停止编译并手动开启)，所以你生成的openssl库文件是32位的，最后静态链接到nginx会出错。目前看来没有很好的方法把x86\_64的参数传到openssl配置文件中 (openssl/config 猜测os架构，设置编译的参数是32位还是64位，默认是32位，然后调用openssl/Configure生成Makefile)

可以在configure之前export KERNEL\_BITS=64，如果还是不起作用就要手到修改了

手动修改 objs/Makefile:

`./config –prefix=/Users/xxx/Downloads/openssl-1.0.1e/.openssl no-shared no-threads`改成

`./Configure darwin64-x86_64-cc –prefix=/Users/xxx/Downloads/openssl-1.0.1e/.openssl no-shared no-threads`再次编译安装即可

```
$sudo make
$ sudo make install
$ sudo /usr/local/nginx/sbin/nginx #启动nginx
```

为了方便可以创建个软连接，或者添加环境变量。

```
sudo ln -s /usr/local/nginx/sbin/nginx /usr/local/bin/nginx #创建软连
export PATH=/usr/local/nginx/sbin/nginx:/usr/local/bin:/usr/local/sbin:$PATH # ~/.bash_profile 中添加环境变量
```

```
sudo nginx
sudo nginx -s stop
sudo nginx -V 查看编译时候的参数
sudo nginx #不指定配置文件地址启动nginx
sudo nginx -c /usr/local/nginx/nginx.conf #指定配置文件地址启动nginx
sudo nginx -t #检测配置文件
sudo nginx -s reload #重新加载配置文件(不停止服务)
```

编译Mysql

```
$ sudo mv mysql-5.6.28-osx10.10-x86_64 /usr/local/mysql
$ cd /usr/local/mysql
$ sudo chown -R _mysql .
$ sudo chgrp -R _mysql .
$ sudo scripts/mysql_install_db --user=_mysql # 初始化(创建默认配置文件、授权表等)
```

初始化的时候有可能会报错。

```
[Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).

$ vi my.cnf
[mysqld]
explicit_defaults_for_timestamp=true
```

```
$ sudo ./support-files/mysql.server start # 启动
$ sudo ./support-files/mysql.server restart # 重启
$ sudo ./support-files/mysql.server stop # 停止
$ sudo ./support-files/mysql.server status # 检查 MySQL 运行状态
```

```
$ sudo ln -s /usr/local/mysql/support-files/mysql.server /usr/local/bin/mysqld
$ sudo mysqld stop
$ sudo mysqld start
```

```
$ sudo /usr/local/mysql/bin/mysql_secure_installation # 设置root密码
$ ./bin/mysql -uroot -p
```

```
$ sudo ln -s /usr/local/mysql/bin/mysql /usr/local/bin/mysql
或者设置环境变量：
$ vi ~/.bash_profile
$ export PATH="/usr/local/mysql/bin:$PATH"
$ source ~/.bash_profile

$ mysql -uroot -p
```

编译PHP

Zlib

`$ sudo ./configure --prefix=/usr/local/webserver/zlib`OpenSSL

```
$ sudo ./config --help

Operating system: i686-apple-darwinDarwin Kernel Version 15.2.0: Fri Nov 13 19:56:56 PST 2015; root:xnu-3248.20.55~2/RELEASE_X86_64
WARNING! If you wish to build 64-bit library, then you have to
invoke './Configure darwin64-x86_64-cc' *manually*.
You have about 5 seconds to press Ctrl-C to abort.
Configuring for darwin-i386-cc
Usage: Configure [no- ...] [enable- ...] [experimental- ...] [-Dxxx] [-lxxx] [-Lxxx] [-fxxx] [-Kxxx] [no-hw-xxx|no-hw] [[no-]threads] [[no-]shared] [[no-]zlib|zlib-dynamic] [no-asm] [no-dso] [no-krb5] [sctp] [386] [--prefix=DIR] [--openssldir=OPENSSLDIR] [--with-xxx[=vvv]] [--test-sanity] os/compiler[:flags]

$ sudo ./Configure darwin64-x86_64-cc --prefix=/usr/local/webserver/openssl
$ make install ## 报错 执行下面的
$ sudo make install_sw
```

Jpeg

`$ sudo ./configure --prefix=/usr/local/webserver/jpeg --enable-shared --enable-static`png

`$ sudo ./configure --prefix=/usr/local/webserver/png`freetype

```
$ sudo ./configure --prefix=/usr/local/webserver/freetype

warning: using extended field designator is an extension [-Wextended-offsetof]
make: Nothing to be done for `unix'.

$ cd builds/unix/
$ sudo ./configure --prefix=/usr/local/webserver/freetype --enable-shared
$ cd ../../
$ sudo make
```

libmcrypt

```
$ sudo ./configure --prefix=/usr/local/webserver/libmcrypt

8 warnings generated.
/bin/sh ../libtool --tag=CC --mode=link gcc -g -O2 -o aestest aes_test.o ../lib/libmcrypt.la
gcc -g -O2 -o .libs/aestest aes_test.o ../lib/.libs/libmcrypt.dylib
creating aestest
Making all in doc
make[2]: Nothing to be done for `all'.
make[2]: Nothing to be done for `all-am'.
#实在不知道什么错，硬着头皮编译安装了。

$ cd libltdl/
$ sudo ./configure --prefix=/usr/local/webserver/libltdl --enable-ltdl-install
```

mhash

`$ sudo ./configure --prefix=/usr/local/webserver/mhash`mcrypt

```
$ sudo ./configure --prefix=/usr/local/webserver/mcrypt --with-libmcrypt-prefix=/usr/local/webserver/libmcrypt/

configure: error: "You need at least libmhash 0.8.15 to compile this program. http://mhash.sf.net/"

$ su root
$ export LDFLAGS="-L/usr/local/webserver/mhash/lib -L/usr/lib"
$ export CFLAGS="-I/usr/local/webserver/mhash/include -I/usr/include"
$ ./configure --prefix=/usr/local/webserver/mcrypt --with-libmcrypt-prefix=/usr/local/webserver/libmcrypt/

rm: libtoolT: No such file or directory

## 就是从这开始往下，磕磕绊绊了。

$ make

rfc2440.c:26:10: fatal error: 'malloc.h' file not found

$ touch malloc.h

22 warnings generated.

/bin/sh ../libtool --tag=CC --mode=link gcc -I/usr/local/webserver/mhash/include -I/usr/include -I/usr/local/webserver/libmcrypt//include -I/usr/local/webserver/libmcrypt/include -Wall -L/usr/local/webserver/mhash/lib -L/usr/lib -o mcrypt extra.o mcrypt.o keys.o random.o rndunix.o xmalloc.o functions.o errors.o bits.o openpgp.o rndwin32.o environ.o getpass.o ufc_crypt.o popen.o classic.o rfc2440.o gaaout.o -lz -lmhash -L/usr/local/webserver/libmcrypt/lib -lmcrypt
libtool: link: gcc -I/usr/local/webserver/mhash/include -I/usr/include -I/usr/local/webserver/libmcrypt//include -I/usr/local/webserver/libmcrypt/include -Wall -o mcrypt extra.o mcrypt.o keys.o random.o rndunix.o xmalloc.o functions.o errors.o bits.o openpgp.o rndwin32.o environ.o getpass.o ufc_crypt.o popen.o classic.o rfc2440.o gaaout.o -L/usr/local/webserver/mhash/lib -L/usr/lib -lz /usr/local/webserver/mhash/lib/libmhash.dylib -L/usr/local/webserver/libmcrypt/lib /usr/local/webserver/libmcrypt/lib/libmcrypt.dylib
Making all in po
make[2]: Nothing to be done for `all'.
make[2]: Nothing to be done for `all-am'.
/Applications/Xcode.app/Contents/Developer/usr/bin/make install-exec-hook
/bin/rm -f /usr/local/webserver/mcrypt/bin/mdecrypt
ln -s mcrypt /usr/local/webserver/mcrypt/bin/mdecrypt
make[2]: Nothing to be done for `install-data-am'.
```

libiconv

`$ sudo ./configure --prefix=/usr/local/webserver/libiconv`PHP

```
# --with-curl --enable-zip
sudo ./configure --prefix=/usr/local/php --enable-fpm --with-mysql=/usr/local/mysql --with-mysqli=/usr/local/mysql/bin/mysql_config --with-config-file-path=/usr/local/php --with-openssl=/usr/local/webserver/openssl --enable-mbstring --with-zlib=/usr/local/webserver/zlib --enable-xml --with-png-dir=/usr/local/webserver/png --with-freetype-dir=/usr/local/webserver/freetype --with-gd --with-jpeg-dir=/usr/local/webserver/jpeg --enable-bcmath --with-mcrypt=/usr/local/webserver/libmcrypt --with-iconv=/usr/local/webserver/libiconv --enable-pcntl --enable-shmop --enable-simplexml --enable-ftp --enable-opcache=no

ld: symbol(s) not found for architecture x86_64
clang: error: linker command failed with exit code 1 (use -v to see invocation)
make: *** [sapi/cli/php] Error 1
```

\## sudo make ZEND\_EXRA\_LIBS=’-liconv’

最后实在是没整好，而且当时比较急，就直接放弃编译了，以后有机会会再次试试的。

源码包链接：

Pcre：http://www.pcre.org/  
Zlib：http://zlib.net  
openssl：http://openssl.org/  
nginx：http://nginx.org/en/download.html  
Mysql：http://dev.mysql.com/downloads/mysql/  
GD库：https://bitbucket.org/libgd/gd-libgd/downloads/libgd-2.1.0.tar.gz  
freetype：http://sourceforge.net/projects/freetype/  
libpng：http://www.libpng.org/pub/png/libpng.html  
libjpeg：http://www.ijg.org/  
curl： http://curl.haxx.se/download.html  
mhash： http://sourceforge.net/projects/mhash/  
mcrypt: http://mcrypt.hellug.gr/
