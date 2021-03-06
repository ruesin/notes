---
title: Redis Blpop
date: 2019-07-26 16:26:53
categories: Redis
---

BLPOP 命令是 LPOP 命令的阻塞版本，当指定列表内没有任何元素可供获取时，连接将被 BLPOP 命令阻塞，直到等待超时或存在可获取元素为止（有另一个客户端对指定key 的任意一个执行 push 命令）。

BLPOP命令指定多个 key 参数时，按照参数 key 的先后顺序依次检查各个列表，并弹出第一个非空列表的头元素。

BLPOP命令接受一个以秒为单位的数字作为超时时间，若超时参数设为 0 ，其表示无超时时间限制（即无限期阻塞等待数据的到来）。

当指定的列表为空且已经超时，返回 nil ；当指定的列表中存在可返回的元素时，返回元素列表，其中第一个元素是被弹出元素所属的 key ，第二个元素是被弹出元素的值。

相同的 key 可以被多个客户端同时阻塞，不同的客户端被放进一个队列中，按“先阻塞先服务”原则，顺序地为 key 执行 BLPOP 命令。

BLPOP 命令可以用于 pipline 中，但把它用在 MULTI/EXEC 块当中没有意义。因为这要求整个服务器被阻塞以保证块执行时的原子性，该行为阻止了其他客户端执行 LPUSH 或 RPUSH 命令。

因此，一个被包裹在 MULTI/EXEC 块内的 BLPOP 命令，行为表现得就像 LPOP 一样，对空列表返回 nil ，对非空列表弹出列表元素，不进行任何阻塞操作。

在调用阻塞队列取操作时，队列中无数据时才会真正的触发代码的阻塞分支。在客户端，Redis对新来的读请求删除了标记(通知)，这样直到阻塞的请求在获得服务前，新来的读请求都不能够被正常的服务。

```c
// ./src/t_list.c

void blpopCommand(client *c) {
    blockingPopGenericCommand(c,LIST_HEAD);
}

void brpoplpushCommand(client *c) {
    mstime_t timeout;

    if (getTimeoutFromObjectOrReply(c,c->argv[3],&timeout,UNIT_SECONDS)
        != C_OK) return;

    robj *key = lookupKeyWrite(c->db, c->argv[1]);

    if (key == NULL) {
        if (c->flags & CLIENT_MULTI) {
            /* 在事务中阻塞空列表会立即返回 */
            addReplyNull(c);
        } else {
            /* 列表为空，客户端阻塞 */
            blockForKeys(c,BLOCKED_LIST,c->argv + 1,1,timeout,c->argv[2],NULL);
        }
    } else {
        if (key->type != OBJ_LIST) {
            addReply(c, shared.wrongtypeerr);
        } else {
            /* 该列表存在并有元素，正常执行 rpoplpushCommand。 */
            serverAssertWithInfo(c,key,listTypeLength(key) > 0);
            rpoplpushCommand(c);
        }
    }
}

```

Redis 是通过 ready_keys 和 blocking_keys 两个链表和事件循环来处理阻塞事件的，BLPOP 不会阻塞 Redis 服务，不会影响其他命令服务。

Redis server 中有两个循环：
- IO循环：Redis 完成客户端连接应答、命令请求处理和命令处理结果回复等
- 定时循环：Redis完成过期key的检测等

Redis 一次连接处理的过程包含：
- IO多路复用检测套接字状态
- 套接字事件分派
- 请求事件处理

当BLPOP的key不存在或为空时，将 key 记录在 database 对应的 blocking_keys 数据结构中。blocking_keys 是一个字典结构，key 对应的是需要监听的名字，value 值是一个列表，里面存放被阻塞的客户端信息。处理完这些，然后也不关闭连接，就一直这样等待有客户向key里添加数据。

当服务器下次收到 PUSH 命令，会检查 blocking_keys 中是否存在对应的 key，如果存在，将 key 添加到 ready_keys 全局链表中，同时将 value 插入链表中并响应客户端。

服务端在每次的事件循环当中处理完客户端请求之后，会遍历 ready_keys 链表，并从 blocking_keys 链表当中找到对应的 client ，进行响应，整个过程并不会阻塞事件循环的执行。

而处理有设置 timeout 的 blocking POP 是通过定时任务来完成的，每隔一定时间就执行 clientsCronHandleTimeout ，将那些已经超时的客户端连接进行关闭。

```c
// ./src/blocked.c

/*
 * 这是当前阻塞 lists/sorted sets/streams 的工作方式，
 * 以BLPOP为例，对于其他 list 操作、sorted sets 和XREA，是一样的
 * - 如果用户调用BLPOP，键存在且包含非空列表，则调用LPOP。没有阻塞时，BLPOP在语义上与LPOP相同
 * - 如果调用了BLPOP而键不存在或列表为空，则需要阻塞。
 *   为了做到这一点，我们删除了在客户端套接字中读取新数据的通知(这样，如果没有提供阻塞请求，我们将不提供新请求)。
 *   我们还将客户端放在字典中(db->blocking_keys)，将键映射到为该键阻塞的客户端列表。
 * - 如果有PUSH数据到这些阻塞的key中，将这个key标记为“ready”。这个命令后，MULTI/EXEC语块、脚本 将会执行。
 *   我们为所有等待这个列表的客户端提供服务，从第一个阻塞列表到最后一个阻塞列表，根据我们在就绪列表中拥有的元素数量进行排序。
 */

/* Set a client in blocking mode for the specified key (list, zset or stream),
 * with the specified timeout. The 'type' argument is BLOCKED_LIST,
 * BLOCKED_ZSET or BLOCKED_STREAM depending on the kind of operation we are
 * waiting for an empty key in order to awake the client. The client is blocked
 * for all the 'numkeys' keys as in the 'keys' argument. When we block for
 * stream keys, we also provide an array of streamID structures: clients will
 * be unblocked only when items with an ID greater or equal to the specified
 * one is appended to the stream. */
void blockForKeys(client *c, int btype, robj **keys, int numkeys, mstime_t timeout, robj *target, streamID *ids) {
    dictEntry *de;
    list *l;
    int j;

    c->bpop.timeout = timeout;
    c->bpop.target = target;

    if (target != NULL) incrRefCount(target);

    for (j = 0; j < numkeys; j++) {
        /* The value associated with the key name in the bpop.keys dictionary
         * is NULL for lists and sorted sets, or the stream ID for streams. */
        void *key_data = NULL;
        if (btype == BLOCKED_STREAM) {
            key_data = zmalloc(sizeof(streamID));
            memcpy(key_data,ids+j,sizeof(streamID));
        }

        /* If the key already exists in the dictionary ignore it. */
        if (dictAdd(c->bpop.keys,keys[j],key_data) != DICT_OK) {
            zfree(key_data);
            continue;
        }
        incrRefCount(keys[j]);

        /* And in the other "side", to map keys -> clients */
        de = dictFind(c->db->blocking_keys,keys[j]);
        if (de == NULL) {
            int retval;

            /* For every key we take a list of clients blocked for it */
            l = listCreate();
            retval = dictAdd(c->db->blocking_keys,keys[j],l);
            incrRefCount(keys[j]);
            serverAssertWithInfo(c,keys[j],retval == DICT_OK);
        } else {
            l = dictGetVal(de);
        }
        listAddNodeTail(l,c);
    }
    blockClient(c,btype);
}

```
