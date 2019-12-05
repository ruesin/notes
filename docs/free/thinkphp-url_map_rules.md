---
title: Thinkphp 3.3 URL映射/解析、路由规则二开
date: 2015-01-13 10:36:52
categories: 开源项目
tags: 
- thinkphp
- thinkphp二开
- thinkphp学习
- thinkphp路由
- thinkphp URL
- thinkphp映射
---

上一次看 Thinkphp 好像两年前，也只是大概涉猎了下，以为不过算是把模版引擎做了下封装，更便捷使用而已。最近没事想再看看，发现已经3.3了，看了下开发文档，越看越觉得架构做得不错，特别是我比较在意的运行速度的优化上。当真是喜爱至极，于是决定做一两个简单操作熟悉一下机制。

首先，我也就这两天大概看了下，还未深入研究，也许我所谓的二开的东西属于画蛇添足，或者本来就有而我没发现，如有误导，还望见谅。

另外，我二开的这些东西只是用作我自己当下的需求使用，或许不太适合做产品或者广泛使用，请谨而慎之。

就我个人而言，是很排斥将代码结构暴漏出来的，而 Thinkphp 偏偏是这样做的，从模块到控制器到方法，一层层的显示出来了。

虽然自带的有 路由规则、URL映射、模块映射、控制器映射、方法映射，但是在我看来，还是不能够满足我的需求，而我偏偏又爱上了它，不舍得抛弃它。那就把它变成我自己的“西施”吧。

需求：

1、访问自定义的url可以默认映射出指定的方法。

Want： 访问 local.ruesin.com/article/3.html 实际上访问的是 local.ruesin.com/home/index/article/id/3.html

可以通过URL映射实现，但是这只适合普通的方法映射，好像写上参数的话就不能用了，使用路由规则和URL映射是无法实现我的需求的。

2、模版页中使用 U 方法输出链接地址，是自定义的URL。

Want： <{:U(‘article’,”,false)}> 输出的是 article 而不是映射的 home/index/article 。

后来考虑这个问题，或许不用二开，直接写URL也是可以的。本来想的是不做二开，硬写URL得了，可是又手痒顺手改了下。。。

做所有二开之前，要先了解配置文件的各种路由和映射，下面便是我的配置文件。

```
// 默认路由规则 针对模块//路由跳转的,输入前面的自动跳后面
'URL_ROUTE_RULES'       =>  array(
        //'cs/:id'=>'/home/index/cs/:1',
), 
// URL映射定义规则//访问前面地址,映射后面的内容
'URL_MAP_RULES'         =>  array(
        'article' => 'hm/in/article',
        'index' => 'hm/in/index'
),
'URL_MODULE_MAP' => array(
        'hm'  => 'home',
),
'URL_CONTROLLER_MAP' => array(
        'in' => 'index',
),
'URL_ACTION_MAP'=>array(
        'index'    =>  array(
                'ts'  => 'test',
        ),
),
```

我是不想让我访问页面的URL中出现参数的键名的，那样的话参数一多URL层级就显得很深，那么在模版解析的时候就也不应该出现，但是正常的解析是必须写键名的，我便去改了下 function.php 下的 U 方法。

`<{:U('article','www/wamp/curl-130',true,true)}>`解析参数：先把参数改成斜杠分割形式的，这样就能区别正常的参数还是二开的参数，再加个必须是在PATHINFO模式下才会生效，把各个参数写入数组，伪参数。

```
if(is_string($vars)) { // aaa=1&bbb=2 转换成数组
    parse_str($vars,$vars);
    //== Ruesin -Bgn
    if(C('URL_MODEL') != 0 && count($vars) == 1 && reset($vars) == null ){
        $key = key($vars);
        if(false !== strpos($key,'/')){
            $vars = explode('/',$key);
        }else{
            $vars[1] = $key;
        }
        $cstUrl = 1; //标识二开过
    }
    //== Ruesin -End
}elseif(!is_array($vars)){
    $vars = array();
}
```

PATHINFO模式下封URL：去查URL映射，看是否有映射，有的话就直接显示映射的地址，而不是完整地址。

```
//== Ruesin -Bgn
$maps = C('URL_MAP_RULES');
if( $maps && array_search(strtolower($url),$maps)) {
    $url = array_search(strtolower($url),$maps);
}
$url =  __APP__.'/'.$url;
//== Ruesin -End
```

封参数：判断URL是否被二开，有的话就不封键名进URL

```
//== Ruesin -Bgn
if($cstUrl){
    if('' !== trim($val))   $url .=  $depr . urlencode($val);
}else{
    if('' !== trim($val))   $url .= $depr . $var . $depr . urlencode($val);
}
//== Ruesin -End
```

最后页面输出的URL为： http://local.ruesin.com/article/www/wamp/curl-130.html

看着URL输出改完了，之前测试的直接访问 http://local.ruesin.com/article 输出的也是 http://local.ruesin.com/hm/in/article 的数据。

那是不是就万事大吉了呢？赶紧点击链接进入看一下，FUCK！ :(

[![no_module](/images/2015/01/no_module.jpg)](/images/2015/01/no_module.jpg)

原来是URL解析的时候，还是按照完整路径走的，要先匹配模块，然后控制器方法，程序把article当成模块了，当然会出错。

那咋弄呢？难道必须要完整路径吗？既然我们能把URL地址改掉，那么我们在他解析内容之前，再给他改回去不就行了吗？不带参数能解析就能说明这块。

打开 /ThinkPHP/Library/Think/Dispatcher.class.php 在 dispatch() 方法的所有操作之前加上

```
//== Ruesin -Bgn
$maps = C('URL_MAP_RULES');
$mods = explode('/', $_SERVER['PATH_INFO']);
if( $maps && $maps[strtolower($mods[1])] ) {
    $mods[1] = $maps[strtolower($mods[1])];
    $_SERVER['PATH_INFO'] = implode('/', $mods);
}
//== Ruesin -End
```

再次尝试访问，可以了吧。。。。
