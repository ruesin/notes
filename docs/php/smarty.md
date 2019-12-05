---
title: 用Smarty模板引擎生成静态HTML文件
date: 2013-12-31 00:00:20
categories: PHP
tags: 
- php
- smarty
---

用php生成静态文件说白了无非就是打开、读取、写入、关闭而已，方法无外乎fopen()，fwrite()，fclose()。  
说来简单、但用在smarty上着实费了我一番功夫、最后还是看手册和网上查才弄好。最后有附smarty手册中对fetch介绍。

用smarty生成静态html文件的关键就是用缓存技术，开启缓冲，用display或者fetch向前台传输数据的时候其实不会显示在view上，打开文件，读取文件，写入文件。  
前者是在display()的同时，增加了ob\_start()、ob\_get\_contents()和fwrite() 函数。  
后者则是利用smarty模板引擎的fetch函数，由smarty解析的文件保存到一个变量，然后再读写文件。

```
/*
* Created on 2013-3-20
* Author: Ruesin
* Link: http://old.ruesin.com
*/

include("./smarty/Smarty.class.php");
//include("./configs/config.php");
$smarty=new Smarty();
$smarty->template_dir='./templates/';
$smarty->compile_dir='./templates_c/';
$smarty->config_dir='./configs/';
$smarty->cache_dir='./cache/';
$smarty->caching = false;
$smarty->left_delimiter='<{';
$smarty->right_delimiter='}>';

//用for循环测试批量生成文件
for($i=1;$i<3;$i++){
$smarty->assign('recont','小信吃了'.$i.'个苹果');
//$smarty->display('index.html');    //我们的目的不是显示、而是获取他的内容
//第一种方法
$content=$smarty->fetch("index.htm");//获得smarty替换后的模板文件内容、也就是display之后的index.php的内容
$fopen=fopen("lgx_".$i.".html","w");
fwrite($fopen,$content);
fclose($fopen);
//第二种方法
/*
ob_start();//开启缓冲区
$smarty->display('index.htm');
$content=ob_get_contents();//获得缓冲区内容
$fopen=fopen("lgx_".$i.".html","w");
fwrite($fopen,$content);
fclose($fopen);
ob_end_claen();//关闭缓冲区
*/
}
/*
//创建html文件的函数
function mkhtml($file,$content){
$fopen = fopen($file,'w');
fwrite($fopen,$content);
fclose($fopen);
}
*/
```

上面两种方式是常用的：  
第一种用display方法，用$content = ob\_get\_contents();得到向前台输出的内容。  
第二种用fetch直接获取向前台输出的内容（两种都不会真正地展示出来中）。

附：smarty手册中对fetch的介绍

[![smarty_fetch](/images/2014/04/smarty_fetch.png)](/images/2014/04/smarty_fetch.png)
