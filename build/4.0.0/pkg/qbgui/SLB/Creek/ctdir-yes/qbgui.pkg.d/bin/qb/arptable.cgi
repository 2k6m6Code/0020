#!/usr/bin/perl -w
require ("/usr/local/apache/qb/language/qblanguage.cgi");
@qblang = QBlanguage();

#require ('./qbmod.cgi');
print "Content-type:text/html \n\n";
use CGI;
my $form= new CGI;

print qq (<html><head><script type="text/javascript" language="javascript" src="./qbjs/jquery.js"></script>
<style type="text/css">
button.menu{
width: 14%;
height: 18px;
font: 10px Verdana;
color: white;
background: #336699;
border:1px solid black;
cursor:hand;
margin-right: 4px;
}
</style>
<!--<button class="menu"  onclick="parent.mainFrame.location=\'lantraffic.cgi\'" 			style="width: 165">$qblang[414]</button>-->
<!--<button class="menu"  onclick="parent.mainFrame.location=\'dhcplog.cgi\'" 			style="width: 165">$qblang[485]</button>-->
<!--<button class="menu"  onclick="parent.mainFrame.location=\'arptable.cgi\'" 			style="width: 165">$qblang[486]</button>-->
<!--<button class="menu"  onclick="parent.mainFrame.location=\'Real_traffic_chart.cgi\'" 		style="width: 165">$qblang[415]</button>-->
<!--<button class="menu"  onclick="parent.mainFrame.location=\'Real_bar_traffic_chart.cgi\'" 	style="width: 165">$qblang[416]</button>-->
<!--<button class="menu"  onclick="parent.mainFrame.location=\'LAN_traffic_chart.cgi\'" 		style="width: 165">$qblang[417]</button>-->
<!--<button class="menu"  onclick="parent.mainFrame.location=\'Total_traffic_chart.cgi\'" 		style="width: 165">$qblang[418]</button>-->
<!--<button class="menu"  onclick="parent.mainFrame.location=\'Total_bar_traffic_chart.cgi\'" 	style="width: 165">$qblang[419]</button>-->
<br>
<script type="text/javascript" language="javascript" src="./qbjs/jquery.dataTables.min.js"></script>
<link rel="stylesheet" href="gui.css" type="text/css"></head><body class="message">);



print qq(<style>table {
	border-width: 1px;
	border-spacing: 0px;
	border-style: solid;
	border-color: black;
	border-collapse: collapse;
	background-color: white;
	font-size: 12px;
	width:80%;
	color: #004488;
}
table th {
    background-color: white;
    border-color: black;
    border-style: solid;
    border-width: 1px;
    padding: 1px;
}
table td {
    background-color: white;
    border-color: black;
    border-style: solid;
    border-width: 1px;
    padding: 3px;
}
body{
    background-color:#336699;
}
.dataTables_filter {

margin-bottom: 5px;
}
.message{
color: #EEEEEE;
font-size: 14px;
}
</style>);


my $info='';
    $head.="Show Q-Balancer ARP Table";
    $info=`/usr/local/apache/qb/setuid/run /bin/cat /var/lib/dhcp/dhcpd.leases`;
    `/usr/local/apache/qb/setuid/run /sbin/arp -na | awk \'\{print \$2,\$4,\$6,\$7\}\' > /tmp/arp`;
    $info=`/usr/local/apache/qb/setuid/run /bin/cat /tmp/arp`;
    if ( !$info )
    {
    	$info="!! Empty Log !!<br>";
    }
    my @info=split(/\n/,$info);
    my $newinfo;
    my $count;
    foreach my $linelog ( @info )
    {
	$linelog =~ s'\('';
	$linelog =~ s'\)'';
	$linelog =~ s/<incomplete>/N\/A /;
    	@detial=split(' ',$linelog);

    	my $ttable .="<tr>";
    	foreach my $mydetial ( @detial )
    	{
    	    if ( $mydetial eq 'on' ) {next;}
    	    $ttable .="<td style='width: 200px;'>";
    	    $ttable .=$mydetial.'</td>';
    	    $newinfo.=$ttable;
	    $ttable ="";
    	}
    	$newinfo.='</tr>'
    }
	
$info= '<table id="example" ><thead><tr><th>IP</th><th>MAC</th><th>Port</th></tr></thead><tbody>';

$info.=$newinfo;
$info.="</tbody></table>";
print '<div align="center">';
print $head."<br>"; 

$info='<pre>'.$info.'</pre>';

print $info; 
$scriptData = '<script type="text/javascript">
$("#example").dataTable({
		
		"iDisplayLength": 50,
		"bPaginate": false,
		"bInfo": false

	});


</script> ';
print qq ($scriptData</div></body></html>);
