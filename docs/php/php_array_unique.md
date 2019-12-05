---
title: PHP一维数组/二维数组去重
date: 2014-03-07 11:22:45
categories: PHP
tags: 
- php
- 数组
---

PHP数组去除重复项,有个内置函数array\_unique ()。

array\_unique() 函数移除数组中的重复的值，并返回结果数组。array\_unique()先将值作为字符串排序，然后对每个值只保留第一个遇到的键名，接着忽略所有后面的键名。也就是说，当几个数组元素的值相等时，只保留第一个元素，其他的元素被删除。被返回的数组将保持第一个数组元素的键类型。即，返回的数组中键名不变。

一维数组去除重复项：

```
$arr=array("Ruesin","PHP","nginx","Mysql","apache","Ruesin");
$row=array_unique($arr);
print_r($row);
```

二维数组去除重复项：

但是php的 array\_unique函数只适用于一维数组，对多维数组并不适用，所以需要我们自己写自定义函数。

本来对二维数组去重，考虑的不过是二维数组中的一维数组不能重复，后来在网上看到了另外一种需求：一维数组中某一键名的值不能重复。

1.因为某一键名的值不能重复

```
function sin_unique($arr, $key){
    $tmp_arr = array();
    foreach($arr as $k => $v){
        if(in_array($v[$key], $tmp_arr)){
            unset($arr[$k]);
        }else{
            $tmp_arr[] = $v[$key];
        }
    }
    return $arr;
}

$arr = array(
    'one'=>array('id' => 111, 'name' => '张三'),
    'tow'=>array('id' => 111, 'name' => '李四'),
    'three'=>array('id' => 222, 'name' => '王五'),
    'four'=>array('id' => 111, 'name' => '李四'),
    'five'=>array('id' => 333, 'name' => '赵六')
);
$row=sin_unique($arr, 'id');
print_r($row);
```

2.二维数组中的一维数组不能重复

```
function unique_arr($array2D){
    foreach ($array2D as $v){
        $v = implode(",",$v); //降维
        $temp[] = $v;
    }
    $temp = array_unique($temp); //去重
    foreach ($temp as $k => $v){
        $temp[$k] = explode(",",$v); //重组
    }
    return $temp;
}

$arr = array(
    'one'=>array('id' => 111, 'name' => '张三'),
    'tow'=>array('id' => 111, 'name' => '李四'),
    'three'=>array('id' => 222, 'name' => '王五'),
    'four'=>array('id' => 111, 'name' => '李四'),
    'five'=>array('id' => 333, 'name' => '赵六')
);
$row=unique_arr($arr);
print_r($row);
```

完善一下

```
function unique_arr($array2D,$stkeep=false,$ndformat=true){
    // 判断是否保留一级数组键 (一级数组键可以为非数字)
    if($stkeep) $stArr = array_keys($array2D);
    // 判断是否保留二级数组键 (所有二级数组键必须相同)
    if($ndformat) $ndArr = array_keys(end($array2D));
    foreach ($array2D as $v){//降维
        $v = implode(",",$v);
        $temp[] = $v;
    }
    $temp = array_unique($temp);//去重
    foreach ($temp as $k => $v){//重组
        if($stkeep){
            $k = $stArr[$k];
        }
        if($ndformat){
            $tempArr = explode(",",$v);
            foreach($tempArr as $ndkey => $ndval){
                $output[$k][$ndArr[$ndkey]] = $ndval;
            }
        }else{
            $output[$k] = explode(",",$v);
        }
    }
    return $output;
}

$array2D = array(
    'one'=>array('id'=>'1111','date'=>'2222'),
    'tow'=>array('id'=>'1111','date'=>'2222'),
    'three'=>array('id'=>'2222','date'=>'3333')
);

print_r($array2D);
print_r(unique_arr($array2D,true));
```
