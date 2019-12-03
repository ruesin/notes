---
title: Yii 2.0 对象加载时，对属性的处理过程
date: 2015-04-16 11:00:34
categories: 开源项目
---

由于工作中暂时没有用到yii，而自己平时又太多的杂事，似乎都没怎么深入过，着实惭愧。  
重新看深入理解yii2.0，似乎更加清晰，本文就是按照自己的理解写一下yii对象加载时，对属性的处理过程。

打开当前应用下的入口文件，可以看到加载了很多配置文件，其实这些配置文件就是一个各种配置项的数组，Yii中就是通过这些数组对对象进行配置的，这一方式贯穿整个Yii。

```
// comment out the following two lines when deployed to production
defined('YII_DEBUG') or define('YII_DEBUG', true);
defined('YII_ENV') or define('YII_ENV', 'dev');

require(__DIR__ . '/../vendor/autoload.php');
require(__DIR__ . '/../vendor/yiisoft/yii2/Yii.php');

$config = require(__DIR__ . '/../config/web.php');

(new yii\web\Application($config))->run();
```

那么这个所谓的配置数组是在哪里用到的呢，逐级追可以看到在 yii\\base\\Object 的构造函数中:

```
public function __construct($config = [])
{
    if (!empty($config)) {
        Yii::configure($this, $config);
    }
    $this->init();
}
```

而 Yii::configure() 是何许人也？其实此方法只是执行了一个数组遍历，将配置数组的键作为属性名，将对应数组元素的值为对象的属性赋值。

```
public static function configure($object, $properties)
{
    foreach ($properties as $name => $value) {
        $object->$name = $value;
    }

    return $object;
}
```

这样你配置数据就可以通过访问 Yii 的属性进行访问了。

但是，到这里还没有完，Yii很多默认的组件，比如 Yii::$app->request ，是配置文件中 components 的嵌套配置数组里的，但是也是直接访问的，是哪里做的处理呢？

在Yii的规则里，如果一个属性是对象，那么他就要通过数组来进行配置。Yii应用 yii\\web\\Application 就是依靠定义专门的setter函数，实现自动处理配置项的。比如，我们上面说的配置项 components 的内容是这样的:

```
'components' => [
    'request' => [
        // !!! insert a secret key in the following (if it is empty) -
        // this is required by cookie validation
        'cookieValidationKey' => 'Ruesin',
    ],
    'user' => [
        'identityClass' => 'common\models\User',
        'enableAutoLogin' => true,
    ],
    'log' => [
        'traceLevel' => YII_DEBUG ? 3 : 0,
        'targets' => [
            [
                'class' => 'yii\log\FileTarget',
                'levels' => ['error', 'warning'],
            ],
        ],
    ],
    'errorHandler' => [
        'errorAction' => 'site/error',
    ],
],
```

Yii 在服务定位器 yii\\di\\ServiceLocator 中定义了一个名为 setComponents 的setter函数。

```
public function setComponents($components)
{
    foreach ($components as $id => $component) {
        $this->set($id, $component);
    }
}
```

```
public function set($id, $definition)
{
    if ($definition === null) {
        unset($this->_components[$id], $this->_definitions[$id]);
        return;
    }

    unset($this->_components[$id]);

    if (is_object($definition) || is_callable($definition, true)) {
        // an object, a class name, or a PHP callable
        $this->_definitions[$id] = $definition;
    } elseif (is_array($definition)) {
        // a configuration array
        if (isset($definition['class'])) {
            $this->_definitions[$id] = $definition;
        } else {
            throw new InvalidConfigException("The configuration for the \"$id\" component must contain a \"class\" element.");
        }
    } else {
        throw new InvalidConfigException("Unexpected configuration type for the \"$id\" component: " . gettype($definition));
    }
}
```

这个方法服务定位器用来注册服务的方法。通过这个方法判断配置文件中的 components 配置项是对象还是数组，如果是数组就实例化成对象。并在 setComponents 方法中将对象赋值给 app 的属性。

所有 yii\\base\\Object 的构建流程是：

 1.引入由外部代码或者通过配置文件规范的配置数组项。  
 2.yii\\base\\Object 构造函数，设置属性的默认值，加载配置数组。  
 3.通过构造函数调用 Yii::configure($this, $config) 设置对象属性的默认值，重写上一步的属性值。如果对象属性还是一个对象或数组，定义并调用 setKey 的setter方法，将数组实例化成对象再复制给app对象的属性。比如我们常用的组件对象就是使用 setComponents 将各个组件实例化成对象并赋值给app对象的属性的。  
 4.如上步骤完成后，调用初始化方法 init() ，通过在 init() 写入代码，可以对配置阶段设置的值进行检查，并规范类的property。

此时，该对象的状态是确定且可靠的，不存在不确定的property。 所有的属性要么是默认值，要么是传入的配置值，如果传入的配置有误或者冲突，那么也经过了检查和规范。 也就是说，你就放心用吧。

如果你的对象继承自 yii\\base\\Object 。那么你要做到一下几点：  
 为对象属性提供setter方法，以正确处理配置过程。  
 如果需要重载构造函数， $config 要作为该构造函数的最后一个参数，并要传递该参数给父构造函数。  
 重载的构造函数的最后，一定记得调用父构造函数。  
 如果重载了初始化方法 init()，注意一定要在重载方法的开头调用父类的 init() 。
