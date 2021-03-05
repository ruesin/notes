---
title: Drony使用记录
date: 2021-03-05 10:00:00
categories: 研究
tags: 
- 抓包
- 安卓逆向
---

## 介绍

快手8.0以上，更改了网络请求方式，导致无法通过[mitmprox](./mitmproxy.md)正常抓取。

可以通过drony或其他vpn的方式，将网络请求转发到代理上。

另外，通过drony比直接在系统设置中管理更方便、灵活。

## 安装
下载地址：

https://apkfab.com/free-apk-download?q=org.sandrob.drony

https://apkcombo.com/apk-downloader/?device=&arches=&sdkInt=&sa=1&lang=en&dpi=480&q=org.sandrob.drony

```
$ adb install drony_1.3.155.apk
```

## 配置

打开`Drony`后，首屏下方的按钮，显示当前VPN的状态：开（ON）、关（OFF）

左滑切换到 设置（SETTINGS），点击 无线网络（Wi-Fi）进入 网络列表（Network list），选择当前连接的网络，进入 网络细节（Network detail）。

- 代理类型（Proxy type）设置为 手动（Manual）
- 主机名（Hostname）、端口号（Port），设置为电脑监听的端口
- 代理类型（Proxy type）设置为 普通http代理（Plain http proxy）
- 过滤默认值（Filter default value）设置为 允许全部（Direct all）
- 点击 规则（Rule），进入编辑规则（不编辑规则也可以开始抓包了）

- 网络ID（Network id） 选择当前 网络SSID
- 行动（Action）选择 本地代理链全部（Local proxy chain）
- 应用程序（Application）选择需要强制代理的APP
- Hostname & Port，指定被转发的请求，不填表示所有请求都会被转发


保存后返回首页，点击底部的按钮，使其处于 开（ON）状态，表示正在转发请求。

> drony只是负责将请求转发到对应的代理服务器，仍然需要常规抓包的配置及证书。


![dront_1.png](/images/2021/drony_1.png)

![dront_2.png](/images/2021/drony_2.png)

![dront_3.png](/images/2021/drony_3.png)

