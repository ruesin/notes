---
title: Mac下编译 rdm
date: 2018-12-14 20:31:19
categories: 本地
---

RedisDesktop 从 0.9.3 开始，不再支持 Windows 和 Mac的免费下载，但仍提供源码，可自行编译。官方给出了使用QT工具编译的文档，本文使用了比较小的QT命令行进行编译安装的。

依赖Xcode，提前从 App Store 安装。

```
$ git clone --recursive https://github.com/uglide/RedisDesktopManager.git -b 0.9.8 rdm && cd ./rdm

## 因为 0.9.9 不支持SSH隧道，所以切回0.9.8
$ git checkout 0.9.8
$ git submodule update --init --recursive

## 安装必要依赖
$ brew install openssl cmake

## 安装QT
$ brew install  qt

$ cd ./src 
$ cp resources/Info.plist.sample resources/Info.plist

```

```
$ ./configure
```

报错1：  
`xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance`  
如果没有安装Xcode，需先安装。  
如果安装多版本Xcode，目录不对，可指定目录：`xcode-select --switch /Applications/Xcode.app/Contents/Developer/`。  

报错2：  
`/Users/sin/tmp/rdm/3rdparty/gbreakpad/src/client/mac/sender/Breakpad.xib:global: error: Compiling for earlier than macOS 10.6 is no longer supported.`  
使用 Xcode 打开 Breakpad.xib，在右侧选择Mac OS版本。  
![rdm.png](/images/20181214/2d0ad0e8675fa1c6bf63eedf4f891d4b.png)

``` 
$ /usr/local/Cellar/qt/5.12.0/bin/qmake CONFIG-=debug
$ make
``` 
报错1：  
make: *** No rule to make target `../bin/osx/release/crashreporter', needed by `../bin/osx/release/rdm.app/Contents/MacOS/crashreporter'.  Stop.  
方案1：  
建议下载 crashreporter 到 ../bin/osx/release 目录，链接: https://pan.baidu.com/s/1qtkunjollYW6I0XefUIGhQ 提取码: dp5h。
方案2：  
编辑 rdm.pro 文件 `vim rdm.pro`，注释如下代码块。
```
#release {
#    CRASHREPORTER_APP.files = $$DESTDIR/crashreporter
#    CRASHREPORTER_APP.path = Contents/MacOS
#    QMAKE_BUNDLE_DATA += CRASHREPORTER_APP
#}
```

*rdm.app* 生成在`../bin/osx/release/`目录下，此时可以本地运行，如果要发送给其他人，还需要将QT依赖打包进去。

```
$ cd ../bin/osx/release/
$ /usr/local/Cellar/qt/5.12.0/bin/macdeployqt rdm.app -qmldir=../../../src/qml
```

附上QT工具下载地址  
http://download.qt.io/archive/qt/5.10/

http://download.qt.io/official_releases/qt/

官方编译文档  
http://docs.redisdesktop.com/en/latest/install/#build-from-source
