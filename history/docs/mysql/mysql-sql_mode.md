---
title: mysql SQL_MODE 的配置。
date: 2016-03-24 09:57:30
categories: MySQL
---

最近接手一个正在运行中的项目，拉到本地运行的时候出了问题，在插入数据库的时候报错 Incorrect integer value: ” for column ‘id’ at row 1。

字面意思就是自增主键ID被写成了空，导致插入失败。原服务器上跑的是正常的，应该是环境的问题了。

打印了下sql语句：
```
INSERT INTO `config` (`id`,`key`,`value`) VALUES ('','aaa','bbb');
```
有些别扭，正常套路，自增主键应该不用写的，不知道当时的程序是怎么想的。

直接执行sql语句也是报错，可见这条语句就是有错的，我本地mysql版本是5.7的，编译好之后很少改配置，除了有一次跑其他项目的时候，改过一次sql_mode，可能是这方面的问题，由于当时并没有深究，遂细查了下。

先说下我怎么解决的，再复制网上查的资料。

查看了下我本地的 my.cnf，看到我之前把默认为空的SQL_MODE写成了：sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES，将SQL_MODE改了成：sql_mode=’NO_ENGINE_SUBSTITUTION’，就可以了。

下面是网上复制的 SQL_MODE 可设置项：

STRICT_TRANS_TABLES：在该模式下，如果一个值不能插入到一个事务表(例如表的存储引擎为InnoDB)中，则中断当前的操作不影响非事务表(例如表的存储引擎为MyISAM)。

ALLOW_INVALID_DATES：该选项并不完全对日期的合法性进行检查，只检查月份是否在1～12之间，日期是否在1～31之间。该模式仅对DATE和DATETIME类型有效，而对TIMESTAMP无效，因为TIMESTAMP总是要求一个合法的输入。

ANSI_QUOTES：启用ANSI_QUOTES后，不能用双引号来引用字符串，因为它将被解释为识别符。

ERROR_FOR_DIVISION_BY_ZERO：在INSERT或UPDATE过程中，如果数据被零除(或MOD(X，0))，则产生错误(否则为警告)。如果未给出该模式，那么数据被零除时MySQL返回NULL。如果用到INSERT IGNORE或UPDATE IGNORE中，MySQL生成被零除警告，但操作结果为NULL。

HIGH_NOT_PRECEDENCE NOT：操作符的优先顺序是表达式。例如，NOT a BETWEEN b AND c被解释为NOT(a BETWEEN b AND c)，在一些旧版本MySQL中， 前面的表达式被解释为(NOT a)BETWEEN b AND c。启用HIGH_NOT_PRECEDENCE SQL模式，可以获得以前旧版本的更高优先级的结果。

IGNORE_SPACE：函数名和括号“(”之间有空格。除了增加一些烦恼，这个选项好像没有任何好处，要访问保存为关键字的数据库、表或列名，用户必须引用该选项。例如某个表中有user这一列，而MySQL数据库中又有user这个函数， user会被解释为函数，如果想要选择user这一列，则需要引用。

NO_AUTO_CREATE_USER：禁止GRANT创建密码为空的用户。

NO_AUTO_VALUE_ON_ZERO：该选项影响列为自增长的插入。在默认设置下，插入0或NULL代表生成下一个自增长值。如果用户希望插入的值为0，而该列又是自增长的，那么这个选项就有用了。

NO_BACKSLASH_ESCAPES：反斜杠“\\”作为普通字符而非转义符。

NO_DIR_IN_CREATE：在创建表时忽视所有INDEX DIRECTORY和DATA DIRECTORY的选项。

NO_ENGINE_SUBSTITUTION：如果需要的存储引擎被禁用或未编译，那么抛出错误。默认用默认的存储引擎替代，并抛出一个异常。

NO_UNSIGNED_SUBTRACTION：之前已经介绍过，启用这个选项后两个UNSIGNED类型相减返回SIGNED类型。

NO_ZERO_DATE：在非严格模式下，可以插入形如“0000-00-00 00:00:00”的非法日期，MySQL数据库仅抛出一个警告。而启用该选项后，MySQL数据库不允许插入零日期，插入零日期会抛出错误而非警告。

NO_ZERO_IN_DATE：在严格模式下，不允许日期和月份为零。如“2011-00-01”和“2011-01-00”这样的格式是不允许的。采用日期或月份为零的格式时MySQL都会直接抛出错误而非警告。

ONLY_FULL_GROUP_BY：对于GROUP BY聚合操作，如果在SELECT中的列没有在GROUP BY中出现，那么这句SQL是不合法的，因为a列不在GROUP BY从句中，

PAD_CHAR_TO_FULL_LENGTH：对于CHAR类型字段，不要截断空洞数据。空洞数据就是自动填充值为0×20的数据。先来看MySQL数据库在默认情况下的表现。

PIPES_AS_CONCAT：将“||”视为字符串的连接操作符而非或运算符，这和Oracle数据库是一样的，也和字符串的拼接函数Concat相类似。

REAL_AS_FLOAT：将REAL视为FLOAT的同义词，而不是DOUBLE的同义词。

STRICT_ALL_TABLES：对所有引擎的表都启用严格模式。(STRICT_TRANS_TABLES只对支持事务的表启用严格模式)。

在严格模式下，一旦任何操作的数据产生问题，都会终止当前的操作。对于启用STRICT_ALL_TABLES选项的非事务引擎来说，这时数据可能停留在一个未知的状态。这可能不是所有非事务引擎愿意看到的一种情况，因此需要非常小心这个选项可能带来的潜在影响。

下面的几种SQL_MODE设置是之前讨论的几种选项的组合：

ANSI：等同于REAL_AS_FLOAT、PIPES_AS_CONCAT和ANSI_QUOTES、IGNORE_SPACE的组合。

ORACLE：等同于PIPES_AS_CONCAT、 ANSI_QUOTES、IGNORE_SPACE、 NO_KEY_OPTIONS、 NO_TABLE_OPTIONS、 NO_FIELD_OPTIONS和NO_AUTO_CREATE_USER的组合。

TRADITIONAL：等同于STRICT_TRANS_TABLES、 STRICT_ALL_TABLES、NO_ZERO_IN_DATE、NO_ZERO_DATE、 ERROR_FOR_DIVISION_BY_ZERO、

NO_AUTO_CREATE_USER和 NO_ENGINE_SUBSTITUTION的组合。

MSSQL：等同于PIPES_AS_CONCAT、 ANSI_QUOTES、 IGNORE_SPACE、NO_KEY_OPTIONS、NO_TABLE_OPTIONS和 NO_FIELD_OPTIONS的组合。

DB2：等同于PIPES_AS_CONCAT、ANSI_QUOTES、 IGNORE_SPACE、NO_KEY_OPTIONS、 NO_TABLE_OPTIONS和NO_FIELD_OPTIONS的组合。

MYSQL323：等同于NO_FIELD_OPTIONS和HIGH_NOT_PRECEDENCE的组合。

MYSQL40：等同于NO_FIELD_OPTIONS和HIGH_NOT_PRECEDENCE的组合。

MAXDB：等同于PIPES_AS_CONCAT、ANSI_QUOTES、IGNORE_SPACE、NO_KEY_OPTIONS、 NO_TABLE_OPTIONS、 NO_FIELD_OPTIONS和 NO_AUTO_CREATE_USER的组合。

SQL_MODE的设置其实是比较冒险的一种设置，因为在这种设置下可以允许一些非法操作，比如可以将NULL插入NOT NULL的字段中，也可以插入一些非法日期，如“2012-12-32”。因此在生产环境中强烈建议开发人员将这个值设为严格模式，这样有些问题可以在数据库的设计和开发阶段就能发现，而如果在生产环境下运行数据库后发现这类问题，那么修改的代价将变得十分巨大。此外，正确地设置SQL_MODE还可以做一些约束(Constraint)检查的工作。
