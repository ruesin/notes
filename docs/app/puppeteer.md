---
title: puppeteer使用记录
date: 2021-03-07 17:00:00
categories: 研究
tags: 
- 抓包
- 安卓逆向
---


## 介绍

puppeteer 是谷歌退出的针对Chrome Headless特性，通过JS调用Chrome DevTools开放的接口与Chrome通信，puppeteer对复杂的Chrome DevTools接口进行了更易用的封装。

在爬虫、测试自动化等方面使用非常方便，作为无头浏览器，是真正运行的无界面渲染的浏览器，可以使程序如真人操作一样执行。

## 安装
```
$ npm i --save puppeteer
```

## 测试

打开百度首页，并截图。
```js
const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('http://www.baidu.com');
    await page.screenshot({path: 'baidu.png'});
    await browser.close();
})();
```

## Demo
[easyPuppeteer](https://github.com/metmit/easyPuppeteer)

## 参考
- https://github.com/puppeteer/puppeteer
- https://www.kancloud.cn/luponu/puppeteer/870133
- https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-getCookies

