---
title: PHP通过将Excel转为csv文本读取(写入)表格(数据库)，实现数据的导入导出
date: 2014-09-16 11:29:05
categories: PHP
---

项目开发中经常碰到的就是数数据的导出备份和导入还原，对开发人员来说当然是直接对数据库操作了。但是大部分非开发人员、用户是不会进行数据库操作的，有时还需要导出表格查看管理等。这时候就需要开发人员做导出导入的功能了。

而最常见的方法就是将数据导出为.csv格式的，既可以用excel打开，又可以将本地的excel数据导入到线上。

当然，也有方法可以直接操作excel，就是使用PHP自定义类phpExcelReader、PHPExcel等。本文主要是写通过将Excel另存为csv之后的操作，咱时不对此方法进行过多赘述。

CSV是逗号分隔值的英文缩写，通常都是纯文本文件。CSV格式是分隔的数据格式，有字段/列分隔的逗号字符和记录/行分隔换行符。通常CSV文件可以用EXCEL正常打开，所以才有了将数据导出为csv格式的方法。

PHP自带的csv函数有——读取：fgetcsv()，写入：fputcsv()。

fgetcsv() 函数从文件指针中读入一行并解析 CSV 字段。解析读入的行并找出 CSV 格式的字段，然后返回一个包含这些字段的数组。

```
$file = fopen(ROOT_DIR.'/taobao.csv','r');
while ($row = fgetcsv($file)) {
    $list[] = $row;
}
fclose($file)
```

fputcsv() 函数将行格式化为 CSV 并写入一个打开的文件。

该函数返回写入字符串的长度。若出错，则返回 false。

fputcsv() 将一行（用 fields 数组传递）格式化为 CSV 格式并写入由 file 指定的文件。

```
$arr = array(
    '0' => array(
	    '0' => 'Ruesin',
	    '1' => 'boy',
	    '2' => '24',
	),
    '1' => array(
		'0' => 'Linney',
		'1' => 'girl',
		'2' => '23',
    )
);
$file = fopen("taobao.csv","w");
foreach ($arr as $line){
	fputcsv($file,$line);
}
fclose($file);
```

至于其他的剩下的就是各种数组的操作了，有兴趣的朋友可以去看下本博有关PHP数组的部分文章。
