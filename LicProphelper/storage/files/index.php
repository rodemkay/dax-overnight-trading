<?php
// Download
if($_FILES && $_FILES["filename"]["tmp_name"]) {
    $name = $_FILES["filename"]["name"];
  if(strripos($name, 'ex4') || strripos($name, 'ex5') || strripos($name, 'png') || strripos($name, 'gif') || strripos($name, 'jpg') || strripos($name, 'zip') || strripos($name, 'txt')) {
	if(move_uploaded_file($_FILES["filename"]["tmp_name"],'../'.$name))
     echo "<b>".$name."</b> downloaded";
	 else echo "Error download";
  } else echo '<span style="color: #b90000;">Invalid file error! <b>Only: ‘ex4’, ‘ex5’, ‘png’, ‘gif’, ‘jpg’, ‘zip’, ‘txt’</b></span>';
  echo '<br><br><button onclick="history.go(-1);"> <<< Back </button>';
  exit;
}
// Delete
if(isset($_GET["nm"])) {
    $name = $_GET["nm"];
  if(strripos($name, 'ex4') || strripos($name, 'ex5') || strripos($name, 'png') || strripos($name, 'gif') || strripos($name, 'jpg') || strripos($name, 'zip') || strripos($name, 'txt')) {
	if(file_exists('../'.$name)) {
	 if(unlink('../'.$name))
	  echo "<b>".$name."</b> Delete";
      else echo "<b>Error:</b> Delete";
    }
     else echo "<b>Error:</b> File not found";
  } else echo '<span style="color: #b90000;">Invalid file error! <b>Only delete: ‘ex4’, ‘ex5’, ‘png’, ‘gif’, ‘jpg’, ‘zip’, ‘txt’</b></span>';
  echo '<br><br><button onclick="history.go(-1);"> <<< Back </button>';
  exit;
}
// Upload
$file_name = $_GET['file'];
if(isset($file_name) and preg_match("/^[a-zA-Z0-9_\.\/\- ]{0,50}\.(ex4|ex5|zip|txt)$/",$file_name) and file_exists('../'.$file_name)) {
 header("HTTP/1.1 200 OK");
 header('Expires: '.gmdate('D, d M Y H:i:s').' GMT');
 // определяем браузер
 $ua = (isset($_SERVER['HTTP_USER_AGENT'])) ? $_SERVER['HTTP_USER_AGENT'] : '';
 $isMSIE = preg_match('@MSIE ([0-9].[0-9]{1,2})@', $ua);
  if($isMSIE){
    // если это Internet Explorer
    header('Content-Disposition: attachment; filename="'.$file_name.'"');
	header('Content-Length: '.filesize('../'.$file_name));
    header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
    header('Pragma: public');
  } else {
    // если это НЕ Internet Explorer
    header('Content-Disposition: attachment; filename="'.$file_name.'"');
	header('Content-Length: '.filesize('../'.$file_name));
    header("Cache-Control: no-cache, must-revalidate");
	header('Pragma: no-cache');
  }
  ob_clean();
  flush();
 readfile('../'.$file_name);
} else {
  echo "File not found";
  exit;
}
?>