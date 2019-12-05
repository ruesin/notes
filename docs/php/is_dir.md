---
title: PHP判断指定目录中的目录和文件。
date: 2013-12-31 00:00:52
categories: PHP
tags: 
- php
---

是在百度php吧中看到有人问的，然后在他原本的基础上修改了下。  
修改后的代码如下：

判断文件夹是否存在

```
<form action="" method="post" name="form">
<input type="text" maxlength="120" name="dirs" size="100" />
<input type="submit" name="ruesin" value="进入目录" />
</form>

////php
if(isset($_POST['phplgx']) && !empty($_POST['dirs'])){
    $dirpath=trim($_POST['dirs']);
    if(file_exists($dirpath)){
        $dir=opendir($dirpath);
        while(false!==($file=readdir($dir))){
            if($file!="."&& $file!=".."){
                if(is_dir($dirpath."/".$file)){
                    echo "文件夹$file";
                }else{
                    echo "文件$file";
                }
            }
        }
    }else{
        echo "您输入的目录不正确!请重新输入";
    }
}else{
    echo "输入目录不能为空。";
}

```

主要改了两个地方。

1、修改前if(isset($\_POST\['phplgx'\]) && empty($\_POST\['dirs'\])) 判断的时候没有判断提交的目录为空 修改后if(isset($\_POST\['phplgx'\]) && !empty($\_POST\['dirs'\]))

2、修改前if(is\_dir($file)) 修改后if(is\_dir($dirpath.”/”.$file))  
原因很简单：在w3school查一下is\_dir的用法说明就很容易懂了——如果文件名存在并且为目录，则返回 true。如果 file 是一个相对路径，则按照当前工作目录检查其相对路径。
