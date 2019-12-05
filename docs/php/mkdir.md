---
title: 利用php函数mkdir递归创建层级目录
date: 2014-07-04 14:25:46
categories: PHP
tags: 
- php
- php函数
- php基础
- mkdir
---

项目开发中免不了要在服务器上创建文件夹，比如上传图片时的目录，模板解析时的目录等。这不当前手下的项目就用到了这个，于是总结了几个循环创建层级目录的方法。

php默认的mkdir一次只能创建一层目录，而要逐层创建各级目录的话，一般都是先从父创建，然后逐层往下创建，但是这样手工创建的话，有点太过于麻烦了。

我们写程序是做什么的？不久是为了能自动化实现我们需要的功能么，这里的方法就是为了能够通过程序帮我们自动创建完成层级目录。

思路有两种：  
一、从上往下(父级→子级)  
1.先判断 父级 目录是否存在，不存在则创建；  
2.判断二级子目录是否存在，不能存在则创建，  
3.在第二步中以子目录作为参数递归调用函数本身。

二、从下往上(子级→父级)  
1.先判断最底层目录是否存在；  
2.判断底层目录的上层目录是否存在，不存在则以上层目录作为参数递归进行。

以下是几种方法：

1：递归创建目录，此种方法是我目前感觉比较好的方法。

```
function mkDirs($dir){
    if(!is_dir($dir)){
        if(!mkDirs(dirname($dir))){
            return false;
        }
        if(!mkdir($dir,0777)){
            return false;
        }
    }
    return true;
}
mkDirs('1/2/3/');
```

2：递归创建级联目录，如果第一个方法不太理解的话，可以结合下面这个方法理解

```
function mkDirs1($path){
    if(is_dir($path)){//已经是目录了就不用创建
        return true;
    }
    if(is_dir(dirname($path))){//父目录已经存在，直接创建
        return mkdir($path);
    }
    mkDirs1(dirname($path));//从子目录往上创建
    return mkdir($path);//因为有父目录，所以可以创建路径
}
//mkDirs1('1/2/3/');
```

3：迭代创建级联目录

```
function makedir($path){
    $arr=array();
    while(!is_dir($path)){
        array_push($arr,$path);//把路径中的各级父目录压入到数组中去，直接有父目录存在为止（即上面一行is_dir判断出来有目录，条件为假退出while循环）
        $path=dirname($path);//父目录
    }
    if(empty($arr)){//arr为空证明上面的while循环没有执行，即目录已经存在
        echo $path,'已经存在';
        return true;
    }
    while(count($arr)){
        $parentdir=array_pop($arr);//弹出最后一个数组单元
        mkdir($parentdir);//从父目录往下创建
    }
}
makedir('1/2/3');
```

PS：有时候程序脚本的文件不一定在网站根目录，而创建的文件需要在根目录创建，那我们就需要用到网站根目录路径：$\_SERVER\['DOCUMENT\_ROOT'\];所以我不建议使用后面的三个方法。  
以下三种是通过’/'分割路径的方法进行创建的。

```
function mk1($dir){
    $arr=explode("/",$dir);
    $path='';
    for($i=0;$i
```
