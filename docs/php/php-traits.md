---
title: PHP的Traits特性实现多继承及代码复用
date: 2015-06-23 11:28:28
categories: PHP
tags: 
- php
- php traits
- php多继承
- php代码复用
- php 基础
- ubuntu git
---

有很多时候，我们会用到所谓的 PHP “多继承”，而在PHP中是不支持多重继承的，但是我们可以通过另类的方法来实现类似多继承的功能。

比如使用组合，在一个类中去将另外一个类设置成属性，使用魔术方法 \_\_call 重定向方法的调用。

比如使用接口，虽然PHP类只能继承一个父类（单继承），但是接口和类不同，接口可以实现多继承。

而 5.4 中的 Traits 的出现，为我提供了另外一种可行的方法。

Traits 是一种为类似 PHP 的单继承语言而准备的代码复用机制，它能让开发者在多个不同的class中实现代码重用。Trait 为了减少单继承语言的限制，使开发人员能够自由地在不同层次结构内独立的类中复用方法集。Traits 和类组合的语义是定义了一种方式来减少复杂性，避免传统多继承和混入类（Mixin）相关的典型问题。

Trait 和一个类相似，但仅仅旨在用细粒度和一致的方式来组合功能。Trait 不能通过它自身来实例化，即不存在类似class的构造函数\_\_construct()。它为传统继承增加了水平特性的组合；也就是说，应用类的成员不需要继承。

**1、使用**

在类中用关键字’use’ 来引用 Traits。多个Traits 用’,'隔开。

```
trait ezcReflectionReturnInfo {
    function getReturnType() { /*1*/ }
    function getReturnDescription() { /*2*/ }
}

class ezcReflectionMethod extends ReflectionMethod {
    use ezcReflectionReturnInfo;
    /* ... */
}

class ezcReflectionFunction extends ReflectionFunction {
    use ezcReflectionReturnInfo;
    /* ... */
}
```

**2、优先级**

从基类继承的成员被 trait 插入的成员所覆盖，来自当前类的成员覆盖 trait 的方法。

```
class Base {
    public function sayHello() {
        echo 'Hello ';
    }
}

trait SayWorld {
    public function sayHello() {
        parent::sayHello();
        echo 'World!';
    }
    public function sayHellos() {
        echo 'Hello World!';
    }
}

class MyHelloWorld extends Base {
    use SayWorld;

    public function sayHellos() {
        echo 'Hello Universe!';
    }
}

$o = new MyHelloWorld();
$o->sayHello();  #Hello World!
$o->sayHellos();  #Hello Universe!
```

**3、多个 trait**

通过逗号分隔，在 use 声明列出多个 trait，可以都插入到一个类中。

```
trait Hello {
    public function sayHello() {
        echo 'Hello ';
    }
}

trait World {
    public function sayWorld() {
        echo 'World';
    }
}

class MyHelloWorld {
    use Hello, World;
}

$o = new MyHelloWorld();
$o->sayHello(); # Hello
$o->sayWorld(); # World
```

**4、多Traits冲突的解决**

如果两个 trait 都插入了一个同名的方法，如果没有明确解决冲突将会产生一个致命错误。

为了解决多个 trait 在同一个类中的命名冲突，需要使用 insteadof 操作符来明确指定使用冲突方法中的哪一个。

以上方式仅允许排除掉其它方法，as 操作符可以将其中一个冲突的方法以另一个名称来引入。

```
trait A{
    public function smallTalk(){
        echo 'a';
    }
    public function bigTalk(){
        echo 'A';
    }
}

trait B{
    public function smallTalk(){
        echo 'b';
    }
    public function bigTalk(){
        echo 'B';
    }
}

class Talker{
    use A,B{
        B::smallTalk insteadof A;
        A::bigTalk insteadof B;
    }
}

class Talkers{
    use A,B{
        B::smallTalk insteadof A;
        A::bigTalk insteadof B;
        B::bigTalk as bTalk;
    }
}

$o = new Talker();
$o->smallTalk(); # b
$o->bigTalk(); # A

$os = new Talkers();
$os->smallTalk(); # b
$os->bigTalk(); #A
$os->bTalk(); # B
```

**5、修改方法的访问控制**

还可以使用as语法来改变Traits中函数的访问权限属性。

```
trait HelloRuesin {
    public function sayHello() {
        echo 'Hello Ruesin';
    }
}

class Hello {
    use HelloRuesin {
        sayHello as protected; ## 修改 sayHello 的访问控制
    }
}

class Ruesin {
    use HelloRuesin {
        sayHello as private sayHellos; ## 给方法一个改变了访问控制的别名 而原版 sayHello 的访问控制则没有发生变化
    }
}

$o  = new Hello();
$os = new Ruesin();
#$o->sayHello(); # 无法访问
$os->sayHello(); # Hello Ruesin
#$os->sayHellos(); # 无法访问
```

**6、用Traits组成新Traits**

正如类能够使用 trait 一样，其它 trait 也能够使用 trait。在 trait 定义时通过使用一个或多个 trait，它能够组合其它 trait 中的部分或全部成员。

```
trait Hello {
    public function sayHello() {
        echo 'Hello';
    }
}

trait Ruesin {
    public function sayRuesin() {
        echo 'Ruesin';
    }
}

trait HelloRuesin {
    use Hello,Ruesin;
}

class SayHelloRuesin {
    use HelloRuesin;
}

$o = new SayHelloRuesin();
$o->sayHello();  #Hello
$o->sayRuesin(); #Ruesin
```

**7、Trait 的抽象成员**

为了对使用的类施加强制要求，trait 支持抽象方法的使用。表示通过抽象方法来进行强制要求

```
trait Hello {
    public function sayHelloRuesin() {
        echo 'Hello '.$this->getName();
    }
    abstract public function getName();
}

class HelloRuesin {
    private $name;
    use Hello;
    public function __construct($name) {
        $this->name = $name;
    }
    public function getName() {
        return $this->name;
    }
}

(new HelloRuesin('Ruesin'))->sayHelloRuesin(); # Hello Ruesin
```

**8、trait 的静态成员**

静态变量可以被 trait 的方法引用，但不能被 trait 定义。Traits 能够为使用的类定义静态方法。

```
trait Counter {
    public function inc() {
        static $c = 0;
        $c = $c + 1;
        echo "$c\n";
    }

    public static function HelloRuesin() {
        #return 'Doing something';
        echo 'Hello Ruesin';
    }
}

class C {
    use Counter;
}

$o = new C(); 
$o->inc(); # 1
$o->inc(); # 2
C::HelloRuesin(); #Hello Ruesin'
```

**9、Trait 定义属性**

如果 trait 定义了一个属性，那类将不能定义同样名称的属性，否则会产生一个错误。如果该属性在类中的定义与在 trait 中的定义兼容（同样的可见性和初始值）则错误的级别是 E\_STRICT，否则是一个致命错误。

```
trait PropertiesTrait {
    public $x = 1;
}

class PropertiesExample {
    use PropertiesTrait;
    #public $same = true; # Strict Standards
    #public $different = true; # 致命错误
}

$example = new PropertiesExample;
$example->x; # 1
```
