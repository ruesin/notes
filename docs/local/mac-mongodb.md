---
title: Mac ox 使用 brew 安装mongodb 及 php mongodb 扩展
date: 2016-02-02 16:52:27
categories: 本地
---

<div>MongoDB 是一个基于分布式文件存储的数据库。由 C++ 语言编写。旨在为 WEB 应用提供可扩展的高性能数据存储解决方案。</div><div>MongoDB 是一个介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最像关系数据库的。他支持的数据结构非常松散，是类似json的bson格式，因此可以存储比较复杂的数据类型。</div><div>Mongo最大的特点是他支持的查询语言非常强大，其语法有点类似于面向对象的查询语言，几乎可以实现类似关系数据库单表查询的绝大部分功能，而且还支持对数据建立索引。</div><div>MongoDB的数据存储上，感觉有点想关系型数据库中的key=>value的数据格式。</div><div>和memcache或者redis差不多，mongodb也是分服务端和客户端的（相对）。用brew 来安装的话是非常方便的。</div><div></div><div>**一、安装mongodb服务。**</div><div>$ brew install mongodb</div><div>[![install_mongodb](/images/2016/02/install_mongodb.jpg)](/images/2016/02/install_mongodb.jpg)</div><div>然后就可以启动了</div><div>$ mongod #但是不加参数这样启动的会一直在终端运行着，无法停止或者退出终端。</div><div>[![mongod](/images/2016/02/mongod.jpg)](/images/2016/02/mongod.jpg)</div><div>看下mongod 的参数就明了了。</div><div>$ mongod –config /usr/local/etc/mongod.conf –fork –logappend</div><div>￼[![mongod_2](/images/2016/02/mongod_2.jpg)](/images/2016/02/mongod_2.jpg)</div><div>**二、php 的 mongodb 扩展** </div><div>search一下就会发现有两个，经过试验，我们要安装php56-mongo。</div><div>$ brew install php56-mongo</div><div>[![install_php_mongo](/images/2016/02/install_php_mongo.jpg)](/images/2016/02/install_php_mongo.jpg)</div><div>然后重启php-fpm和nginx就可以了。</div>
