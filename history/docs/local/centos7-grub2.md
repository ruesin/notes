---
title: Centos7 + Windows7 双系统，通过修改grub2，重新添加 Win7 启动引导项
date: 2014-12-23 16:15:55
categories: 本地
---

家里几个老电脑闲着实在是浪费，于是决定折腾centos玩，玩坏了也不心疼。  
当然，为了考虑家里其他人的偶尔使用，肯定是得装双系统了。  
废话不多说，按照以往的经验，Windows 7 装起，然后装 CentOs 7，CentOS 7 的改变还真的不少，至少安装时就感觉跟以前版本有很大不同。  
装好后重启，发现启动项里没有 Windows？！第一反应就是磁盘分区的时候，我引导盘那么弄好，赶紧近PE，一看Win的系统还在，修复下引导项，重启，可以正常启动Windows7了，可是这样一来Centos又没了。  
重装下Centos吧，到分区那里特别留心了下，没什么问题，安装完成，重启，又没 Win 了！难道这个版本的centos是直接冲掉grub而不是添加？  
好吧，我去手动添加上win的启动。。。

当然，我们可以直接修改grub的配置文件 /boot/grub2/grub.cfg 。但是看到里面有警告：不要编辑这个文件，他是通过grub2-mkconfig 使用配置文件模版和设置自动生成的。

[![grub2](/images/2014/12/grub2.jpg)](/images/2014/12/grub2.jpg)  
so、修改这个文件虽然可以达到效果，但是在系统执行grub2-mkconfig之后你修改的配置就会失效。  
所以，我们要去修改模版文件，然后执行 grub2-mkconfig 自动重建grub2引导。

```
$ sudo vi /etc/grub.d/40_custom

#!/bin/sh
exec tail -n +3 $0
# This file provides an easy way to add custom menu entries.  Simply type the
# menu entries you want to add after this comment.  Be careful not to change
# the 'exec tail' line above.
menuentry 'Windows7'{
set root=(hd0,1)
chainloader +1
}

$ grub2-mkconfig -o /boot/grub2/grub.cfg
$ reboot
```

注意，grub2中第一块磁盘的第一个分区是(hd0,1)，而不是(hd0,0)，这一点跟grub有稍许不同，还有不要自作聪明的改sda什么的。。。
