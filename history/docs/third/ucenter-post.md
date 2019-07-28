---
title: Ucenter接口请求数据流程剖析
date: 2014-12-05 10:21:33
categories: 三方产品
---

有用到Ucenter的朋友想来大部分都会搭建环境、配置应用，而一般也仅仅是停留在使用Ucenter，不涉及到接口的开发，所以除了需要开发时程序员会追程序的流程，应该很少有人会在意这些吧？

所谓Ucenter，就是指用户中心的意思，也就是多个应用用户打通，实现单点登录。原理也很简单，Ucenter提供各种操作的接口，供多个应用请求，各站点共用一个用户中心，各站点数据共用统一，方便用户管理和使用。

本文就以新建一个订单接口为例，和大家一起剖析下Ucenter的整个请求的流程，注意前提是已经将应用连通了哦，不太会的朋友可以去用Ucenter指定支持的项目做实验，比如Ecmall、ecshop、discuz等，博主这篇文章就是在Ecmall下完成的。

1.引用ucenter客户端文件

`include (ROOT_PATH . '/uc_client/client.php');`2.创建订单操作类

```
class UcPassportOrder
{
    function create_order($data){
        return outer_call('uc_create_order', array($data));
    }
}
```

3.实例化订单操作类并调用创建订单方法

```
$Uc = new UcPassportOrder();
$Uc->create_order($data);
```

4.自动调用client文件里的uc\_create\_order()方法

```
function uc_create_order ($data)
{
    $return = call_user_func(UC_API_FUNC, 'order', 'create_order', array('data'=>$data));
    return $return;
}
```

5.请求ucenter接口控制器方法。

根据请求api的方法确定请求的类型是mysql还是post

`define('UC_API_FUNC', UC_CONNECT == 'mysql' ? 'uc_api_mysql' : 'uc_api_post');`我们这里就已post为例，其实mysql是一样的，只不过post的是远程的，mysql请求的是本地的，其他的方法啦，数据啦完全都是一样的。

所以我们要请求的是服务端 order控制器下的create\_order方法。control/order.php

```
class ordercontrol extends base {

    function __construct() {
        $this->orderscontrol();
    }

    function orderscontrol() {
        parent::__construct();
        $this->load('order'); //加载订单模型
    }

    function oncreate_order(){
        $this->init_input();
        $data = $this->input('data');
        $status = $_ENV['order']->create($data);//请求订单模型里的create方法
        if($status){
            return $status;
        } else {
            return 0;
        }
    }
}
```

6.请求order订单模型下的方法，实现数据操作  
/model/order.php

```
class ordermodel {

    var $db;
    var $base;

    function __construct(&$base) {
        $this->ordermodel($base);
    }

    function ordermodel(&$base) {
        $this->base = $base;
        $this->db = $base->db;
    }

    function create($data){
        $return = $this->db->insert("order",$data);
        return $return;
    }
}
```

到此为止，客户端对服务端的请求已经完成，剩下的就是服务端一步步将结果返回给客户端。
