---
title: Ionic + cordova 构建 webapp 项目
date: 2016-07-07 14:17:56
categories: 前端
---

本文只是非常简单的记录了，ionic从新项目到打包的过程，并没有做任何的其他开发配置。具体内部的开发，请查阅ionic、angularjs文档等，打包配置等请查阅相关文档。

开发环境是Windows，ubuntu + mac同理，测试平台为android，ios同理。

1.安装node.js  
https://nodejs.org/dist/v4.4.5/  
http://nodejs.org/download/

2.设置npm镜像  
`npm config set registry  https://registry.npm.taobao.org`

3.安装 cordova+ionic
```
npm install -g cordova ionic
npm update -g cordova ionic
```

4.创建APP项目
```
ionic start myapp [template] //template：blank（空项目）、tabs（带导航条）、sidemenu（带侧滑菜单）
ionic platform add android
ionic build android
ionic platform add ios
ionic build ios
ionic run android //连接数据线直接测试
```

安卓打包环境配置：  
1.JDK安装配置 下载地址：http://www.oracle.com/technetwork/java/javase/downloads/index.html  
安装的时候，jdk、jre装在同级目录下。  
配置环境变量，在系统变量中新建 JAVA_HOME，值为jdk的安装目录 D:\Program Files\Java\jdk1.8.0_91。  
在PATH中添加 `%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin` 。  
系统变量中新建 CLASSPATH，值为 `.;%JAVA_HOME%\lib;%JAVA_HOME%\lib\tools.jar`。  
`java -version`

2.Android SDK 下载地址：http://developer.android.com/sdk/index.html 或 http://www.android-studio.org/  
安装完成后配置环境变量，在系统变量中新建 ANDROID_HOME，值为安装目录 `D:\Program Files\Android\android-sdk` 。在PATH中添加 `D:\Program Files\Android\android-sdk**;**%ANDROID_HOME%\tools;` 。  
`android -h`  

这时候SDK安装工具算是好了，然后就可以从SDK Manager中管理安装需要的SDK版本和GOOGLE API版本和文档了。这里主要看你安装的ionic对应的android版本，在你的ionic项目目录的platforms\android\project.properties文件中可以找到target=android-23。这里标识了项目所用的API版本，后面的数字刚好对应你在SDK Manager中看到的那些API后面的数字。

问题：
1.安装完SDK后，配置环境变量。
[![ionic_1](/images/2016/07/ionic_1.png)](/images/2016/07/ionic_1.png)

2.SDK Manager中安装响应的API。
[![ionic_2](/images/2016/07/ionic_2.png)](/images/2016/07/ionic_2.png)
