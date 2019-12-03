---
title: Windows下php+redis安装
date: 2015-04-15 09:42:59
categories: PHP
---

有个项目需要在加载页面的时候执行大量的数据处理，按正常套路走的话速度会比较慢，而这时redis就是比较适合的选择了。

本地Windows下php的redis扩展安装过程，如下所示。

下载安装包，将安装包解压后看以看到几个文件：

[![redis_file](/images/2015/04/redis_file.jpg)](/images/2015/04/redis_file.jpg)

最后两个start文件是我自己添加的，稍后会看到用途的。

**redis-server.exe**：服务程序  
**redis-check-dump.exe**：本地数据库检查  
**redis-check-aof.exe**：更新日志检查  
r**edis-benchmark.exe**：性能测试，用以模拟同时由N个客户端发送M个 SETs/GETs 查询 (类似于 Apache 的ab 工具).

网上有人说还需要自己写conf文件，我下载的包里就有这个文件，直接忽略过了。

启动redis服务：**redis-server.exe Redis.conf**

[![redis_server_start](/images/2015/04/redis_server_start.jpg)](/images/2015/04/redis_server_start.jpg)

启动cmd窗口要一直开着，关闭后则Redis服务关闭。  
对于这里我之前好像写过一篇博文，里面有说用vb不显示cmd窗口的，本文最后会贴出。

服务启动后，就需要设置客户端了：**redis-cli.exe -h 127.0.0.1 -p 6379**

[![redis_client_start](/images/2015/04/redis_client_start.jpg)](/images/2015/04/redis_client_start.jpg)

至此，redis服务已经设置完毕，剩下的就是php扩展的开启，下载对应版本的扩展文件，在php.ini中添加扩展：

```
extension=php_igbinary.dll
extension=php_redis.dll
```

phpinfo();查看redis扩展开启情况。

[![php_redis](/images/2015/04/php_redis.jpg)](/images/2015/04/php_redis.jpg)

```
$redis = new Redis();
$redis->connect("127.0.0.1", "6379");
$redis->set("name", "Ruesin");
echo $redis->get("name");
//Ruesin
//这时的name已经写入到缓存，就算你现在删掉set，打印出来的也是Ruesin
```

PS：  
我们本地测试时一直开着个cmd窗口总是不爽的，特别是处女座的同学们。so、我用vb处理了下。  
创建 start.bat

```
cd E:\host\Redis1
E:
redis-server.exe Redis.conf
```

创建 start.vbe

```
set ws=wscript.createobject("wscript.shell")
ws.run "start.bat /start",0
```

需要启用服务的时候只需要点击一下start.vbe即可，当然如果想要开机启动的话，可以创建一个快捷方式，放到启动文件夹里。
