---
title: Yii 2.0 授权 Authorization
date: 2015-07-28 13:57:17
categories: 开源项目
---

在任何系统中，权限设计是最基础的东西，在 Yii2 中，使用授权的形式来检验一个用户有足够权限来做些事情。

Yii提供两种授权方法：访问控制过滤（ACF)和基于角色的访问控制（RBAC)。

**一、Access Control Filter 访问控制过滤**

访问控制过滤（ACF)是一个简单的授权方法，非常适合于在只需要一些简单访问控制的程序中使用。正如名字所标示的，访问控制过滤（ACF)是一个动作过滤，它可以作为一个扩展附加到一个控制器或是一个模块。

```
public function behaviors()
{
    return [
        'access' => [
            'class' => yii\filters\AccessControl::className(),
            //'only' => ['logout', 'signup'],   //只对 logout signup 进行验证
            'rules' => [  //[[yii\filters\AccessRule|accessrules]]
                //所有访客都可以访问signup方法
                [
                    'actions' => ['signup'],   
                    'allow' => true,
                    'roles' => ['?'],// matches a guest user (not authenticated yet)
                ],
                //已授权的用户可以访问logout
                [
                    'actions' => ['logout'],
                    'allow' => true,
                    'roles' => ['@'],  //matches an authenticated user
                ],
				//匿名函数验证
                [
                    'actions' => ['special-callback'],
                    'allow' => true,
                    'matchCallback' => function ($rule, $action) {
                        return date('d-m') === '31-10';
                    }
                ],
                //others deny
            ],
        ],
    ];
}
```

当访问控制过滤（ACF)进行授权检查时，它会从上到下地一个接着一个地测试那些规则直至找到一个相符的。相符的允许值将立即用于判断用户是否被授权。如果没有一个规则符合，这就意味着这个用户“没有”被授权，访问控制过滤（ACF)将阻止它进一步的动作请求。

默认情况下，当访问控制过滤（ACF)探测到一个用户没有被授权进入当前动作时，它只会作下面的工作：

如果这个用户是个访客，ACF将会调用\[\[yii\\web\\User::loginRequired()\]\]，将浏览器重定向到配置的登录页面。

如果用户已有授权，ACF会抛出一个\[\[yii\\web\\ForbiddenHttpException\]\]。

你可以通过定义配置\[\[yii\\filters\\AccessControl::denyCallback\]\]的属性来对这个扩展进行自定义：

```
[
    'class' => AccessControl::className(),
    'denyCallback' => function ($rule, $action) {
        throw new \Exception('You are not allowed to access this page 您没有被允许访问这个页面！');
    }
]
```

\[\[yii\\filters\\AccessRule|Access rules\]\] 验证规则是很灵活的，支持许多选项，还可以有IP、请求类型、匿名函数等验证，具体的可以跟踪到 \[\[yii\\filters\\AccessRule\]\] 查看。

\[\[yii\\filters\\AccessRule\]\]：指定是一个“允许”规则还是一个“禁止”规则。

\[\[yii\\filters\\AccessRule::actions|actions\]\]：指定这个规则与哪些动作匹配。这应该是一个动作的ID的数组。比较是区分大小写的。如果这个选项是空的或是没有设置，这意味着这个规则适用于所有的动作。

\[\[yii\\filters\\AccessRule::controllers|controllers\]\]：指定这个规则与哪些控制器匹配。这应该是一个控制器的ID的数组。比较是区分大小写的。如果这个选项是空的或是没有设置，这意味着这个规则适用于所有的控制器。

\[\[yii\\filters\\AccessRule::roles|roles\]\]：指定这个规则与哪些用户角色匹配。两个特别的用户角色已经被确立，它们将通过\[\[yii\\web\\User::isGuest\]\]来检查。

？：匹配访客（还没有被授权）

@：匹配一个已授权用户

使用其他角色名称的已授权用户，将会调用\[\[yii\\web\\User::can()\]\]，就走到基于角色的访问控制（RBAC)了。如果这个选项是空的或是没有设置，这意味着这个规则适用于所有的角色。

\[\[yii\\filters\\AccessRule::ips|ips\]\]：指定这个规则匹配哪一个\[\[yii\\web\\Request::userIP|clientIP addresses\]\]。一个IP地址可以在末尾包含一个通配符，这样就可以匹配具有相同前缀的所有IP地址。比如，“192.168.”，匹配“192.168.”节中所有的IP地址。如果这个选项是空的或是没有设置，这意味着这个规则适用于所有的IP。

\[\[yii\\filters\\AccessRule::verbs|verbs\]\]:指定这个规则匹配哪种请求方法（比如GET，POST)。比较是区分大小写的。

\[\[yii\\filters\\AccessRule::matchCallback|matchCallback\]\]：指定一个PHP可调用，它将被调用来检查这个规则是否可以执行。

\[\[yii\\filters\\AccessRule::denyCallback|denyCallback\]\]：指定一个PHP可调用，在这个规则拒绝访问时它将被调用。

**二、基于角色的访问控制（RBAC）**

基于角色的访问控制（RBAC）是用非常灵活的方式来控制访问，提供了简单而又功能强大的集中的访问控制。

Yii提供了两种鉴权管理器：yii\\rbac\\PhpManager 和 yii\\rbac\\DbManager。

前者使用一个PHP脚本文件管理鉴权数据，而后者是把数据存储在数据库里面。PhpManager主要适用于授权的数据不是太大，不需要经常变动的角色和权限管理的应用(例如,一个个人博客系统的授权数据)。DbManager 更适用于较复杂的授权数据。

**2.1 基于文件的配置的RBAC**

在定义鉴权数据并执行访问检查之前，必须先配置authManager组件。

```
'authManager' => [
    'class' => 'yii\rbac\PhpManager',
    'defaultRoles' => ['guest'],
],
```

默认的，yii\\rbac\\PhpManager 在三个文件里面存储RBAC数据：

@app/rbac/items.php //定义角色和许可，在角色和许可间建立关系  
@app/rbac/assignments.php’ //分配角色给用户  
@app/rbac/rules.php’ //定义规则，把规则跟角色和许可关联起来 规则就是访问检查的时候执行的一段代码，它来决定相应的角色或者权限是否适用于当前用户。

请确保这三个文件对服务器进程可写，有时你需要手动的去创建这些文件。

```
items.php

return [
    'createPost' => [
        'type' => 2,
        'description' => 'Create a post',
    ],
    'updatePost' => [
        'type' => 2,
        'description' => 'Update post',
    ],
    'read' => [
        'type' => 2,
        'description' => 'Read',
    ],
    'author' => [
        'type' => 1,
        'children' => [
            'createPost',
            'read',
            'updateOwnPost',
        ],
    ],
    'admin' => [
        'type' => 1,
        'children' => [
            'updatePost',
            'author',
        ],
    ],
    'updateOwnPost' => [
        'type' => 2,
        'description' => 'Update own post',
        'ruleName' => 'isAuthor',
        'children' => [
            'updatePost',
        ],
    ],
];
```

```
assignments.php

return [
    2 => [
        'author',
    ],
    1 => [
        'admin',
    ],
];
```

```
rules.php

return [
    'isAuthor' => 'O:19:"yii\\rbac\\AuthorRule":3:{s:4:"name";s:8:"isAuthor";s:9:"createdAt";N;s:9:"updatedAt";N;}',
];
```

如果刚开始不太清楚结构，可以通过authManager提供的API创建一个控制台命令来生成示例代码。

```
namespace console\controllers;

use yii\console\Controller;

class RbacController extends \yii\console\Controller 
{
    public function actionInit()
    {
        $auth = \Yii::$app->authManager;

        // 添加”创建文章”许可
        $createPost = $auth->createPermission('createPost');
        $createPost->description = 'Create a post';
        $auth->add($createPost);

        // 添加”更新文章”许可
        $updatePost = $auth->createPermission('updatePost');
        $updatePost->description = 'Update post';
        $auth->add($updatePost);

        // 添加”查看文章”许可
        $reader = $auth->createPermission('read');
        $reader->description = 'Read';
        $auth->add($reader);

        // 添加“作者”角色，接着赋予这个角色“创建文章”的许可
        $author = $auth->createRole('author');
        $auth->add($author);

        $auth->addChild($author, $createPost);
        $auth->addChild($author, $reader);

        // 添加“管理员”角色，接着赋予这个角色“更新文章”的许可
        // 与“作者角色的一样
        $admin = $auth->createRole('admin');
        $auth->add($admin);
        $auth->addChild($admin, $updatePost);
        $auth->addChild($admin, $author);

        //添加一条规则
        $rule = new \yii\rbac\AuthorRule;
        $auth->add($rule);

        //添加“updateOwnPost”权限，并且和上面的规则关联起来
        $updateOwnPost = $auth->createPermission('updateOwnPost');
        $updateOwnPost->description = 'Update own post';
        $updateOwnPost->ruleName = $rule->name;
        $auth->add($updateOwnPost);

        // "updateOwnPost" will be used from "updatePost"
        $auth->addChild($updateOwnPost, $updatePost);

        // allow "author" to update their own posts
        $auth->addChild($author, $updateOwnPost);

        // 分配角色给用户。1和2是用户ID，用IdentityInterface::getId()获取到的
        // 经常出现在您的User模块中。
        $auth->assign($author, 2);
        $auth->assign($admin, 1);
    }
}
```

当鉴权数据准备好之后，就可以进行访问检查了。可以通过配置ACF进行自动校验，也可以在某一个要操作的方法中进行校验。前者其实也是调用的后者的方法。

```
if (\Yii::$app->user->can('createPost')) {
    // create post
}
```

**2.2 以DB为基础的存储RBAC**

如果是数据经常变动并且后台需要灵活管理，用DB形式的是比较好的一个选择。

Yii2 的RBAC一共是用到了五张表：四张auth表和一张user表。其中 auth 表位于 vendor/yiisoft/yii2/rbac/migration， 可使用命令生成 yii migrate –migrationPath=@yii/rbac/migrations/

auth\_item ：存储角色或权限的表。name为权限名，用 type 字段来标识是角色还是权限， 1 为角色 , 2 为权限 。

auth\_item\_child：角色权限关联表。角色是一组权限的集合，和上面的auth\_item相关联，用来保存角色和权限的关系，两个字段均对应 auth\_item 表的 name 字段。  
角色可以包含角色或权限，权限可以包含权限。  
如果要得到一个角色的所有的权限，要做两方面的查找，一个是递归查找当前权限所有的子权限， 一个是查看所包含的角色的所有的权限以及子权限。所以在使用中不建议让权限继承，只让角色继承。而且继承深度也不宜太深。

auth\_assignment：权限（角色）和用户的关联表，这个表用来存储给用户分配的角色或者权限，一个用户的权限包含两部分，一部分是所指定的角色代表的权限，一部分就是直接所指定的权限。

auth\_rule：规则表 一个用户要执行一个操作除了要看他有没有这个权限外，还要看他的这个权限能不能执行。 auth\_item 中还有一个字段： \[rule\_name\] 。这个字段用来标明这个角色或者权限能不能成功执行。

1、配置 Rbac，生成数据表。

```
'authManager' => [
    'class' => 'yii\rbac\DbManager',
    'itemTable' => 'auth_item',
    'assignmentTable' => 'auth_assignment',
    'itemChildTable' => 'auth_item_child',
],
```

`yii migrate --migrationPath=@yii/rbac/migrations/ `2、创建一个 许可 Permiassion

```
public function createPermission($item)
{
    $auth = Yii::$app->authManager;

    $createPost = $auth->createPermission($item);
    $createPost->description = '创建了 ' . $item . ' 许可';
    $auth->add($createPost);
}
```

3、创建一个 角色 roles

```
public function createRole($item)
{
    $auth = Yii::$app->authManager;
    $role = $auth->createRole($item);
    $role->description = '创建了 ' . $item . ' 角色';
    $auth->add($role);
}
```

4、给角色分配许可

```
static public function createEmpowerment($items)
{
    $auth = Yii::$app->authManager;
    $parent = $auth->createRole($items['name']);
    $child = $auth->createPermission($items['description']);

    $auth->addChild($parent, $child);
}
```

5、给角色分配用户

```
static public function assign($item)
{
    $auth = Yii::$app->authManager;
    $reader = $auth->createRole($item['name']);
    $auth->assign($reader, $item['description']);
}
```

6、验证用户是否有权限

```
public function beforeAction($action)
{
    $action = Yii::$app->controller->action->id;
    if(\Yii::$app->user->can($action)){
        return true;
    }else{
        throw new \yii\web\UnauthorizedHttpException('对不起，您现在还没获此操作的权限');
    }
}
```

实际操作与 PhpManager 异曲同工，都是创建权限、创建角色、分配权限、绑定用户。

当然，yii只是为我们提供了基础的授权机制，你尽可以在此基础上大动手脚，比如用户表看不上，改user组件，权限表不符合自己的审美，改组件+数据表。。。

附：  
yii\\rbac: Item 为角色或者权限的基类，其中用字段type来标识  
yii\\rbac: Role 为代表角色的类  
yii\\rbac: Permission 为代表权限的类  
yii\\rbac: Assignment 为代表用户角色或者权限的类  
yii\\rbac: Rule 为代表角色或权限能否执行的判定规则

参考:

http://pan.baidu.com/s/1dDrWUbR
