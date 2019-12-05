---
title: PHP 性能分析之 XHGui
date: 2016-02-15 10:48:20
categories: PHP
tags: 
- php
- xhgui
- xhprof
- php xhprof
---

<div>性能分析是衡量应用程序在代码级别的相对性能。性能分析将捕捉的事件包括：CPU的使用，内存的使用，函数的调用时长和次数，以及调用图。性能分析的行为也会影响应用性能。</div><div></div><div>影响整体应用性能的原因：数据存储、外部资源、糟糕的代码。烂代码其实算是很小的一部分，很少会有因为代码太糟糕而导致服务器崩溃的。</div><div></div><div>开发过程中经常会有人使用时间戳或者Xdebug来进行分析。前者只是很局部的一种分析，非常局限。而 Xdebug 会收集很多不必要的额外信息，这些信息对性能分析来说并不是特别必要，过多的收集信息本身就很吃性能，所以很少会应用在生产环境中。</div><div></div><div>Profiling是一项用来观察程序性能的技术，非常适用于发现程序的瓶颈或者紧张的资源。Profiling能够深入程序的内部，展现request处理过程中每一部分代码的性能；同时，也可以确定有问题的请求（request）；对于有问题的请求，我们还可以确定性能问题发生在请求内部的位置。</div><div></div><div>对于PHP，我们有多种Profiling工具，Xhprof 由 Facebook 发布的，包含一个基本的用户界面用于查看性能数据。XHprof 是为了在生产环境中使用而打造的。它对性能的影响很小，同时收集足够的信息用于诊断性能问题。XHprof 和 OneAPM 都是被动分析器。</div><div></div><div>XHGui 构建在XHProf之上，对分析结果做了更好的存储（MongoDB），增强了用户界面用于查看、比较和分析性能数据。</div><div></div><div>本文是记录基于 Mac Ox 的安装过程的，其他平台的可以灵活变换、触类旁通。</div><div></div><div>由于是基于xhprof的，所以要先安装php的xhprof扩展。</div><div></div><div>brew install php56-xhprof</div><div>￼</div><div>从git上克隆 XHGui 到本地，配置本地web服务到此目录，设置缓存目录的权限，可以直接为777，开启mongodb服务。</div><div></div><div>添加mongo索引，提高性能。</div><div></div><div>$ mongo</div><div>> use xhprof</div><div>> db.results.ensureIndex( { ‘meta.SERVER.REQUEST\_TIME’ : -1 } )</div><div>> db.results.ensureIndex( { ‘profile.main().wt’ : -1 } )</div><div>> db.results.ensureIndex( { ‘profile.main().mu’ : -1 } )</div><div>> db.results.ensureIndex( { ‘profile.main().cpu’ : -1 } )</div><div>> db.results.ensureIndex( { ‘meta.url’ : 1 } )</div><div></div><div>执行脚本，进行安装，会检测依赖以及缓存目录的权限。</div><div></div><div>[![xhgui-install](/images/2016/02/xhgui-install.jpg)](/images/2016/02/xhgui-install.jpg)</div><div></div><div>在要分析的项目入口文件中引用 XHGui/external/header.php 即可开始进行性能分析。</div><div></div><div>如果要修改对请求分析的命中率，可以修改配置文件 XHGui/config/config.default.php 中的 profiler.enable 键的值，当然如果想每次都记录，直接return true 就可以。</div><div></div><div>[![xhgui-profiler.enable](/images/2016/02/xhgui-profiler.enable.jpg)](/images/2016/02/xhgui-profiler.enable.jpg)</div><div></div><div>其他配置可参考git文档：https://github.com/perftools/xhgui。</div><div>￼￼</div>
