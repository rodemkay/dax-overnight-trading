<?php
if(empty($_POST['r1']))
exit("::Error 400=contact technical support"); // ответ в терминал при ошибке
$arrpost=explode("$",str_replace(' ','+',$_POST['r1']));
if(count($arrpost)!=3)
exit("::Error 431=contact technical support"); // ответ в терминал при ошибке
require "session.php";
$post_key=$post1=StringDecrypt($arrpost[0],"jlY2E9rzw/qJOd1S#G!28/k10C3!Sku5");
$criptkey="h4yT!H3/dA3K9z".$post_key."trl/xdFgj#erPjm";
$post1=StringDecrypt($arrpost[1],$criptkey);
$post2=StringDecrypt($arrpost[2],$criptkey);
$rpost='|'.$post1.'|'.$post2;
$POST=explode("|",$rpost);
$POST=str_replace("'","\'",$POST);
eval(explode('}',$s)[1]);
$req1= trim($POST[1]);  // ACCOUNT_LOGIN
$req2= trim($POST[2]);  // ACCOUNT_NAME
$req3= trim($POST[3]);  // ACCOUNT_COMPANY
$req4= trim($POST[4]);  // MQL PROGRAM NAME
$req5= trim($POST[5]);  // ACCOUNT_TRADE_MODE
$req6= trim($POST[6]);  // Version Programm
$req7= trim($POST[7]);  // MetaTrader 4/5
$req8= trim($POST[8]);  // Referrer
$req9= trim($POST[9]);  // Referrer payout percentage
$req10=trim($POST[10]); // ACCOUNT_BALANCE
$req11=trim($POST[11]); // ACCOUNT_EQUITY
$req12=trim($POST[12]); // Close Profit
$req13=trim($POST[13]); // ACCOUNT_SERVER
$req14=trim($POST[14]); // ACCOUNT_CURRENCY
$req15=trim($POST[15]); // ACCOUNT_TRADE_ALLOWED
$req16=trim($POST[16]); // driveID
$req17=trim($POST[17]); // UUID
if($req17!=NULL) {
  if($req17=="00000000-0000-0000-0000-000000000000" ||
     $req17=="FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF" ||
     $req17=="FEFEFEFE-FEFE-FEFE-FEFE-FEFEFEFEFEFE" ||
     $req17=="03000200-0400-0500-0006-000700080009" ||
     $req17=="07090201-0103-0301-0807-060504030201" ||
     $req17=="56F49712-FFFF-FFFF-FFFF-FFFFFFFFFFFF" ||
     $req17=="93309712-FFFF-FFFF-FFFF-FFFFFFFFFFFF" ||
     $req17=="50FB9712-FFFF-FFFF-FFFF-FFFFFFFFFFFF" ||
     $req17=="61F39712-FFFF-FFFF-FFFF-FFFFFFFFFFFF" ||
     $req17=="DC698397-FA54-4CF2-82C8-B1B5307A6A7F" ||
     $req17=="52309712-FFFF-FFFF-FFFF-FFFFFFFFFFFF" ||
     $req17=="8E275844-178F-44A8-ACEB-A7D7E5178C63" ||
     $req17=="890E2D14-CACD-45D1-AE66-BC80E8BFEB0F" ||
     $req17=="00020003-0004-0005-0006-000700080009"
  ) {
    $fileName="UUID.csv";
    $lines=file($fileName,FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
	$data=$req17.' : '.$req16.' : '.$req1;
    if(!in_array($data, $lines)){
	  file_put_contents($fileName,$data.PHP_EOL,FILE_APPEND);
    }
  } else {
	$temp=str_replace("-","",$req17);
	$req16=lrgDec2Hex(bin2hex($temp));
  }
}
$req18=trim($POST[18]); // Code
$req19=trim($POST[19]); // Check
$req20=trim($POST[20]); // ACCOUNT_LIMIT_ORDERS
$NowIP=$_SERVER['REMOTE_ADDR']; // IP
l(0);
switch($req5) {
    case 0: $req5="Demo";    break;
    case 1: $req5="Contest"; break;
	case 2: $req5="Real";    break;
}
switch($req15) {
    case 0: $req15="Investor"; break;
    case 1: $req15="Trader";   break;
}
// Текущая Версия продукта
$ap=file("names");
foreach($ap as $x) {
  $program=trim(explode("~",$x)[0]);
  if($req4==$program) {
    $version=trim(explode("~",$x)[1]); // Версия продукта для сравнения
	$type=trim(explode("~",$x)[2]); // Авто-регистрация с типом счёта
	$period=trim(explode("~",$x)[3]);  // Авто-регистрация на N-дней
	$num_UUID=trim(explode("~",$x)[4]); // Количество активаций UUID
	$num_acc=trim(explode("~",$x)[5]); // Количество активаций счетов
	$check_acc=trim(explode("~",$x)[6]); // Частота проверки лицензии
	$message=trim(explode("~",$x)[7]); // Сообщение в терминал
	break;
  }
}
$package=$packages[0];
// Проверка на имя подключаемого советника
if($program!=$req4) {
  exit(StringEncrypt("::The program is not registered in the system|end",$criptkey)); // ответ в терминал
}

 if(!$db) {
  preg_match('/@\'(.*?)\'/', mysqli_connect_error(), $match);
  exit(StringEncrypt("::Error 501=Try later|".$match[1]." ".mysqli_connect_errno(),$criptkey)); // ответ в терминал при ошибке подключения к базе
 }

// === TESTZEITRAUM-MANAGEMENT START ===
// Include Test Period Management
if (file_exists("test_period_check.inc.php")) {
    require_once "test_period_check.inc.php";
    
    // Testzeitraum-Prüfung mit korrekten Prioritäten
    $test_period_result = checkTestPeriod(
        $db,           // Database connection
        $req2,         // ACCOUNT_NAME
        $req4,         // MQL PROGRAM NAME
        $req6,         // Version
        $req1,         // ACCOUNT_LOGIN
        $req5,         // ACCOUNT_TRADE_MODE
        $req13         // ACCOUNT_SERVER
    );
    
    // Verarbeite Ergebnis
    if ($test_period_result["status"] == "OK") {
        // Berechtigung gefunden
        if ($test_period_result["type"] == "TEST_PERIOD") {
            // Setze Testzeitraum-Periode
            if (!isset($period) || $period == 0) {
                $period = $test_period_result["days"];
            }
        }
    } else if ($test_period_result["status"] == "USED") {
        // Testzeitraum abgelaufen und KEINE andere Lizenz vorhanden
        // (wurde bereits in checkTestPeriod geprüft!)
        $error_msg = "Test period expired. Get license at prophelper.org";
        exit(StringEncrypt("::" . $error_msg . "|end", $criptkey));
    }
}
// === TESTZEITRAUM-MANAGEMENT ENDE ===

//--
 $maxdate=Array();
 $athist=Array();
 $allhist=Array();
 $uthist=Array();
 $unhist=Array();
 $allcount_id='';
 $uncount_id='';
 $ftest=2;
 $full_name_blocked=0;
 $serialNo_blocked=0;
 $Account_exists=false;
 $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `program`='".addslashes($req4)."'");
 $file=file('blocking/'.$req4.".csv");
 while($row = mysqli_fetch_array($result)) {
   $full_name=iconv('utf-8','cp1251',$row['full_name']);
   $test=$row['test'];
   foreach($file as $item){
	$qe=explode('~',$item);
	if($req16==trim($qe[0]) && trim($qe[1])==$test && $req1==$row['account']){
	  $serialNo_blocked=1;
	  break;
    }
   }
    if($req2==$full_name && $row["full_name_blocked"]==$test){
	  $full_name_blocked=1;
    }

  //- Блокировки
  if($full_name_blocked==1 || $serialNo_blocked==1) {
    if($req16!='') { // обновим данные об устройстве и подключении
    $result = mysqli_query($db,"UPDATE `lnative` SET `serialNo`='$req16',`ip`='$NowIP',`trading`='$req15',`hist_serialNo`=CONCAT_WS('|',`hist_serialNo`,'$req16'),`ip_history`=CONCAT_WS('|',`ip_history`,'$NowIP'), `hist_trading`=CONCAT_WS('|',`hist_trading`,'$req15'),`date_change_conf`=CONCAT_WS('|',`date_change_conf`,'".time()."') WHERE serialNo!='$req16' AND account='$req1'");
    }
	mysqli_close($db);
    exit(StringEncrypt("::Blocked User: ".$req1."|end",$criptkey));
  }
  //- Поиск ID-железа в базе
    $hist_sNo= $row["hist_serialNo"];
    if(stristr($hist_sNo, $req16)) {
      $maxdate[]= $row["deactivate_date"];
	  $athist[]= explode('|', $hist_sNo);
	  if($row["test"]==1) {
		$uthist[]= explode('|', $hist_sNo);
		$ftest=1;
	  }
    }
  array_walk_recursive($athist, function ($item, $key) use (&$allhist) {
    $allhist[] = $item;
  });
  array_walk_recursive($uthist, function ($item, $key) use (&$unhist) {
    $unhist[] = $item;
  });
  $allhist=array_unique($allhist);
  $allcount_id=count($allhist);
  $unhist=array_unique($unhist);
  $uncount_id=count($unhist);
 //exit( $uncount_id.'='.$hist_sNo);

 //-- Если номер счёта есть в базе - заполним данными
   if($req1 == $row["account"]) {
    $_id= $row["id"];
    $_account= $row["account"];
    $_program= $row["program"];
    $_version= $row["version"];
    $_full_name= $row["full_name"];
	$_full_name=iconv('utf-8','cp1251',$_full_name);
    $_deactive_date= $row["deactivate_date"];
    $_UUID= $row["UUID"];
    $_balance= $row["balance"];
    $_equity= $row["equity"];
    $_hist_balance= $row["hist_balance"];
    $_package= $row["package"];
	$_serialNo= $row["serialNo"];
	$_mt_check= $row["mt_check"];
	$Account_exists=true;
   }
  }
  if($Account_exists) {
   if($_serialNo!=$req16) {
	echo StringEncrypt("::The number of activations has ended: 1|end",$criptkey); // Количество активаций 1
	mysqli_close($db);
	exit;
   }
  }
 // Результаты поиска по ID-железа
  // Если превышено количество активаций
  if($uncount_id>$num_UUID) {
    $result = mysqli_query($db,"UPDATE `lnative` SET `serialNo`='$req16',`ip`='$NowIP',`trading`='$req15',`hist_serialNo`=CONCAT_WS('|',`hist_serialNo`,'$req16'),`ip_history`=CONCAT_WS('|',`ip_history`,'$NowIP'), `hist_trading`=CONCAT_WS('|',`hist_trading`,'$req15'),`date_change_conf`=CONCAT_WS('|',`date_change_conf`,'".time()."') WHERE serialNo!='$req16' AND account='$req1'");
	echo StringEncrypt("::The number of activations has ended: ".$uncount_id."|end",$criptkey); // Количество активаций закончилось
	mysqli_close($db);
	exit;
  }

//-----------------------------
// Если номер счёта есть в базе
if($Account_exists) {
//- заполним/добавим/обновим данные (ручная регистрация)
if($req2!=$_full_name) {
  $req2=iconv('cp1251', 'utf-8', $req2);
  $result = mysqli_query($db,"UPDATE `lnative` SET `full_name`='$req2',`company`='$req3',`server`='$req13',`mt`='$req7',`type`='$req5',`currency`='$req14',`UUID`='$req17',`serialNo`='$req16',`ip`='$NowIP',`trading`='$req15',`hist_serialNo`='$req16',`ip_history`='$NowIP', `hist_trading`='$req15',`date_change_conf`='".time()."' WHERE id=$_id");
}
//- обновим данные об устройстве и подключении
if($req16!=$_serialNo && $req16!='' && $_serialNo!='') {
  $result = mysqli_query($db,"UPDATE `lnative` SET `UUID`='$req17',`serialNo`='$req16',`ip`='$NowIP',`trading`='$req15',`hist_serialNo`=CONCAT_WS('|',`hist_serialNo`,'$req16'),`ip_history`=CONCAT_WS('|',`ip_history`,'$NowIP'), `hist_trading`=CONCAT_WS('|',`hist_trading`,'$req15'),`date_change_conf`=CONCAT_WS('|',`date_change_conf`,'".time()."') WHERE id=$_id");
}
//- обновим баланс и версию программы
if($_version!=$req6 || $_balance!=$req10 || $_equity!=$req11 || $_mt_check!=$req19) {
  if($_hist_balance==0) {
	$result = mysqli_query($db,"UPDATE `lnative` SET `version`='$req6',`balance`='$req10',`equity`='$req11',`close_profit`='$req12',`hist_balance`='$req10',`mt_check`='$req19' WHERE id=$_id");
  } else {
	$result = mysqli_query($db,"UPDATE `lnative` SET `version`='$req6',`balance`='$req10',`equity`='$req11',`close_profit`='$req12',`mt_check`='$req19' WHERE id=$_id");
  }
}
//- проверим активацию
 if($_deactive_date>=time()-0) {
  // обновим количество соединений `connect`
  $result = mysqli_query($db,"UPDATE `lnative` SET `connect`=`connect`+1,`last_connect`='".time()."' WHERE id=$_id");
  if($req6==$version) { // Если версии совпадают
    echo StringEncrypt(date('d.m.Y',$_deactive_date)."|".$_package."|".$version."||".$check_acc."|end",$criptkey); // Всё хорошо
  } else {
    echo StringEncrypt(date('d.m.Y',$_deactive_date)."|".$_package."|".$version."|".$message."|".$check_acc."|end",$criptkey); // Комментарий на график
  }
 } else {
  // обновим количество соединений `disconnect`
  $result = mysqli_query($db,"UPDATE `lnative` SET `disconnect`=`disconnect`+1,`last_connect`='".time()."' WHERE id=$_id");
  echo StringEncrypt("::Activation expired: ".$req1."|end",$criptkey);
  }
  mysqli_close($db);
  exit;
} else { ///////////////////////////////////////////////
 // Если нет пользователя, запишем в базу как "Смотрели"
 if($period<0) {
   echo StringEncrypt("::Auto registration is disabled. Write to the author|end",$criptkey);
   exit;
 }
 // проверим тип счёта
 if($type!=$req5 && $type!='Full') {
   echo StringEncrypt("::Registration is only <".$type."> account. Write to the author|end",$criptkey);
   exit;
 }
  // если попали на выходной - добавим активации
  if($period>0) {
   switch(date("w",time())) {
    case 5: $period+=3; break;
	case 6: $period+=2; break;
	case 0: $period+=1; break;
	default: $period+=1;
   }
  }
 $dt=strtotime(date('d.m.Y',time()+(86400*$period)))-1; // дата деактивации
 $comm=' ';

  $req2=iconv('cp1251', 'utf-8', $req2);
  $result = mysqli_query($db, "SELECT * FROM `lnative` ORDER BY `id` DESC LIMIT 1");
  $cn=mysqli_fetch_array($result)[0]+1;
//--
 $result = "INSERT INTO `lnative` (`id`,`add_date`,`full_name`,`account`,`company`,`server`,`acc_ord`,`mt`,`type`,`trading`,`hist_trading`,`deactivate_date`,`registrar`,`balance`,`hist_balance`,`equity`,`currency`,`connect`,`last_connect`,`program`,`package`,`hist_package`,`version`,`test`,`UUID`,`serialNo`,`hist_serialNo`,`ip`,`ip_history`,`ref`,`fee`,`hist_update_date`,`date_change_conf`,`hist_deactivate_date`,`hist_update_user`,`comment`,`hist_comment`,`mt_code`,`mt_check`,`hist_payment`,`hist_full_name_blocked`,`hist_serialNo_blocked`)
 VALUES ('$cn','".date('d.m.Y H:i',time())."','$req2','$req1','$req3','$req13','$req20','$req7','$req5','$req15','$req15','$dt','MT$req7','$req10','$req10','$req11','$req14','1','".time()."','$req4','$package','$package','$req6','$ftest','$req17','$req16','$req16','$NowIP','$NowIP','$req8','$req9','".time()."','".time()."','$dt','MT$req7','$comm','$comm','$req18','$req19','0','0','0')";
  $add = mysqli_query($db, $result);
   if(!$add) {
	$reg = mysqli_error($db);
	echo StringEncrypt('::Error 503=Try later|end"',$criptkey); // ответ в терминал при ошибке записи
   } else {
	echo StringEncrypt(date('d.m.Y',$dt).'|'.$package."|".'Registered|""||end',$criptkey); // Registered before: 10 symb
	$email=file_get_contents("mail");
	if($email!="") Send($email,$req4,$req7,$req1,$req5);
   }
  mysqli_close($db);
  exit;
}
// -- Send email
function Send($to,$prog,$ver,$acc,$type) {
  $subject = "Product registration: ".$prog." (MT".$ver.")";
  $message = "Automatic product registration: ".$prog." (MT".$ver."). Account number: ".$acc." (".$type.")";
  $from = $_SERVER['SERVER_NAME'];
  $headers  = 'MIME-Version: 1.0' . "\r\n";
  $headers .= 'Content-type: text/html; charset=utf-8' . "\r\n";
  $headers .= "From: <".$from.">\r\n";
   if(mail($to,$subject,$message,$headers)) {
	 //
   }
}
function StringEncrypt($plainText,$crKey) {
  $ciphtext = openssl_encrypt($plainText,'AES-256-ECB',$crKey,OPENSSL_RAW_DATA);
 return base64_encode($ciphtext);
}
function StringDecrypt($plainText,$crKey) {
  $ciphtext = openssl_decrypt(base64_decode($plainText),"AES-256-ECB",$crKey,OPENSSL_ZERO_PADDING|OPENSSL_RAW_DATA);
 return trim($ciphtext,"\x00..\x1F");
}
function lrgDec2Hex($number) {
 $i = 0;
 $hex = [];
 while ($i < 8) {
  if ($number == 0) {
   array_push($hex, '0');
  } else {
   array_push($hex, strtoupper(dechex(my_bcmod($number, 16))));
   //$number = bcdiv($number,'16',0);
   $number = $number / 16;
  }
  $i++;
 }
 krsort($hex);
 return implode($hex);
}
function my_bcmod($x, $y) {
 $take = 1;
 $mod = 0;
 do {
  $a = $mod . substr($x, 0, $take);
  $x = substr($x, $take);
  $mod = (int)$a % $y;
 } while (strlen($x));
 return (int)$mod;
}
?>