<?php
if($_POST['act']=='reload'){
	$exec = "/usr/local/apache/qb/setuid/run ";
	//執行狀態分析
        exec("$exec /usr/local/apache/qb/status/ispsessions.pl src> /usr/local/apache/qb/status/sessions.status");
	//exec("$exec /usr/local/apache/qb/status/rate.cgi > /usr/local/apache/qb/status/rate.status");
	//開始分析log
	$decode_filename = '/usr/local/apache/qb/status/sessions.status';
	if(file_exists($decode_filename)){
	$name = array();
	$val = array();
	$val_total = 0;
	$rowt=0;
	$fsize = filesize ($decode_filename);
		$fd = fopen ($decode_filename, 'r');
			while($contents = fgets ($fd, $fsize)){
			                $rowt++;
			                if ($rowt > 30) break;
					$ptn = "/(\S+) (\d+).*/";
					preg_match($ptn,$contents,$data);
					array_push($name, $data[1]." ,$data[2] sessions");
					array_push($val, $data[2]);
					$val_total += $data[2];
			}
		fclose($fd);
	
		$num = count($name);
		for($k=0 ; $k<$num ; $k++){
		        //echo $val_total.'<br>';
		        //echo $val[$k].'<br>';
		        $vals = $val_total&&$val[$k]?round($val[$k]/$val_total*100,2):0;
		        $chart_value .= "<set label='".$name[$k]."' value='".$vals."'/>";
			//$chart_value .= "<set label='".$name[$k]."' value='".round($val[$k]/$val_total*100,2)."'/>";
		}
	}
}
?>
<div align="center" style="width:100%; margin-top:30px">
	<div id="reload_area">
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
		<div id="chartdiv1" align="center"></div>
		<script type="text/javascript">
			//var myChart = new FusionCharts("swf/piechart.swf", "myChartId", "710", "300", "0", "0");
			var myChart = new FusionCharts("swf/piechart.swf", "myChartId", "850", "450", "0", "0");
			myChart.setDataXML("<chart basefontsize='12' caption='' bgcolor='#A0D2EA'  subcaption='Sessions' xAxisName='Month' yAxisName='Sales' numberSuffix='％' palette='4' enableSmartLabels='1' bgAlpha='40,100' bgAngle='360' showBorder='1' startingAngle='50'><?php echo $chart_value;?></chart>");
			myChart.render("chartdiv1");
		</script>
	</div>
</div>
