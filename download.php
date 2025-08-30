<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Download</title>
<link rel="icon" href="/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="/favicon.ico" />
<link type="text/css" rel="stylesheet" href="/download/css/fancybox.css">
<link type="text/css" rel="stylesheet" href="/download/css/m_fancybox.css">
<script src="/download/js/jquery-3.6.0.min.js"></script>
<script src="/download/js/fancybox.umd.js"></script>
<style>
body{background:#ececec;background-image:url(/download/images/bg_body.png)}
.head{background:#d1d7e3;font-size:22px;margin:5px 0;padding:5px;font-family:MONOSPACE}
.myButton{box-shadow:inset 0 1px 0 0 #fff;background:linear-gradient(to bottom,#edf3e8 5%,#d1f5bc 100%);background-color:#cdffa4;border-radius:5px;border:1px solid #828282;display:inline-block;cursor:pointer;color:#565656;font-family:Arial;font-size:14px;font-weight:bold;padding:3px 4px;text-shadow:0 1px 0 #fff}
.myButton:hover{background:linear-gradient(to bottom,#cdffa4 5%,#a9fb79 100%);background-color:#d1f5bc}
.myButton:active{position:relative;top:1px}
p.myText{font-size:17px;font-weight:bold;font-family:sans-serif;color:#ff4138}
</style>
</head>
<body>
<div style="text-align: center">
<div class="head"><b>Download programs</b></div>
<?php
 $path = $_SERVER['DOCUMENT_ROOT'].'/storage/';
 if($open = scandir($path)) {
  $result=array();
  for($i = 0; $i < count($open); $i++) {
   if(is_dir($path.$open[$i])) continue;
    $result[] = $open[$i];
   }
 }
  $cn=0;
  $ap=file("./files/price");
  foreach($ap as $str) {
	$list=array();
	$temp=array();
	$img=array();
    foreach($result as $k => $v) {
     if(preg_split("/\.[^.]+$/",$v)[0]==explode("~",$str)[0]) {
	   preg_match('/[^.]*$/',$v,$f);
	   if($f[0]=='gif'||$f[0]=='jpg'||$f[0]=='png'||$f[0]=='GIF'||$f[0]=='JPG'||$f[0]=='PNG') {
        $temp[] = [
         'name' => $v,
         'time' => filemtime($path.$v),
        ];
	   }
	   if($f[0]=='zip'||$f[0]=='txt'||$f[0]=='ex4'||$f[0]=='ex5') {
		$list[$k] = array($v,$f[0]);
	   }
     }
	}
    usort($temp, function($a, $b){ return $a['time'] - $b['time']; });
    $img = array_column($temp,'name');
	$cList=count($list);
	$cImg=count($img);
	//--
	if($cList || $cImg)
	 echo '<div style="font-size:22px;font-weight:bold;color:#007dd5;font-family:sans-serif;margin:10px 0 7px">'.trim(explode("~", $str)[0]).'</div>';
	//--
	$cn++;
    if($cImg) {
       echo '<div class="BlockCarousel">
             <div id="mainCarousel_'.$cn.'" class="mainCarousel carousel">';
       foreach($img as $v) {
         echo '<div class="carousel__slide" data-src="/storage/'.$v.'" data-fancybox="gallery_'.$cn.'" data-caption="'.preg_split("/\.[^.]+$/",$v)[0].'"><img src="/storage/'.$v.'" alt="'.$v.'" /></div>';
       }
       echo '</div>
	         <div id="thumbCarousel_'.$cn.'" class="thumbCarousel carousel mx-auto">';
       foreach($img as $v) {
         echo '<div class="carousel__slide"><img class="panzoom__content" src="/storage/'.$v.'" alt="'.preg_split("/\.[^.]+$/",$v)[0].'" /></div>';
       }
       echo '</div>
	         </div>';
     }
    //--
    foreach($list as $v) {
	   if($v[1]=='zip') {
		  echo '<form action="/storage/files/?file='.$v[0].'" method="post">';
           echo '<p class="myText">Settings: <button class="myButton" title="Download">'.$v[0].'</button></p>';
          echo '</form>';
	   }
    }
    //--
    foreach($list as $v) {
	   if($v[1]=='txt') {
		  echo '<form action="/storage/files/?file='.$v[0].'" method="post">';
           echo '<p class="myText">Description: <button class="myButton" title="Download">'.$v[0].'</button></p>';
          echo '</form>';
	   }
	}
    //--
    foreach($list as $v) {
	   if($v[1]=='ex4' || $v[1]=='ex5') {
		  echo '<form action="/storage/files/?file='.$v[0].'" method="post">';
           echo '<p class="myText">MetaTrader '.substr($v[1],2).': <button class="myButton" title="Download">'.$v[0].'</button></p>';
          echo '</form>';
	   }
    }
    //--
    if($cList || $cImg) {
	    $parts = explode("~", $str);
	    if(isset($parts[2]) && trim($parts[2])!='') {
		 echo '<a href="'.trim($parts[2]).'" target="_blank"><img src="/storage/files/buy.gif" alt="Buy '.trim($parts[0]).'" title="'.trim($parts[0]).'" /></a>';
	    }
	    if(isset($parts[1]) && trim($parts[1])!='') {
	     echo '<div style="font-size:24px;font-weight:bold;color:#696cb9;font-family:sans-serif;margin-top:-18px;padding-left:14px"><span>'.trim($parts[1]).'</span> <span style="font-size:18px">USD</span></div>';
	    }
	  echo '<div style="border-bottom:5px dotted #cdcdcd;margin:20px 15px"></div>';
    }
  }
?>
</div>
<div class="head" style="text-align:center;font-size:20px;color:#0b00b9;">
<?php
$email=file_get_contents("./files/mail");
if($email!="") echo '<span id="ml"></span>';
?>
</div>
<script>
$(function() {
function StartCarousel(param){
const mainCarousel = new Carousel(document.querySelector("#mainCarousel_"+param), {
  Dots: false,
});
const thumbCarousel = new Carousel(document.querySelector("#thumbCarousel_"+param), {
 Dots: false,
  Sync: {
    target: mainCarousel,
    friction: 0,
  },
  Navigation: false,
  center: true,
  slidesPerPage: 1,
  infinite: false,
});
Fancybox.bind('[data-fancybox="gallery_'+param+'"]', {
  Toolbar: false,
  closeButton: "top",
  Carousel: {
    on: {
      change: (that) => {
        mainCarousel.slideTo(mainCarousel.findPageForSlide(that.page), {
          friction: 0,
        });
      },
    },
  },
});
}
//--
var count = $('.BlockCarousel').length;
 for(c=1;c<=count;c++) {
  StartCarousel(c);
 }
//--
 $('#ml').html('Contact E-mail: <span style="color:#003469"><?=$email?></span>');
});
</script>
</body>
</html>