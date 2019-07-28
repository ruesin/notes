---
title: Ecstore通过dbschema更改数据表。WARNING:512 @ ALTER IGNORE TABLE 
date: 2015-04-20 08:47:59
categories: 三方产品
---

最近做了个项目，二开了b2c\_members数据表，dbschema定义很规范，执行cmd update，本地测试一切正常，测试服务器上也没问题，后续的一系列的数据操作都是好的。自信满满的把文件交付给了客户，可是在客户服务器上更新时，却报错了！

[![cmd_update](/images/2015/04/cmd_update.jpg)](/images/2015/04/cmd_update.jpg)

请大家不要介意这蛋疼的win服务器，其实我也很蛋疼。。。

而我的dbschema里没定义什么东西啊，只是简单的加了个字段。

[![dbschema](/images/2015/04/dbschema.jpg)](/images/2015/04/dbschema.jpg)

WARNING:512 @ ALTER IGNORE TABLE `sdb\_b2c\_members`  
ADD COLUMN `scu\_id` mediumint(8) unsigned default 0 comment ‘联盟商ID’ A  
FTER crm\_member\_id;:You have an error in your SQL syntax; check the manual that  
corresponds to your MySQL server version for the right syntax to use near ‘IGNOR  
E TABLE `sdb\_b2c\_members`  
ADD COLUMN `scu\_id` mediumint(8) unsigned defau’ at line 1

查看了下服务器mysql版本，mysql 5.7！而我本地的好像是 5.0 还是几来着。难道是版本问题？但是如果版本有问题，APP安装时就应该报错啊。

在网上各种搜索，没有发现有遇到同样问题的人。而报错说得很明显了，应该是 IGNOR  
E TABLE 有错，换了个关键词搜—— IGNOR  
E TABLE mysql 5.7，终于搜索到了官方文档。

[![mysql57_ignore](/images/2015/04/mysql57_ignore.jpg)](/images/2015/04/mysql57_ignore.jpg)

看文档中说的是，5.7以后移除了 IGNORE 这个扩展，以前用的最高版本的mysql是5.6，还真没注意过这个问题。

那现在的解决办法就有了，要么降级服务器mysql版本，要么就是更改ecstore中拼接sql语句的地方。

跟客户商量过后，显然是不同意降级版本，那就只能去改底层文件了。

打开 **/app/base/lib/application/dbtable.php** ， 搜索 **ALTER IGNORE TABLE** 替换成 **ALTER TABLE** 。再执行 **cmd update** 就OK了。

请注意，ecstore中，如果有数据表字段的修改等操作，需要通过 dbschema 进行操作，直接操作数据库是不起作用的。（这是常识-\_-!）

其实后来想想，完全没必要二开这个文件的，可以在新app中加数据表做统计。但现在已经上线了，而且也解决了，就将错就错的走吧。

mysql官方文档：

http://bugs.mysql.com/bug.php?id=40344

http://dev.mysql.com/worklog/task/?id=7395
