---
title: mitmproxy使用记录
date: 2021-03-04 14:00:00
categories: 研究
tags: 
- 抓包
- 安卓逆向
---

## 介绍

中间人代理（man-in-the-middle proxy）是一个免费开源的交互式HTTP/HTTPS代理，可以用来拦截、修改、保存HTTP/HTTPS请求，类似Fiddler、Charles。

可以根据提供的Python API进行编程，通过Python代码来控制请求和响应、篡改转发返回以及请求体。

比如仿真爬虫，利用手机模拟器、无头浏览器来抓取数据，mitmpproxy 作为代理可以拦截、存储爬虫获取到的数据、修改数据调整爬虫的行为。

https://www.mitmproxy.org/

https://github.com/mitmproxy/mitmproxy

> 也可了解基于Nodejs开发的anyproxy，功能与mitmproxy基本一致，使用js定制脚本。

## 安装

```
$ sudo pip3 install mitmproxy
```
https://docs.mitmproxy.org/stable/overview-installation/

## 启动
安装完成后，将拥有三个命令：mitmproxy、mitmdump、mitmweb，三个命令的功能一致，只是交互界面、应用场景不同。

- mitmproxy：命令行界面，可以看到实时请求，通过命令过滤、查看、导出、编辑请求，`mitmproxy -p 18888`。
- mitmweb：浏览器界面，`mitmweb -p 18888`。
- mitmdump：加载自定义脚本，通过脚本控制、拦截、修改请求和响应，`mitmdump -s test.py -p 18888 -w request.log -q`。

## 证书

生成证书，并信任该证书。
```
$ mitmdump
$ ls ~/.mitmproxy
```

**IOS**或**安卓7以下**的手机：

手机设置代理为当前IP & Port，浏览器访问`mitm.it`下载对应系统的证书，安装证书并信任，即可拦截HTTPS请求。

**安卓7以上**的手机：

1、查看证书的hash值，第一行的8个16进制即是，比如：c8750f0d
```
$ openssl x509 -inform PEM -subject_hash_old -in  ~/.mitmproxy/mitmproxy-ca-cert.pem
```

2、将证书拷贝为`c8750f0d.0`（后缀是数字0）
```
$ cp ~/.mitmproxy/mitmproxy-ca-cert.pem c8750f0d.0
```

3、将证书文件写入到Android的系统证书列表，由于是访问了system目录，需要root并挂载
```
$ adb root 
$ adb remount
$ adb shell rm -f /system/etc/security/cacerts/c8750f0d.0
$ adb push c8750f0d.0 /system/etc/security/cacerts/c8750f0d.0
$ pause
```

或者
```
$ adb push c8750f0d.0 /system_root/system/etc/security/cacerts
```
如果无法`$ adb root`，可以先推送到临时目录，然后su之后cp到系统目录。有些小米手机操作system目录，可以进入re模式写命令拷贝。

有些APP就算有证书也无法抓到HTTPS包（根本看不到请求），比如快手，是因为没有使用常规的http协议，可以结合VPN工具转发，比如`Drony`。

> 为了方便团队协作，建议使用统一的证书，将`~/.mitmproxy`及`c8750f0d.0`分发给团队成员，电脑和手机使用同一个证书。

## 快捷键
通常使用mitmproxy模式分析请求，下面是一些常用快捷键，也可以使用`?`查看更多帮助。
- ?：查看帮助
- q：退出当前界面：从详情页退出到列表页、从列表页退出程序。
- z：清屏，清理掉列表页所有请求。
- d：删除当前选中的请求。
- f：过滤列表中的请求，比如`f`之后，输入`user_info`，就只能看到URL包含`user_info`的请求了。
- e：在列表中，导出当前选中的请求，通常导出curl以分析请求信息。
- r：重新发送请求。
- w：将当前列表中的所有请求，保存到一个文件中。比如，抓完一个APP（如抖音）的从安装到初始化完成的生命周期后，清理掉无用的请求，将列表保存下来，在需要的时候使用`L`加载。
- L：加载之前报错是请求列表。
- enter：进入当前选中请求的详情。
- tab：切到下一个tab。
- b：在详情页可以保存响应结果（response.body）、请求信息（request.body）等

## 脚本

本地调试完成后，通过脚本实现自动化处理是更常用的场景。
```
$ mitmdump -s test.py -p 18888 -w request.log -q
```
- -s：指定脚本文件
- -p：指定监听端口
- -w：将输出存储到指定文件
- -q：网络请求不再默认输出，可以自行输出

在脚本中按规则写回调函数，即可在对应场景自动执行。但不太建议生产环境中如此使用，不够灵活。

```python
import mitmproxy.http
from mitmproxy import ctx

def request(flow: mitmproxy.http.HTTPFlow):
    ctx.log.info("请求地址是：" + flow.request.url)
```

更常用的是通过`addons`数组加载多个类实例，类的方法实现了`mitmproxy`的事件，会在事件发生时调用对应的方法。

```python
import mitmproxy.http

class Aweme:
    def __init__(self):
        pass

    def request(self, flow: mitmproxy.http.HTTPFlow):
        print("抖音地址：" + flow.request.url)

class GifMaker:
    def __init__(self):
        pass

    def request(self, flow: mitmproxy.http.HTTPFlow):
        print("快手地址：" + flow.request.url)

addons = [
    Aweme(),
    GifMaker()
]
```

可参考[easyMitmproxy](./) // TODD。