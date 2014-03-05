<?php
$exec = "/usr/local/apache/qb/setuid/run ";

//權限判斷
exec("$exec /usr/local/apache/qb/logincheck.cgi > /usr/local/apache/qb/status/logincheck");


//執行狀態分析
exec("$exec /usr/local/apache/qb/status/getsysstatus.cgi");
	//Cpu Usage
	$op = fopen('cpu.status','r');
	$ptn = '/(\d+)\s*.*/';
	$text1 = fgets($op,4096);
	preg_match($ptn,$text1,$data1);
	
	//ram Usage
	$op = fopen('memory.status','r');
	$ptn = "/(\d*)\s*,\s*(\d*)\s*KBytes,\s*(\d*)\s*,\s*(\d*).*/";
	$text2 = fgets($op,4096);
	preg_match($ptn,$text2,$data2);
	
	//ramdisk Usage
	$op = fopen('ramdisk.status','r');
	$ptn = "/(\d*)\s*,\s*(\d*)\s*KBytes,\s*(\d*)\s*,\s*(\d*).*/";
	$text3 = fgets($op,4096);
	preg_match($ptn,$text3,$data3);
		
	//Concurrent session
	$op = fopen('session.status','r');
	$ptn = "/(\d*)\s*,\s*(\d*)\s*,\s*(\d*)\s*,\s*(\d*).*/";
	$text4 = fgets($op,4096);
	preg_match($ptn,$text4,$data4);
	
	//Cache Usage
	$op = fopen('cache.status','r');
	$ptn = "/(\d*)\s*,\s*(\d*)\s*KBytes,\s*(\d*)\s*,\s*(\d*).*/";
	$test5 = fgets($op,4096);
	preg_match($ptn,$text5,$data5);
	

	$color = array();
	$color[1] = $data1[1] > 95?'990000':'006600';
	$color[2] = $data2[1] > 95?'990000':'006600';
	$color[3] = $data3[1] > 95?'990000':'006600';
	$color[4] = $data4[1] > 95?'990000':'006600';
	$color[5] = $data5[1] > 95?'990000':'006600';
	//end
	$chart_value .= "<set label='CPU Usage' color='{$color[1]}' value='".$data1[1]."'/>";
	$chart_value .= "<set label='Memory Usage(Used={$data2[2]}K,Available={$data2[4]}K)' color='{$color[2]}' value='".$data2[1]."'/>";
	$chart_value .= "<set label='|-------Cache Usage(Total={$data5[2]}K)' color='{$color[5]}' value='".$data5[1]."'/>";
	$chart_value .= "<set label='Ramdisk Usage(Total={$data3[2]},Available={$data3[4]})' color='{$color[3]}' value='".$data3[1]."'/>";
	$chart_value .= "<set label='Concurrent session(Max={$data4[2]},Concurrent={$data4[4]})' color='{$color[4]}' value='".$data4[1]."'/>";
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
	<div id="reload_area">
	</div>
</div>
<div align="center" class="subject_white" style="width:100%; margin-top:20px">If you can't see the BarChart,you need to install<a href="http://www.adobe.com/shockwave/download/download.cgi?P1_Prod_Version=ShockwaveFlash" target="_blank"> adobe flash player</a>.</div>
</body>
</html>
<script language="javascript" type="text/javascript">
function DOreload(){
	var container = {
	success: 'reload_area',
	failure: ''
	};
	var url = 'reload_area2.php?' ;
	var qstr = 'act=reload';
	MJ_repeat(container, url, qstr, 10);
}
DOreload();
</script>
