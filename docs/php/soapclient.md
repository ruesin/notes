---
title: 本地 SoapClient 响应时间过长
date: 2015-07-29 11:03:37
categories: PHP
tags: 
- SoapClient
- php SoapClient
---

本地搭建的环境开发一直没问题的，但是前两天做一个soap接口的时候，出现了匪夷所思的事情。

本地调试，每次刷新一下页面都要十几秒，太恶心了，开发者工具没有发现请求外部数据，难道是封装的代码中有问题？遂准备用 fiddler 看下，然后诡异的事情就发生了——页面秒刷了。。。

对比线上的，一样的代码，响应迅速，那么应该就是我本地环境的问题了。

先看了host文件，没问题。

然后一步步翻查代码，查到了问题所在，是实例化 SoapClient 类的时候耗了太多时间。但是这是用的php自带的类库，按说应该没问题啊。

[![soapclient](/images/2015/07/soapclient.jpg)](/images/2015/07/soapclient.jpg)

看了下apache日志，发现在重启apache的时候会有两个警告，理论上是应该不影响的啊。

AH00548: NameVirtualHost has no effect and will be removed in the next release E:/host/Apache2.4/conf/vhosts.conf:2  
AH00558: httpd.exe: Could not reliably determine the server’s fully qualified domain name, using fe80::fdce:4909:f353:5321. Set the ‘ServerName’ directive globally to suppress this message

注释掉 NameVirtualHost \*:80

设置 ServerName localhost

再次重启apache服务，刷新页面，秒刷！！！

以为万事大吉了，没想到还是有问题，在firefox上是可以每次都秒刷的，但是在chrome上刷新大概10次左右就会有一次长响应。打开fiddler后就不会出现这问题，着实诡异。。
