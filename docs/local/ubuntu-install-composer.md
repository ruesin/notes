---
title: Ubuntu 下 安装 composer
date: 2016-01-04 19:34:24
categories: 本地
tags: 
- ubuntu
- ubuntu web环境
- composer
- ubuntu memcache
---

Composer提供了一个非常方便的安装程序，Ubuntu下可以很简单的在命令行下载。可以免费下载（https://getcomposer.org/installer），感兴趣的同学可以去Github上看下它的工作原理，是纯PHP的源。

基本的两种方式

curl -sS https://getcomposer.org/installer | php

php -r “readfile(‘https://getcomposer.org/installer’);” | php

在工作目录下使用 php composer.phar 命令就可以运行Composer了。

但是这样实在是不够方便，总不能每个项目目录下都拷贝一份吧。

mv composer.phar /usr/local/bin/composer

将可执行文件移动到任意一个全局变量目录下，就可以在系统中全局使用了。

当然，也可以在下载安装的时候加一些参数，直接安装到命令目录下。

curl -sS https://getcomposer.org/installer | sudo php — –install-dir=/usr/local/bin –filename=composer

–install-dir 定义安装的目录。  
–filename 更改文件名称。

然后就可以全局使用 composer 替代 php composer.phpar 了。

至于，有时候会被墙的事儿，可以更改配置中国镜像，也可以修改hosts，或者直接上梯子了。

更新composer，经常用到。  
sudo composer self-update

查看状态  
composer -version

文档：

https://getcomposer.org/doc/00-intro.md

https://github.com/5-say/composer-doc-cn/blob/master/cn-introduction/04-schema.md#minimum-stability
