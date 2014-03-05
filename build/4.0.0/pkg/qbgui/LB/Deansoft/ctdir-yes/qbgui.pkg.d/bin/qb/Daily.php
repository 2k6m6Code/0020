<!DOCTYPE html><html><head><meta charset="UTF-8">
<link rel="stylesheet" href="jquery-ui-1.10.3.custom.css" />
<link rel="stylesheet" href="../gui.css" type="text/css">
<script type="text/javascript" src="jquery-1.10.2.js"></script>
<script src="highcharts.min.js"></script>
<script src="exporting.js"></script>


</head>
<body bgcolor="#336699" text="#ffffff" link="#000040" >
<div align="center" style="width: 100%; margin: 12px auto 5px auto;">
<form name="lantgaffic" method="post" action="query.php" style="width:100%">
<table cellspacing="0" border="0">
<tr><td class="bigtitle" align="center">Daily Graphic</td></tr></table>
<div style="width:75%" align="center">
<table width="100%" border="1"><tr>
<td class="body" align="center">Query Condition</td>
<tr><td class="body" align="center">Date Time :
<?php
date_default_timezone_set("Asia/Taipei");
$now_TW=time();
$date_T_m_d = date('Y/m/d',$now_TW);
$date_h = date('H',$now_TW);
$date_i = date('i',$now_TW);
$date_s = date('s',$now_TW);
echo '<input type="text" id="datepicker" style="width:90px" value='.$date_T_m_d.">";


/* echo '<select id="start_hr">';
$date_h--;
for($x=0;$x<24;$x++)
{
    if ($x < 10)$x='0'.$x;
    if ($x == $date_h)
    	echo '<option value='.$x.' selected>'.$x.'</option>';
    else
    	echo '<option value='.$x.'>'.$x.'</option>';
}
echo '</select><a>Hour</a>';

echo '&nbsp;&nbsp;&nbsp;<a>IP : </a>';
echo '<input type="text" style="width:90px" value="" >&nbsp;&nbsp;&nbsp;'; */

?>

<tr><td align="center"><input type="button" id="query" value="Query" onclick="Submit();"></td></tr>
<!--
<tr><td align="center">
<input type="button" id="day" value="<<Day" onclick="Submit();">&nbsp;&nbsp;
<input type="button" id="hour" value="<<Hour" onclick="Submit();">&nbsp;&nbsp;
<input type="button" id="today" value="Today" onclick="Submit();">&nbsp;&nbsp;
<input type="button" id="Hour" value="Hour>>" onclick="Submit();">&nbsp;&nbsp;
<input type="button" id="Day" value="Day>>" onclick="Submit();">&nbsp;&nbsp;
</td></tr>
-->
</table></div>
<img id="load_gif" src="image/loading.gif" style="display:none;">
<div id="flows" style="width:75%;height:200px"></div>
<div id="bytes" style="width:75%;height:200px"></div>
<div id="packets" style="width:75%;height:200px"></div>
<div id="bps" style="width:75%;height:200px"></div>
<div id="pps" style="width:75%;height:200px"></div>
<div id="bpp" style="width:75%;height:200px"></div>
<script src="jquery-ui-1.10.3.custom.js"></script>
<script src="jquery.ui.datepicker-zh-TW.js"></script>
<script src="../qbjs/jquery.dataTables.min.js"></script>
<script language="javascript">

Submit();

$( "#datepicker" ).datepicker({
    regional:"zh-TW",
    defaultDate: "+1w",
	changeYear: true,
    changeMonth: true,
    numberOfMonths: 1,
    showButtonPanel: true
});

function Submit()
{
	$("#load_gif").css('display','block'); 
	$("#query").attr('disabled', true);
    var time = document.getElementById("datepicker").value;
    var tmp = new Array();
    tmp = time.split("/");
    var option=tmp[0]+tmp[1]+tmp[2];
	var y=tmp[0];
	var m=tmp[1];
	var d=tmp[2];
$.ajax({
    url: 'image_data.php',
    cache: false,
    dataType: 'html',
    type:'GET',
    data: { option:option},
    error: function(xhr) {
        alert('Ajax request ERROR');
    },
    success: function(response) {
        var test = new Array();
        test = response.split(",:");
        for (var i=0;i<test.length;i++)
        {
            var tmp = new Array();
            tmp = test[i].split(/-:/);
            if (tmp[0].match("flows") == "flows")
            {
               var tmp_1 = new Array();
               var tmp_2 = new Array();
               tmp_1 = tmp[1].split(/,/);
               for(var x=0;x<tmp_1.length;x++)
               {
                   tmp_2[x]=(tmp_1[x]++);
               } 
               creat_map('flows',tmp_2,y,m,d);
            }
            if (tmp[0].match("bytes") == "bytes")
            {
               var tmp_1 = new Array();
               var tmp_2 = new Array();
			   var num = tmp[1].replace(/\w\,/g,',');
			   num = num.replace(/\w$/g,'');
			   //alert(num);
			   tmp_1 = num.split(/,/);
               //tmp_1 = tmp[1].split(/,/);
               for(var x=0;x<tmp_1.length;x++)
               {
                   tmp_2[x]=(tmp_1[x]++);
               } 
               creat_map('bytes',tmp_2,y,m,d);
            }
            if (tmp[0].match("packets") == "packets")
            {
               var tmp_1 = new Array();
               var tmp_2 = new Array();
               tmp_1 = tmp[1].split(/,/);
               for(var x=0;x<tmp_1.length;x++)
               {
                   tmp_2[x]=(tmp_1[x]++);
               } 
               creat_map('packets',tmp_2,y,m,d);
            }
            if (tmp[0].match("bps") == "bps")
            {
               var tmp_1 = new Array();
               var tmp_2 = new Array();
               tmp_1 = tmp[1].split(/,/);
               for(var x=0;x<tmp_1.length;x++)
               {
                   tmp_2[x]=(tmp_1[x]++);
               } 
               creat_map('bps',tmp_2,y,m,d);
            }
            if (tmp[0].match("pps") == "pps")
            {
               var tmp_1 = new Array();
               var tmp_2 = new Array();
               tmp_1 = tmp[1].split(/,/);
               for(var x=0;x<tmp_1.length;x++)
               {
                   tmp_2[x]=(tmp_1[x]++);
               } 
               creat_map('pps',tmp_2,y,m,d);
            }
            if (tmp[0].match("bpp") == "bpp")
            {
               var tmp_1 = new Array();
               var tmp_2 = new Array();
               tmp_1 = tmp[1].split(/,/);
               for(var x=0;x<tmp_1.length;x++)
               {
                   tmp_2[x]=(tmp_1[x]++);
               } 
               creat_map('bpp',tmp_2,y,m,d);
            }
            
        }
		$("#load_gif").css('display','none');
		$("#query").attr('disabled', false);
    }
});
}

function creat_map(o,a,y,m,d)
{
	var Today=new Date();
	var y=y;
	var m=m-1;
	var d=d
    $('#'+o).highcharts({
    	title:{
            text:o
    	},
    	xAxis:{
	    type:'datetime',
	    maxZoom:24*3600000,//fourteendays
    	    title:{
	    	text:null
    	    }
        },
	yAxis:{
	    title:{
		text:''
	    }
	},
	tooltip:{
	    shared:true
	},
	legend:{
	    enabled:false
	},
	plotOptions:{
	    area:{
		fillColor:{
		    linearGradient:{x1:0,y1:0,x2:0,y2:1},
		    stops:[
			[0,Highcharts.getOptions().colors[0]],
			[1,Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
		    ]
		},
		lineWidth:1,
		marker:{
		    enabled:false
		},
		shadow:false,
		    states:{
		    	hover:{
			    lineWidth:1
			}
		    },
		    threshold:null
		    }
		},
		series:[{
		    type:'area',
		    name:o,
		    pointInterval:1800000,
		    pointStart:Date.UTC(y,m,d),
		    data:a
		}]
	});

}
</script>
</body></html>
