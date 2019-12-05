---
title: Yii 2.0 的安装，遇到的问题及解决。
date: 2015-03-02 08:18:12
categories: 开源项目
tags: 
- Yii
- Yii2.0
- Yii2.0 安装
- php扩展
---

上一次接触Yii还是N久之前Yii 1.1 的时候，模糊记得结构跟TP很像，安装和新建都用脚手架。  
最近看了下Yii2的文档，发现与 1.1 相比，加入了许多新特性，几乎算是重构了，于是觉得再次学习一下。

安装 Yii 有两种方法：  
1、使用 Composer 命令安装。  
2、下载一个归档文件。  
官方推荐的是前者，这样只需执行一条简单的命令就可以安装新的扩展或更新 Yii 了。

**一、通过 Composer 安装**

Composer 是PHP中用来管理依赖（dependency）关系的工具。你可以在自己的项目中声明所依赖的外部工具库（libraries），Composer会帮你安装这些依赖的库文件。  
对于 Composer 在这里不做过多赘述，直接下载并运行 \[Composer-Setup.exe\](https://getcomposer.org/Composer-Setup.exe)。Composer 的安装要开启 PHP 的 openssl 支持。

Composer 安装后，切换到一个可通过 Web 访问的目录，执行如下命令即可安装 Yii ：

`composer create-project --prefer-dist yiisoft/yii2-app-basic basic`如上命令会将 Yii 安装在名为 `basic` 的目录中。

注意：这里我们安装的是基本模版，如果想安装高级模版，请执行下面的命令：

`composer create-project yiisoft/yii2-app-advanced advanced 2.0.3`**二、通过归档文件安装**

1\. 从 \[yiiframework.com\](http://www.yiiframework.com/download/yii2-basic) 下载归档文件。  
2\. 将下载的文件解压缩到 Web 目录中。  
3\. 修改 `config/web.php` 文件，给 `cookieValidationKey` 配置项添加一个密钥(若你通过 Composer 安装，则此步骤会自动完成)：

```
// !!! insert a secret key in the following (if it is empty) - this is required by cookie validation
'cookieValidationKey' => '在此处输入你的密钥',
```

**问题及解决**

在我通过 composer 安装的时候匆匆忙忙执行了安装命令，可是报错了，头大了半天，再去仔细看官方文档的时候发现自己疏忽大意了。

```
e:\host\www\yii20>composer create-project --prefer-dist yiisoft/yii2-app-basic basic
Installing yiisoft/yii2-app-basic (2.0.2)
- Installing yiisoft/yii2-app-basic (2.0.2)
Loading from cache

Created project in basic
Loading composer repositories with package information
Installing dependencies (including require-dev)
Your requirements could not be resolved to an installable set of packages.

Problem 1
- yiisoft/yii2 2.0.2 requires bower-asset/jquery 2.1.*@stable | 1.11.*@stable -> no matching package found.
- yiisoft/yii2 2.0.1 requires bower-asset/jquery 2.1.*@stable | 1.11.*@stable -> no matching package found.
- yiisoft/yii2 2.0.0 requires bower-asset/jquery 2.1.*@stable | 1.11.*@stable -> no matching package found.
- Installation request for yiisoft/yii2 * -> satisfiable by yiisoft/yii2[2.0.0, 2.0.1, 2.0.2].

Potential causes:
- A typo in the package name
- The package is not available in a stable-enough version according to your minimum-stability setting
see <https://groups.google.com/d/topic/composer-dev/_g3ASeIFlrc/discussion> for more details.

Read <http://getcomposer.org/doc/articles/troubleshooting.md> for further common problems.
```

后来查了下发现，原来是我漏装了fxp/composer-asset-plugin。如果有仔细看官方文档的话，会发现在执行安装命令之前有执行安装这个插件的命令。

`composer global require "fxp/composer-asset-plugin:1.0.0-beta4"`[![yii2.0-install](/images/2015/03/yii2.0-install.png)](/images/2015/03/yii2.0-install.png)安装上插件后再次执行安装命令即可，第一次安装的时候会下载并安装框架本身和一个应用程序的基本骨架，之后会缓存在composer中，再次安装的时候就会直接从缓存中读取了。

PS：如果不想一直等着下载，但又想使用composer安装，可以下载一个归档文件，然后在里面执行命令，就会copy本地的文件安装了。
