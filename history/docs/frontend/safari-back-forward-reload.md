---
title: safari浏览器下前进后退重载页面
date: 2015-10-26 15:09:45
categories: 前端
---

程序中有太多的地方需要处理完事件后，返回到上一页，并且要重载页面，显示最新内容。因为之前一直是做PC端的，这次做的是嵌入到APP中的wap，也习惯性的使用了 history.go(-1);，起先并没有注意到这个细节，后来被他人提醒才发现，在safari下保存成功后退上一步后，页面还是老页面，并没有重新加载。

经过各种调试、查询，发现是safari的缓存机制的问题，说是为客户体验着想，而在网上查，也大部分都是说怎么设置的，并没有涉及到代码层。由于当时时间紧张，又有其他事情做，便搁置未解决，暂时使用了location.href，但是这样又有了问题，跳转是没事儿了，可是APP上加的后退history.go(-1)，即：使用正常后退时，又出问题了，会返回到实际上是往前的一步。

想了各种套层，替换历史记录的方法，最终都觉得不是可行的办法，今日又静心搜索了下，找到一种可行的办法，在页面头部加上：

<script>window.onunload=function(){};</script>

注意：是加在要后退重载的也页面头部，至少目前是好使了。

下面是网搜的其他办法，有的试了（不好使），有的嫌太繁琐没有试验，仅作留存。

在页面中加隐藏框架  
<iframe style=”height:0px;width:0px;visibility:hidden” src=”about:blank”></iframe>

头部加meta标签  
<meta http-equiv=”pragma” content=”no-cache”>  
<meta http-equiv=”Cache-Control” CONTENT=”no-store”>  
<META HTTP-EQUIV=”Expires” CONTENT=”0″>

其他杂七杂八的各种方法，就不一一罗列了，有兴趣的朋友可以谷歌、百度。
