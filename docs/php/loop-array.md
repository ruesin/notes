---
title: PHP遍历数组常用方法foreach,for,while的性能比较
date: 2014-06-18 14:22:42
categories: PHP
tags: 
- php
- 数组
- php性能
- php数组
- php效率
---

工作中我们经常会用到数组遍历操作，常用的方法有foreach(),for(),while()，一般情况下我是习惯性使用foreach，没有考虑过执行效率，今天突发奇想对比一下这几个方法的性能。

从网上查了很多理论，实践是检验真理的唯一标准，那咱们就做个试验测试一下吧。

```
/*
* 分别用for/while/foreach
* 对包含10000个元素的数组进行各项操作
* 1.简单数组遍历,不对数组进行操作
* 2.对数组进行操作
* 3.通过函数对数组操作
*/
$max = 10000;
$arr = range(0, $max);
$temp = '';

// for
$t1 = microtime(true);
for ($i = 0; $i < $max; $i++) {
    $temp = $temp + 1;
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "for 无操作   : {$t}".'<br />';

$t1 = microtime(true);
for ($i = 0; $i < $max; $i++) {
    $arr[$i] = $arr[$i] + 1;
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "for 有操作   : {$t}".'<br />';

$t1 = microtime(true);
for ($i = 0; $i < $max; $i++) {
    addOne($arr[$i]);
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "for 用函数 : {$t}".'<br />';

echo "<hr />";

// while
$i=1;
$t1 = microtime(true);
while ($i < count($arr)) {
    $temp = $temp +1;
    $i++;
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "while 无操作 : {$t}".'<br />';
$i=1;
$t1 = microtime(true);
while ($i < count($arr)) {
    $arr[$i] = $arr[$i] + 1;
    $i++;
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "while 有操作 : {$t}".'<br />';
$i=1;
$t1 = microtime(true);
while ($i < count($arr)) {
    addOne($arr[$i]);
    $i++;
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "while 用函数 : {$t}".'<br />';

echo "<hr />";

// foreach 有 key
echo "foreach 有 key <br />";
$t1 = microtime(true);
foreach ($arr as $k => &$v) {
    $temp = $temp + 1;
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "foreach 无操作 : {$t}".'<br />';

$t1 = microtime(true);
foreach ($arr as $k => &$v) {
    $v = $v + 1;
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "foreach 有操作 : {$t}".'<br />';

$t1 = microtime(true);
foreach ($arr as $k => &$v) {
    addOne($v);
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "foreach 用函数 : {$t}".'<br />';

echo "<hr/>";

// foreach 无 key
echo "foreach 无 key <br />";
$t1 = microtime(true);
foreach ($arr as $v) {
    $temp = $temp + 1;
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "foreach 无操作 : {$t}".'<br />';

$t1 = microtime(true);
foreach ($arr as $v) {
    $v = $v + 1;
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "foreach 有操作 : {$t}".'<br />';

$t1 = microtime(true);
foreach ($arr as $v) {
    addOne($v);
}
$t2 = microtime(true);
$t = $t2 - $t1;
echo "foreach 用函数 : {$t}".'<br />';

//function
function addOne(&$item) {
    $item = $item + 1;
}
```

结果

```
for     无操作 : 0.0033011436462402
for     有操作 : 0.0045318603515625
for     用函数 : 0.0088419914245605
while   无操作 : 0.0087449550628662
while   有操作 : 0.0098490715026855
while   用函数 : 0.0072541236877441
foreach 有 key
foreach 无操作 : 0.0014090538024902
foreach 有操作 : 0.0011789798736572
foreach 用函数 : 0.003734827041626
foreach 无 key
foreach 无操作 : 0.00086092948913574
foreach 有操作 : 0.00080299377441406
foreach 用函数 : 0.0035700798034668
```

整体效果来看：while的性能是最差的，其次是for，而执行效率最快的是foreach，特别是没有使用$key时。

**foreach/for**

for循环是PHP中最复杂的循环结构。expr1 在循环开始前无条件求值一次。expr2 在每次循环开始前求值。expr3 在每次循环之后被求值（执行）。  
而对于遍历数组for需要知道数组长度再用$i++来操作，一次循环要进行多次条件判断或计算，而foreach不需要进行计算和判断，可自动检测并输入key,和value。

foreach 有key/无key

foreach (array as $value)遍历给定的 array 数组。每次循环中，当前单元的值被赋给 $value 并且数组内部的指针向前移一步。  
foreach (array as $key => $value)不仅要有上述操作，而且当前单元的键值也会在每次循环中被赋给变量$key。

**foreach/while**

foreach是对数组副本进行操作（通过拷贝数组），而while则通过移动数组内部指标进行操作，一般逻辑下认为，while应该比foreach快（因为foreach在开始执行的时候首先把数组复制进去，而while直接移动内部指标。），但结果刚刚相反。原因应该是，foreach是PHP内部实现，而while是通用的循环结构。  
而PHP内部的复制机制是“引用计数，写时复制”，也就是说，即便在PHP里复制一个变量，最初的形式从根本上说其实仍然是引用的形式，只有当变量的内容发生变化时，才会出现真正的复制，之所以这么做是出于节省内存消耗得目的，同时也提升了复制的效率。

**for/while**

理论上感觉这两个应该是一样的啊,循环/计算/判断/循环… 可是为什么性能差这么多? 希望有哪位朋友看到能讲解一下.

注: 当 foreach 开始执行时，数组内部的指针会自动指向第一个单元。这意味着不需要在 foreach 循环之前调用 reset()。  
注: 除非数组是被引用，foreach 所操作的是指定数组的一个拷贝，而不是该数组本身。因此数组指针不会被 each() 结构改变，对返回的数组单元的修改也不会影响原数组。  
注: foreach 不支持用“@”来禁止错误信息的能力。  
注: 自php5起，foreach 可以很容易地通过在 $value 之前加上 & 来修改数组的单元，此方法将以引用赋值而不是拷贝一个值。
