<?php
$exec = "/usr/local/apache/qb/setuid/run ";

//執行狀態分析
exec("$exec /usr/local/apache/qb/status/getsysstatus.cgi");

if($_POST['act']=='reload'){
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
	$text5 = fgets($op,4096);
	preg_match($ptn,$text5,$data5);

	$color = array();
	$color[1] = $data1[1] > 95?'990000':'006600';
	$color[2] = $data2[1] > 95?'990000':'006600';
	$color[3] = $data3[1] > 95?'990000':'006600';
	$color[4] = $data4[1] > 95?'990000':'006600';
	$color[5] = $data5[1] > 95?'990000':'006600';
	//end
	$chart_value .= "<set label='CPU Usage' color='{$color[1]}' value='".$data1[1]."'/>";
	$chart_value .= "<set label='Memory Usage(Used={$data2[2]}KB,Available={$data2[4]}KB)' color='{$color[2]}' value='".$data2[1]."'/>";
	$chart_value .= "<set label='|-------Cache Usage(Total={$data5[2]}KB)' color='{$color[5]}' value='".$data5[1]."'/>";
	$chart_value .= "<set label='Ramdisk Usage(Total={$data3[2]}KB,Available={$data3[4]}KB)' color='{$color[3]}' value='".$data3[1]."'/>";
	$chart_value .= "<set label='Concurrent session(Max={$data4[2]},Concurrent={$data4[4]})' color='{$color[4]}' value='".$data4[1]."'/>";

}
?>


			<div align="center" class="style1">
				<strong>
				<?php 
					$uptime = exec('uptime');
					$ptn = '/(\S+)\s*up\s*([^,]+).*/';
					preg_match($ptn,$uptime,$time_data);
					$uptime = 'Present time:'.$time_data[1].' Uptime:'.$time_data[2];
					echo $uptime;
				?>
				</strong>
			</div>
<div id="chartdiv" align="center" style="float:right;width:100%; z-index:1"></div>
				<script type="text/javascript">
				var myChart = new FusionCharts("swf/barchart.swf", "myChartId", "710", "220", "0", "0");
				myChart.setDataXML("<chart basefontsize='12' caption='' bgcolor='#A0D2EA' subcaption='' xAxisName='' yAxisName='Usage' numberSuffix='％' palette='2' bgAlpha='40,100' bgAngle='360' animation='0'><?php echo $chart_value;?></chart>");
				myChart.render("chartdiv");
			   </script>
