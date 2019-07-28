---
title: Centos 搭建多版本库svn服务器
date: 2016-07-06 14:35:06
categories: 运维
---

```
创建版本库文件夹  
# mkdir -p /data/svn/sinsvn  
创建版本库  
# svnadmin create /data/svn/sinsvn  
# mkdir -p /data/www/sinsvn  
导入所需管理的项目到版本库repository中  
# svn import /data/www/sinsvn/ file:///data/svn/sinsvn -m "svn first test"  
检查是否导入成功  
# svn list –verbose file:///data/svn/sinsvn  
修改版本库的配置文件  
# vim /data/svn/sinsvn/conf/svnserve.conf
```

```
[general]  
anon-access = none  
auth-access = write  
password-db = ../../passwd  
authz-db = ../../authz  
realm =sinsvn
```

`cp /data/svn/sinsvn/conf/passwd /data/svn  `
`cp /data/svn/sinsvn/conf/authz /data/svn`

修改允许访问版本库的用户文件  
`# vim /data/svn/passwd  `
```
[users]  
harry = harryssecret  
sin = sinssecret  
surpersin = surpersin
```

`# vim /data/svn/authz  `
```
[groups]  
myteam = harry,sin

[/]  
surpersin = rw

[sinsvn:/]  
@myteam = rw

[secsvn:/www]  
@myteam =r  
sin= rw

[sincms:/]  
sin= rw  
harry=  
```
启动 svn 服务  
`# svnserve -d -r /data/svn/`

至此，版本库 sinsvn 就可以使用了。  
多项目的话，有几种解决方案：  
1.启动多个svn服务，每个SVN监听不同的IP或端口。  
`# svnserve -d –listen-port 3690 -r /data/svn1  `
`# svnserve -d –listen-port 3691 -r /data/svn2`

2.在一个版本库下，按项目分不同目录，在authz控制各项目目录的权限。  
```
[sinsvn:/pro1]  
sin= rw  
[sinsvn:/pro2]  
@myteam =rw
```

3.SVN服务监听版本库的根目录 /data/svn，然后在/data/svn下创建多个版本库，在各版本库下的配置文件中，指定用户及权限文件到根目录下的文件，就可以集中管理了，上面的例子已经是按照这么做的了。  
`# svnserve -d -r /data/svn/`

svn 自动更新钩子：  
```
# cd /data/svn/sinsvn/hooks  
# cp post-commit.tmpl post-commit  
# vim post-commit
```
```
export LANG=zh_CN.utf-8  
REPOS="1"
REV="2"
SVN=/usr/bin/svn  
WEB=/data/website/shebao/  
LOG=/data/svn/logs/shebao.log  
$SVN update $WEB –username ruesin –password ruesin  
if [ $? == 0 ]  
then  
echo "$REPOS" "$REV" >> $LOG  
echo `date` >> $LOG  
echo "####################" >> $LOG  
fi
```
