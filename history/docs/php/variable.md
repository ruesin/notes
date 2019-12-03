---
title: php可变变量
date: 2013-12-31 00:00:46
categories: PHP
---

$$a这样的写法曾经在百度贴吧上看过、也大概知道它的用法、只是一直没用过、也没见过具体的解释。

昨天看书的时候才知道它的名字——可变变量。

可变变量的变量名可以动态地设置和使用。一个可变变量使用一个普通变量的值作为该可变变量的变量名。

```
$a='hello';
$$a='world';
echo $a;      //输出hello
echo $$a;     //输出world
echo ${$a};   //输出world
echo $hello;  //输出world
```

要将可变变量用于数组，必须解决一个模棱两可的问题。这就是当写下$$a\[1\]时，解析器需要知道是想要$a\[1\]作为一个变量呢，还是想要$$a作为一个变量并取出该变量中索引为 \[1\] 的值。解决此问题的语法是，对第一种情况用${$a\[1\]}，对第二种情况用${$a}\[1\]。

注意：在 PHP 的函数和类的方法中，超全局变量不可用作可变变量。