---
title: Ucenter中全局变量$_ENV的用法
date: 2014-11-09 16:54:34
categories: 三方产品
tags: 
- php
- php基础
- ucenter
- 全局变量
---

二开ucenter，翻看代码，追到 /client/control/user.php ，看到注册会员时的这段代码。

$uid = $\_ENV\['user'\]->add\_user($username, $password, $email,$imdomain,0, $questionid, $answer);

额，不止一次的承认自己的基础知识不够扎实，看到这里的$\_ENV，竟然还要去查一下。

有兴趣的可以去查一下官方手册，这里大概解释一下，$\_ENV是PHP中的一个包含服务器端环境变量的数组。它是PHP中一个超级全局变量，我们可以在PHP程序的任何地方直接访问它。它与$HTTP\_ENV\_VARS包含相同的信息，但$HTTP\_ENV\_VARS不是一个超全局变量。

那么，它在ucenter的用法是什么呢？

看到不明变量的时候，首先就是去打印一下了，在这里我们会看到数组包含两个对象（user、note），如果这是包含model的大数组的话，为什么只包含了这两个对象呢？而在之前，打印的话又是空的，很显然，这个全局变量数组在不同的地方有不同的值。

我在想，这里的变量是不是跟使用 $\_POST\['user'\] 时差不多？是自定义的一个值？是给 $\_EVN 设置一个key，存储进去我们实例化的对象，从而达到，在程序的任何地方都可以直接访问，这样就无须在函数中使用global关键字了，避免了全局变量的污染。

继续追踪代码，果然验证了我的理论，在 uc\_client/model/base.php 中，load()方法定义了 $\_ENV\[$model\] 并赋值，所以我们在不同的地方打印 $\_ENV 的话，会打印出不同的值。

```
function load($model, $base = NULL) {
    $base = $base ? $base : $this;
    if(empty($_ENV[$model])) {
        require_once UC_ROOT."./model/$model.php";
        eval('$_ENV[$model] = new '.$model.'model($base);');
    }
    return $_ENV[$model];
}
```
