---
title: Ecstore 2.0 安装默认被隐藏掉的APP
date: 2014-08-25 14:25:35
categories: 三方产品
---

翻看Ecstore 2.0 的APP文件夹，可以发现有几个常用的APP，可是在后台应用中心却看不到。比如：groupactivity（团购）、cps（网站联盟）、 timedbuy （限时抢购）等。但是有做过Ecstore1.2经验的朋友都知道，这些APP在Ecstore1.2中都是正常的，这是什么原因呢？

原来，这是因为这几个APP是基于Ecstore1.2版本开发的，系统升级2.0之后，有很多方法都被舍弃了，导致这些APP在2.0中存在很多漏洞，看起来好像半成品一样，但是官方为了给开发者提供开发借鉴，并没有把这些APP删除掉，而是简单的隐藏掉，避免引起不必要的麻烦。

那如果我们想要安装这些被隐藏的APP要怎么做呢？

有经验的朋友可能会立马想到命令行安装。

对的，这是一个简单粗暴有力的方法，直接 cmd install groupactivity ， 安装成功。虽然在后台应用中心还是看不到被安装的APP，但是此APP已经可以使用了。（前提是此APP没有漏洞哦o(∩\_∩)o）

[![install](/images/2014/08/install.jpg)](/images/2014/08/install.jpg)  
第一种方法对于有经验的朋友来说当然是最直接最快捷的办法，但不是所有的人都会（喜欢）用命令行的，又考虑到后期维护的问题，我们能不能把隐藏掉的APP在应用中心显示出来呢？答案当然是肯定的！（这不废话嘛，能隐藏肯定能显示。-\_-:）

修改\[ecstore\_path\]/config/deploy.xml，将  
<app id=”groupactivity” default=”false” locked=”true” hidden=”true” />  
修改为  
<app id=”groupactivity” default=”false” locked=”true” hidden=”false” />  
然后登录后台，应用中心就可以看到团购APP了。

[![hidden](/images/2014/08/hidden.jpg)](/images/2014/08/hidden.jpg)  
注：这些APP是官方的弃子，擅自使用，后果自负哦。
