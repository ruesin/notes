---
title: smarty添加自定义插件功能
date: 2014-09-28 14:32:07
categories: PHP
tags: 
- php
- php基础
- smarty
- smarty插件
---

smarty插件是smarty模版引擎的核心，没有插件的smarty几乎什么都做不了。  
分析smarty的代码结构，主要有三部分：  
./Smarty.class.php //smarty入口文件  
./sysplugins //系统插件  
./plugins //外部插件

所以我们今天说的自定义插件就在./plugins下面，可以在他下面进行插件的开发。

插件文件的命名规则是type.name.php, 插件文件中的的函数命名规则是smarty\_type\_name()。  
type指的是类型,有下面几种可选; name: 自定义的插件名称。

```
    function
    modifier
    block
    compiler
    prefilter
    postfilter
    outputfilter
    resource
    insert
```

我们常用的插件有文件名以modifier.开头的变量调节器，文件名以function.开头的自定义函数。本文也就只简单举两个这类型的例子，起到个抛砖引玉的作用。

1.变量调节器插件。  
modifier.trim.php

```
function smarty_modifier_trim($string){
    return trim($string);
}
```

index.html

`{$str|trim}`2.自定义函数插件  
function.print.php

```
function smarty_function_print.php($params){
    print_r($params);
}
```

index.html

`{print arg=$arr}`
