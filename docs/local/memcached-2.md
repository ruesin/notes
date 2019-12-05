---
title: Windows下分布式缓存Memcached环境的搭建安装配置
date: 2014-11-12 17:02:36
categories: 本地
tags: 
- memcache
- memcached
- Memcached安装
- memcache php
---

现在谈 Memcached 已经没有什么新意了，翻过来覆过去无非就那么点东西（基础），本文也仅仅是为了做个记录而已。在Windows下搭建 Memcached 的开发调试环境，网上随便一搜一大堆，说得也都千篇一律，也就不浪费大家的时间了，直接切入正题，写Memcached和memcache的安装过程，至于原理、理论什么的放在《[分布式缓存Memcached/memcached/memcache详解及区别](http://old.ruesin.com/system/server/memcached-184.html)》这篇文章里，避免了读者的阅读疲劳。

**服务端的Memcached安装：**  
1\. 下载memcache的windows稳定版，解压放某个盘下面，比如在 e:\\host\\bin\\memcached  
2\. 在命令行模式下输入 ‘e:\\host\\bin\\memcached\\memcached.exe -d install’ 安装  
3\. 再输入： ‘e:\\host\\bin\\memcached\\memcached.exe -d start’ 启动。

以后memcached将作为windows的一个服务每次开机时自动启动。这样服务器端已经安装完毕了。

**php扩展组件的memcache的安装：**  
1\. 下载php\_memcache.dll，请自己查找对应的php版本的文件  
2\. 在 php.ini 中添加 ‘extension=php\_memcache.dll’  
3\. 重启Apache服务，输出phpinfo，如果有memcache，那么就说明安装成功！

**memcached的基本设置：**  
-p 监听的端口  
-l 连接的IP地址, 默认是本机  
-d start 启动memcached服务  
-d restart 重起memcached服务  
-d stop|shutdown 关闭正在运行的memcached服务  
-d install 安装memcached服务  
-d uninstall 卸载memcached服务  
-u 以的身份运行 (仅在以root运行的时候有效)  
-m 最大内存使用，单位MB。默认64MB  
-M 内存耗尽时返回错误，而不是删除项  
-c 最大同时连接数，默认是1024  
-f 块大小增长因子，默认是1.25  
-n 最小分配空间，key+value+flags默认是48  
-h 显示帮助

**测试：**  
$mem = new Memcache;  
$mem->connect(“127.0.0.1″, 11211); //连接Memcached服务器，默认端口为11211  
$mem->set(‘key’, ‘Old value’); //存值  
$val = $mem->get(‘key’); //取值  
echo ‘Old Value:’.$val . “<br>”;

$mem->replace(‘key’, ‘Replace value’); //替换数据  
$val = $mem->get(‘key’);  
echo “Replace value: ” . $val . “<br>”;

$mem->delete(‘key’); //删除数据  
$val = $mem->get(‘key’);  
echo “No value: ” . $val . “<br>”;

$mem->flush(); //清除所有数据

$mem->close(); //关闭连接
