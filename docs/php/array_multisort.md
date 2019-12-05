---
title: PHP函数array_multisort实现多维数组按照键值进行排序
date: 2014-02-26 10:31:05
categories: PHP
tags: 
- php
- 数组
---

一直以来对PHP数组排序都是随手用系统函数或者常用的排序办法，或者直接自己写函数了。

今天工作中涉及到了二维数组按照某个键值进行排序时，顺道把php的数组排序函数温习了下。正所谓温故而知新嘛。

需求：在给出的产品列表中，把参加团购的商品放在最前面，即根据二维数组中的 is\_group 项对数组进行排序。

```
$aProduct = array(
    0=> array('goods_id' => 1,'name' =>'iPhone 4','is_group' =>0),
    1=> array('goods_id' => 2,'name' =>'iPhone 4s','is_group' =>0),
    2=> array('goods_id' => 3,'name' =>'iPhone 5','is_group' =>1),
    3=> array('goods_id' => 4,'name' =>'iPhone 5s','is_group' =>0)
);
function arraySort($multi_array,$sort_key,$sort=SORT_ASC){
    if(is_array($multi_array)){
        foreach ($multi_array as $row_array){
            if(is_array($row_array)){
                $key_array[] = $row_array[$sort_key];
            }else{
                return false;
            }
        }
    }else{
        return false;
    }
    array_multisort($key_array,$sort,$multi_array);
    return $multi_array;
}
print_r(arraySort($aProduct,'is_group',SORT_DESC));exit;
```

整个过程中的核心是对PHP内置函数array\_multisort()的使用。下面是对array\_multisort的简单介绍：

array\_multisort() 可以用来一次对多个数组进行排序，或者根据某一维或多维对多维数组进行排序。成功返回 TRUE，失败则返回 FALSE。

这个函数的排序类似 SQL 的 ORDER BY 子句的功能，参数中的数组被当成一个表的列并以行来进行排序，第一个数组是要排序的主要数组。数组中的行（值）比较为相同的话，就会按照下一个输入数组中相应值的大小进行排序，依此类推。

本函数的参数结非常灵活，第一个参数必须是一个数组。随后的每一个参数可能是数组，也可能是下面的排序顺序标志之一：

排序顺序：  
SORT\_ASC – 默认，按升序排列。(A-Z)  
SORT\_DESC – 按降序排列。(Z-A)

排序类型：  
SORT\_REGULAR – 默认。将每一项按常规顺序排列。  
SORT\_NUMERIC – 将每一项按数字顺序排列。  
SORT\_STRING – 将每一项按字母顺序排列。

PS：每个数组后指定的排序标志仅对该数组有效，并且每个数组之后不能指定两个同类的排序标志。

PS：字符串键名将被保留，但是数字键将被重新索引，从 0 开始，并以 1 递增。
