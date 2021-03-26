---
title: xposed 使用记录
date: 2021-3-26 14:00:00
categories: 研究
tags: 
- 自动化
- 安卓逆向
---

## 介绍
Xposed 是 Android 平台上著名的 Java 层 Hook 框架，通过在安装 Xposed 框架、编写 Xposed 模块，可以对任意 Android 应用的 Java 方法进行 Hook。

Android运行的核心是zygote进程，zygote 进程是 Android 系统中第一个拥有 Java 运行环境的进程，它是由 init 进程通过解析 init.rc 文件创建出来的，从 init 进程 fork 而来。

zygote 进程的可执行文件是 /system/bin/app_process，通过替换 app_process 文件，在其中加载了 XposedBridge.jar 这个 Dex 代码包，它包含 Xposed 的 Java 层实现代码和提供给 Xposed 模块的 API 代码。

所有运行在 Java 虚拟机中的系统服务以及应用都是由 zygote 进程克隆出来的，被克隆出来的子进程将继承 zygote 进程的所有资源。

通过替换app_process文件，就可以将 Xposed 代码继承到 Android 应用进程中，从而实现将 Xposed 代码加载到每一个进程中的目的。

在 Hook 一个指定方法时，提供要 Hook 方法的名字、参数列表类型和方法所在类型，和一个用于处理 Hook 的回调方法（XC_MethodHook），这个回调用于修改原始方法的逻辑。

Xposed 取得这个方法的反射对象，然后将反射对象和回调方法一起传递给 Xposed 的 Native 层代码，注册为Native层函数，当执行到该方法时，虚拟机会先执行Native层函数，转发给回调方法，然后执行Java层函数。

Xposed 模块是一个普通的 Android 应用，通过 Xposed 框架提供的 Hook API 对任意应用的 Java 方法进行 Hook。

在设备上安装 Xposed 框架和模块，然后在 Xposed 框架应用中启用这个模块，重新启动设备后，Xposed 模块将被激活，当任意的应用运行起来后，模块的 Hook 代码将会在这个应用进程中被加载，然后执行，从而对这个应用的 Java 方法进行指定 Hook 操作。

## 安装
- Xposed：https://github.com/rovo89/Xposed
- XposedInstaller：https://github.com/rovo89/XposedInstaller
- XposedInstaller：https://repo.xposed.info/module/de.robv.android.xposed.installer

### Xposed

1. 从 https://repo.xposed.info/module/de.robv.android.xposed.installer 下载管理器`XposedInstaller_3.1.5.apk`
2. 安装管理器到设备`adb install XposedInstaller_3.1.5.apk`
3. 打开`xposedInstaller`，首页点击框架右侧的“云”，选择“install”。

也可以选择离线安装：
```
$ wget http://dl-xda.xposed.info/framework/sdk24/arm64/xposed-v89-sdk24-arm64.zip
$ adb push xposed-v89-sdk24-arm64.zip /data/local/tmp/
$ adb shell

$ su
# cd /data/local/tmp
# find / -name 'de.robv.android.xposed.installer'
/config/sdcardfs/de.robv.android.xposed.installer
/data/media/0/Android/data/de.robv.android.xposed.installer
/data/misc/profiles/cur/0/de.robv.android.xposed.installer
/data/misc/profiles/ref/de.robv.android.xposed.installer
/data/data/de.robv.android.xposed.installer
/data/user_de/0/de.robv.android.xposed.installer
/mnt/runtime/write/emulated/0/Android/data/de.robv.android.xposed.installer
/mnt/runtime/read/emulated/0/Android/data/de.robv.android.xposed.installer
/mnt/runtime/default/emulated/0/Android/data/de.robv.android.xposed.installer
/storage/emulated/0/Android/data/de.robv.android.xposed.installer

# cp xposed-v89-sdk24-arm64.zip /data/media/0/Android/data/de.robv.android.xposed.installer/cache/downloads/framework/
```

### EdXposed
Xposed对8.0及之后版本支持不好，选择使用Edxposed。

- 下载Magisk：https://github.com/topjohnwu/Magisk/releases
- 下载Riru：https://github.com/RikkaApps/Riru/releases
- 下载EdXposed：https://github.com/ElderDrivers/EdXposed/releases
- 下载EdXposedManager：https://github.com/ElderDrivers/EdXposedManager/releases

1. 安装Magisk：`adb install Magisk-v22.0.apk`
2. 推送riru、EdXposed到手机，在 Magisk 底部第四个菜单中，本地导入安装 riru、EdXposed。（也可以选择在线安装）
3. 安装EdXposedManager：`adb install EdXposedManager-4.6.2-46200-org.meowcat.edxposed.manager-release.apk`
4. 重启手机

Xposed 或 EdXposed 安装成功后，安装Xposed模块，在Xposed Installer 或 EdXposedManager 中启用模块，重启手机即可。

## 模块
Xposed 模块是一个普通的 Android 应用，通过 Xposed 框架提供的 Hook API 对任意应用的 Java 方法进行 Hook。

APP开发前，需要配置对API的依赖。

### 添加 XposedBridge API依赖
#### 方法一：jcenter
在build.gradle中配置：
```
repositories {
    jcenter();
}

dependencies {
    ...
    compileOnly 'de.robv.android.xposed:api:82'
    ...
}
```

#### 方法二：离线安装
下载`api-82.jar`：https://bintray.com/rovo89/de.robv.android.xposed/api 到`/app/libs`中，右键"Add As Library"添加这个jar包。

修改app下的build.gradle：
```
compileOnly files('libs/api-82.jar')
```

### 修改 AndroidManifest.xml 文件
在Application标签里面加三个meta-data：
```
<!-- 是否是xposed模块，xposed根据这个来判断是否是模块 -->
<meta-data android:name="xposedmodule" android:value="true" />

<!-- 模块描述，显示在xposed模块列表那里第二行 -->
<meta-data android:name="xposeddescription" android:value="Xposed模块示例" />

<!-- 最低xposed版本号(lib文件名可知) -->
<meta-data android:name="xposedminversion" android:value="30" />
```

### 编写hook类

创建`com.metmit.xp.HookMain`类，实现IXposedHookLoadPackage接口，重写handleLoadPackage方法。

### xposed_init文件
在`main`目录下创建`assets`目录，在`assets`目录下创建`xposed_init`文件。这个就是模块的入口，将相关`hook`类的全限定名称写入此文件中，如有多个类，则每行写一个：
```
com.metmit.xp.HookMain
```

快速上手使用Xposed：https://github.com/metmit/easyXposed