<?php
$exec = "/usr/local/apache/qb/setuid/run ";
//執行狀態分析
exec("$exec /usr/local/apache/qb/status/rate.cgi > /usr/local/apache/qb/status/rate.status");
//開始分析log
$decode_filename = '/usr/local/apache/qb/status/rate.status';
if(file_exists($decode_filename)){
$name = array();
$val_in = array();
$val_out = array();
$val_total = array();
$val_in_total = 0;
$val_out_total = 0;
$val_total_total = 0;
$fsize = filesize ($decode_filename);
	$fd = fopen ($decode_filename, 'r');
		while($contents = fgets ($fd, $fsize)){
			if(strpos($contents,'gmaster.add')){
				$ptn = "/window.parent.gmaster.add\(\"(\S+)\", \"(\S+)\", \"(\S+)\", \"(\d+)\", \"(\d+) \", \"(\d+)\", \"(\d+)\", \"(\d+)\", \"(\d+)\", \"(\d+)\".*/";
				preg_match($ptn,$contents,$data);
				array_push($name,$data[1]."({$data[8]}/{$data[9]})");
				array_push($val_in,$data[5]+$data[7]);
				array_push($val_out,$data[4]+$data[6]);
				array_push($val_total,$data[4]+$data[5]+$data[6]+$data[7]);
				$val_in_total += $data[5]+$data[7];
				$val_out_total += $data[4]+$data[6];
				$val_total_total += $data[4]+$data[5]+$data[6]+$data[7];
			}
		}
	fclose($fd);

	$num = count($name);
	for($k=0 ; $k<$num ; $k++){
		if($val_in_total){
			$chart_value_IN .= "<set label='".$name[$k]."' value='".round($val_in[$k]/$val_in_total*100,2)."'/>";
		} else {
			$chart_value_IN .= "<set label='".$name[$k]."' value='".round(1/$num*100,2)."'/>";
		}

		if($val_out_total){
			$chart_value_OUT .= "<set label='".$name[$k]."' value='".round($val_out[$k]/$val_out_total*100,2)."'/>";
		} else {
			$chart_value_OUT .= "<set label='".$name[$k]."' value='".round(1/$num*100,2)."'/>";
		}
		
		if($val_total_total){
			$chart_value_TOTAL .= "<set label='".$name[$k]."' value='".round($val_total[$k]/$val_total_total*100,2)."'/>";
		} else {
			$chart_value_TOTAL .= "<set label='".$name[$k]."' value='".round(1/$num*100,2)."'/>";
		}
	}
	
}
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title></title>
<style type="text/css">
<!--
body,td,th {
	font-family: 新細明體;
	font-size: 9pt;
}
body {
	margin-left: 0px;
	margin-top: 0px;
	margin-right: 0px;
	margin-bottom: 0px;
	background-image: url();
	background-color: #336699;
}
-->
</style>
<link href="cms.css" rel="stylesheet" type="text/css">
<script language="javascript" type="text/javascript" src="script/chartfun.js"></script>
<script language="javascript" type="text/javascript" src="script/myproto.js"></script>
<script language="javascript" type="text/javascript">
function check_file(){
	if(arguments[0] != ''){
		document.getElementById('bak').style.display = '';
	}
	else {
		document.getElementById('bak').style.display = 'none';
	}
}

function format_check(){
	if(confirm("Format this unit and reboot it!!!")){
		document.form1.action = "<?php echo $_SERVER['PHP_SELF'].'?acts=Format';?>"
		document.form1.submit();
	}
}

function MM_goToURL() { //v3.0
  var i, args=MM_goToURL.arguments; document.MM_returnValue = false;
  for (i=0; i<(args.length-1); i+=2) eval(args[i]+".location='"+args[i+1]+"'");
}

function login_check(){
	var success = function(transport){
					if(transport.responseText=="0"){
						location.href = "../index.cgi";
					}
				  }
	var failure = function(){ alert('Something went wrong...');}
	var url = '../logincheck.cgi';
	var qstr = '';
	MJ_query( url, qstr, success, failure);
}
login_check();

</script>
<style type="text/css">
<!--
.style1 {color: #FFFFFF}
-->
</style>
</head>

<body>
<div align="center" style="width:100%; margin-top:30px">
<div align="center">
<div style="color:#fff;  font:12px Verdana;"></select>Auto Refresh Per
        <select id="refreshtime" name="refreshtime">
		  
          <option value="5">5</option>
          <option value="10">10</option>
		  <option value="30">30</option>
          <option value="60">60</option>
		  
        </select> seconds
        <input type="button" onclick="Switch(this.value)" id="switch" style="width:60" class="qb" value="Stop" /></div>
	<form method="get" name="form" id="form">
		<select name="types" id="types" onChange="this.form.submit()">
			<option value="1" <?php echo ($_GET['types']==1 || empty($_GET['types']))?'selected':'';?>>InBound</option>
			<option value="2" <?php echo ($_GET['types']==2)?'selected':'';?>>OutBound</option>
			<option value="3" <?php echo ($_GET['types']==3)?'selected':'';?>>Total</option>
			<option value="4" <?php echo ($_GET['types']==4)?'selected':'';?>>Overview</option>
		</select>
	</form>
	</div>
	<div id="reload_area">

	</div>
</div>
<div align="center" class="subject_white" style="width:100%; margin-top:20px">If you can't see the PieChart,you need to install<a href="http://www.adobe.com/shockwave/download/download.cgi?P1_Prod_Version=ShockwaveFlash" target="_blank"> adobe flash player</a>.</div>
</body>
</html>
<script language="javascript" type="text/javascript">
var secinput = document.getElementById("refreshtime");

var stopinput = document.getElementById("switch");

function DOreload(ttvvar){
	var container = {
	success: 'reload_area',
	failure: ''
	};
	var url = 'rate_decodes.php?' ;
	var qstr = 'act=reload&types='+$('types').value;
	MJ_repeat(container, url, qstr, ttvvar);
}
function Switch (name)
{
if ( name == "Stop"){
stopinput.value ="Run";
MJ_stop();
}else{
stopinput.value="Stop";
DOreload(secinput.value);
}
}
DOreload(secinput.value);
</script>
