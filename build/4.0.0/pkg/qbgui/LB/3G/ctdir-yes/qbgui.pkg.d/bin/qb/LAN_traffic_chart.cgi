#!/usr/bin/perl
require ("/usr/local/apache/qb/language/qblanguage.cgi");
@qblang = QBlanguage();
BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use Data::Dumper;
use CGI;
use CGI::Ajax;
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type:text/html\n\n";
my $zone=XMLread('/usr/local/apache/qbconf/zonecfg.xml');
my $isp=XMLread('/usr/local/apache/qbconf/basic.xml');
my $isplist=$isp->{isp};
my $zonelist=$zone->{nat};
my $dmzlist=$zone->{dmz};
# runCommand(command=>'rm', params=>'-f /proc/net/ipt_account/*');
#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{interface} = $form->param('interface');
$action{refreshtime} = $form->param('refreshtime');

#print qq (<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> );
#print qq (<!DOCTYPE html><head><meta charset="UTF-8"><script type="text/javascript" src="jquery-1.9.1.min.js"></script>
print qq (<html><head><script type="text/javascript" src="jquery-1.9.1.min.js"></script>
<script type="text/javascript" src ="./qbjs/jquery.js">
</script><script language="javascript" type="text/javascript" src="../qbjs/excanvas.min.js">
</script><script type="text/javascript" language="javascript" src="../qbjs/jquery.flot.js">
</script><script type="text/javascript" language="javascript" src="../qbjs/jquery.flot.selection.js">
</script><style type="text/css">table.sortable thead{background-color:#eee;color:#666666;font-weight: bold;cursor: default;}button.menu{margin-right: 4px;height:18px;width:14%;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style><link rel="stylesheet" href="../gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);
#print qq (<button  onclick="parent.mainFrame.location='lantraffic.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[414]</button>);
#print qq (<button  onclick="parent.mainFrame.location='dhcplog.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[485]</button>);
#print qq (<button  onclick="parent.mainFrame.location='arptable.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[486]</button>);
#print qq (<button  onclick="parent.mainFrame.location='Real_traffic_chart.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[415]</button>);
#print qq (<button  onclick="parent.mainFrame.location='Real_bar_traffic_chart.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[416]</button>);
#print qq (<button  onclick="parent.mainFrame.location='LAN_traffic_chart.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[417]</button>);
#print qq (<button  onclick="parent.mainFrame.location='Total_traffic_chart.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[418]</button>);
#print qq (<button  onclick="parent.mainFrame.location='Total_bar_traffic_chart.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[419]</button>);
my $xmllive=-e "/usr/local/apache/qbconf/lantraffic";
my $live = ($xmllive)?('1'):('0');
print qq (<input type="hidden" id="filelive" value="$live"/>);
print qq(<div align="center" style="margin-top: 12px;">);
foreach my $nic ( @$zonelist )
{
    if ($nic->{natid} eq 'system' || $nic->{network} eq ""){next;}
    my $status = ( $action{interface} eq $nic->{network} ) ? 'selected' : '';
    # print qq (<option $status id="T" value="$nic->{network}">$nic->{network}</option>);
    $name = $nic->{network};
    $name =~ s/\/.*//;
    runCommand(command=>'/usr/local/apache/qb/setuid/opreset.sh ', params=>qq ($nic->{network}).' '.qq ($name));
}
sleep(1);
$info=runCommand(command=>'cat', params=>"/proc/net/ipt_account/10.10.1.0");
$file="/tmp/lantraffic";
$info='<pre>'.$info.'</pre>';
# print $info;
print 'IP address:<input type="text" name="iptext" id="iptext" class="OBtitle" style="margin-right: 4px;"/>';
print '<select name="idd" class="OBtitle" id="sidd">';
# foreach my $nic ( @$zonelist ) {
# if($nic->{network} ne ""){
# print '<option value="'.$nic->{network}.'">'.$nic->{network}.'</option>';
# }
# print qq (<br />);
# }

print '</select>';

# print '<span id="ssip"></span>';
print 'Time:<select id="siddtime" class="OBtitle" name="siddtime">
<option value="">ALL</option>
<option value="30">Last 30 minute</option>
<option value="60">Last 1 hour</option>
<option value="180">Last 3 hour</option>
<option value="360">Last 6 hour</option>
<option value="720">Last 12 hour</option>
<option value="1440">Last 1 day</option>
<option value="4320">Last 3 day</option>
<option value="10080">Last 7 day</option>
</select>';
print qq(<input id="btidd" type="button" class="OBtitle" value="Apply" /><input type="checkbox" size="100%" id="enabled"/>Enabled);
print qq(</div><div id="all">);
print qq(<div id="placeholder" style="width:600px;height:300px;background-color: white;margin: auto;"></div>);
print qq(<div style="margin: 0 auto 10px;width:400px;height:50px;background-color:#FFFFFF;" id="overview"></div>);
print qq(<div id="placeholderUP" style="width:600px;height:300px;background-color: white;margin: auto;"></div>);
print qq(<div style="margin: 0 auto 10px;width:400px;height:50px;background-color:#FFFFFF;" id="overviewUP"></div></div>);
# print qq ( <input class="dataUpdate" type="button" value="Poll for data">);
print << "QB_TRAFFIC";
<script type="text/javascript">

\$(window).load(function(){
    if (\$("#filelive").val() == "0")
    {
        \$("#all").attr("style","display:none");
   	\$(".OBtitle").attr("disabled",true);
    }
    else
    {
    	\$("#all").attr("style","display:block");
    	\$(".OBtitle").attr("disabled",false);
    	\$("#enabled").attr("checked",true);
    }
});

\$("#enabled").click(function() {
    var motion;
    \$(this).attr("disabled",true);
    if (\$(this).attr("checked"))
    {
        \$("#all").attr("style","display:block");
        \$(".OBtitle").attr("disabled",false);
        motion="ADD";
    }
    else
    {
        \$("#all").attr("style","display:none");
        \$(".OBtitle").attr("disabled",true);
        motion="DEL";
    }
    \$.get("LAN_traffic.cgi",{action:motion},function(){
        \$("#enabled").attr("disabled",false);
    	alert("Change Success!!");
    });
});

\$.get("getiptablesip.cgi", function(data){
//alert("Data Loaded: " + data);
var iplist = data.split(",");
iplist.sort(function(a,b){
			var ipaa = a.split(".");
			var ipbb = b.split(".");
			ipaa = ipaa[3]*1+ipaa[2]*256+ipaa[1]*256*256+ipaa[0]*256*256*256;
			ipbb = ipbb[3]*1+ipbb[2]*256+ipbb[1]*256*256+ipbb[0]*256*256*256;
			var stv =ipaa-ipbb;
			return stv;});
for(var pp = 0; pp<iplist.length;pp++){
iplist[pp] =  '<option value="'+iplist[pp]+'">'+iplist[pp]+'</option>';
\$("#sidd").append(iplist[pp]);
}
\$("#iptext").val(\$("#sidd").val());
\$("#btidd").click();
});

\$("#sidd").change(function() {
//alert('Index: ');
  \$("#iptext").val(\$("#sidd").val());
});

			\$("#btidd").click(function() {
				var selectval = \$("#iptext").val();
			  //alert(selectval);
			  \$.ajax({
               
                url: 'load_lan_traffic_2json.cgi?tm='+selectval,
                method: 'GET',
                dataType: 'json',
                success: onDataReceived
				});
			});
function onDataReceived(jsondata){
//alert(jsondata);    
	var intime =\$("#siddtime").val();
	var lenarr = jsondata[0].data.length;
	if(intime !=""){
		for(var tt=0;tt<lenarr-(intime*1);tt++){
				jsondata[0].data.shift();			
				jsondata[1].data.shift();
		}
	}
onDataReceivedDL([jsondata[0]]);
onDataReceivedUP([jsondata[1]]);
}
            function onDataReceivedDL(series) {
				var ndate = new Date();
				var timezonem = ndate.getTimezoneOffset();
				for(var d = 0;d<series[0].data.length;d++){
				series[0].data[d][0]-=timezonem*60*1000;
				//series[1].data[d][0]-=timezonem*60*1000;
				}
				var options = {
					   series: {
							lines: { show: true, lineWidth: 2 ,fill: false,fillColor: "#336699" },
							shadowSize: 0
						},
					colors: [ "#0000FF"],
					yaxis: { min: 0, autoscaleMargin: 0.001 },
						xaxis: { mode: "time", tickLength: 5 },
						selection: { mode: "x" },
						grid: { 
						//markings: weekendAreas

							}
					};
				
				var plot = \$.plot(\$("#placeholder"), series, options);
				
				var overview = \$.plot(\$("#overview"), series, {
										series: {
											lines: { show: true, lineWidth: 1  },
											shadowSize: 0
										},
										legend: {
											show: 0},
										colors: [ "#FF0000"],
											xaxis: { ticks: [], mode: "time" },
											yaxis: { ticks: [], min: 0, autoscaleMargin: 0.05 },
											selection: { mode: "x" }
										});

				// now connect the two
				\$("#placeholder").unbind("plotselected");
				\$("#placeholder").bind("plotselected", function (event, ranges) {
				if(ranges.xaxis.to - ranges.xaxis.from<300000){
				alert('Min ranges 5 Minutes');
				
				return false;
				}
					// do the zooming
					plot = \$.plot(\$("#placeholder"), series,
								  \$.extend(true, {}, options, {
									  xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to }
								  }));

					// don't fire event on the overview to prevent eternal loop
					overview.setSelection(ranges, true);
				});
				
				\$("#overview").bind("plotselected", function (event, ranges) {
					plot.setSelection(ranges);
				});
            }

function onDataReceivedUP(series) {
				var ndate = new Date();
				var timezonem = ndate.getTimezoneOffset();
				for(var d = 0;d<series[0].data.length;d++){
				series[0].data[d][0]-=timezonem*60*1000;
				//series[1].data[d][0]-=timezonem*60*1000;
				}
				var options = {
					   series: {
							lines: { show: true, lineWidth: 2 ,fill: false,fillColor: "#336699" },
							shadowSize: 0
						},
					colors: [ "#0000FF"],
					yaxis: { min: 0, autoscaleMargin: 0.001 },
						xaxis: { mode: "time", tickLength: 5 },
						selection: { mode: "x" },
						grid: { 
						//markings: weekendAreas

							}
					};
				
				var plot = \$.plot(\$("#placeholderUP"), series, options);
				
				var overview = \$.plot(\$("#overviewUP"), series, {
										series: {
											lines: { show: true, lineWidth: 1  },
											shadowSize: 0
										},
										legend: {
											show: 0},
										colors: [ "#FF0000"],
											xaxis: { ticks: [], mode: "time" },
											yaxis: { ticks: [], min: 0, autoscaleMargin: 0.05 },
											selection: { mode: "x" }
										});

				// now connect the two
				\$("#placeholderUP").unbind("plotselected");
				\$("#placeholderUP").bind("plotselected", function (event, ranges) {
				if(ranges.xaxis.to - ranges.xaxis.from<300000){
				alert('Min ranges 5 Minutes');
				
				return false;
				}
					// do the zooming
					plot = \$.plot(\$("#placeholderUP"), series,
								  \$.extend(true, {}, options, {
									  xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to }
								  }));

					// don't fire event on the overview to prevent eternal loop
					overview.setSelection(ranges, true);
				});
				
				\$("#overviewUP").bind("plotselected", function (event, ranges) {
					plot.setSelection(ranges);
				});
}

</script>
QB_TRAFFIC
print qq(</body></html>)
