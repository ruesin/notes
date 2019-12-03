---
title: 分布式缓存Memcached/memcached/memcache详解及区别
date: 2014-11-12 16:54:45
categories: 基础
---

先来解释下标题中的三种写法：首字母大写的Memcached，指的是Memcached服务器，就是独立运行Memcached的后台服务器，用于存储缓存数据的“容器”。memcached和memcache是Memcached的客户端，通过二者访问Memcached服务器，向容器存取数据。两者用途一致，但在用法上有稍微差异。

**一、Memcached**  
Memcached 是一个高性能分布式的内存对象缓存系统，通过缓存数据库查询结果，减少数据库访问次数，减少数据库的负载压力，提高动态web应用的性能。

Memcached 是以守护程序方式运行于一个或多个服务器中，随时接受客户端的连接操作，客户端与 Memcached 服务建立连接，根据请求存取对象，每个被存取的对象都有一个唯一的标识符 key，存取操作均通过这个 key 进行，保存到 Memcached 中的对象实际上是放置内存中的，并不是保存在 cache 文件中的，所以 Memcached 存取数据非常高效。注意，这些对象并不是持久的，服务停止之后，里边的数据就会丢失。

Memcached本身基于分布式的系统，可独立于网站应用本身，很容易实现服务器间数据共享。在 Memcached 中可以保存的item数据量是没有限制的，只有内存足够。Memcached单进程最大使用内存为2G，要使用更多内存，可以分多个端口开启多个Memcached进程，进行分布式搭建，毕竟单台Memcache的内存容量的有限的。

但是那些不需要“分布”的，不需要共享的，或者干脆规模小到只有一台服务器的应用，Memcached不会带来任何好处，相反还会拖慢系统效率，因为网络连接同样需要资源。

由于 Memcache服务器端都是直接通过客户端连接后直接操作，没有任何的验证过程，这样如果服务器是直接暴露在互联网上的话是比较危险，所以 Memcached 应放在防火墙里面。

**二、memcached 和 memcache 的区别**  
memcache最早是在2004年2月开发的，而memcached最早是在2009年1月开发的。所以memcache的历史比memcached久。那是不是可以这么理解： memcached 是 memcache 的升级版？

安装memcache扩展，直接导入扩展，更改下php.ini即可。但是在安装memcached的时候，你要先安装libmemcached，libmemcached是memcache的C客户端，它具有的优点是低内存，线程安全等特点。在高并发下，稳定性比memcache有明显提高。

memcache的方法特别少，只有很少一部分基本的操作方法，比 memcached 少很多，具体的可以查询官方手册。

所以总的来说，二者是没有太多其他区别的，只不过是 memcached 比 memcache 多了一些对守护进程的操作方法，性能更好一些。

**三、三者关系描述**  
Memcached 就比如是一个水库（容器），memcache 是一个塑料管，memcached 是一个PVC管。我们可以通过塑料管或者PVC管为水库上水或者取水，用哪种方式因人而异，而PVC管在输送水的效率上明显比塑料管快，而且可以装阀门、开口做分支等等，比塑料管的花样多。

说 Memcached 是服务端，很多人都会搅浑这个概念，说memcache不就是装在服务器上的么，不也是服务端么？ Memcached 是可以独立在web服务器之外的任何服务器，甚至可以是集群，而说它是服务端，其实是相对的概念，相对与web服务器的memcache来说是服务端，memcache所在的web服务器相对与用户PC机来说又是服务端。

另外，我 Windows 搭建的环境，没能成功安装 memcached，很受挫。希望有高手可以指点一二。。

======================

• 在 Memcached 中可以保存的item数据量是没有限制的，只有内存足够  
• Memcached单进程最大使用内存为2G，要使用更多内存，可以分多个端口开启多个Memcached进程  
• 最大30天的数据过期时间, 设置为永久的也会在这个时间过期，常量REALTIME\_MAXDELTA 60\*60\*24\*30 控制  
• 最大键长为250字节，大于该长度无法存储，常量KEY\_MAX\_LENGTH 250 控制  
• 单个item最大数据是1MB，超过1MB数据不予存储，常量POWER\_BLOCK 1048576 进行控制，它是默认的slab大小  
• 最大同时连接数是200，通过 conn\_init()中的freetotal 进行控制，最大软连接数是1024，通过settings.maxconns=1024 进行控制  
• 跟空间占用相关的参数：settings.factor=1.25, settings.chunk\_size=48, 影响slab的数据占用和步进方式

memcache的文档在：[http://pecl.php.net/package/memcache](http://pecl.php.net/package/memcache "http://pecl.php.net/package/memcache")

memcached的文档在：[http://pecl.php.net/package/memcached](http://pecl.php.net/package/memcached "http://pecl.php.net/package/memcached")
