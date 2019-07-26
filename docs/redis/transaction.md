---
title: Redis 事务
date: 2019-07-26 16:22:49
categories: Redis
---

事务(Transaction)：指作为单个逻辑工作单元执行的一系列操作。事务必须满足ACID原则(原子性、一致性、隔离性和持久性)。简单来说事务其实就是打包一组操作（或者命令）作为一个整体，在事务处理时将顺序执行这些操作，并返回结果，如果其中任何一个环节出错，所有的操作将被回滚。

`Redis`事务中的所有命令会序列化、按顺序地执行，事务在执行的过程中，不会被其他客户端发送来的命令请求所打断，事务中的命令要么全部被执行，要么全部都不执行。 

在Redis中实现事务主要依靠以下几个命令来实现：

1. WATCH：监视一个或多个`key`，如果在事务执行之前这些`key`被其他命令所改动，那么事务将被打断

2. UNWATCH：取消`WATCH`命令对所有`key`的监视

3. MULTI：标记一个事务块的开始，事务块内的多条命令会按照先后顺序被放进一个队列当中，最后由`EXEC`命令原子性(atomic)地执行

4. EXEC：执行所有事务块内的命令，返回值是按命令执行的先后顺序排列，当操作被打断时，返回空值`nil`

5. DISCARD：取消事务放弃执行事务块内的所有命令

如果客户端在使用`MULTI`开启了一个事务之后，因为断线而没有成功执行`EXEC`，那么事务中的所有命令都不会被执行；如果执行了`EXEC`，那么事务中的所有命令都会被执行，同一事务内的命令错误不会阻塞后续命令。 

当使用`AOF`方式做持久化的时候，`Redis`会使用单个`write(2)`命令将事务写入到磁盘中。如果`Redis`服务器因为某些原因被管理员杀死，或者遇上某种硬件故障，那么可能只有部分事务命令会被成功写入到磁盘中。如果`Redis`在重新启动时发现`AOF`文件出了这样的问题，那么它会退出，并汇报一个错误。使用`redis-check-aof`程序可以修复这一问题：它会移除`AOF`文件中不完整事务的信息，确保服务器可以顺利启动。

从`2.2`版本开始，`Redis`还可以通过乐观锁（optimistic lock）实现`CAS`（check-and-set）操作。

`Redis`中使用`MULTI`命令标记事务的开始，可以理解为在传统关系型数据库中的`BEGIN TRANCATION`语句，`Redis`将执行该命令的客户端从非事务状态切换成事务状态，这一切换是通过在客户端状态的`flags`属性中打开`REDIS_MULTI`标识完成：
```c
// src/multi.c
void multiCommand(client *c) {
    if (c->flags & CLIENT_MULTI) {
        addReplyError(c,"MULTI calls can not be nested");
        return;
    }
    c->flags |= CLIENT_MULTI; // 打开事务标识
    addReply(c,shared.ok);
}
```

客户端打开事务标识后，只有：EXEC，DISCARD，WATCH，MULTI命令会被立即执行，其它命令服务器不会立即执行，而是将这些命令放入到一个事务队列里面，然后向客户端返回一个QUEUED回复。

Redis中事务的提交(EXEC)和回滚(DISCARD)，可以看做关系型数据库中的COMMIT、ROLLBACK。

Redis客户端有自己的事务状态，这个状态保存在客户端状态mstate属性中，mstate的结构体类型是multiState：
```c
// src/server.h
typedef struct multiState {
    multiCmd *commands;     /* Array of MULTI commands */ // 存放 MULTI commands 的数组
    int count;              /* Total number of MULTI commands */ // 命令数量
    int cmd_flags;          /* The accumulated command flags OR-ed together.
                               So if at least a command has a given flag, it
                               will be set in this field. */
    int minreplicas;        /* MINREPLICAS for synchronous replication */
    time_t minreplicas_timeout; /* MINREPLICAS timeout as unixtime. */
} multiState;

/* Client MULTI/EXEC state */
typedef struct multiCmd {
    robj **argv; // 参数
    int argc;    // 参数数量
    struct redisCommand *cmd; // 命令指针
} multiCmd;
```

事务队列以先进先出的保存方法，较先入队的命令会被放到数组的前面，而较后入队的命令则会被放到数组的后面。

当开启事务标识的客户端发送EXEC命令的时候，服务器就会执行，客户端对应的事务队列里的命令：
```c
// src/multi.c

void execCommand(client *c) {
    int j;
    robj **orig_argv;
    int orig_argc;
    struct redisCommand *orig_cmd;
    int must_propagate = 0; //同步持久化，同步主从节点
    int was_master = server.masterhost == NULL;
    
    //如果客户端没有开启事务标识
    if (!(c->flags & CLIENT_MULTI)) {
        addReplyError(c,"EXEC without MULTI");
        return;
    }
    
    // 检查是否需要放弃 EXEC 
    /* Check if we need to abort the EXEC because:
     * 1) Some WATCHed key was touched.  如果WATCH的key被修改了就放弃执行
     * 2) There was a previous error while queueing commands.  在排队以前发生了错误
     * A failed EXEC in the first case returns a multi bulk nil object
     * (technically it is not an error but a special behavior), while
     * in the second an EXECABORT error is returned. 
     * 在第一种情况下，失败的EXEC返回一个多块nil对象(从技术上讲，它不是一个错误，而是一个特殊的行为)
     * 在第二种情况下，返回一个EXECABORT错误。
     */
    if (c->flags & (CLIENT_DIRTY_CAS|CLIENT_DIRTY_EXEC)) {
        addReply(c, c->flags & CLIENT_DIRTY_EXEC ? shared.execaborterr :
                                                   shared.nullarray[c->resp]);
        discardTransaction(c);
        goto handle_monitor;
    }

    /* If there are write commands inside the transaction, and this is a read
     * only slave, we want to send an error. This happens when the transaction
     * was initiated when the instance was a master or a writable replica and
     * then the configuration changed (for example instance was turned into
     * a replica). */
    if (!server.loading && server.masterhost && server.repl_slave_ro &&
        !(c->flags & CLIENT_MASTER) && c->mstate.cmd_flags & CMD_WRITE)
    {
        addReplyError(c,
            "Transaction contains write commands but instance "
            "is now a read-only replica. EXEC aborted.");
        discardTransaction(c);
        goto handle_monitor;
    }
    
    // 执行事务队列中所有的命令
    unwatchAllKeys(c); /* 因为Redis是单线程的，所以这里当检测到watch的key没有别修改后就统一clear掉所有的watch */
    orig_argv = c->argv;
    orig_argc = c->argc;
    orig_cmd = c->cmd;
    addReplyArrayLen(c,c->mstate.count);
    for (j = 0; j < c->mstate.count; j++) {
        c->argc = c->mstate.commands[j].argc;
        c->argv = c->mstate.commands[j].argv;
        c->cmd = c->mstate.commands[j].cmd;

        /* Propagate a MULTI request once we encounter the first command which
         * is not readonly nor an administrative one.
         * This way we'll deliver the MULTI/..../EXEC block as a whole and
         * both the AOF and the replication link will have the same consistency
         * and atomicity guarantees. */
         //同步主从节点和持久化
        if (!must_propagate && !(c->cmd->flags & (CMD_READONLY|CMD_ADMIN))) {
            execCommandPropagateMulti(c);
            must_propagate = 1;
        }
        // 执行命令
        call(c,server.loading ? CMD_CALL_NONE : CMD_CALL_FULL);

        /* Commands may alter argc/argv, restore mstate. */
        c->mstate.commands[j].argc = c->argc;
        c->mstate.commands[j].argv = c->argv;
        c->mstate.commands[j].cmd = c->cmd;
    }
    c->argv = orig_argv;
    c->argc = orig_argc;
    c->cmd = orig_cmd;
    discardTransaction(c); // 取消客户端的事务标识

    /* Make sure the EXEC command will be propagated as well if MULTI
     * was already propagated. */
    if (must_propagate) {
        int is_master = server.masterhost == NULL;
        server.dirty++;
        /* If inside the MULTI/EXEC block this instance was suddenly
         * switched from master to slave (using the SLAVEOF command), the
         * initial MULTI was propagated into the replication backlog, but the
         * rest was not. We need to make sure to at least terminate the
         * backlog with the final EXEC. */
        if (server.repl_backlog && was_master && !is_master) {
            char *execcmd = "*1\r\n$4\r\nEXEC\r\n";
            feedReplicationBacklog(execcmd,strlen(execcmd));
        }
    }

handle_monitor:
    /* Send EXEC to clients waiting data from MONITOR. We do it here
     * since the natural order of commands execution is actually:
     * MUTLI, EXEC, ... commands inside transaction ...
     * Instead EXEC is flagged as CMD_SKIP_MONITOR in the command
     * table, and we do it here with correct ordering. */
    if (listLength(server.monitors) && !server.loading)
        replicationFeedMonitors(c,server.monitors,c->db->id,c->argv,c->argc);
}
```

事务在执行`EXEC`之前，入队的命令可能会出错，比如，语法错误（参数数量错误、参数名错误等）、内存不足等。

在`Redis 2.6.5`以前，入队成功返回`QUEUED`；否则入队失败，`Redis`只执行事务中入队成功的命令，忽略入队失败的命令。

从`Redis 2.6.5`开始，服务器会对命令入队失败的情况进行记录，并在客户端调用`EXEC`命令时，拒绝执行并自动放弃这个事务，使得在`pipeline`中包含事务变得简单，因为发送事务和读取事务的回复都只需要和服务器进行一次通讯。 

命令可能在`EXEC`调用之后失败。比如，将列表命令用在了字符串键上面，事务中的命令可能处理了错误类型的键。即使事务中有某些命令在执行时产生了错误，事务中的其他命令仍然会继续执行。

在传统关系型数据库中的事务必须依靠ACID来保证事务的可靠性和安全性，在Redis中事务总是具有一致性(Consistency)和隔离性(Isolation)，并且当Redis运行在某种特定的持久化模式下，事务也具有耐久性(Durability)；但是并不总是能够保证原子性(Atomicity)，在正常状态下一个事务的所有命令是能按照原子性的原则执行的，但是执行的中途遇到错误，不会回滚，而是继续执行后续命令。
```
127.0.0.1:6379> set name "ruesin"
OK
127.0.0.1:6379> multi
OK
127.0.0.1:6379> set gender "m"
QUEUED
127.0.0.1:6379> rpush name "30"
QUEUED
127.0.0.1:6379> set age "30"
QUEUED
127.0.0.1:6379> exec
1) OK
2) (error) WRONGTYPE Operation against a key holding the wrong kind of value
3) OK
127.0.0.1:6379>
```
Redis的作者在事务功能的文档中解释说，不支持事务回滚是因为这种复杂的功能和Redis追求的简单高效的设计主旨不符合，并且他认为，Redis事务的执行时，错误通常都是编程错误造成的，这种错误通常只会出现在开发环境中，而很少会在实际的生产环境中出现，所以他认为没有必要为Redis开发事务回滚功能。所以我们在讨论Redis事务回滚的时候，一定要区分命令发生错误的时候。

不对回滚进行支持，可以使`Redis`内部保持简单且快速，`Redis`命令只会因为错误的语法而失败（并且这些问题不能在入队时发现），或是命令用在了错误类型的键上面：这也就是说，从实用性的角度来说，失败的命令是由编程错误造成的，而这些错误应该在开发的过程中被发现，而不应该出现在生产环境中。 

在通常情况下，回滚并不能解决编程错误带来的问题。比如，你本来想通过`INCR`命令将键的值加上`1`，却不小心加上了`2`，又或者对错误类型的键执行了`INCR`，回滚是没有办法处理这些情况的。 
鉴于没有任何机制能避免程序员自己造成的错误，并且这类错误通常不会在生产环境中出现，所以`Redis`选择了更简单、更快速的无回滚方式来处理事务。

可以通过事务，实现`zpop`功能，如下为`predis`的事务示例：
```php
function zpop($client, $key)
{
    $element = null;
    $options = array(
        'cas' => true,      // Initialize with support for CAS operations
        'watch' => $key,    // Key that needs to be WATCHed to detect changes
        'retry' => 3,       // Number of retries on aborted transactions, after
                            // which the client bails out with an exception.
    );
    $client->transaction($options, function ($tx) use ($key, &$element) {
        @list($element) = $tx->zrange($key, 0, 0);
        if (isset($element)) {
            $tx->multi();   // With CAS, MULTI *must* be explicitly invoked.
            $tx->zrem($key, $element);
        }
    });
    return $element;
}
$client = new Predis\Client($single_server);
$zpopped = zpop($client, 'zset');
echo isset($zpopped) ? "ZPOPed $zpopped" : 'Nothing to ZPOP!', PHP_EOL;
```

Redis事务在使用中有一些需要注意的点：

当事务与锁同时使用，锁的机制将无法体现，比如我们业务中有，当`hsetnx`执行成功时，才可以`rpush`数据，当加入到事务中时，不论`hsetnx`是否成功，都会执行`rpush`。

```php
// 
$redis->multi();
if ($redis->hsetnx('students_hash', '28', 'ruesin')) {
    $push = $redis->rpush('students_list', 'ruesin');
    echo "push:";var_dump($push);
} else {
    $dis = $redis->discard();
    echo "dis:";var_dump($dis);
    die('fail');
}
$exec = $redis->exec();
echo "exec:";var_dump($exec);
die('success');

// 多次执行后，发现 hash 永远是一条数据，而list则随着执行次数增加
// push:string(6) "QUEUED"
// exec:array(2) {
//   [0]=> int(0) // hsetnx 失败
//   [1]=> int(6) // 返回list条数
// }
// success
```

事务中使用 blpop、bzpopmin等阻塞命令时，无法达到预期的阻塞效果。

```
127.0.0.1:6379> MULTI
OK
127.0.0.1:6379> BLPOP test_list_a test_list_b 30
QUEUED
127.0.0.1:6379> EXEC
1) (nil)
```
BLPOP 可以用于流水线 (pipline, 批量地发送多个命令并读入多个回复)，但把它用在 MULTI / EXEC 块当中没有意义。因为这要求整个服务器被阻塞以保证块执行时的原子性，该行为阻止了其他客户端执行 LPUSH 或 RPUSH 命令。

因此，一个被包裹在 MULTI / EXEC 块内的 BLPOP 命令，行为表现得就像 LPOP 一样，对空列表返回 nil ，对非空列表弹出列表元素，不进行任何阻塞操作。

[BLPOP解析](./blpop.md)
