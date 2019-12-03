---
title: PHP图像识别技术
date: 2015-04-01 10:19:21
categories: PHP
---

其实图像识别技术与我们平时做的密码验证之类的没有什么区别，都是事先把要校验的数据入库，然后使用时将录入（识别）的数据与库中的数据做对比，只不过图像识别技术有一部分的容错性，而我们平时的密码验证是要100%匹配。

前几天，有朋友谈到做游戏点击抽奖，识别图片中的文字，当时立马想到的就是js控制或者flash做遮罩层，感觉这种办法是最方便快捷效果好，而且节省服务器资源，但是那边提的要求竟然是通过php识别图像中的文字。

赶巧那两天的新闻有：1、马云人脸识别支付；2、12306使用新的验证码，说什么现在国内的抢票软件都不能用了，发布不到一天就被破解。然后又很凑巧的那天早上看了一篇Java的图像识别技术文章。于是就琢磨着看一下PHP的图像识别技术。

其实所谓的图像识别，已经不是什么新技术了，起码我找到的资料都是很早之前的了。只不过我一直没涉及到这方面的工作，就一直没看过。

先说下这次实验的需求：有一张图片，里面三个位置分别有三个数字，要求取出相应位置的数字的值。（眼尖的同学可能会看出下面的代码是我拿的别人的，没错，的确是我直接copy别人并删减的，毕竟我对这些也是浅尝辄止，最后会贴出原作者的初始代码）

[![jd](/images/2015/04/jd.png)](/images/2015/04/jd.png)

```
class gjPhone
{

    protected $imgPath; // 图片路径
    protected $imgSize; // 图片大小
    protected $hecData; // 分离后数组
    protected $horData; // 横向整理的数据
    protected $verData; // 纵向整理的数据
    function __construct ($path)
    {
        $this->imgPath = $path;
    }

    public function getHec ()
    {
        $size = getimagesize($this->imgPath);
        $res = imagecreatefrompng($this->imgPath);
        for ($i = 0; $i imgSize = $size;
        $this->hecData = $data;
    }

    public function magHorData ()
    {
        $data = $this->hecData;
        $size = $this->imgSize;
        $z = 0;
        for ($i = 0; $i horData = $newdata;
    }

    public function showPhone ($ndatas)
    {
        error_reporting(0);
        $phone = null;
        $d = 0;
        foreach ($ndatas as $key => $val) {
            if (in_array(1, $val)) {
                foreach ($val as $k => $v) {
                    $ndArr[$d] .= $v;
                }
            }
            if (! in_array(1, $val)) {
                $d ++;
            }
        }
        foreach ($ndArr as $key01 => $val01) {
            $phone .= $this->initData($val01);
        }
        return $phone;
    }

    /**
     * 初始数据
     */
    public function initData ($numStr)
    {
        $result = null;
        $data = array(
                '1' => '00000000111000000000000001110000000001001000100000000010100011000000000011000110000000000110000100000000010110011000000',
                '5' => '00000000001000000000000000010000000000100100100000000000101001110000000000100000110000000011000000100000001101000010000',
                '10' => '00000011100011100000000011001100100100100010010001000110000100100010001100001001000100011000010010001001001001100010100'
        );
        foreach ($data as $key => $val) {
            similar_text($numStr, $val, $pre);
            if ($pre > 95) { // 相似度95%以上
                $result = $key;
                break;
            }
        }
        return $result;
    }
}

$imgurl = 'jd.png';
list ($width, $heght, $type, $attr) = getimagesize($imgurl);
$new_w = 17;
$new_h = 11;
$thisimage = imagecreatetruecolor($new_w, $new_h); // $new_w, $new_h 为裁剪后的图片宽高
$background = imagecolorallocate($thisimage, 255, 255, 255);
imagefilledrectangle($thisimage, 0, 0, $new_w, $new_h, $background);
$oldimg = imagecreatefrompng($imgurl); // 载入原始图片
                                       
// 首先定位要取图的位置(这里可以通过前端js或者其他手段定位，由于我这是测试，所以就ps定位并写死了)
$weizhi = array(
        '1' => 165,
        '5' => 308,
        '10' => 456
);

foreach ($weizhi as $wwzz) {
    $src_y = 108;
    imagecopy($thisimage, $oldimg, 0, 0, $wwzz, $src_y, $new_w, $new_h); // $src_y,$new_w为原图中裁剪区域的左上角坐标拷贝图像的一部分将src_im图像中坐标从src_x，src_y开始，宽度为src_w，高度为src_h的一部分拷贝到dst_im图像中坐标为dst_x和dst_y的位置上。
    $tem_png = 'tem_1.png';
    imagepng($thisimage, __DIR__ . '/' . $tem_png); // 通过定位从原图中copy出想要识别的位置并生成新的缓存图，用以后面的图像识别类使用。
    
    $gjPhone = new gjPhone($tem_png); // 实例化类
    $gjPhone->getHec(); // 进行图像像素分离
    $horData = $gjPhone->magHorData(); // 将分离出是数据转成01表示的图像、这里可以根据自己喜好定
    $phone = $gjPhone->showPhone($horData); // 将转换好的01表示的数据与库中的数据进行匹配，匹配度95以上就算成功，库这里由于是做测试就直接写了数组
    echo '| ' . $phone . ' | ';
}
```

如此看来，其实12306验证码被破解也算是有情可原了，也没必要那么的口诛笔伐了罢。只要不断的抓验证码图片并转成自己程序可读的数据存入库里，然后验证的时候进行匹配就可以了。那么阿里的人脸识别支付原理也算是理解了，只不过他们做的可能会很精细。

前端时间有看到阿里云的一个验证码形式，刚开始感觉可能会好点，现在看来，只要有心，其实也是可以破解的啊。

[![ali_vcode](/images/2015/04/ali_vcode.jpg)](/images/2015/04/ali_vcode.jpg)  
好了，下面是原作代码。

```
/**
 * 电话号码识别.
 * @author by zsc for 2010.03.24
 */
class gjPhone
{

    protected $imgPath; // 图片路径
    protected $imgSize; // 图片大小
    protected $hecData; // 分离后数组
    protected $horData; // 横向整理的数据
    protected $verData; // 纵向整理的数据
    function __construct ($path)
    {
        $this->imgPath = $path;
    }

    /**
     * 颜色分离转换...
     *
     * @param unknown_type $path            
     * @return unknown
     */
    public function getHec ()
    {
        $size = getimagesize($this->imgPath);
        $res = imagecreatefrompng($this->imgPath);
        for ($i = 0; $i < $size[1]; ++ $i) {
            for ($j = 0; $j < $size[0]; ++ $j) {
                $rgb = imagecolorat($res, $j, $i);
                $rgbarray = imagecolorsforindex($res, $rgb);
                if ($rgbarray['red'] < 125 || $rgbarray['green'] < 125 ||
                         $rgbarray['blue'] < 125) {
                    $data[$i][$j] = 1;
                } else {
                    $data[$i][$j] = 0;
                }
            }
        }
        $this->imgSize = $size;
        $this->hecData = $data;
    }

    /**
     * 颜色分离后的数据横向整理...
     *
     * @return unknown
     */
    public function magHorData ()
    {
        $data = $this->hecData;
        $size = $this->imgSize;
        $z = 0;
        for ($i = 0; $i < $size[1]; ++ $i) {
            if (in_array('1', $data[$i])) {
                $z ++;
                for ($j = 0; $j < $size[0]; ++ $j) {
                    if ($data[$i][$j] == '1') {
                        $newdata[$z][$j] = 1;
                    } else {
                        $newdata[$z][$j] = 0;
                    }
                }
            }
        }
        return $this->horData = $newdata;
    }

    /**
     * 整理纵向数据...
     *
     * @return unknown
     */
    public function magVerData ($newdata)
    {
        for ($i = 0; $i < 132; ++ $i) {
            for ($j = 1; $j < 13; ++ $j) {
                $ndata[$i][$j] = $newdata[$j][$i];
            }
        }
        
        $sum = count($ndata);
        $c = 0;
        for ($a = 0; $a < $sum; $a ++) {
            $value = $ndata[$a];
            if (in_array(1, $value)) {
                $ndatas[$c] = $value;
                $c ++;
            } elseif (is_array($ndatas)) {
                $b = $c - 1;
                if (in_array(1, $ndatas[$b])) {
                    $ndatas[$c] = $value;
                    $c ++;
                }
            }
        }
        
        return $this->verData = $ndatas;
    }

    /**
     * 显示电话号码...
     *
     * @return unknown
     */
    public function showPhone ($ndatas)
    {
        $phone = null;
        $d = 0;
        foreach ($ndatas as $key => $val) {
            if (in_array(1, $val)) {
                foreach ($val as $k => $v) {
                    $ndArr[$d] .= $v;
                }
            }
            if (! in_array(1, $val)) {
                $d ++;
            }
        }
        foreach ($ndArr as $key01 => $val01) {
            $phone .= $this->initData($val01);
        }
        return $phone;
    }

    /**
     * 分离显示...
     *
     * @param unknown_type $dataArr            
     */
    function drawWH ($dataArr)
    {
        if (is_array($dataArr)) {
            foreach ($dataArr as $key => $val) {
                foreach ($val as $k => $v) {
                    if ($v == 0) {
                        $c .= "<font color='#FFFFFF'>" . $v . "</font>";
                    } else {
                        $c .= $v;
                    }
                }
                $c .= "<br/>";
            }
        }
        echo $c;
    }

    /**
     * 初始数据...
     *
     * @param unknown_type $numStr            
     * @return unknown
     */
    public function initData ($numStr)
    {
        $result = null;
        $data = array(
                0 => '000011111000001111111110011000000011110000000001110000000001110000000001110000000001011000000011011100000111000111111100000001110000',
                1 => '011000000000011000000000111111111111111111111111',
                2 => '001000000011011000000111110000001101110000011001110000011001110000110001111001100001011111100001000110000001',
                3 => '001000000010011000000011110000000001110000000001110000110001110000110001011001110011011111011111000110001100',
                4 => '000000001100000000111100000001111100000011101100000111001100001100001100011000001100111111111111111111111111000000001100000000000100',
                5 => '111111000001111111000001110001000001110001000001110001100001110001100001110000110011110000111111000000001100',
                6 => '000011111000001111111110011000110011110001100001110001100001110001100001110001100001010001110011010000111111000000001100',
                7 => '110000000000110000000111110000111111110001110000110111000000111100000000111000000000111000000000',
                8 => '000100011110011111111111110011100001110001100001110001100001110001100001110011100001011111111111000100011110',
                9 => '001111000000011111100001110000110001110000110001110000110001110000110001011000100001011111100111000111111110000001110000'
        );
        foreach ($data as $key => $val) {
            similar_text($numStr, $val, $pre);
            if ($pre > 95) { // 相似度95%以上
                $result = $key;
                break;
            }
        }
        return $result;
    }
}

$imgPath = "http://bj.ganji.com/tel/5463013757650d6c5e31093e563c51315b6c5c6c5237.png";
$gjPhone = new gjPhone($imgPath);
// 进行颜色分离
$gjPhone->getHec();
// 画出横向数据
$horData = $gjPhone->magHorData();
echo "===============横向数据==============<br/><br/><br/>";
$gjPhone->drawWH($horData);
// 画出纵向数据
$verData = $gjPhone->magVerData($horData);
echo "<br/><br/><br/>===============纵向数据==============< br/><br/><br/>";
$gjPhone->drawWH($verData);

// 输出电话
$phone = $gjPhone->showPhone($verData);
echo "<br/><br/><br/>===============电话==============<br /><br/><br/>" . $phone;
```
