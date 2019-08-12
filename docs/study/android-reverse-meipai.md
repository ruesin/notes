---
title: 【安卓逆向】获取美拍APP签名算法
date: 2019-07-28 20:45:01
categories: 研究
---

美拍版本是`8.2.38`，通过本次逆向整理了下安卓APP的完整逆向过程。

## 准备
安卓逆向，需要反编译APK并获取源码，主要用到工具：
- [ApkTool](https://ibotpeaches.github.io/Apktool/install/)：
  有对APK的编译、反编译、签名等功能，可利用ApkTool查看apk的xml文件、AndroidManifest.xml和图片等
    1. 下载`apktool`及`apktool_2.4.0.jar`，将`apktool_2.4.0.jar`重命名为`apktool.jar`
    2. 将`apktool.jar`和`apktool`移动到`/usr/local/bin`目录下，并增加可执行权限
    3. 在终端输入apktool看是否可以运行，如果不可以需要在系统偏好设置中打开安全与隐私中点击仍要运行apktool.jar
- [dex2jar](https://sourceforge.net/projects/dex2jar/files/)：
  将dex文件转换成jar文件，转换成jar后我们才好借助JD-GUI来查看反编译dex后的代码
- [JD-GUI](http://jd.benow.ca/)：
  一款Java反编译器GUI，通过它查看反编译后的dex的代码，通常需要配合dex2jar使用

## 反编译apk

使用`ApkTool`反编译APK得到xml文件、AndroidManifest.xml和图片

```shell
$ cd /Users/sin/Desktop/mp
$ apktool d meipai.apk
```
如果在反编译时出现警告：
```
S: WARNING: Could not write to (/Users/sin/Library/apktool/framework), using /var/folders/x9/pbjwtndx1sl9cgy_qdmyb17r0000gn/T/ instead...
S: Please be aware this is a volatile directory and frameworks could go missing, please utilize --frame-path if the default storage directory is unavailable
I: Loading resource table from file: /var/folders/x9/pbjwtndx1sl9cgy_qdmyb17r0000gn/T/1.apk
```
创建对应目录即可：
```shell
mkdir -p /Users/sin/Library/apktool/framework
```

也可以将文件夹编译为apk`apktool b meipai -o new_meipai.apk`，在`meipai`文件夹中生成`build`、`dist`两个文件夹，这就是编译后生成的文件，`new_meipai.apk`在`dist`中。

如果重新打包时报错：`W: /Users/sin/Desktop/android/meipai/res/color/x.xml:6: error: No resource identifier found for attribute 'alpha' in package 'com.meitu.meipaimv'`。编译的时候找不到资源id，通过查apktool的命令帮助，可以通过-r参数来避免resc的反编译，在重新打包时就不会重新编译resc文件包括xml，`apktool -r d dou2.apk -o test`。

`APkTool`只是将资源文件提取处理，对于.dex类型的文件是无法查看的，需要用`dex2jar`转换代码。

## dex转jar

使用解压软件将`meipai.apk`进行解压，也可更改文件后缀为`meipai.zip`，然后解压。

解压后的classes.dex文件就是项目的源码，如果使用了`MultiDex`将会有多个dex文件，将dex文件拷贝到dex2jar目录下。

```shell
$ cd /Users/sin/Desktop/mp/dex2jar-2.0
$ chmod +x *.sh
$ ./d2j-dex2jar.sh classes.dex
$ ./d2j-dex2jar.sh classes2.dex
$ ./d2j-dex2jar.sh classes3.dex
$ ./d2j-dex2jar.sh classes4.dex
$ ./d2j-dex2jar.sh classes5.dex
```
也可以直接解APK文件：`./d2j-dex2jar.sh /Users/sin/Desktop/mp/meipai.apk`

使用解压软件打开apk 和使用apktool反编译出的apk不同：
- 直接解压apk和使用apktool反编译apk都能获得AndroidManifest.xml，但直接解压获得的AndroidManifest.xml是乱码的，无法直接查看
- 直接解压apk获得res资源文件是不包含resources.arsc部分的，而使用apktool反编译出来的res是包含的

## JD-GUI查看Jar代码
直接运行`JD-GUI.app`，将`classes-dex2jar.jar`拖拽到JD-GUI界面上即可。

## 查找签名
在`JD-GUI`中可搜索关键词，比如抓包的feed流地址：`https://api.meipai.com/hot/feed_timeline.json?is_from_scroll=0&page=5&memory=2&guid=a6aa36a625129418e5da01bc2a8d6a8c&sdk_version=4.6.1-201905071358%40aar&timestamp=1565584900671&timezone=GMT%2B8&is_root=2&carrier=&device_brand=HUAWEI&user_agent=Mozilla%252F5.0%2B%2528Linux%253B%2BAndroid%2B6.0.1%253B%2BMate%2B10%2BPro%2BBuild%252FV417IR%253B%2Bwv%2529%2BAppleWebKit%252F537.36%2B%2528KHTML%252C%2Blike%2BGecko%2529%2BVersion%252F4.0%2BChrome%252F52.0.2743.100%2BMobile%2BSafari%252F537.36&language=zh-Hans&client_id=1089857302&device_id=008796751994005&version=8238&channel=meipai_setupbutton&model=Mate+10+Pro&os=6.0.1&origin_channel=meipai_setupbutton&imei=008796751994005&mac=02%3A00%3A00%3A00%3A00%3A00&stat_gid=1898125227&android_id=e37be4c3555be003&local_time=1565584901542&lat=39.912591&lon=116.539574&network=wifi&resolution=800*1280&teenager_status=0&sig=49b8427a8ccef6f6901db24128fa382d&sigVersion=1.3&sigTime=1565584901566`

通过搜索`sigTime`，很快定位到签名类位于`com.meitu.secret.SigEntity`类中，此类中提供了几个签名方法，如果不知道是哪个，可以继续翻代码或者hook。

这里我们已经知道外部调用的是`generatorSigWithFinal`方法，而此方法中最终调用的是一个`native`方法`nativeGeneratorSigFinal`，此方法定义在`.so`文件中。

通过阅读此类，`System.loadLibrary("release_sig");`，发现调用的是`librelease_sig.so`文件，此文件在`./lib/armeabi-v7a/librelease_sig.so`

## 使用Xposed HOOK
通过阅读jar代码，一般情况下可以拼接出参数，但是比较复杂的时候，最好的办法还是hook，具体的hook代码可参考 https://github.com/ruesin/sinXposed

通过hook，可以拿到`native`方法`nativeGeneratorSigFinal`的参数：
```
07-29 14:58:37.166  5960  6579 I test: test paramString0: friendships/followers.json
07-29 14:58:37.166  5960  6579 I test: test paramString1-1: [1644140716, 3, zh-Hans, 1089857302, 008796751994005, 8238, meipai_setupbutton, Mate 10 Pro, 6.0.1, meipai_setupbutton, 008796751994005, 02:00:00:00:00:00, 1898125227, e37be4c3555be003, 1564383517163, 39.912602, 116.539565, wifi, 800*1280, 0]
07-29 14:58:37.166  5960  6579 I test: test paramString2: 10001
07-29 14:58:37.166  5960  6579 I test: test paramString3: com.meitu.meipaimv.MeiPaiApplication@5f73d9e
07-29 14:58:37.166  5960  6579 I test: test result: com.meitu.secret.SigEntity@d4eb541
```

## 解析 so 文件
解析so文件可以使用`IDA`或`Hopper`，这里使用的是[IDA](https://www.hex-rays.com/products/ida/)。

通过`IDA`打开`librelease_sig.so`文件后，可在左侧边栏快速定位方法`Java_com_meitu_secret_SigEntity_nativeGeneratorSigFinal`。

双击打开方法后，按`F5`转成`C`代码，大概能够看出这个方法是对字符串做了系列处理，然后md5的，另外还做了加盐处理，具体加盐可以搜索字符串：`⇧+F12`打开字符串列表窗口，在窗口内搜索。

## 签名
将解析的签名代码翻译成伪代码，并使用同样的参数进行签名，对比是否一致。

## 其他
美拍签名是比较简单的，在JAVA中加载so，然后调用so中的方法。so中的方法也比较简单，通过分析即可写出伪代码。

在其他很多时候，我们在hook到代码后，可能无法直接分析so文件，或者分析so很困难。这时可以自建空白安卓项目，引入so文件，模拟调用so方法，然后在IDA中断点调试。