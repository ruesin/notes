---
title: PHP函数extract()详细介绍
date: 2014-06-11 16:35:20
categories: PHP
tags: 
- php
- php函数
- php基础
- extract
---

前些日子接了个ecmall的项目，虽然跟ecstore比起来，代码差得不是一点半点，但也是有可圈可点的地方的。

这不就让我认识了个不熟悉甚至说是没用过的php内置函数extract()。

官方的解释是:从数组中把变量导入到当前的符号表中。对于数组中的每个元素，键名用于变量名，键值用于变量值。

有时候直接看官方的例子可能不太明了，加个例子就OK了。

```
$arr=array(
    "fields"         => "g.*,v.attr_value",
    "conditions"    => "g.type_id=1 and v.part_id=1",
    "join"            => "belongs_to_partattr",
    'order'            => "g.sort_order",
    'limit'          => 3,
    'count'          => true,
);
print_r(extract($arr));
echo "<br>";
print_r($conditions);
```

说白了就是把数组换成了N个变量，变量名是键名，变量值是键值。

类似于下面的效果:

```
foreach($arr as $k=>$v){
    $$k=$v;
}
echo $conditions."<br>";
```

注意:extract函数返回的是成功设置的变量数目。

总共有三个参数，一般只会用到第一个.其他参数请参考官方文档。

[![extract](/images/2014/06/extract.jpg)](/images/2014/06/extract.jpg)
