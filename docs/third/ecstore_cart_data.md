---
title: Ecstore读取普通商品购物车数据流程
date: 2014-08-27 17:50:58
categories: 三方产品
---

电商项目，主要就是围绕这个购物车、订单这个流程来的，之前我们讨论了Ecstore的加入购物车流程，既然商品加入购物车了，肯定是要读取出来以用来在页面中展示，写入订单信息等。

其实在《[Ecstore普通商品加入购物车流程](http://old.ruesin.com/open/ecstore/ecstore_cart_add-125.html "Ecstore普通商品加入购物车流程")》中我们就已经涉及到了读取购物车数据，只是没有细讲而已。

从加入购物车到提交订单，为了校验数据完整性、合法性，几乎每步都会有取出购物车数据的操作。

Ecstore读取购物车数据的地方主要有：1.商品加入购物车成功时的弹窗提示；2.购物车页面；3.订单确认页；4.mini购物车等。

虽然每个地方的入口不尽一样，但最后还都是从b2c\_mdl\_cart->get\_objects()获取数据的。所以我们的流程图也是从get\_objects()开始的。

流程图：

[![cart_data](/images/2014/08/cart_data.jpg)](/images/2014/08/cart_data.jpg)

1.b2c\_mdl\_cart->get\_objects()  
获取购物车数据的总的接口，会循环调取埋点S(b2c\_cart\_process\_apps)的process()方法获取数据；然后会设置购物车商品数；抛出购物车项。。

2.b2c\_cart\_process\_get->process()  
会有判断是购物车还是订单操作以调取不同的方法，我们暂时只考虑购物车的数据获取；$this->\_cart\_process()。  
然后是对获取数据的信息统计操作。b2c\_mdl\_cart->count\_objects()。

3.b2c\_cart\_process\_get->\_cart\_process()  
获取埋点，按照购物车类型不同，循环调取数据。S(b2c\_cart\_object\_apps)->getAll()。

4.b2c\_cart\_object\_goods->getAll()  
会有几个数据校验什么的，最后是走$this->\_get()。

5.b2c\_cart\_object\_goods->\_get()  
到了这里，基本上到了获取数据信息的底层。在此方法中会先调取$this->\_get\_basic()，获取购物车的基本信息；然后是$this->\_get\_products()，获取货品的详细信息。获取库存信息，商品数量信息等。  
至于\_get\_basic、\_get\_products的内部操作就不做赘述了。

6.b2c\_mdl\_cart->count\_objects()  
在第二步有说，获取信息之后，要对商品信息进行各种统计。通过此方法对购物车项的总数据进行统计。  
调取埋点S(b2c\_cart\_object\_apps)的count()方法。

7.b2c\_cart\_object\_goods->count()  
统计购物车中商品项数据。这里只是走了普通商品的流程。通过埋点还会走其他的类，用以统计其他类别的数据。

8.b2c\_cart\_object\_goods->\_count()  
统计单件的数据信息，统计每一个商品的数据信息。

9.b2c\_cart\_object\_goods->\_count\_product()  
统计货品的数据信息。

总体流程就是获取信息，统计格式化信息。统一使用。
