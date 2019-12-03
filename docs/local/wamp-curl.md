---
title: wamp在win64位下PHP环境无法开启php_curl扩展组件
date: 2014-07-11 12:53:03
categories: 本地
---

工作中用到了Curl，去Wamp设置里勾选开启Curl后，检测环境还是没有开启，php程序显示Call to undefined function curl\_init()错误。  
以为是wamp设置的bug，去php.ini里看了下，扩展已经开启了。其实出现这种情况一般都是因为没有加载到php的扩展文件导致的。  
逐步检查：  
1.配置文件已修改  
extension=php\_curl.dll  
2.扩展目录中存在扩展文件  
php\_curl.dll  
3.php.ini 中扩展目录指向正常  
extension\_dir = “e:/host/bin/php/php5.3.13/ext/”

检查到这里我就有点百思不得其解了。

后来考虑是不是这扩展文件有错(这一点实在没有去怀疑过…)，于是去单独下载了个对应版本的64位PHP，将php\_curl.dll覆盖，重启服务，正常了。。。

看来真的是文件有错，总之是解决了。

具体解决步骤如下：  
1.配置文件开启php\_curl.dll(去掉前面的’;')。  
2.下载修复过的php\_curl.dll文件，扩展目录下。  
3.重新启动wamp服务。

本地开发环境其实没必要自己搭配的，毕竟不是用做服务器的，开发为的不就是快速高效吗，本地高效开发环境我还是比较推荐wamp的，wamp所有的工作都已经帮你配置完成了，拥有非常多的设置选项可以按需选择，非常易用。当然，你也可以手动去修改配置文件。
