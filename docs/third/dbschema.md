---
title: 详解Ecstore中的数据表结构定义文件dbschema
date: 2014-04-10 11:25:59
categories: 三方产品
tags: 
- ecstore
- dbschema
- sdfpath
---

任何系统的操作无非都是对数据库的各种操作的结合,而对于ecstore的数据库操作可能与其他常见项目有些不太一样.  
可能有新入手的朋友会尝试在数据库中直接创建表,可是发现创建之后不能使用,那是因为ecstore的缓存机制的原因.  
ecstore的数据库表不是常规那种直接在数据库中操作增删表的,而是通过定义dbschema目录下的数据表文件进行定义.  
官方目录结构对dbschema目录的解释是:

`app/{$app_name}/dbschema    {$app_name}的数据库表定义文件`通过文档可以理解,在ecos安装时,会扫描相关app中的dbschema中的文件,用这个文件生成相应的表结构并创建,同时也用来定义desktop app的列表项,即finder列表及操作项.

通常情况下数据库的一个表会对应一个dbschema定义文件(数据库表定义文件)和一个model.数据库表名采用下划线命名法, 并且只允许小写字母.  
**dbschema约定:**  
表名: {$db\_prefix}{$app\_name}\_{$filename}  
数据库表名前缀: {$db\_prefix} 系统默认为sdb\_, 定义在config/config.php里, DB\_PREFIX  
文件名: $filename.php  
存放目录名: app/{$app\_name}/dbschema  
完整文件名: app/{$app\_name}/dbschema/{$filename}.php  
对应的model类名: {$app\_name}\_mdl\_{$filename}  
所属app: {$app\_name}

dbschema文件内容返回的是一个数组形式,每个键值都有不同的定义,下面给出一个简单的例子加以说明.

```
$db['members']=array (
    'columns' => array(
        'ruesin_id' =>  //键值即是字段名称
        array (
            'type' => 'int(8)',                       // 字段类型
            'pkey' => true,                           // 是否是主键 默认为false
            'required' => true,                       // 不能为空 默认为false
            'extra' => 'auto_increment',              // 扩展值//自增//如果要用一般只使用这个即可
            'comment' => app::get('b2c')->_('用户名'),//注释
            'sdfpath' => 'pam_account/account_id',    //保存数据时的数组格式
            'label' => app::get('b2c')->_('用户名'),  //显示的名称
            'width' => 110,                           //本列的初始宽度
            'searchtype' => 'has',                    //搜索的类型//详细可参考数据查询过滤器_filter
            'filtertype' => 'normal',                 //高级筛选的过滤类型//设置为normal按type的来生成过滤
            'filterdefault' => 'true',                //默认在高级筛选中显示
            'order' => 20,                            //在列表中的权重//越小越靠前
            'in_list' => true,                        //是否显示在列表项中
            'default_in_list' => true,                //默认显示在列表项中
            'is_title'=>true,
        ),
        'member_lv_id' =>
        array(
            'type' => 'table:member_lv@b2c',           //关联b2c app下member_lv表中的主键类型
            'default' => 0,                            // 默认值
            'required' => true,
            'editable' => false,
        ),
        'status' =>
        array(
            'default' => 'programmer',
            'type' => array (     // 生成枚举类型
            'programmer' => app::get('b2c')->_('程序员'),
            'literature' => app::get('b2c')->_('文艺青年'),
            ),
            'label' => app::get('b2c')->_('身份'),
            'width' => 100,
            'in_list' => true,
            'default_in_list' => true,
        )
    ),
    'version' => '$Rev: 44008 $' ,                       //版本号
    'engine' => 'innodb' ,                               //mysql引擎
    'comment' => app::get('b2c')->_('Ruesin的数据表'),   //表描述
);
```

#### 一、字段类型

系统中定义的字段类型有很多,详细可查询官方文档,这里只列出了一些比较特别的.并稍作介绍.  
**1.关联主键表**

```
'type' => 'table:member_lv@b2c',
//关联b2c应用下member_lv表中的主键类型
//如果在同一app下,可省略@appname
```

**2.枚举类型**

```
'type' => array (
    'programmer' => app::get('b2c')->_('程序员'),
    'literature' => app::get('b2c')->_('文艺青年'),
),
// 生成枚举类型 enum('programmer','literature')
// 高级搜索将产生一个select选项可以进行选择
// 在后台finder列表中,会根据查询出来的值显示出枚举出的数据
```

**3.email类型**  
//存在数据库中的类型是varchar(255),虽然可以直接写成mysql类型,但在这里写了email类型后,使用dbeav的save时会验证是否是email类型的数据 如果不是将抛出异常.  
(跟money类型异曲同工,其实有很多类型由于在程序中我们都有验证,所以可以直接写成mysql类型的)

#### 二、后台finder列表

**1.searchtype**  
列表页中简单搜索的处理方式,如果dbschema中存在searchtype则会在desktop列表上显示相关的简单搜索,而searchtype的类型使用的是dbeav中的过滤器\_filter类型

```
'than'=>' > '.$var,
'lthan'=>' < '.$var,
'nequal'=>' = \''.$var.'\'',
'noequal'=>' <> \''.$var.'\'',
'tequal'=>' = \''.$var.'\'',
'sthan'=>' <= '.$var,
'bthan'=>' >= '.$var,
'has'=>' like \'%'.$var.'%\'',
'head'=>' like \''.$var.'%\'',
'foot'=>' like \'%'.$var.'\'',
'nohas'=>' not like \'%'.$var.'%\'',
'between'=>' {field}>='.$var[0].' and '.' {field}<'.$var[1],
'in' =>" in ('".implode("','",(array)$var)."') ",

```

#### 三、sdfpath

刚开始看到sdfpath时感觉有点\*\*\*,也不知道是哪位高人前辈命名的~~平时自己做的app也很少用到,所以也没做过多注意.  
后来二开order时,又看到这个,感觉好二~~~ 于是有看了下dbschema里后理解了,说下自己的见解,也给大家起点抛砖引玉的作用.

```
'name' =>
array(
    'type' => 'varchar(20)',
),
'email' =>
array(
    'type' => 'email',
    'sdfpath' => 'connect/email',
),
```

保存的时候,POST的数组是:

```
$_POST=array(
    'name'=>'Ruesin',
    'connect'=>array(
        'email'=>'ruesin@163.com',
    )
);
```

至此,数据表定义文件dbschema已经大体给介绍完了,虽然有很多详细细节没有讲解,但是结合官方文档查看即可,而本文的介绍的很多是官方文档没有明确介绍的部分,大家可以拿此文和官方文档一起学习.

创建好dbschema文件后,记得cmd update一下哦,不然是无法更新出数据表的~~
