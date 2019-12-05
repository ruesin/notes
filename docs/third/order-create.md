---
title: Ecstore 订单生成流程
date: 2014-09-09 16:13:21
categories: 三方产品
tags: 
- ecstore
- ecstore购物车
- ecstore源码
- ecstore订单
---

前面几篇文章已经介绍了Ecstore从加入购物车到读取购物车的流程，也做了购物车的各种校验，那么下面要做的就是生成订单了。

生成订单流程总的为四步：获取购物车流程，格式化购物车数据，写入订单表，清除购物车数据。

生成订单的操作的入口是b2c\_ctl\_site\_order->create()。

[![order_create](/images/2014/09/order_create.jpg)](/images/2014/09/order_create.jpg)

1.b2c\_mdl\_cart->get\_objects()  
获取购物车的所有数据。

2.b2c\_order\_create->generate()  
订单标准数据生成。根据传过来的购物车数据、POST数据，生成订单所需要的标准数据。

会先后调用两个方法：1.\_chgdata 格式化订单数据，比如积分信息、各子订单数据、订单优惠信息等；2.S(b2c\_order.beforecreate)->generate() 调用订单生成前的操作埋点。

3.b2c\_order\_create->save()  
将订单的各项数据分别保存到响应的表里，没有过多的可以描述的地方。只需要注意是不止是往一个表中写数据！

4.b2c\_mdl\_cart\_bojects->remove\_object()  
订单生成成功后，清除购物车响应的数据。  
在这里会判断是否为快速购买，因为快速购买的数据是直接保存在session中的，如果是快速购买，直接清除对应的session就行了。如果不是快速购买，会根据是否为清空购物车做一步或两步操作。  
调用埋点S(b2c\_cart\_object\_apps) 的 delete()删除指定的购物车项。更新购物车cookie数据。

万年不变的原则，从购物车到订单，每一步都要做数据校验！
