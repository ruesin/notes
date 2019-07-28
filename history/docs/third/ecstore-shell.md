---
title: Ecstore 更改 dbschema 后执行 cmd update 不更新数据库
date: 2015-01-05 14:47:29
categories: 三方产品
---

不知道大家有没有碰到过，反正我刚接触Ecstore的时候，按照官方教程改了数据库文件，执行cmd update之后，数据库没有变化！

其实也不能说是不更新，而是第一次改的时候可以更新，再改再update就不好使了，当时遇到这个情况还是非常郁闷的，重启apache服务也不管用，一气之下把电脑重启了，再试、可以了。但总不能每次都要重启下电脑吧？

后来是发现只要关闭cmd窗口再次打开就可以更新了，就下了结论说是缓存的问题，然后就搁置了，最近又有朋友问到我这个问题，才想起来记录一下，顺便还原一下当时的经历。

注意：本文所述均为Windows下的操作。

**第一阶段：**  
1.随便改一个表的一个字段，以members表的name字段为例，将dbschema中的name字段改成nameaa，执行cmd update。

[![ecstore_shell_11](/images/2015/01/ecstore_shell_11.jpg)](/images/2015/01/ecstore_shell_11.jpg)

2.不关cmd窗口，将dbschema中的nameaa字段改回name，执行cmd update。

[![ecstore_shell_12](/images/2015/01/ecstore_shell_12.jpg)](/images/2015/01/ecstore_shell_12.jpg)

可以发现，虽然刷刷刷的走了一大堆的缓存，但是，没有看到更改数据表的语句执行，查看数据库，也没有被更改。

3.继续不关cmd窗口，执行shell文件中说到的强制更新数据库命令。

[![ecstore_shell_13](/images/2015/01/ecstore_shell_13.jpg)](/images/2015/01/ecstore_shell_13.jpg)

发现，还是没有更新。

4.关闭cmd，重新打开，执行update，可以了。

[![ecstore_shell_14](/images/2015/01/ecstore_shell_14.jpg)](/images/2015/01/ecstore_shell_14.jpg)

第一阶段总结：  
关闭cmd重新打开是可以正常更新数据库的，结论就是每次更新数据库，要重新打开一下cmd窗口。  
但是，shell文件中，明明白白说得很清楚，有强制刷新的命令，是不是因为我操作的第二步骤，导致后面的强制刷新也不行呢？那就把2跳过执行下试试。

**第二阶段：**  
1.同第一阶段 1

2.继续不关cmd窗口，执行shell文件中说到的强制更新数据库命令。

[![ecstore_shell_22](/images/2015/01/ecstore_shell_22.jpg)](/images/2015/01/ecstore_shell_22.jpg)

跟第一阶段的2一样，虽然刷刷刷的走了一大堆的缓存，但是，没有看到更改数据表的语句执行，查看数据库，也没有被更改。

第二阶段总结：  
强制更新数据库命令不管用。

**第三阶段：**  
看dbschema中有一个 version ，是不是他控制的呢？尝试更改 version ，然后重新来一遍第一阶段的步骤，还是不行。

最后总结，看来是shell命令真的缓存了，具体背后怎么走的流程，暂时没去翻看，而我们想要实现每次的updata都能成功，目前也只能关闭重新打开cmd窗口了。

PS：这个问题好像只在Windows下有问题，服务器上我操作时没碰到过这情况。。  
PS：后来我发现，其他的更改在update之前也要关闭重新打开一下，再后来就慢慢养成了每次更新之后都直接关闭的习惯。  
PS：执行cmd操作前要记得配置环境变量哦。
