---
title: PHP一个简单的对称加密函数实现数据的加密解密
date: 2015-06-19 13:54:21
categories: PHP
---

项目中有一个地方用到了将用户ID加密、传至下个接点进行反解的需求。（原谅我不能透漏太多-\_-!），第一个想到的就是康盛Ucenter中的一个函数，后来搜了下，在简明魔法中也找到了个简单的方法，遂整合了下，形成了自己使用的函数。

**一、对称加密**

发送方将明文使用密钥和算法处理成密文发送出去，接收方使用密钥和算法将密文处理成明文，发收信双方使用同一个密钥对数据进行加密和解密。

[![symmetric](/images/2015/06/symmetric.jpg)](/images/2015/06/symmetric.jpg)

因为使用同一个密钥加密、解密，所以安全性上不仅与算法有关，密钥的安全也很重要。

当然并不是密钥越复杂越好，相反密钥通常比较小的，因为虽然密钥越大，加密越强，但加密与解密的过程越慢，所以密钥的大小既要照顾到安全性，也要照顾到效率。

毕竟对称加密算法的特点是算法公开、计算量小、加密速度快、加密效率高，没了效率高这一优势，还不如直接用非对称加密。

此外，每对用户每次使用对称加密算法时，都需要使用其他人不知道的惟一钥匙，这会使得发收信双方所拥有的钥匙数量呈几何级数增长，密钥管理成为用户的负担。

对称加密算法在分布式网络系统上使用较为困难，主要是因为密钥管理困难，使用成本较高。

**二、非对称加密**

非对称加密相对来说，就安全很多了，它使用了一对密钥，公开密钥和私有密钥，分别用来进行加密和解密。私钥只能由一方安全保管，不能外泄，而公钥则可以发给任何请求它的人。

[![asymmetric](/images/2015/06/asymmetric-.jpg)](/images/2015/06/asymmetric-.jpg)

最常见的非对称加密，应该就是银行系统，支付平台了。比如我们申请支付宝或者银联支付的接口时，会得到一个公钥，商城中进行支付是，用公钥将信息加密提交给平台，平台使用密钥对你的信息解密，进行支付操作等。

虽然非对称加密很安全，但是和对称加密比起来，它非常的慢，所以我们一般处理的话，大部分是用对称加密来传送消息，但对称加密所使用的密钥我们可以通过非对称加密的方式发送出去，回想一下你申请到的支付接口，是不是给了你一对密钥呢？^.^

**三、结合使用**

对称性加密速度快，发送大量数据时用比较好。非对称加密加密和解密花费时间长、速度慢，只适合对少量数据进行加密，但是，非对称加密的安全性是极高的。

扬长避短：将对称加密的密钥使用非对称加密的公钥进行加密，然后发送出去，接收方使用私钥进行解密得到对称加密的密钥，然后双方可以使用对称加密来进行沟通。

[![both](/images/2015/06/both.jpg)](/images/2015/06/both.jpg)

项目中使用的方法不宜透露，只在这里列出两个其他的例子吧。第一个是ucenter中的，第二个是简明魔法中看到的。

需要注意的是，由于是base64算法，加密后的字符串有可能会出现 + \\ ，如果是用在url中，是不友好的，可以在外部或改下方法，正则验证递归调取下。

```
/**
 * 字符串加密以及解密函数
 * @param string $string 原文或者密文
 * @param string $operation 操作(ENCODE | DECODE), 默认为 DECODE
 * @param string $key 密钥
 * @param int $expiry 密文有效期, 加密时候有效， 单位 秒，0 为永久有效
 * @return string 处理后的 原文或者 经过 base64_encode 处理后的密文
 */
function _authcode ($string, $operation = 'DECODE', $key = 'Ruesin', $expiry = 0)
{
    $ckey_length = 4;
    
    $key = md5($key);
    $keya = md5(substr($key, 0, 16));
    $keyb = md5(substr($key, 16, 16));
    $keyc = $ckey_length ? ($operation == 'DECODE' ? substr($string, 0, 
            $ckey_length) : substr(md5(microtime()), - $ckey_length)) : '';
    
    $cryptkey = $keya . md5($keya . $keyc);
    $key_length = strlen($cryptkey);
    
    $string = $operation == 'DECODE' ? base64_decode(
            substr($string, $ckey_length)) : sprintf('%010d', 
            $expiry ? $expiry + time() : 0) . substr(md5($string . $keyb), 0, 16) .
             $string;
    $string_length = strlen($string);
    
    $result = '';
    $box = range(0, 255);
    
    $rndkey = array();
    for ($i = 0; $i  0) &&
                 substr($result, 10, 16) ==
                 substr(md5(substr($result, 26) . $keyb), 0, 16)) {
            return substr($result, 26);
        } else {
            return '';
        }
    } else {
        return $keyc . str_replace('=', '', base64_encode($result));
    }
}
```

```
/*********************************************************************
函数名称:encrypt
函数作用:加密解密字符串
使用方法:
加密     :encrypt('str','E','nowamagic');
解密     :encrypt('被加密过的字符串','D','nowamagic');
参数说明:
$string   :需要加密解密的字符串
$operation:判断是加密还是解密:E:加密   D:解密
$key      :加密的钥匙(密匙);
*********************************************************************/
function encrypt($string,$operation,$key='')
{
    $key=md5($key);
    $key_length=strlen($key);
    $string=$operation=='D'?base64_decode($string):substr(md5($string.$key),0,8).$string;
    $string_length=strlen($string);
    $rndkey=$box=array();
    $result='';
    for($i=0;$i<=255;$i++)
    {
        $rndkey[$i]=ord($key[$i%$key_length]);
        $box[$i]=$i;
    }
    for($j=$i=0;$i<256;$i++)
    {
        $j=($j+$box[$i]+$rndkey[$i])%256;
        $tmp=$box[$i];
        $box[$i]=$box[$j];
        $box[$j]=$tmp;
    }
    for($a=$j=$i=0;$i<$string_length;$i++)
    {
        $a=($a+1)%256;
        $j=($j+$box[$a])%256;
        $tmp=$box[$a];
        $box[$a]=$box[$j];
        $box[$j]=$tmp;
        $result.=chr(ord($string[$i])^($box[($box[$a]+$box[$j])%256]));
    }
    if($operation=='D')
    {
        if(substr($result,0,8)==substr(md5(substr($result,8).$key),0,8))
        {
            return substr($result,8);
        }
        else
        {
            return'';
        }
    }
    else
    {
        return str_replace('=','',base64_encode($result));
    }
}
```
