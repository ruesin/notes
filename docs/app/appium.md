---
title: appium 使用记录
date: 2021-03-12 00:00:00
categories: 研究
tags: 
- 自动化
- 安卓逆向
---

## 介绍
Appium 是一个开源、跨平台的自动化测试工具，可以用来测试原生、移动 Web 和混合应用。

Appium 使用了系统自带的自动化框架。不需要把 Appium 或者第三方的代码编译进应用中，保证测试使用的应用与最终发布的应用是一致的。

系统自带的自动化框架：
- iOS 9.3 及以上: 苹果的 XCUITest
- iOS 9.3 及以下: 苹果的 UIAutomation
- Android 4.3+: 谷歌的 UiAutomator / UiAutomator2
- Android 2.3+: 谷歌的 Instrumentation. (通过绑定独立的项目—— Selendroid 提供对 Instrumentation 的支持)
- Windows: 微软的 WinAppDriver

Appium 把系统提供的框架封装进一套 API —— WebDriver API 中。WebDriver（也叫「Selenium WebDriver」）规定了一个客户端-服务器协议（称为 JSON Wire Protocol），按照这种客户端-服务器架构，可以使用任何语言编写的客户端向服务器发送适当的 HTTP 请求。

客户端程序库不过是一个简单的 HTTP 客户端，只要客户端能够发送HTTP请求给服务端，那么客户端用什么语言来实现都是可以的，Appium 客户端支持 Selenium WebDriver 支持的所有语言，更可以使用Selenium WebDriver的Api。

## 原理

Appium 是一个经典的客户端/服务器架构，服务端核心是一个暴露 REST API 的 用Node.js 写的 WEB 服务器，接受来自客户端的连接，监听命令并在移动设备上执行，答复 HTTP 响应来描述执行结果。

客户端程序想服务器发送一个POST /session 请求，请求中包含一个被称作「预期能力（Desired Capabilities）」的 JSON 对象。服务器将开启一个自动化会话，返回一个会话ID，之后的所有自动化都在这一个会话的上下文中执行。

预期能力（Desired Capabilities）是一些发送给 Appium 服务器的键值对集合，它告诉服务器我们想要启动什么类型的自动化会话。也有许多能力（Capabilities）可以修改服务器在自动化过程中行为。

除了使用脚本请求服务器的方式自动化，还可以安装Appium Desktop，是一个Appium 服务器的图形界面封装，它打包了 Appium 服务器运行需要的所有东西，它们还提供一个 Inspector 使你可以查看应用程序的层级结构，可以在调试时使用。

客户端发送自动化请求到服务端之后，服务端将命令通过socket连接发送到手机，再将命令转换为手机自动化命令执行。

安卓设备上socket服务器是通过bootstrap.jar创建的，bootstrap本身就是一个测试脚本，运行后就会创建一个socket服务，接收appium服务器发送过来的请求。

运行原理：

1. 客户端请求服务端，发送配置信息、建立session连接。

2. 服务端推送bootstrap.jar到设备、安装appium-settings和uiautomator2。

3. uiautomator运行bootstrap.jar（appium-settings），启动socket服务，用于Appium和手机建立连接，将appium的命令转换为uiautomator命令。

## 安装

安装Appium-Server
```
$ npm install -g appium
$ appium
```

安装Appium-client
http://appium.io/docs/en/about-appium/appium-clients/index.html
```
$ pip install Appium-Python-Client
```

安装Appium-Desktop
https://github.com/appium/appium-desktop/releases


## 使用

启动server
```python

import os

from appium.webdriver.appium_service import AppiumService

device_udid = "aaaaaaaa"
appium_port = "4723"
bp_port = str(int(appium_port) + 2000)

log_file = os.path.join('/tmp/' + device_udid + '-appium.log')

service = AppiumService()
service.start(args=['-p', appium_port, '-bp', bp_port, '-U', device_udid,
                    '--session-override', '--no-reset',
                    '--log-level', 'error', '--log', log_file], timeout_ms=2000)
```

执行命令（跳转抖音用户主页）
```python
from appium import webdriver

device_udid = "aaaaaaaa"

desired_caps = {
    'platformName': 'Android',
    'udid': device_udid,
    'deviceName': device_udid,
    'platformVersion': "7.0",
    'appPackage': 'com.ss.android.ugc.aweme',
    'appActivity': 'com.ss.android.ugc.aweme.main.MainActivity',
    "noReset": True,
    "newCommandTimeout": 600000,
    "autoAcceptAlerts": True,
    "recreateChromeDriverSessions": True,
    "unicodeKeyboard": True,
    "resetKeyboard": True,
}
_device_session = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps, direct_connection=True)

url = "snssdk1128://user/profile/104255897823?refer=web&gd_label=click_wap_profile_bottom&type=need_follow&needlaunchlog=1"
_device_session.get(url)
```
## 文档
- http://appium.io/docs/cn/about-appium/intro/
- https://github.com/metmit/easyAppium
