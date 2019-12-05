---
title: form data 与 request payload之间的区别，及PHP中接收
date: 2015-10-31 07:54:57
categories: PHP
tags: 
- php
- php基础
- request payload
- ajax request payload
- php request payload
- php curl
---

与前端交互一直都是POST、GET的，从来没有出现过以外。

前些天给其他人写接口，用来接收参数，这边是PHP端就直接$\_POST接收了，很快整完交工。

可是试行两天后，那边说有请求过，可是我这边却没有数据，一再对了N遍，最后直接让那边前端给截图看他给我传的参数了，截图过来后，当时就懵逼了，没有form data，而数据却在request payload里头。

之前没用过这种形式啊，而且我这头的模拟数据也不是用的这种，又不好让那边改，只能在php端改接收方式了。

POST表单请求提交时，使用的Content-Type是 application/x-www-form-urlencoded，而使用原生AJAX的POST请求如果不指定请求头RequestHeader，默认使用的Content-Type是 text/plain;charset=UTF-8。在html中form的Content-type默认值：Content-type：application/x-www-form-urlencoded。

如果使用ajax请求，在请求头中出现 request payload导致参数的方式改变了 ,那么解决办法就是：

`headers: {'Content-Type':'application/x-www-form-urlencoded'}`或者使用ajax设置：

`$.ajaxSetup({contentType: 'application/x-www-form-urlencoded'});`下面是一个 request payload 的例子。

```
$.ajax({
    url: 'http://test.com/test.php?act=action',
    type: 'POST',
    contentType: 'text/plain; charset=utf-8', // 正常 application/x-www-form-urlencoded
    traditional: true,
    data:{"name":"zhangsan", "age": 28}
    success: function(res, status, xhr) {

    }
});
```

在PHP端接收参数使用的是：

```
$data = file_get_contents( "php://input");
$data = $GLOBALS['HTTP_RAW_POST_DATA'];
```

意思很简单明了，设置 contentType 为 text/plain; charset=utf-8 ，请求的数据实际就是以文本形式放在请求头里。而如果使用 application/x-www-form-urlencoded ，就是以form表单的形式请求。

实际上，request payload 用的地方也很多，比如想传json做参数的时候。
