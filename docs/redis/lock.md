---
title: Redis 锁
date: 2019-07-26 10:21:32
categories: Redis
---

系统中经常需要有加锁的场景，单进程可以在各语言内加锁，单节点可以有文件锁等。业内有很多可以实现锁的方案，Redis也有很多实现。

### INCR
`Incr`命令将`key`中储存的数字值增一，返回执行 INCR 命令之后 key 的值。

如果`key`不存在，那么`key`的值会先被初始化为`0`，然后再执行`INCR`操作。

如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。

如果返回值等于1，表示抢锁成功；如果返回的数大于1，表示抢锁失败。

```
127.0.0.1:6379> INCR sin
(integer) 1
127.0.0.1:6379> INCR sin
(integer) 2
127.0.0.1:6379> get sin
"2"
127.0.0.1:6379> EXPIRE sin 1
(integer) 1
127.0.0.1:6379> get sin
(nil)
```

### SETNX
`Setnx`（SET if Not eXists）命令在指定的`key`不存在时，为`key`设置指定的值。

设置成功，返回`1`，表示抢锁成功。 设置失败，返回`0`，表示抢锁失败。

```
127.0.0.1:6379> SETNX sin 1
(integer) 1
127.0.0.1:6379> SETNX sin 1
(integer) 0
127.0.0.1:6379> GET sin
"1"
127.0.0.1:6379> EXPIRE sin 1
(integer) 1
127.0.0.1:6379> GET sin
(nil)
```

上面两种方法都需要设置`key`过期，以期望达到锁过期时自动释放，也可以在业务处理完成后主动`DEL`释放。但是如果业务逻辑意外退出了，导致创建了锁但没有删除，那么这个锁将一直存在，造成死锁。

但是借助`Expire`来设置就不是原子性操作了，也可以通过事务来确保原子性，但是还是有些问题，比如`Redis`事务中前一个命令执行失败了，并不会退出当前事务，而是继续执行。

### SET

`SET`命令用于设置给定`key`的值。如果`key`已经存储其他值，`SET`就覆写旧值，且无视类型。

从Redis 2.6.12开始`SET key value [EX seconds] [PX milliseconds] [NX|XX]`支持一组修改其行为的选项：
- EX：设置指定的过期时间，以秒为单位
- PX：设置指定的过期时间，以毫秒为单位
- NX：仅设置key（如果key尚不存在）
- XX：仅设置key（如果key已存在）

> 由于SET命令选项可以替换`SETNX`、`SETEX`、`PSETEX`，因此在将来的Redis版本中，这三个命令可能会被弃用并最终被删除。

在 Redis 2.6.12 以前版本，SET命令总是返回`OK`。

从 Redis 2.6.12 版本开始，SET在设置操作成功完成时，才返回`OK`。如果指定了`NX`或`XX`选项但未满足条件，则返回`Nil`。

注意：不鼓励使用以下模式来支持Redlock算法，该算法实现起来稍微复杂一些，但提供了更好的保证并且具有容错能力。

命令`SET resource-name anystring NX EX max-lock-time`是一种使用Redis实现锁的简单方法。

如果上面的命令返回OK，则客户端可以获取锁（如果命令返回Nil，则在一段时间后重试）。

可以使用`DEL`删除锁，或者等到过期时间后，自动释放锁。

但是假设我么设置的过期时间为10秒，而由于意外原因导致业务逻辑10秒内未处理完毕，这时锁已经自动释放了；如果此时其他进程又重新设置了此锁，此时调用了`DEL`命令删除锁；那么就可能会存在第三个进程又抢到锁，导致两个进程同时处理一个逻辑。

为了使系统更加健壮，可以修改解锁模式，`value`不要设置为固定字符串，而是设置一个不可猜测的大型随机字符串。

主动释放锁时不直接使用`DEL`释放锁，而是发送一个脚本，该脚本仅在值匹配时才删除密钥。

即增加对`value`的检查，只解除自己加的锁。类似于`CAS`，不过是`compare-and-delete`。

`SET resource-name token-value NX PX 10000`

```lua
if redis.call("get",KEYS[1]) == ARGV[1]
then
    return redis.call("del",KEYS[1])
else
    return 0
end
```
应使用`EVAL "...script..." 1 resource-name token-value`调用该`lua`脚本。

PHP示例：
```php
$key = 'ruesin_lock';
$value = 'ruesin_' . mt_rand(100000, 999999);
$isLock = Redis::set($key, $value, 'ex', 10, 'nx');
if ($isLock) {
    if (Redis::get($key) == $value) {  //防止提前过期，误删其它请求创建的锁
        // code...
        Redis::del($key);
    }
}
```

### RedLock

`Redis`官方提出了一种权威的基于`Redis`实现分布式锁的方式名[Redlock](https://redis.io/topics/distlock)，此种方式比原先的单节点的方法更安全。

它可以保证以下特性：
- 安全特性：互斥访问，即永远只有一个`client`能拿到锁
- 避免死锁：最终`client`都可能拿到锁，不会出现死锁的情况，即使原本锁住某资源的`client crash`了或者出现了网络分区
- 容错性：只要大部分`Redis`节点存活就可以正常提供服务

大概实现原理和`SET`相似，可以直接使用官方提供写好的代码：
```php
# 创建一个锁管理器
$servers = [
    ['127.0.0.1', 6379, 0.01],
    ['127.0.0.1', 6389, 0.01],
    ['127.0.0.1', 6399, 0.01],
];

$redLock = new RedLock($servers);

//获取锁 
// my_resource_name 是尝试锁定的唯一标识符，1000是有效时间的毫秒数
$lock = $redLock->lock('my_resource_name', 1000);
//Array
//(
//    [validity] => 9897.3020019531
//    [resource] => my_resource_name
//    [token] => 53771bfa1e775
//)

// 释放锁
$redLock->unlock($lock)
```
如果未获取锁定，则返回值为false，否则返回表示锁定的数组：

- validity：一个整数，表示锁有效的毫秒数
- resource：用户指定的锁定资源的名称
- token：一个随机令牌值，用于安全地回收锁

可以设置重试次数（默认为3）和用于获取锁定的重试延迟（默认为200毫秒），实际上，是在`$retryDelay / 2`毫秒和指定的`$retryDelay`值之间随机选择重试延迟。
