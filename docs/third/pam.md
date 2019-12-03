---
title: ecstore 授权以及后台跳过激活验证 
date: 2014-06-14 10:38:55
categories: 三方产品
---

shopexID  
商派的id，用来生成证书.  
注册: http://my.shopex.cn/index.php?ctl=ent&act=register

授权文件.在配置文件下，config这个文件必须有可写权限，在激活的时候会生成授权文件.里面的证书id.  
config/certi.php

证书:通常是利用shopexID 生成的.

节点：  
app/base/cmd inactive\_node\_id 取消节点  
app/base/cmd active\_node\_id 激活节点

kvstore/setting/base/035172bd070e9c3469d50ea80b020fee.php

注意:证书、节点直接影响与ocs绑定.  
排查方法：http://open.shopex.cn/journal/rpc 查看ocs信息日志 输入msg\_id

删除授权文件，直接，退出直接 就会需要激活码 激活….

矩阵记录绑定产品的请求url的，这个是更新不了，只能重新生成证书 节点…  
1.取消节点.  
2.删除kv文件.  
3.删除授权证书

待激活…

激活后 授权证书、节点、证书 都会新生成

跳过激活码：(修改文件)  
desktop/lib/cert/certcheck.php 32/130 直接return(else的地方也直接返回)  
desktop/controller/passport.php 注释代码.登录之前的预先验证
