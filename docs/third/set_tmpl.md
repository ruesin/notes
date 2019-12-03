---
title: Ecstore后台管理新加一种页面模版类型供前台渲染使用
date: 2014-09-15 14:53:42
categories: 三方产品
---

本文写的是在后台模版管理→页面管理→新增页面 时，左侧多加一种页面类型，前台渲染时可以使用相应模版。

在二次开发的时候可能极少用到此处，因为官方提供的页面模版类型已经基本够用了。但是在新增APP时有可能会用到。

首先翻看官方自带的这些，可以发现这些是在site APP下控制的，根据Ecstore的惯常手段，肯定不可能这么笨的写死，每次都改这里，肯定是写在扩展中了。

是有个扩展是网站主题模版的。我们就以抽奖APP做为例子吧。首先在扩展文件中写下埋点。

```
<service id="site.site_theme_tmpl">
    <class>draw_theme_tmpl</class>
</service>
```

然后在对应埋点文件里添加方法

```
public function __get_tmpl_list(){
    $ctl = array(
        'draw' => '抽奖活动详细页'
    );
        return $ctl;
}
```

这时我们去看后台→站点→模版列表→页面管理→添加新页面，就可以看到新增的页面类型了。然后我们添加一个页面，随便修改下保存。

[![set_tmpl1](/images/2014/09/set_tmpl1.jpg)](/images/2014/09/set_tmpl1.jpg)

在前台渲染方法中加入 $this->set\_tmpl(‘draw’); 即可。

[![set_tmpl2](/images/2014/09/set_tmpl2.jpg)](/images/2014/09/set_tmpl2.jpg)

注意，可能有朋友会把这个方法和下面两个方法弄混。

$this->page();  
$this->set\_tmpl\_file();

1.$this->set\_tmpl(‘draw’); //是指定要用哪个类型的模版，如果指定模版文件就用指定的，没有指定就用当前类型下的默认文件；  
2.$this->set\_tmpl\_file(); //是指具体用哪个模版文件  
3.$this->page(‘site/index.html’); //是指渲染到哪个页面，用来替换模版中的<{main}>。
