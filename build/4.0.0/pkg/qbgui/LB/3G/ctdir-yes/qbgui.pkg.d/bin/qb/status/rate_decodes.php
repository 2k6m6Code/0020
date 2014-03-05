<?php
if($_POST['act']=='reload'){
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
		<?php if($_POST['types']==1 || empty($_POST['types'])){?>
		<div id="chartdiv1" align="center"></div>
		<script type="text/javascript">
			var myChart = new FusionCharts("swf/piechart.swf", "myChartId", "710", "300", "0", "0");
			myChart.setDataXML("<chart basefontsize='12' caption='' bgcolor='#A0D2EA'  subcaption='InBound' xAxisName='Month' yAxisName='Sales' numberSuffix='％' palette='4' enableSmartLabels='1' bgAlpha='40,100' bgAngle='360' showBorder='1' startingAngle='50'><?php echo $chart_value_IN;?></chart>");
			myChart.render("chartdiv1");
		</script>
		<?php } else if($_POST['types']==2){?>
		<div id="chartdiv2" align="center"></div>
		<script type="text/javascript">
			var myChart = new FusionCharts("swf/piechart.swf", "myChartId", "710", "300", "0", "0");
			myChart.setDataXML("<chart basefontsize='12' caption='' bgcolor='#A0D2EA'  subcaption='OutBound' xAxisName='Month' yAxisName='Sales' numberSuffix='％' palette='4' enableSmartLabels='1' bgAlpha='40,100' bgAngle='360' showBorder='1' startingAngle='50'><?php echo $chart_value_OUT;?></chart>");
			myChart.render("chartdiv2");
		</script>
		<?php } else if($_POST['types']==3){?>
		<div id="chartdiv3" align="center"></div>
		<script type="text/javascript">
			var myChart = new FusionCharts("swf/piechart.swf", "myChartId", "710", "300", "0", "0");
			myChart.setDataXML("<chart basefontsize='12' caption='' bgcolor='#A0D2EA'  subcaption='Total' xAxisName='Month' yAxisName='Sales' numberSuffix='％' palette='4' enableSmartLabels='1' bgAlpha='40,100' bgAngle='360' showBorder='1' startingAngle='50'><?php echo $chart_value_TOTAL;?></chart>");
			myChart.render("chartdiv3");
		</script>
		<?php } else if ($_POST['types']==4){?>
		<div id="chartdiv1" align="center"></div>
		<script type="text/javascript">
			var myChart = new FusionCharts("swf/piechart.swf", "myChartId", "710", "300", "0", "0");
			myChart.setDataXML("<chart basefontsize='12' caption='' bgcolor='#A0D2EA'  subcaption='InBound' xAxisName='Month' yAxisName='Sales' numberSuffix='％' palette='4' enableSmartLabels='1' bgAlpha='40,100' bgAngle='360' showBorder='1' startingAngle='50'><?php echo $chart_value_IN;?></chart>");
			myChart.render("chartdiv1");
		</script>
		<br />
		<div id="chartdiv2" align="center"></div>
		<script type="text/javascript">
			var myChart = new FusionCharts("swf/piechart.swf", "myChartId", "710", "300", "0", "0");
			myChart.setDataXML("<chart basefontsize='12' caption='' bgcolor='#A0D2EA'  subcaption='OutBound' xAxisName='Month' yAxisName='Sales' numberSuffix='％' palette='4' enableSmartLabels='1' bgAlpha='40,100' bgAngle='360' showBorder='1' startingAngle='50'><?php echo $chart_value_OUT;?></chart>");
			myChart.render("chartdiv2");
		</script>
		<br />
		<div id="chartdiv3" align="center"></div>
		<script type="text/javascript">
			var myChart = new FusionCharts("swf/piechart.swf", "myChartId", "710", "300", "0", "0");
			myChart.setDataXML("<chart basefontsize='12' caption='' bgcolor='#A0D2EA'  subcaption='Total' xAxisName='Month' yAxisName='Sales' numberSuffix='％' palette='4' enableSmartLabels='1' bgAlpha='40,100' bgAngle='360' showBorder='1' startingAngle='50'><?php echo $chart_value_TOTAL;?></chart>");
			myChart.render("chartdiv3");
		</script>				
		<?php }?>
	</div>
</div>
