---
title: PHP获取客户端的网卡mac物理地址
date: 2014-09-29 17:47:10
categories: PHP
---

获取客户端的mac地址是非常有用的一个功能，因为它是客户端的不可变的唯一标识，更换IP或者清除本地记录都是没用的。

所以获取mac地址经常会用到购买软件时的一机一激活码，网站注册每台机器只能注册一次等等。

在电商系统开发中，常见的一个功能就是：用户在没有登录的状态下将商品加入购物车，登录后自动将购物车数据同步上来。对此的解决办法我们一般都是使用COOKIE或者SESSION解决即可。其实也可以用获取客户端的mac地址作为唯一标识存入到数据库中，登录成功后再进行匹配。

大数据时代的云很多时候都有用到此类方法。

网上查询整理的代码如下：

```
class GetMac{
    var $result   = array(); 
    var $macAddrs = array(); //所有mac地址
    var $macAddr;            //第一个mac地址

    function __construct($OS){
        $this->GetMac($OS);
    }

    function GetMac($OS){
        switch ( strtolower($OS) ){
        	case "unix": break;
        	case "solaris": break;
        	case "aix": break;
        	case "linux":
        	    $this->getLinux();
        	    break;
        	default: 
        	    $this->getWindows();
        	    break;
        }
        $tem = array();
        foreach($this->result as $val){
            if(preg_match("/[0-9a-f][0-9a-f][:-]"."[0-9a-f][0-9a-f][:-]"."[0-9a-f][0-9a-f][:-]"."[0-9a-f][0-9a-f][:-]"."[0-9a-f][0-9a-f][:-]"."[0-9a-f][0-9a-f]/i",$val,$tem) ){
                $this->macAddr = $tem[0];//多个网卡时，会返回第一个网卡的mac地址，一般够用。
                break;
                //$this->macAddrs[] = $temp_array[0];//返回所有的mac地址
            }
        }
        unset($temp_array);
        return $this->macAddr;
    }
    //Linux系统
    function getLinux(){
        @exec("ifconfig -a", $this->result);
        return $this->result;
    }
    //Windows系统
    function getWindows(){
        @exec("ipconfig /all", $this->result);
        if ( $this->result ) {
            return $this->result;
        } else {
            $ipconfig = $_SERVER["WINDIR"]."\system32\ipconfig.exe";
            if(is_file($ipconfig)) {
                @exec($ipconfig." /all", $this->result);
            } else {
                @exec($_SERVER["WINDIR"]."\system\ipconfig.exe /all", $this->result);
                return $this->result;
            }
        }
    }
}

$obj = new GetMac(PHP_OS);
print_r($obj->result);
echo $obj->macAddr;
//获取客户端
//$result=`arp -a $REMOTE_ADDR`;
//$result=`nbtstat -a $REMOTE_ADDR`;
//print_r($result);
exit;
```
