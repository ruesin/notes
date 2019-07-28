---
title: ruesin 不在 sudoers 文件中。此事将被报告。
date: 2014-12-27 17:02:15
categories: 本地
---

要用普通用户执行sudo，可是提示 “ruesin 不在 sudoers 文件中。此事将被报告。”

```
[sudo] password for ruesin:
ruesin 不在 sudoers 文件中。此事将被报告。
```

网上有人说切换到root，把sudoers文件改为读写，然后修改sudoers文件，把ruesin用户添加上。

```
$ su root
密码：
#chmod 740 /etc/sudoers
#vi /etc/sudoers
```

但是一般情况下，是不建议直接修改/etc/sudoers这个文件的，Linux提供有专用的命令：visudo

```
$ su root
密码：
# visudo
```

在 root ALL=(ALL) ALL 后面加上 ruesin ALL=(ALL) ALL

```
root    ALL=(ALL)       ALL
ruesin ALL=(ALL) ALL
```

说明：格式为（用户名 网络中的主机=（执行命令的目标用户） 执行的命令范围）  
保存后切换会普通用户测试权限提升成功。

`# su ruesin`
