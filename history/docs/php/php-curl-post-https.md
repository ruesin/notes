---
title: php 使用 curl post 请求 https 
date: 2015-11-02 08:49:22
categories: PHP
---

今天做wap请求微信APP支付， PHP端要post请求API生成预支付订单，获取订单号。

请求地址为：

https://api.weixin.qq.com/pay/genprepay?access\_token=ACCESS\_TOKEN

请求方法是要post，json数据。

本来，这些都没什么，在原来封装的curl方法中加个header参数即可。可是实际测试时，一直返回false，拿本地的url测试，又是正常，翻了半天没想通理由，按照官方文档来说，如果是json格式错误，起码应有个错误码啊。

于是，开始对比本地url和远端API的不同，终于，最后发现了不同所在，微信api使用的是https，而且在人家官方文档的开始就已经声明了，自己没注意到而已。

知道了问题所在就好解决了，当请求https的数据时，会要求证书，在请求时加上两个参数，忽略下ssl的证书检查好了。

```
function postJsonCurl($url, $data_string) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // 跳过证书检查
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, true);  // 从证书中检查SSL加密算法是否存在
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Content-Type: application/json; charset=utf-8',
        'Content-Length: ' . strlen($data_string))
    );
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 300);
    
    ob_start();
    curl_exec($ch);
    $result= ob_get_contents();
    ob_end_clean();
    return $result;
}
```
