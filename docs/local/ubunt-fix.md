---
title: Ubuntu删除文件过度，导致依赖丢失，系统崩溃
date: 2015-12-31 23:39:14
categories: 本地
---

用久了Ubuntu，老毛病又犯了，看着dash中一大堆用不到的东西，就犯膈应，想清理清理系统。

结果，各种删东西，导致依赖被删错了，直接导致的结果是，无法联网，没有系统设置，没有软件中心，编译软件时各种报错，总之，就是废废了。如果只是某些东西坏了，还能联网还好说，怎么都能给修复了。

不能联网是个大事，尝试了很多办法，都没办法修复。

最终，只能livecd引导修复了。

由于电脑是双系统的，系统是通过windows硬盘安装的，所以修复也是走老路。

打开easyBCD，添加条目→NeoGrub→安装→配置，配置文件添加，注意root索引要写对应的镜像放的磁盘位置，我的电脑只有一块硬盘，镜像放在了C盘中，所以写了(hd0,0)，第一块硬盘的第一个分区。

将ISO镜像中casper下的vmlinuz.efi和initrd.lz也提取到C盘。

title Install Ubuntu  
root (hd0,0)  
kernel (hd0,0)/vmlinuz.efi boot=casper iso-scan/filename=/ubuntu-15.10-desktop-amd64.iso ro quiet splash locale=zh\_CN.UTF-8  
initrd (hd0,0)/initrd.lz

保存重启。

选择 Install Ubuntu ，进入Ubuntu试用安装界面。

注意，选择Install Ubuntu 报错，有可能就是配置文件没写好，可以根据报错，按‘e’编辑配置启动。

配置联网，选择安装，弹窗是否卸载分区时，选择否，然后选择第一项，尽最大可能的保留用户数据安装。

然后就稍等安装就好了。

系统装好就能看到用户主目录文档啦、配置啦都还有保留的，先依次执行下更新、清理。

sudo apt-get update  
suso apt-get upgrade  
sudo apt-get -f install  
sudo apt-get autoclean  
sudo apt-get autoremove

之前编译的东西以及配置都还在，但是通过apt-get安装的组件需要重新安装一下。
