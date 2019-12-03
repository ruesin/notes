---
title: Git 基本概念、操作及用法
date: 2015-06-25 16:18:41
categories: 基础
---

Git是一款免费、开源的分布式版本控制系统，用于敏捷高效地处理任何或小或大的项目。与常用的版本控制工具 CVS, Subversion 等不同，它采用了分布式版本库的方式，不必服务器端软件支持，开发者可以提交到本地，每个开发者通过克隆，在本地机器上拷贝一个完整的Git仓库，使源代码的发布和交流极其方便。Git 最为出色的是它的合并跟踪（merge tracing）能力。

**一、安装**

sudo apt-get install git

windows下可以使用msysgit

安装完之后设置用户和邮箱

git config –global user.name Ruesin  
git config –global user.email ruesin@163.com

还有其他配置

git config –global color.ui true ## 显示颜色

git config –global alias.st status ## 配置别名

**二、创建版本库**

mkdir ruesinGit  
cd ruesinGit

创建版本库可以直接本地创建一个新的，也可以从克隆一个已存在的版本库

git init ##初始化创建本地版本库

git clone ssh:… ## 克隆一个已存在的版本库

**三、本地基本操作**

git status #查看差异文件以及是否有提交  
git diff #查看文件具体修改了哪  
git log #查看提交日志 –pretty=oneline 只显示一行  
git reflog ## 记录操作到日志，可以看到每个版本号里到操作

git add test.txt ## 添加到暂存区  
git commit -m ‘版本注释’ ## 提交到版本库

git checkout — file ## 丢弃工作区的修改，实际是用版本库里的版本替换工作区的版本  
git reset HEAD file ## 撤销掉暂存区中的修改，重新放回工作区  
git reset –hard HEAD^ #回跳到一个版本  
git reset –hard 257ec2c044 #跳到指定版本 可以往后往前

rm file  
git rm file ## 删除版本库中的文件

**四、分支操作**

git checkout -b dev #创建并切换到dev分支

git branch dev ## 创建 dev 分支  
git checkout dev ## 切换到 dev 分支

git branch #查看当前分支  
\* dev # 当前分支  
master

在dev分支下操作

vi test.txt  
git add test.txt  
git commit -m “branch test”

git checkout master ## 切换回master分支  
cat test.txt ## 查看test.txt 文件内容 没有任何更改

git merge dev ## 将 dev 分支合并到 当前分支 master

git branch -d dev ## 删除dev分支

如果在两个分支下都编辑连test.txt文件同一位置，合并的时候就会冲突，这时候就需要手工去修复了。

看一下冲突的文件，打开之后回发现冲突的内容Git用<<<<<<<，=======，>>>>>>>标记出来了。

将冲突的地方修复一下，再次添加、提交即可。

git默认使用到是快速合并Fast forward，在这种模式下，删除分支后，会丢掉分支信息。可以使用 –no-ff 参数禁用Fast forward模式，这样Git就会在merge时生成一个新的commit，这样，从分支历史上就可以看出分支信息。

git merge –no-ff -m “merge with no-ff” dev ## 合并并提交分支

git log –graph –pretty=oneline –abbrev-commit ## 查看分支合并到路线

修复Bug时可以通过创建一个临时分支来修复，修复成功后再将临时分支删掉。但是，你现在正在dev分支上工作，并且只做到了一半，为了保证项目的正常运行，还不能提交。

这时候就需要 stash 功能了。

git stash ## 把当前工作现场“储藏”起来

git status 查看工作区，就是干净的（除非有没有被Git管理的文件）

找到要修复Bug的分支，假设是 master分支，从 master 创建临时分支，进行修复、提交、合并、删除临时分支。

然后回到 dev 分支，进行现场恢复。

git stash list ## 查看存储的“现场”列表  
stash@{0}: WIP on dev: 6224937 add merge

git stash pop ## 恢复并删除

\## git stash apply ## 恢复  
\## git stash drop ## 删除

\## git stash apply stash@{0} ## 恢复指定的场景

开发新功能时与修复BUG一样，最好也是创建一个新分支，这样新功能如果要舍弃或者怎样的都不会干涉到主分支。

git branch -D <name> ## 强行删除一个没有被合并过的分支

**五、连接远程仓库进行多人协作工作**

先看下个人文件夹下是否有 .ssh ，没有的话需要创建一个 SSH Key， .ssh 中有两个文件 id\_rsa（私钥） 和 id\_rsa.pub（公钥），我们需要用到公钥。

ssh-keygen -t rsa -C ruesin@163.com

登录github — setting — SSH Key — Add ，将公钥添加上，保证只有自己可以提交。

然后创建远程一个仓库 testgit 。

在创建版本库时有说到两种创建方式，第一种形式是现在本地创建了版本库，写了很多东西，关联并推送到远程仓库。

git push -u origin master ## 将 master 关联并推送到远程

推送之前是要先把本地库（分支）和远程库关联的，由于远程库是空的，第一次推送master分支时，加上-u参数，Git不但会把本地的master分支内容推送的远程新的master分支，还会把本地的master分支和远程的master分支关联起来。

git push origin master ## 将 master 推送到远程

git remote add origin git@server-name:path/repo-name.git ## 关联远程库

前面说到是先有本地库，后有远程库的时候，另外一种形式是先创建远程库，然后，从远程库克隆。

git clone https://github.com/Ruesin/testgit.git

Git支持多种协议，默认的git://使用ssh，但也可以使用https等其他协议。使用https除了速度慢以外，还有个最大的麻烦是每次推送都必须输入口令，通过ssh支持的原生git协议速度最快。

git remote ## 查看远程库信息

git remote -v ## 查看远程库信息

git branch –set-upstream-to=origin/dev

从本地推送分支，使用git push origin branch-name，如果推送失败，先用git pull抓取远程的新提交

git pull ## 拉取远程数据 更新至本地  
git push origin master #推送本地master到远程origin

在本地创建和远程分支对应的分支，使用git checkout -b branch-name origin/branch-name，本地和远程分支的名称最好一致；

如果git pull提示“no tracking information”，则说明本地分支和远程分支的链接关系没有创建，用命令 git branch –set-upstream branch-name origin/branch-name。

有时候配置文件、缓存文件什么的我们是不需要推送拉取的，在Git工作区的根目录下创建一个特殊的.gitignore文件，然后把要忽略的文件名填进去，Git就会自动忽略这些文件。GitHub中各种忽略推送的配置文件：https://github.com/github/gitignore

**六、标签管理**

发布一个版本时，我们通常先在版本库中打一个标签，这样，就唯一确定了打标签时刻的版本。将来无论什么时候，取某个标签的版本，就是把那个打标签的时刻的历史版本取出来。所以，标签也是版本库的一个快照。

git checkout master ## 切换到 master 分支  
git tag v1.0 ## 打上 v1.0 标签

git tag ## 查看所有标签 标签不是按时间顺序列出，而是按字母排序的

git show v1.0 ## 查看标签信息

git log –pretty=oneline –abbrev-commit ## 查看历史版本  
git tag v0.9 6224937 ## 打标签到指定版本

git tag -a v0.1 -m “version 0.1 released” 3628164 ## 创建带有说明的标签，用-a指定标签名，-m指定说明文字

git tag -s v0.2 -m “signed version 0.2 released” fec145a ## 通过-s用私钥签名一个标签

签名采用PGP签名，因此，必须首先安装gpg（GnuPG），如果没有找到gpg，或者没有gpg密钥对，就会报错

参考：http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000

手册：http://pan.baidu.com/s/1bndfEDx
