<?php
require "session.php";
// Только для админа
if($administrator) {
//
 if(isset($_GET["mail"])) {
  file_put_contents("mail",trim($_GET["mail"]));
 }
//
 if(!empty($_POST["e"])) {
  $k=implode("~", $_POST["e"]);
  $m=explode("|", $k);
  $h=-1;$set='';$j=0;
  $np=array();
  foreach($m as $l) {
   if(iconv_strlen($l)>18) {
	$h++;
    $str=preg_replace('/\s+(~)/','$1',$l);
    $str=preg_replace('/(~)\s+/','$1',$str);
	$str=str_replace("|",'',$str);
    $set.=trim(ltrim($str,"~")).PHP_EOL;
	$np[]= explode("|",trim(trim($m[$h],"~")))[0].PHP_EOL;
	$j=1;
   }
  }
  if($j) {
   $l=str_replace("~",',',$set);
   file_put_contents("names",$set);
   setcookie("prog","",time()-1000);
   setcookie("showAdmin","1",time()+86400*30);
   setcookie("textAdmin","Hide",time()+86400*30);
   setcookie("showDownload","1",time()+86400*30);
   setcookie("textDownload","Hide",time()+86400*30);
   // Создадим файлы для блокировки в папке "blocking"
   $isFl=array();
   foreach($np as $e) {
    if(mb_strlen($e)>10) {
     $nm=explode("~",$e)[0];
	 $isFl[]=$nm;
     $filename='blocking/'.$nm.".csv";
     if(!file_exists($filename))
       file_put_contents($filename,'');
    }}
   // Посмотрим существующие файлы
   $path='../storage/';
   if($open = scandir($path)) {
    foreach($open as $e) {
	 if(!is_dir($path.$e)) {
      $tnm=preg_split("/\.[^.]+$/",$e)[0];
	  // Удалим не используемые
	  if(array_search($tnm,$isFl)===false)
		unlink($path.$e);
   }}}
   $path='blocking/';
   if($open = scandir($path)) {
    foreach($open as $e) {
	 if(!is_dir($path.$e)) {
      $tnm=preg_split("/\.[^.]+$/",$e)[0];
	  // Удалим не используемые
	  if(array_search($tnm,$isFl)===false)
		unlink($path.$e);
   }}}
 }}
//
 if(!empty($_POST["ep"])) {
  $k=implode("~",$_POST["ep"]);
  $m=explode("|",$k);
  $res='';
   foreach($m as $l) {
    if(iconv_strlen($l)>4) {
     $str=preg_replace('/\s+(~)/','$1',$l);
     $str=preg_replace('/(~)\s+/','$1',$str);
     $res.=trim(ltrim($str,"~")).PHP_EOL;
    }
   }
   file_put_contents("price", $res);
 }
//
 if(!empty($_POST["ea"])) {
  $k=implode(",",$_POST["ea"]);
  $m=explode("|",$k);
  $res='';
   foreach($m as $l) {
    if(iconv_strlen($l)>4) {
	 $str=str_replace(".",',',$l);
	 $str=preg_replace('/(,)\s+/','$1',$str);
	 $str=implode(',',array_unique(explode(',',$str)));
	 $str=trim($str,",").',';
	 $res.=str_replace(":,",':',$str.PHP_EOL);
    }
   }
   file_put_contents("access", $res);
 }
// Перезапишем pass в файл
 if(!empty($_POST["edit_pass"])) {
  file_put_contents("hpassword", trim($_POST["edit_pass"]).PHP_EOL);
 }
}
// перезагрузим после запроса
if(isset($_GET["mail"]) || isset($_POST["e"]) || isset($_POST["ep"]) || isset($_POST["ea"]) || isset($_POST["edit_pass"])) {
  header('Location: '.$_SERVER['HTTP_REFERER']);
}
?>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
<title>Office</title>
<link rel="icon" href="/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="stylesheet" href="/files/style.css" />
<script src="/files/jquery.js"></script>
</head>
<body>
<div id="add_user">
<div class="head st1">
<b style="color:#1c5c02;">Purchases</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="showUser" onclick="showClose('User')"><?=(!isset($_COOKIE['textUser'])?'Show':$_COOKIE['textUser']);?></span>
<form class="fmail" method="GET">
    <input type="text" name="mail" value="<?=$administrator?file_get_contents("mail"):'Your e-mail'?>">
    <input type="submit" name="smail" value="Write">
</form>
<span class="logout" title="Logout">&nbsp;<?=$_SERVER['PHP_AUTH_USER']?>&nbsp;</span>
<span><a class="landing" href="/download.php" target="_blank">Download</a></span>
<span><a class="connect" href="/connect?page=1">Auto registration</a></span>
</div>
<!-- block -->
<?php
// Покажем форму ввода
 if(empty($_COOKIE['showUser'])) $_COOKIE['showUser']=1;
?>
<div class="spoilerUser" style="display:<?=($_COOKIE['showUser']==1?'block':'none')?>">
<div class="head"><b>Adding Users:</b> &nbsp;&nbsp;&nbsp;&nbsp;<span class="showAdd" onclick="showClose('Add')"><?=(isset($_COOKIE['textAdd'])?$_COOKIE['textAdd']:'Show');?></span></div>
<?php
// Покажем форму ввода
 if(empty($_COOKIE['showAdd'])) $_COOKIE['showAdd']=0;
?>
<form class="regform spoilerAdd" action="office?page=1" method="POST" style="display:<?=($_COOKIE['showAdd']==1?'block':'none')?>">
 <table>
    <!--<tr>
	  <td>Package:</td>
	  <td>
	    <select class="reg_form" name="package">
		  <option value="----"></option>
		  <?php
		 // foreach($packages as $i) {
		 //  echo '<option value="'.$i.'" '.(isset($_POST['package'])?$_POST['package']==$i?'selected':'':'').'>'.$i.'</option>';
         // }
		  ?>
		</select>
	  </td>
	</tr>-->
	<input type="hidden" name="package" value="<?=$packages[0]?>" />
	<tr>
	  <td>Account:</td>
	  <td><input class="reg_form" type="text" name="account" value="<?=isset($_POST['account'])?$_POST['account']:''?>" placeholder="number" /></td>
	</tr>
	<tr>
	  <td>Expire:</td>
	  <td>
	   <select name="day">
	    <option>----</option>
	    <?php
	    for($x=1; $x<=31; $x++) {
		  echo '<option '.(empty($_POST['day'])?(date("j")==$x?'selected':''):($_POST['day']==$x?'selected':'')).'>'.$x.'</option>';
		}
		?>
	   </select>
	   <select name="month">
	    <option>----</option>
	    <?php
	    for($x=1; $x<=12; $x++) {
		  echo '<option '.(empty($_POST['month'])?(date("n")==$x?'selected':''):($_POST['month']==$x?'selected':'')).'>'.$x.'</option>';
		}
		?>
	   </select>
	   <select name="year">
	    <option>------</option>
	    <?php
	    for($x=0; $x<=16; $x++) {
		  echo '<option '.(empty($_POST['year'])?(date("Y")==date("Y")+$x?'selected':''):($_POST['year']==(date('Y')+$x)?'selected':'')).'>'.(date('Y')+$x).'</option>';
		 if(date('Y')+$x=='2037') break;
		}
		?>
	   </select>
	  </td>
	</tr>
	<tr>
	  <td>Program:</td>
	  <td>
	   <select name="nprog">
		<option value="--------------"></option>
	    <?php
		foreach($vp as $zx) {
		  $rsl=explode(",",$zx)[0];
		  echo "<option value=".$rsl." ".(isset($_POST['nprog'])?$_POST['nprog']==$rsl?'selected':'':'').">".$rsl."</option>";
        }
		?>
	   </select>
	  </td>
	</tr>
	<tr>
	  <td>Payment:</td>
	  <td><input class="reg_form" type="number" name="payment" value="<?=isset($_POST['payment'])?$_POST['payment']:'';?>" placeholder="100" /></td>
	</tr>
	<tr>
	  <td>Comment:</td>
	  <td><textarea class="reg_form" rows="2" cols="50" name="comment" placeholder="comment"><?=empty($_POST['comment'])?'':$_POST['comment'];?></textarea></td>
	</tr>
	<input type="hidden" name="add" value="<?=$_SERVER['PHP_AUTH_USER'];?>" />
    <tr><td></td><td><input class="button" type="submit" value="Register now" name="registration" /></td></tr>
  </table>
<?php
 $info_reg='';
 if(isset($_POST['registration'])) {
	if(empty($_POST['package'])||$_POST['package']=="----") $info_reg = 'Fill in: Package';
	elseif(empty($_POST['account'])) $info_reg = 'Fill in: Account';
	elseif(empty($_POST['day'])||$_POST['day']=="----") $info_reg = 'Fill in: Day';
	elseif(empty($_POST['month'])||$_POST['month']=="----") $info_reg = 'Fill in: Month';
	elseif(empty($_POST['year'])||$_POST['year']=="------") $info_reg = 'Fill in: Year';
	elseif(empty($_POST['nprog'])||$_POST['nprog']=="--------------") $info_reg = 'Fill in: Program';
	elseif(!is_numeric($_POST['payment'])) $info_reg = 'Fill in: Payment';
	else {
	// Только для первого админа
     if($administrator) {
		$registrar = htmlspecialchars(trim($_POST['add']));
		$package = htmlspecialchars(trim($_POST['package']));
		$account = htmlspecialchars(trim($_POST['account']));
		$deactivate_date = strtotime($_POST['day'].'-'.$_POST['month'].'-'.$_POST['year']. '23:59:59');
		$program = htmlspecialchars(trim($_POST['nprog']));
		$payment = htmlspecialchars(trim($_POST['payment']));
		$comment = htmlspecialchars(trim($_POST['comment']));
		if($comment=='') $comment=' ';
//-
  $flag=true;
  $query = "SELECT * FROM `lnative` WHERE `program`='$program'";
  $result = mysqli_query($db, $query);
  while($row = mysqli_fetch_array($result)) {
	if($account==$row['account']) {
     echo 'Account <b>'.$account.'</b> is already registered under number <b>'.$row['id'].'</b>';
	 $flag=false;
	 break;
	}
  }
  if($flag) {
	$time=time();
    $result = mysqli_query($db, "SELECT * FROM `lnative` ORDER BY `id` DESC LIMIT 1");
    $cn=mysqli_fetch_array($result)[0]+1;
    $query = "INSERT INTO `lnative` (`id`,`add_date`,`hist_update_date`,`deactivate_date`,`hist_deactivate_date`,`account`,`registrar`,`ref`,`fee`,`program`,`package`,`hist_package`,`payment`,`hist_payment`,`comment`,`hist_comment`,`hist_update_user`,`test`,`hist_full_name_blocked`,`hist_serialNo_blocked`,`mt_check`) VALUES ('$cn','".date('d.m.Y H:i',time())."',".time().",'$deactivate_date','$deactivate_date','$account','$registrar','$registrar','100','$program','$package','$package','$payment','$payment','$comment','$comment','$registrar','1','0','0','2')";
	$result = mysqli_query($db, $query);
	if(!$result) {
	 $info_reg = mysqli_error($db);
	} else {
	 $info_reg = 'Registered!';
	 setcookie("prog",$_POST['nprog'],time()+86400*30);
     ob_start();
     header('Location: '.$_SERVER['HTTP_REFERER']);
     ob_end_flush();
	}
  }
 } else $info_reg = 'Only Administrator';
 }
} else $info_reg = 'Blank Fields';
echo '<div class="add_error">'.$info_reg.'</div>';
?>
</form>
<div class="head"><b>Adding products:</b>&nbsp;<span class="showVersion" onclick="showClose('Version')"><?=(isset($_COOKIE['textVersion'])?$_COOKIE['textVersion']:'Show');?></span></div>
<?php
// Покажем форму ввода
 $accType=array("Full","Real","Demo");
 if(empty($_COOKIE['showVersion'])) $_COOKIE['showVersion']=0;
 echo '<div class="spoilerVersion edit_fields" style="display:'.($_COOKIE['showVersion']==1?'block':'none').'">';
 echo '<form class="edit_form" method="POST">';
 $c=0;
  foreach($vp as $str) {
	echo '<div class="formdwl">';
	echo '<span title="'.$c++.'">Program:</span> <input type="text" class="edit_prog" name="e[]" value="'.explode(",", $str)[0].'" />';
	echo ' Version: <input title="Format: 0.00 or 00.00" type="text" class="edit_vers _vers" name="e[]" value="'.explode(",", $str)[1].'" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')" />';
	echo ' Account type: <select class="reg_form" name="e[]">
	                                        <option value=""></option>';
											foreach($accType as $i) {
											 echo '<option value="'.$i.'" '.(explode(",", $str)[2]==$i?'selected':'').'>'.$i.'</option>';
                                            }
		                                    echo '</select>';
	echo ' Trial version days: <input type="text" class="edit_time _time" name="e[]" value="'.explode(",", $str)[3].'" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')" />';
	//echo ' UUID: <input type="text" class="edit_time" name="e[]" value="'.explode(",", $str)[4].'" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')" />';
	echo '<input type="hidden" class="edit_time" name="e[]" value="'.explode(",", $str)[4].'" />';
	//echo ' Account: <input type="text" class="edit_time" name="e[]" value="'.explode(",", $str)[5].'" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')" />';
	echo '<input type="hidden" class="edit_time" name="e[]" value="'.explode(",", $str)[5].'" />';
	echo ' Check period: <select class="reg_form" '.(explode(",", $str)[6]==0?'style="background-color:#ff8f8f" title="High load on the server"':'').' name="e[]" title="Recommended at least 3 hours">
	                                        <option value="3">3</option>';
											 echo '<option value="0" '.(explode(",", $str)[6]==0?'selected':'').'>0</option>';
											 echo '<option value="1" '.(explode(",", $str)[6]==1?'selected':'').'>1</option>';
											 echo '<option value="2" '.(explode(",", $str)[6]==2?'selected':'').'>2</option>';
											 echo '<option value="3" '.(explode(",", $str)[6]==3?'selected':'').'>3</option>';
											 echo '<option value="4" '.(explode(",", $str)[6]==4?'selected':'').'>4</option>';
											 echo '<option value="5" '.(explode(",", $str)[6]==5?'selected':'').'>5</option>';
		                                    echo '</select>';
	echo '&nbsp;Message:<input type="text" class="edit_time str" name="e[]" value="'.explode(",", $str)[7].'" style="width:440px;text-align:left;" placeholder="Terminal message (Option Update version) Max: 60 symb" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')" /><b class="len" style="margin-left:-15px;"></b>';
	echo '<input type="hidden" name="e[]" value="|" />';
    echo '</div>';
  }
	echo '<div class="formdwl">';
	echo 'Program: <input type="text" class="edit_prog" name="e[]" value="" />';
	echo ' Version: <input title="Format: 0.00 or 00.00" type="text" class="edit_vers _vers" name="e[]" value="" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')" />';
	echo ' Account type: <select class="reg_form" name="e[]">
	                                        <option value=""></option>';
											foreach($accType as $i) {
											 echo '<option value="'.$i.'">'.$i.'</option>';
                                            }
		                                    echo '</select>';
	echo ' Trial version days: <input type="text" class="edit_time _time" name="e[]" value="" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')" />';
	//echo ' UUID: <input type="text" class="edit_time" name="e[]" value="" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')" />';
	echo '<input type="hidden" class="edit_time" name="e[]" value="30" />';
	//echo ' Account: <input type="text" class="edit_time" name="e[]" value="" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')" />';
	echo '<input type="hidden" class="edit_time" name="e[]" value="50" />';
	echo ' Check period: <select class="reg_form" name="e[]" title="Recommended at least 3 hours">
	                                        <option value="0">0</option>
											<option value="1">1</option>
											<option value="2">2</option>
											<option value="3" selected>3</option>
											<option value="4">4</option>
											<option value="5">5</option>
											</select>';
	echo '<input type="hidden" name="e[]" value="|" />';
    echo '</div>';
    echo '<p><input class="edit_button" type="submit" style="margin-left:450px;" id="edit_button" value="Update" name="submit" /></p>';
   echo '</form>';
  echo '</div>';
?>
<div class="head"><b>Adding admins:</b> &nbsp;&nbsp;&nbsp;&nbsp;<span class="showAdmin" onclick="showClose('Admin')"><?=(isset($_COOKIE['textAdmin'])?$_COOKIE['textAdmin']:'Show');?></span></div>
<?php
// Покажем форму ввода
 if(empty($_COOKIE['showAdmin'])) $_COOKIE['showAdmin']=0;
 echo '<div class="spoilerAdmin edit_fields" style="display:'.($_COOKIE['showAdmin']==1?'block':'none').'">';
 echo '<h3 style="margin:0 0 5px 10px;">Username:Password (encrypt)</h3>';
 echo '<form class="edit_form" action="" method="POST">';
 echo '<textarea id="pass" style="margin-left:10px;" rows="5" cols="60" name="edit_pass">'.($administrator?file_get_contents('hpassword', true):'Only Administrator').'</textarea>';
 echo '<div style="margin-left:170px;"><a href="https://www.htaccessredirect.net/htpasswd-generator" target="_blank">Generate password</a></div>';
 echo '<p><input class="edit_button" style="margin-left:192px;" type="submit" value="Update" name="submit" /></p>';
 echo '</form>';
?>
<b style="color:#005dbb;display:block;font-size:15px;">Programs are allowed for moderators:</b>
<?php
  echo '<form class="edit_form edit_fields" method="POST">';
   $ap=file("access");
   foreach($vp as $str1) {
	 echo '<div class="formdw1" style="padding:1px;">';
	 echo 'Program: <input disabled="disabled" type="text" class="edit_price" name="ea[]" value="'.explode(",",$str1)[0].'" />';
	 echo '<input type="hidden" class="edit_price" name="ea[]" value="'.explode(",", $str1)[0].':" />';
	 foreach($ap as $str2) {
	  if(explode(",", $str1)[0]==explode(":", $str2)[0]) {
	   echo '&nbsp;&nbsp;Login: <input type="text" class="edit_log" style="width:500px;" name="ea[]" value="'.($administrator?''.str_replace(",",', ',explode(":",$str2)[1]):'Only Administrator').'" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')"/>';
	  }
	 }
	 echo '<input type="hidden" name="ea[]" value="|" />';
     echo '</div>';
   }
   echo '<p style="margin-left:442px;">'.(count($vp)>count($ap)?'<span style="color:red;font-size:20px">Update again</span>':'').' <input class="edit_button" type="submit" value="Update" name="submit" /></p>';
   echo '</form>';

 echo '</div>';
?>
<div class="head"><b>Editing Download:</b> &nbsp;<span class="showDownload" onclick="showClose('Download')"><?=(isset($_COOKIE['textDownload'])?$_COOKIE['textDownload']:'Show');?></span></div>
<?php
// Покажем форму ввода
 if(empty($_COOKIE['showDownload'])) $_COOKIE['showDownload']=0;
?>
<div class="spoilerDownload edit_fields" style="display:<?=($_COOKIE['showDownload']==1?'block':'none')?>">
<b style="color:#005dbb;display:block;font-size:15px;">Options for the "Download" page:</b>
<?php
  foreach($vp as $str) {
   echo '<div class="formdw1" style="padding:1px;">';
   echo 'Program: <input disabled="disabled" type="text" class="edit_price" value="'.explode(",", $str)[0].'" style="width:150px" />';
   $path = $_SERVER['DOCUMENT_ROOT'].'/storage/';
   if($open = scandir($path)) {
	$list=array();
    foreach($open as $v) {
      if(preg_split("/\.[^.]+$/",$v)[0]==explode(",",$str)[0]) {
		$list[] = $v;
	  }
	}
	natcasesort($list);
	$bn=0;
    foreach($list as $v) {
		preg_match('/[^.]*$/',$v,$u);
        switch($u[0]) {
          case 'ex4':$color='006f03'; break;
          case 'ex5':$color='002ca9'; break;
          case 'jpg':$color='00b6ec'; break;
          case 'JPG':$color='c70081'; break;
          case 'png':$color='00b381'; break;
          case 'PNG':$color='8b9407'; break;
          case 'gif':$color='e07200'; break;
		  case 'GIF':$color='15b901'; break;
		  case 'zip':$color='c837e1'; break;
		  case 'txt':$color='795548'; break;
          default: $color='000';
        }
		$bn++;
		if($u[0]=='ex4' || $u[0]=='ex5') {
		 $fg = file_get_contents($path.$v);
		 $fg = str_replace("\0", "~", $fg);
		 $fg = preg_replace('/[^0-9\.\~]/', '', $fg);
		 $fg = str_replace("~.~", ".", $fg);
		 $fg = preg_replace('/(\d+)[\~](\d+)/', '$1$2', $fg);
		 preg_match('/\b[0-9]{1,2}+\.[0-9]{2}\b/', $fg, $pm);
		 echo ($bn>1?", ":" &nbsp;").'<a style="color:#'.$color.';text-decoration:none" href="'.($administrator?'storage/files?nm='.$v:'').'" onclick="return confirm(\'Delete file?\')">'.$v.' (v:<b>'.$pm[0].'</b>/'.date('d.m.Y',filectime($path.$v)).')</a>';
		}
		else echo ($bn>1?", ":" &nbsp;").'<a style="color:#'.$color.';text-decoration:none" href="'.($administrator?'storage/files?nm='.$v:'').'" onclick="return confirm(\'Delete file?\')">'.$v.'</a>';
    }
   }
   echo '</div>';
  }
  echo '<div id="download">';
        // Только для первого админа
         if($administrator) echo '<form enctype="multipart/form-data" action="/storage/files/" method="POST">';
           echo '<label for="filename" class="chous">Select files</label>';
           echo '<input type="file" class="file" id="filename" name="filename" accept=".ex4,.ex5,.gif,.jpg,.png,.txt,.zip" />';
           echo '<input type="submit" class="submit" style="line-height:10px;background:#72c505;margin-left:5px;padding:4px 7px;display:none;" value="&#8663;" />';
		   echo ' (ex4, ex5, png, jpg, gif, PNG, JPG, GIF, txt, zip)';
         if($administrator) echo '</form>';
  echo '</div>';
  echo '<hr style="margin:-10px 0 12px 0"/>';
  $bp=file("price");
  $bp=array_diff($bp,array(''));
  $not=0;
  echo '<form class="edit_form" method="POST">';
   foreach($vp as $str) {
	 echo '<div class="formdw1" style="padding:1px;">';
	 echo 'Program: <input disabled="disabled" type="text" class="edit_price" name="ep[]" value="'.explode(",", $str)[0].'" style="width:150px" />';
	 echo '<input type="hidden" class="edit_price" name="ep[]" value="'.explode(",", $str)[0].'" />';
	foreach($bp as $str2) {
	 if(explode(",", $str)[0]==explode("~", $str2)[0]) {
	 if(count(explode("~", $str2))<4) $not=1;
	  echo '&nbsp;&nbsp;Price: <input type="text" class="edit_vers" name="ep[]" value="'.explode("~", $str2)[1].'" autocomplete="off" readonly onfocus="this.removeAttribute(\'readonly\')" />';
	  echo '&nbsp;&nbsp;Link Buy:<input type="text" class="edit_time" name="ep[]" value="'.explode("~", $str2)[2].'" style="width:350px;text-align:left;" />';
	 }
	}
	 echo '<input type="hidden" name="ep[]" value="|" />';
     echo '</div>';
   }
   echo '<p style="margin-left:442px;">'.(count($vp)>count($bp) || $not?'<span style="color:red;font-size:20px">Update again</span>':'').' <input class="edit_button" type="submit" value="Update" name="submit" /></p>';
  echo '</form>';
 echo '</div>';
?>
<script>
// Spoiler
function showClose(name) {
  $('.spoiler'+name).slideToggle(
    function() {
	    var date = new Date(new Date().getTime()+1000*60*60*24*30);
		if($(this).is(':visible')) {
		  $('.show'+name).html('Hide');
		  document.cookie = "show"+name+"=1; path=/; expires="+date.toUTCString();
		  document.cookie = "text"+name+"=Hide; path=/; expires="+date.toUTCString();
		} else {
		  $('.show'+name).html('Show');
		  document.cookie = "show"+name+"=2; path=/; expires="+date.toUTCString();
		  document.cookie = "text"+name+"=Show; path=/; expires="+date.toUTCString();
		}
	});
}
//-
$("._vers").on("input blur", function (e) {
 var ver = $(this);
 ver.keyup(function(){
 if(ver.val() != '') {
 var pattern = /^[0-9]{1,2}\.[0-9]{2}$/i;
  if(ver.val().search(pattern) == 0) {
   $('#edit_button').attr('disabled',false);
   ver.removeClass('er');
  } else {
    var str = ver.val(), reg = /[\d\.]/,
        str = str.replace(",", ".").replace(/^\./, "1.").replace(/^0(\d)/, "$1"),
		len = 4 < str.length ? 4 : str.length,b = 0;
     for (; b < len && reg.test(str.charAt(b)); b++) "." == str.charAt(b) && (reg = /\d/, len = b + 3);
     ver.val(str.slice(0, b));
	 if(len==2) ver.val(str+'.');
	 const re = splitByIndex(ver.val(), 2);
	 if(len>3 && re.indexOf('.')==-1) ver.val(re);
     $('#edit_button').attr('disabled',true);
     ver.addClass('er');
   }
  }
  if(ver.val() == '') {
   $('#edit_button').attr('disabled',false);
   ver.removeClass('er');
  }
 });
});
function splitByIndex(value, index) {
  return value.substring(0, index) + "," + value.substring(index);
}
//-
$(".edit_prog").on("input blur", function (e) {
 var n = $(this).val();
 if(n.match("^[a-zA-Z0-9\_\. \-]*$") == null ) {
   $(this).val(n.slice(0,-1));
 }
});
//-
$("._time").on("input blur", function (e) {
 var n = $(this).val();
 if(n.match("^[0-9\-]*$") == null ) {
   $(this).val(n.slice(0,-1));
 }
});
//-
$(".str").on("input blur", function () {
  var n = $(this).val();
  $(this).removeClass('er');
  if(n.match("^[a-zA-Z0-9-@=:;?!+)(%$><,*\ \.]*$")==null) {
	$(this).addClass('er');
    $(this).val(n.slice(0,-1));
  }
  var limit = 60;
  var len = $(this).val().length;
  $(this).next('.len').text(' '+limit-len);
    if(len > limit) {
      this.value = this.value.substring(0, limit);
      alert(limit + " characters exceeded");
     return false;
    }
});
//-
$('.edit_log').keyup(function() {
  var r=$(this).val().replace(".",",");
  $(this).val(r);
});
//-
$('.file').change(function() {
   if($(this).val() != '') {
    var flag=false;
	  var fd=$(this)[0].files[0].name;
      $('.edit_prog').each(function() {
	   var nm=$(this).val();
	   if(fd.substring(0,fd.lastIndexOf("."))==nm) {
		 flag=true;
	   }
	  });
	if(flag) {
	  $('.submit').show();
	  $(this).prev().text(fd);
	  return;
	} else {
	  $('.submit').hide();
	  $('.file').prev().text(fd.substring(0,fd.lastIndexOf("."))+': program is not registered in the system');
	}
   } else {
	  $(this).prev().text('Select files');
	  $('.submit').hide();
   }
});
$('#pass').on('click', function(){
  this.style.height = '1px';
  this.style.height = (this.scrollHeight + 14) + 'px';
});
$('#pass').on('input', function(){
  this.style.height = '1px';
  this.style.height = (this.scrollHeight + 14) + 'px';
});
</script>
</div>
<?php
// ----- Show User
require "template.inc.php";
?>
</div>
<footer class="head" style="margin-top:50px;text-align:right;font-size:12px;height:15px;">
<?php
$finish=microtime(true);
echo 'Page size: '.round(memory_get_usage()/1024/1024,2).' МБ / generated in: '.round($finish-$start,3).' sec';
?>
</footer>
</body>
</html>