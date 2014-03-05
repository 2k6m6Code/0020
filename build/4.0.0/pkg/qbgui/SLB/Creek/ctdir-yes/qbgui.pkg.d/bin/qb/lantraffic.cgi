#!/usr/bin/perl
require ("/usr/local/apache/qb/language/qblanguage.cgi");
@qblang = QBlanguage();
BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use XML::Simple;
use CGI;
#require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type:text/html\n\n";

my $zone=XMLin('/usr/local/apache/qbconf/zonecfg.xml');
my $isp=XMLin('/usr/local/apache/qbconf/basic.xml');
my $isplist=$isp->{isp};
my $zonelist=$zone->{nat};
my $dmzlist=$zone->{dmz};

#runCommand(command=>'/usr/local/apache/qb/setuidrun /bin/rm', params=>'-f /proc/net/ipt_account/*');
`/usr/local/apache/qb/setuid/run /bin/rm -f /proc/net/ipt_account/*`;
#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;

$action{action} = $form->param('action');
$action{interface} = $form->param('interface');
$action{refreshtime} = $form->param('refreshtime');

#//#tables_filter{text-align: left;} table.sortable thead{background-color:#eee;color:#666666;font-weight: bold;cursor: default;}
#print qq (<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> );
#print qq (<!DOCTYPE html><html><head><meta charset="UTF-8">);
#print qq (<script type="text/javascript" src ="sorttable.js"></script>);
#print qq (<script type="text/javascript" src ="./qbjs/jquery.js"></script>
print qq (<html><head><script type="text/javascript" language="javascript" src="./qbjs/jquery.js"></script>
<style type="text/css">
button.menu
{
width: 14%;
height:18px;
font:10px Verdana;
color:white;
background:#336699;
border:1px solid black;
cursor:hand;
margin-right: 4px;
}
body{
background-color:#336699;
}
.message{
color: #EEEEEE;
font-size: 14px;
}

</style>
<!--<button onclick="parent.mainFrame.location='lantraffic.cgi'" 			style="width: 165" hidefocus="true" class="menu">$qblang[414]</button>-->
<!--<button onclick="parent.mainFrame.location='dhcplog.cgi'" 			style="width: 165" hidefocus="true" class="menu">$qblang[485]</button>-->
<!--<button onclick="parent.mainFrame.location='arptable.cgi'" 			style="width: 165" hidefocus="true" class="menu">$qblang[486]</button>-->
<!--<button onclick="parent.mainFrame.location='Real_traffic_chart.cgi'" 		style="width: 165" hidefocus="true" class="menu">$qblang[415]</button>-->
<!--<button onclick="parent.mainFrame.location='Real_bar_traffic_chart.cgi'" 	style="width: 165" hidefocus="true" class="menu">$qblang[416]</button>-->
<!--<button onclick="parent.mainFrame.location='LAN_traffic_chart.cgi'" 		style="width: 165" hidefocus="true" class="menu">$qblang[417]</button>-->
<!--<button onclick="parent.mainFrame.location='Total_traffic_chart.cgi'" 		style="width: 165" hidefocus="true" class="menu">$qblang[418]</button>-->
<!--<button onclick="parent.mainFrame.location='Total_bar_traffic_chart.cgi'" 	style="width: 165" hidefocus="true" class="menu">$qblang[419]</button>-->


<link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

print qq(<div align="center" style="width: 600px; margin: 12px auto 5px auto;">);
#------- start to draw every form object to interact with users --------------------------------

print qq(<form name="lantgaffic" method="post" action="lantraffic.cgi" style="width:600">);
print qq (<table cellspacing="0" border="0">);
# print qq (<tr><td class="bigtitle">LAN Traffic Status</td></tr></table>);
print qq (<tr><td class="bigtitle">Real Time Traffic</td></tr></table>);
print qq (<div style="width:600">);
print qq (<table width="100%" border="0"><tr>);
print qq (<td class="body" align="left">Host&nbsp&nbsp);
print qq (<select name="interface" id="interface" style="width:220"> );
print qq (<option value="ALL">ALL);
print qq (<option>SUBNET);
foreach my $nic ( @$zonelist )
{
    if ($nic->{natid} eq 'system' || $nic->{network} eq ""){next;}
    my $status = ( $action{interface} eq $nic->{network} ) ? 'selected' : '';
    print qq (<option $status id="T" value="$nic->{network}">$nic->{network}</option>);
    $name = $nic->{network};
    $name =~ s/\/.*//;
    #runCommand(command=>'/usr/local/apache/qb/setuid/opreset.sh ', params=>qq ($nic->{network}).' '.qq ($name));
    `/usr/local/apache/qb/setuid/run /usr/local/apache/qb/setuid/opreset.sh $nic->{network} $name`;
}
print qq (<option>DMZ);
foreach my $dmz ( @$dmzlist )
{
    if ($dmz->{enabled} ne '1' || $dmz->{mode} eq "" || $dmz->{nic} eq "") {next;}
    foreach my $isp ( @$isplist ) 
    {
        if ($isp->{iid} ne $dmz->{isp} || $isp->{alive} ne "1" || $isp->{subnet} eq ""){next;}
        my $status = ( $action{interface} eq $isp->{subnet} ) ? 'selected' : '';
        print qq (<option $status id="T" value="$isp->{subnet}">$isp->{subnet}</option>);
        $name = $isp->{subnet};
        $name =~ s/\/.*//;
        #runCommand(command=>'/usr/local/apache/qb/setuid/opreset.sh ', params=>qq ($isp->{subnet}).' '.qq ($name));     
        `/usr/local/apache/qb/setuid/run /usr/local/apache/qb/setuid/opreset.sh $isp->{subnet} $name`;     
    }
}
print qq (</select>);
print qq (&nbsp&nbspAuto Refresh Per);
print qq (<select name="refreshtime" id="refreshtime">);
my @time=(3,5,7,9);
foreach my $tm ( @time )
{
    my $status = ( $action{refreshtime} eq $tm ) ? ( 'selected' ) : ( '' );
    print qq(<option value="$tm" $status>$tm</option>);
}
print qq (</select>seconds&nbsp&nbsp);
print qq (<input type="button" value="Stop" class="qb" style="width:60" id="switch" onclick="Switch(this.value)">);
print qq (</td></tr></table>);
print qq (</div>);

print << "QB_TRAFFIC";

<script type="text/javascript" language="javascript" src="../qbjs/jquery.dataTables.min.js"></script>
<script type="text/javascript" src="../grid.js"></script>
<script language="javascript">
(function (\$, document, undefined) {

	var pluses = /\\+/g;

	function raw(s) {
		return s;
	}

	function decoded(s) {
		return decodeURIComponent(s.replace(pluses, ' '));
	}

	var config = \$.cookie = function (key, value, options) {

		// write
		if (value !== undefined) {
			options = \$.extend({}, config.defaults, options);

			if (value === null) {
				options.expires = -1;
			}

			if (typeof options.expires === 'number') {
				var days = options.expires, t = options.expires = new Date();
				t.setDate(t.getDate() + days);
			}

			value = config.json ? JSON.stringify(value) : String(value);

			return (document.cookie = [
				encodeURIComponent(key), '=', config.raw ? value : encodeURIComponent(value),
				options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
				options.path    ? '; path=' + options.path : '',
				options.domain  ? '; domain=' + options.domain : '',
				options.secure  ? '; secure' : ''
			].join(''));
		}

		// read
		var decode = config.raw ? raw : decoded;
		var cookies = document.cookie.split('; ');
		for (var i = 0, parts; (parts = cookies[i] && cookies[i].split('=')); i++) {
			if (decode(parts.shift()) === key) {
				var cookie = decode(parts.join('='));
				return config.json ? JSON.parse(cookie) : cookie;
			}
		}

		return null;
	};

	config.defaults = {};

	\$.removeCookie = function (key, options) {
		if (\$.cookie(key) !== null) {
			\$.cookie(key, null, options);
			return true;
		}
		return false;
	};

})(jQuery, document);
function Switch (name)
{
	if ( name == "Stop"){
		 \$("#switch").val("Run");
	}else{
		 \$("#switch").val("Stop");
		 auto_refresh();
	}
}

function auto_refresh()
{	
    	setTimeout("Ajax();",(parseInt(\$("#refreshtime").val())-1)*1000);
}

function Ajax()
{    
     var tmp = \$("#interface").val();
     var data="";
     var url = "lantc1.cgi";
     if (tmp == "ALL"){
        for (var x = 2; x < \$("#interface").children("option").length ; x ++)
        {
            if( \$("#interface").children("option").eq(x).val() != "DMZ")
            data += \$("#interface").children("option").eq(x).val() + ","; 
        }
     	var db = data + "&time="+new Date().getTime();
     }else{
     	//var url = "lantc1.cgi?tm="+ tmp + "&time="+new Date().getTime();
     	var db = tmp + "&time="+new Date().getTime();
     }
     \$.get(url,{tm:db},
     //queryReqHandler = new ActiveXObject("Microsoft.XMLHTTP");
     //queryReqHandler.onreadystatechange =fno;
     //queryReqHandler.open("GET",url,true);
     //queryReqHandler.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
     //var str='';
     //queryReqHandler.send(null);
//}

function fno(data)
{	
        var status;
	if(\$("#switch").val() == "Stop"){
	\$("#table").html(data);
	
	var oTable =  \$('#tables').dataTable({
		"fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {
			/* Calculate the market share for browsers on this page */
			var iPageMarket = 0;
			var iPageMarket2 = 0;
			for ( var i=iStart ; i<iEnd ; i++ )
			{
				iPageMarket += aaData[ aiDisplay[i] ][4].split(' ')[0]*1;
				iPageMarket2 += aaData[ aiDisplay[i] ][5].split(' ')[0]*1;
			}
			
			/* Modify the footer row to match what we want */
			var nCells = nRow.getElementsByTagName('th');
			nCells[4].innerHTML = iPageMarket.toFixed(2) + " Kbps";
			nCells[5].innerHTML = iPageMarket2.toFixed(2) + " Kbps";
		},
		"bPaginate": false,
		"bInfo": false,
		"aoColumns": [
            { "sType": 'html' },
            { "sType": 'string-case' },
            { "sType": 'string-case' },
            { "sType": 'string-case' },
            { "sType": 'string-case' },
            { "sType": 'string-case' }
        ]
	});
	jQuery.fn.dataTableExt.oSort['html-asc']  = function(x,y) {
	    var xx1 = x.split('.');
	    var yy1 = y.split('.');
	    x = xx1[0]*255*255*255+xx1[1]*255*255+xx1[2]*255+xx1[3];
	    y = yy1[0]*255*255*255+yy1[1]*255*255+yy1[2]*255+yy1[3];
	    var ssv3 = x-y;
    	    return ssv3;
	};
	jQuery.fn.dataTableExt.oSort['html-desc']  = function(x,y) {
	    var xx1 = x.split('.');
	    var yy1 = y.split('.');
	    x = xx1[0]*255*255*255+xx1[1]*255*255+xx1[2]*255+xx1[3];
	    y = yy1[0]*255*255*255+yy1[1]*255*255+yy1[2]*255+yy1[3];
	    var ssv3 = y-x;
    	    return ssv3;
	};
	jQuery.fn.dataTableExt.oSort['string-case-asc']  = function(x,y) {
	    x = x.replace(" Kbps","");
	    y = y.replace(" Kbps","");
	    var ssv3 = x-y;
            return ssv3;
	};
	 
	jQuery.fn.dataTableExt.oSort['string-case-desc'] = function(x,y) {
	    x = x.replace(" Kbps","");
	    y = y.replace(" Kbps","");
	    var ssv3 = y-x;
    	    return ssv3;
	};
	\$("input[type='text']").val(\$.cookie("searchinput"));
	oTable.fnFilter( \$("input[type='text']").val());
	\$("input[type='text']").keyup(function () { 
	    \$.cookie("searchinput", \$("input[type='text']").val());
	});
	\$("th").eq(4).click();
	\$("th").eq(4).click();
	auto_refresh();
	}
    });
}
auto_refresh();


</script>

QB_TRAFFIC

print qq (<div class="divframe" style="width:600" id="table">);
print qq (</div></table>);
print qq (<div id="show" style="display:none"></div>);
print qq(<input type="hidden" name="action" value="$action{action}">);
print qq(</form></div></body></html>);
