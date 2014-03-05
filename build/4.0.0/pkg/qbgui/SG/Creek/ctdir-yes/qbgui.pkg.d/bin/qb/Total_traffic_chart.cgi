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
#print qq (<!DOCTYPE html><head><meta charset="UTF-8"><script type="text/javascript" src ="./qbjs/jquery.js">
print qq (<html><head><script type="text/javascript" src ="./qbjs/jquery.js">
</script><script language="javascript" type="text/javascript" src="./qbjs/excanvas.min.js">
</script><script type="text/javascript" language="javascript" src="./qbjs/jquery.flot.js">
</script><script type="text/javascript" language="javascript" src="./qbjs/jquery.flot.pie.js">
</script><style type="text/css">table.sortable thead{background-color:#eee;color:#666666;font-weight: bold;cursor: default;}button.menu{margin-right: 4px;height:18px;width:14%;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style><link rel="stylesheet" href="../gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);
#print qq (<button  onclick="parent.mainFrame.location='lantraffic.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[414]</button>);
#print qq (<button  onclick="parent.mainFrame.location='dhcplog.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[485]</button>);
#print qq (<button  onclick="parent.mainFrame.location='arptable.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[486]</button>);
#print qq (<button  onclick="parent.mainFrame.location='Real_traffic_chart.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[415]</button>);
#print qq (<button  onclick="parent.mainFrame.location='Real_bar_traffic_chart.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[416]</button>);
#print qq (<button  onclick="parent.mainFrame.location='LAN_traffic_chart.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[417]</button>);
#print qq (<button  onclick="parent.mainFrame.location='Total_traffic_chart.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[418]</button>);
#print qq (<button  onclick="parent.mainFrame.location='Total_bar_traffic_chart.cgi'" style="width:170" hidefocus="true" class="menu">$qblang[419]</button>);
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
print 'Subnet address:<input type="text" name="iptext" id="iptext" style="margin-right: 4px;"/>';
print '<select name="idd" id="sidd" style="margin-right: 4px;">';
# foreach my $nic ( @$zonelist ) {
# if($nic->{network} ne ""){
# print '<option value="'.$nic->{network}.'">'.$nic->{network}.'</option>';
# }
# print qq (<br />);
# }

print '</select>';
print 'Time:<select id="siddtime" name="siddtime">
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
# print '<span id="ssip"></span>';
print '<input id="btidd" type="button" value="Apply" />';
print qq(</div>);
print qq(<div id="dtt" style="width: 100%; text-align: center;margin:30px auto auto auto;">Download</div>);
print qq(<div id="placeholder" style="width:600px;height:300px;background-color: white;margin: auto;"></div>);
print qq(<div id="utt" style="width: 100%; text-align: center;margin:30px auto 0px auto;">Upload</div>);
print qq(<div id="placeholderUP" style="width:600px;height:300px;background-color: white;margin:5px auto 2px auto;"></div>);
# print qq(<div style="margin: 0 auto 10px;width:400px;height:50px;background-color:#FFFFFF;" id="overview"></div>);
# print qq ( <input class="dataUpdate" type="button" value="Poll for data">);
print << "QB_TRAFFIC";
<script type="text/javascript">

\$.get("getiptablesip.cgi", function(data){
//alert("Data Loaded: " + data);
var iplist = data.split(",");


// \$("#ssip").append('<select name="idd" id="sidd">');
for(var pp = 0; pp<iplist.length;pp++){
	var ipaa = iplist[pp].split(".");
	if(ipaa[3]==="0"){


	iplist[pp] =  '<option value="'+iplist[pp]+'">'+iplist[pp]+'</option>';
	\$("#sidd").append(iplist[pp]);
	}
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
				var intime = \$("#siddtime").val();
				if(intime != ""){
				var myDate = new Date(); 
				var myEpoch = myDate.getTime()/1000.0;
				
				var sumtimer = parseInt(myEpoch)-60*(intime);
				var sumstr = '&ti='+sumtimer;
				}else{
				var sumstr = '';
				}
			  //alert(selectval);
			  \$.ajax({
                // usually, we'll just call the same URL, a script
                // connected to a database, but in this case we only
                // have static example files so we need to modify the
                // URL
                url: 'load_total_traffic_2json.cgi?tm='+selectval+'&ty=a'+sumstr,
                method: 'GET',
                dataType: 'json',
                success: onDataReceived
				});
			  \$.ajax({
                // usually, we'll just call the same URL, a script
                // connected to a database, but in this case we only
                // have static example files so we need to modify the
                // URL
                url: 'load_total_traffic_2json.cgi?tm='+selectval+'&ty=b'+sumstr,
                method: 'GET',
                dataType: 'json',
                success: onDataReceivedUP
				});
			});

            function onDataReceived(data) {
			data.pop();
			for(var rr = 0;rr <data.length;rr++){
			data[rr].label = data[rr].label.replace("-Download","")+" ("+data[rr].data+"Kbps)";
			}
				\$.plot(\$("#placeholder"), data,
				{
			series: {
            pie: {
                show: true,
				combine: {
                    color: '#999',
                    threshold: 0.02
                }
            }
        },
        grid: {
            hoverable: true,
            clickable: true
        }
				});
				\$("#placeholder").unbind("plothover", eventshow);
				\$("#placeholder").bind("plothover", eventshow);
            }
		function onDataReceivedUP(data) {
		data.pop();
		for(var rr = 0;rr <data.length;rr++){
		data[rr].label = data[rr].label.replace("-Upload","")+" ("+data[rr].data+"Kbps)";
			}
				\$.plot(\$("#placeholderUP"), data,
				{
			series: {
            pie: {
                show: true,
				combine: {
                    color: '#999',
                    threshold: 0.01
                }
            }
        },
        grid: {
            hoverable: true,
            clickable: true
        }
				});
				\$("#placeholderUP").unbind("plothover", eventshow);
				\$("#placeholderUP").bind("plothover", eventshow);
            }

		
function pieClick(event, pos, obj)
{
if (!obj)
return;
percent = parseFloat(obj.series.percent).toFixed(2);
alert(''+obj.series.label+': '+percent+'%');
} 


function showTooltip(x, y, contents,bcolor, areAbsoluteXY) {
	var rootElt = 'body';
	\$('<div id="tooltip" class="tooltip-with-bg">' + contents + '</div>').css( {
	'background-color': bcolor,
	border:'1px solid #336699',
	position: 'absolute',
	display: 'none',
	'z-index':'1010',
	'text-shadow': '0px 1px 3px black',
	color: '#FFF',
	top: y,
	left: x
	}).prependTo(rootElt).show();
} 

function eventshow(event, pos, item) {
    if (item) {
        if (previousPoint != item.datapoint) {
            previousPoint = item.datapoint;
 
            //delete de precedente tooltip
            \$('.tooltip-with-bg').remove();
 
            var x = item.datapoint[0];
 
            //All the bars concerning a same x value must display a tooltip with this value and not the shifted value
            if(item.series.bars.order){
                for(var i=0; i < item.series.data.length; i++){
                    if(item.series.data[i][3] == item.datapoint[0])
                        x = item.series.data[i][0];
                }
            }
 
            var y = item.datapoint[1];
 
            showTooltip(pos.pageX+15, pos.pageY+15, x.toFixed(3)+" %",item.series.color);
 
        }
    }
    else {
        \$('.tooltip-with-bg').remove();
        previousPoint = null;
    }
 
}

</script>
QB_TRAFFIC
print qq(</body></html>)