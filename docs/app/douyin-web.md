---
title: 获取抖音网页版签名_signature算法
date: 2021-03-25 00:00:00
categories: 研究
tags: 
- 爬虫
- 逆向
---

## 查找
打开页面及控制台：https://www.iesdouyin.com/share/user/104255897823?sec_uid=MS4wLjABAAAA8U_l6rBzmy7bcy6xOJel4v0RzoR_wfAubGPeJimN__4

### 方法一
控制台 - “Network”标签下，搜索“_signature”，在“index.xxxxx.js”中赋值的。

![douyin_web_1.png](/images/2021/douyin_web_1.png)

在“index.xxxxx.js”中搜索“signature = ”，赋值内容为`signature = (0, _bytedAcrawler.sign)(nonce);`。

![douyin_web_2.png](/images/2021/douyin_web_2.png)

### 方法二
控制台 - “Sources”标签下，添加“XHR/fetch Breakpoints”，值为`web/api/v2/aweme/post`。

刷新页面，可以看到调用链“Call Stack”，找到`signature = (0, _bytedAcrawler.sign)(nonce);`

![douyin_web_3.png](/images/2021/douyin_web_3.png)

## 分析
```js
// config = {uid: userId}
function init(config) {
  dytk = config.dytk;
  params.user_id = config.uid;
  params.sec_uid = _utils2.default.getUrlParam(window.location.href, "sec_uid");
  if (params.sec_uid != "") {
    delete params.user_id;
  }
  config.sec_uid = params.sec_uid;
  nonce = config.uid;
  signature = (0, _bytedAcrawler.sign)(nonce);
}
```

在“index.xxxxx.js”中搜索“_bytedAcrawler = ”，`var _bytedAcrawler = __webpack_require__("9bd2804c7e68ac461d65");`。

通过`__webpack_require__`引用了“vendor.xxx.js”中的`9bd2804c7e68ac461d65`模块。

由于是webpack打包的JS代码，简单分析加载逻辑：

“index.xxx.js”是一个自调用的函数，将定义的“modules”都通过`__webpack_require__`加载到`installedModules`变量中。通过`installedChunks`的定义，判断加载后主动调用那些“module”。

在“index.xxx.js”加载模块时，定义了全局变量`window["webpackJsonp"]`。在vendor.xxx.js中，调用了`window["webpackJsonp"].push`，实现逻辑是调用`webpackJsonpCallback`继续向`installedModules`添加模块，并判断哪些需要主动调用。

可以理解，两个文件都是加载模块，并主动调用预定义的模块。

## 实现

拖出`__webpack_require__`方法、`9bd2804c7e68ac461d65`模块，预加载方法之后即可使用。

```js
var modules = {
    "9bd2804c7e68ac461d65": (function(module, exports) {
        Function(function(t){return 'xxxxxxxxx'}, [Object.defineProperty(exports,'__esModule',{value:!0})]);
    }),
}

var installedModules = {};

function __webpack_require__(moduleId) {
    if (installedModules[moduleId]) {
        return installedModules[moduleId].exports;
    }
    var module = installedModules[moduleId] = {
        i: moduleId,
        l: false,
        exports: {}
    };
    modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
    module.l = true;
    return module.exports;
}

var _bytedAcrawler = __webpack_require__("9bd2804c7e68ac461d65");
var signature = _bytedAcrawler.sign("104255897823");
console.log(signature)

```

> 在算法内会读一些浏览器信息、密钥等，如果没有配置会报错 或者 生成的签名不可用。