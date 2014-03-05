<!DOCTYPE html><html><head><meta charset="UTF-8">
<link rel="stylesheet" href="../jquery-ui-1.10.3.custom.css" />
<script type="text/javascript" src="../jquery-1.10.2.js"></script>
<script src="../highcharts.min.js"></script>
<script src="../highcharts-more.js"></script>
<script src="../exporting.js"></script>
<script src="meter.js"></script>
<link rel="stylesheet" href="gui.css" type="text/css">
<style type="text/css">
button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>
</head>
<body bgcolor="#336699" text="#ffffff" link="#000040" >
<div align="center" style="width: 100%; margin: 12px auto 5px auto;">
<form name="lantgaffic" method="post" action="speed_page.php" style="width:100%">
<table cellspacing="0" border="0">
<tr><td class="bigtitle" align="center">Speed Status</td></tr>
<tr><td align="center">
<select id="op">
<?php
$f = fopen('/usr/local/apache/active/basic.xml','r');
while( $data = fgets($f)) 
{ 
    preg_match('/ispname=\"(.*?)\"/s',$data,$data2);
    $data3=str_replace('ispname=','',$data2[0]);
    if (str_replace('"','',$data3) != '')
    echo '<option value="'.str_replace('"','',$data3).'">'.str_replace('"','',$data3).'</option>';
}
fclose( $f );
?>
</select>
</td></tr>
</table>
<div style="width:75%" align="center">
<table width="100%" border="0">
    <tr>
	<td class="body" align="center" >
	    <div id="down" style="width: 300px; max-width: 400px; height: 300px; margin: 0 auto"></div>
	    <input id="down_option" type="hidden" value="HiNet">
        </td>
        
        <td class="body" align="center" >
       	    <div id="loss" style="width: 400px; height: 300px; margin: 0 auto"></div> 
        </td>
    </tr>
    <tr>
	<td class="body" align="center" >
	    <div id="up" style="width: 300px; max-width: 400px; height: 300px; margin: 0 auto;"></div>
	    <input id="up_option" type="hidden" value="HiNet">
        </td>
        
        <td class="body" align="center" >
       	    <div id="latency" style="width: 400px; height: 300px; margin: 0 auto"></div> 
        </td>
    </tr>
    
</table>
<script type="text/javascript" >

var speed1 = new speed_meter();
var la = new latency_loss();
$(function(){
<?php
$name=$_GET[name];
echo '$("select option[value='.$name.']").attr("selected",true);';
?>
$("#op").trigger('change');
});

$("#op").change(function(){
    var name = $(this).val();
$.get("speed_data.pl",{name:name,option:"down-total"},function (yy){
    var speed=speed1;
    speed.set('10000','0','5000','8000','Kb/s','Download Speed','down','2000',name,yy*1000);
    speed.creat();
});
$.get("speed_data.pl",{name:name,option:"up-total"},function (yy){
    var speed=speed1;
    speed.set('10000','0','5000','8000','Kb/s','Upload Speed','up','2000',name,yy*1000);
    speed.creat();
});
la.set('latency',$(this).val(),'Latency','ms');
la.creat();
la.set('loss',$(this).val(),'Packet Loss','%');
la.creat();

});

Highcharts.setOptions({
    global: {
	useUTC: false
    }
});

function latency_loss()
{    
    this.id='';
    this.name='';
    this.title='';
    
    this.set=(function(id,name,title,unit){
        this.id=id;
        this.name=name;
        this.title=title;
        this.unit=unit;
    });
   
    this.creat=(function(){
    var chart,id=this.id,name=this.name,title=this.title,unit=this.unit;
    $('#'+id).highcharts({
            chart: {
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function() {
    
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function() {
                            
                            var x = (new Date()).getTime(), // current time
                                y = '';
                    	    $.get("speed_data.pl",{name:name,option:id},function(yy){
                                series.addPoint([x, Math.round(yy)], true, true);
                   	    });
                        }, 1000);
                    }
                }
            },
            title: {
                text: "[ " + name + " ] " + title
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: unit
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                        Highcharts.numberFormat(this.y, 2) + unit;
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: name,
                data: (function() {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;
    
                    for (i = -19; i <= 0; i++) {
                        data.push({
                            x: time + i * 1000,
                            y: Math.round(0)
                        });
                    }
                    return data;
                })()
            }]
        });
    });
}
</script>

</body></html>
