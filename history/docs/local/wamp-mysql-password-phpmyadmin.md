---
title: Wamp下修改mysql的默认空密码并设置phpmyadmin是否验证密码登录
date: 2014-11-11 11:30:56
categories: 本地
---

为了方便开发使用，wamp默认的mysql是没有密码的。但是我们很多时候为了方便开发，与线上配置文件一致等，就需要设置数据库的密码。可能会有同学想到这里就去各种搜索，以为wamp需要什么特殊配置，其实，wamp和自己搭建的环境是一样的，只不过是wamp把各部件集中在一起，并提供了可视化操作而已。那么到底要怎么做呢？下面有两种办法可以解决。

一、通过phpmyadmin可视化操作

打开phpmyadmin，点击权限，这时页面上会显示一张用户权限表，找到用户为：root、主机为：localhost的数据行，点击后面的修改按钮，弹出详细的权限配置页面，找到里面的修改密码项， 两次输入你想修改的密码后，点击执行就完成了数据库中root@localhost权限的密码修改。也可以将其他的权限一并修改了。

二、通过mysql控制台进行操作

点击wamp，找到mysql下的控制台。

[![mysql-console](/images/2014/11/mysql-console.jpg)](/images/2014/11/mysql-console.jpg)

```
mysql> use mysql
Database changed
mysql> update user set password=PASSWORD('root') where user='root';
Query OK, 0 rows affected (0.06 sec)
Rows matched: 3  Changed: 0  Warnings: 0
mysql> flush privileges;
Query OK, 0 rows affected (0.05 sec)
```

好的，到这里为止呢，mysql的密码已经修改完成了。

但是呢，改完之后，我们发现phpmyadmin无法登录了。

```
#1045 - Access denied for user 'root'@'localhost' (using password: NO)
phpMyAdmin 尝试连接到 MySQL 服务器，但服务器拒绝连接。您应该检查配置文件中的主机、用户名和密码，并确认这些信息与 MySQL 服务器管理员所给出的信息一致。
```

这因为，wamp下的phpmyadmin默认设置的是用户无需验证自动登录，之前配置文件中设置的是密码为空，而我们刚才把密码改过了，所以才会报错。

在 wamp/apps/phpmyadmin 目录下找到 config.inc.php 文件， 将 $cfg\['Servers'\]\[$i\]\['password'\] 的值修改为我们刚才设置的密码。重启wamp服务，再次访问phpmyadmin就可以了。

`$cfg['Servers'][$i]['password'] = 'root';`通常情况下，我们本地按照刚才的设置，无需验证即可登录phpmyadmin是非常方便的，但避免不了某些强迫症同学想要设置成验证登录（比如博主..）。还是修改配置文件，将登录类型由config改为cookie即可。

`$cfg['Servers'][$i]['auth_type'] = 'cookie'; //原来为config`如果设置登录类型为cookies的话，之前设置的 $cfg\['Servers'\]\[$i\]\['user'\] 和 $cfg\['Servers'\]\[$i\]\['password'\] 就等同于无了，因为已经不走配置文件了。

可能还会出现这个问题，登录 phpmyadmin 提示“配置文件现在需要一个短语密码”，其实也没什么影响的，但是实在别扭的话也可以解决。打开 wamp\\apps\\phpmyadmin\\libraries\\config.default.php 。

`$cfg['blowfish_secret'] = '任意字符串';`最后还是那句话，wamp不过是把各个部件集中在一起了，省去了我们依次安装配置的麻烦，其他的跟自己搭建的环境没什么不同，按照正常思路配置就行。
