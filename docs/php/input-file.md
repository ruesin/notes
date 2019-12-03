---
title: php+jquery 无刷新上传图片
date: 2014-10-13 14:52:24
categories: PHP
---

项目中我们经常会用到图片（文件）上传功能，简单粗暴的方法就是直接自带的input file，高端华丽点的就是swfupload。本文是为了优化了下用户体验前提下对自带组件进行简单的加工。粗制滥造只为给各位起到抛砖引玉的作用。  
**html**

```
<div id="upImgBox">
    <img id="upImgImage" src="/public/images/upload-pic.png" width="135" height="110" />
</div>
<style>
    .upImgBox{position:relative;width:135px}
    .upImgImage{}
    .upImgFile{position:absolute; top:0; left:0px; width:135px; height:110px; filter:alpha(opacity:0);opacity: 0;}
</style>
<script src="/public/js/jquery.min.js"></script>
<script src="/public/js/jquery.form.js"></script>
<script>
    $('#upImgFile').change(function(){
        $('#myForm').ajaxSubmit({
            type:"post",
            url:'index.php?ctl=image&act=upImg',
            dataType: 'json', 
            success:function(res){
                alert(res.msg);
                $('#upImgImage').attr('src',res.img);
            }
        });
    });
</script>

```

[![input_file1](/images/2014/10/input_file1.jpg)](/images/2014/10/input_file1.jpg)

**PHP**

```
public function upImg(){
    $res['num'] = -1;
    if(!empty($_FILES)){
        $fileTypes = array("image/gif","image/jpeg");

        $upload_name = $_FILES["file"]["name"];
        $upload_type = $_FILES["file"]["type"];
        $upload_size = $_FILES["file"]["size"];

        $tmp_name    = $_FILES["file"]["tmp_name"];

        $server_name = "/upload/".date("Y/m")."/".$upload_name;

        if(in_array($upload_type,$fileTypes)){
            $server_file = $_SERVER['DOCUMENT_ROOT'].iconv("UTF-8","gb2312", $server_name);//防止文件名称中文乱码
            if(move_uploaded_file($tmp_name,$server_file)){
                $res['num'] = 1;
                $res['msg'] = '上传成功!';
                $res['img'] = $server_name;
            }else{
                $res['msg'] = '上传失败!';
            }
        }else{
            $res['msg'] = '不支持此文件类型，请重新选择!';
        }
    }else{
        $res['msg'] = '请选择文件!';
    }
    echo json_encode($res);      
}
```
