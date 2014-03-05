#!/usr/bin/perl
require ("/usr/local/apache/qb/language/qblanguage.cgi");
@qblang = QBlanguage();
BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }
require ("/usr/local/apache/qb/qbmod.cgi");

use CGI;
my $form = new CGI;
my $option = $form->param('option');
print "Content-type:text/html\n\n";
#---------------- Just for form to show available items of subnets and services ------------------
print qq (<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> );
print qq (<!DOCTYPE html><html><head><meta charset="UTF-8">);
print qq (<link rel="stylesheet" href="jquery-ui-1.10.3.custom.css" />);
print qq (<script src="jquery-1.9.1.js"></script>);
print qq (<script type="text/javascript" src="../grid.js"></script>);
print qq (<link rel="stylesheet" href="/resources/demos/style.css" />);
print qq (<script type="text/javascript" src ="sorttable.js"></script><script type="text/javascript" src ="../qbjs/jquery.js"></script><style type="text/css">#tables_filter{text-align: left;} table.sortable thead{background-color:#eee;color:#666666;font-weight: bold;cursor: default;}button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style><link rel="stylesheet" href="../gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);
print qq (<div align="center" style="width: 100%; margin: 12px auto 5px auto;">);

print qq (<input id="option" value="$option" type="hidden">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="lantgaffic" method="post" action="lantraffic.cgi" style="width:100%">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td class="bigtitle" align="center"></td></tr></table>);
print qq (<div style="width:75%" align="center">);
print qq (<table width="100%" border="1"><tr>);
print qq (<td class="body" align="center" >Query Condition</td>);
print qq (<tr><td class="body" align="center" >Date Time : );
my ($sec, $min, $hour, $day, $mon, $year) = localtime(time);
if ($day < 10 ){$day='0'.$day;}
$mon++;
if ($mon < 10 ){$mon='0'.$mon;}
$now_date=join("/",($year+1900,$mon,$day));
print qq (<input type="text" id="datepicker" style="width:90px" value="$now_date"/>);
print qq (&nbsp<select id="start_hr">);
$hour--;
if ($hour < 10 ){$hour='0'.$hour;}
foreach my $tm (0..23 )
{
    if ($tm < 10 ){$tm = '0'.$tm;}
    if ($hour eq $tm)
    {
        print qq(<option value="$tm" selected>$tm</option>);
    }else
    {
        print qq(<option value="$tm" >$tm</option>);
    }
}
print qq (</select>);

my $display = '';
my $text = '';
my $goto = '-->';
if (!grep(/query/,$option))
{
   $display = "display:none";
   $text ='Hour&nbsp;&nbsp;';
   $goto ='';
}

print qq (<select id="start_sec" style="$display">);
foreach my $tm (0..59 )
{
    if ($tm < 10 ){$tm = '0'.$tm;}
    print qq(<option value="$tm" >$tm</option>);
}
print qq (</select>$text);

print qq ($goto<input type="text" id="datepicker_1" style="width:90px;$display" value="$now_date"/>);
print qq (&nbsp;<select id="end_hr" style="$display">);
$hour++;
foreach my $tm (0..23 )
{
    if ($tm < 10 ){$tm = '0'.$tm;}
    if ($hour eq $tm)
    {
        print qq(<option value="$tm" selected>$tm</option>);
    }else
    {
        print qq(<option value="$tm" >$tm</option>);
    }
}
print qq (</select>);

print qq (<select id="end_sec" style="$display">);
foreach my $tm (0..59 )
{
    if ($tm < 10 ){$tm = '0'.$tm;}
    print qq(<option value="$tm" >$tm</option>);
}
print qq (</select>);

#print qq (&nbsp;&nbsp;Core Switch : <select id="core_switch"><option value="all">ALL</option></select>&nbsp;&nbsp;);
print qq (<a name="noquery" >Report Type : </a><select id="report_type" name="noquery">);
print qq (<option value="0">Hourly</option>);
print qq (<option value="1">Daily</option>);
print qq (<option value="2">Weekly</option>);
print qq (<option value="3">Monthly</option>);
print qq (<option value="4">Yearly</option>);
print qq (<option value="5">Quarterly</option>);
print qq (</select>&nbsp;&nbsp;);

print qq (<a name="noquery" >Time Segment : </a><select id="time_seqment" name="noquery">);
print qq (<option value="0">All Time</option>);
print qq (<option value="1">Work Time</option>);
print qq (<option value="2">Off Time</option>);
print qq (</select></td></tr>);

print qq (<tr><td align="center">);
print qq (<a name="noquery">Packet Direction : </a><a id="ip_name" name="noquery"></a>&nbsp;&nbsp;&nbsp;);
print qq (Group By : <select id="ip_option" ></select>&nbsp;&nbsp;);
print qq (<a name="noquery">Unit : </a><select id="ip_unit" name="noquery"><option value="all">ALL</option>);
my $flow_tmp = XMLread("/usr/local/apache/qbconf/flow.xml");
my $flow = $flow_tmp->{user};
foreach my $oo (@$flow)
{
    if ($oo->{schname} eq 'system'){next;}
    print qq (<option value="$oo->{schname}">$oo->{schname}</option>);
}
print qq (</select>&nbsp;&nbsp;);
print qq (Search for IP : <input id="ip_search" value="">);
print qq (</td></tr>);

print qq (<tr><td align="center">);

print qq (<a name="noquery">Protocol : </a><select id="protocol" name="noquery">);
print qq (<option value="all">ALL</option>);
print qq (</select>&nbsp;&nbsp;);

print qq (<a name="noquery">Order by : </a><select id="order" name="noquery">);
print qq (<option value="-s record/bytes">Bytes</option>);
print qq (<option value="-s record/flows">Flows</option>);
print qq (<option value="-s record/packets">Packets</option>);
print qq (</select>&nbsp;&nbsp;);

print qq (<a name="noquery">&nbsp; &nbsp;Top : </a>);
print qq (<select id="top_1" name="noquery">);
print qq (<option value="10">10</option>);
print qq (<option value="20">20</option>);
print qq (<option value="50">50</option>);
print qq (<option value="100">100</option>);
print qq (<option value="200">200</option>);
print qq (<option value="500">500</option>);
print qq (</select></td></tr>);

print qq (<tr><td align="center"><input type="button" id="query" value="Query" onclick="Submit();"></td></tr>);

print qq (</table></div>);

print qq (<img id="load_gif" src="image/loading.gif" style="display:none;">);

print << "QB_TRAFFIC";

<script src="jquery-ui-1.10.3.custom.js"></script>
<script src="jquery.ui.datepicker-zh-TW.js"></script>
<script src="../qbjs/jquery.dataTables.min.js"></script>
<script src="search.js"></script>
<script language="javascript">

var option = \$("#option").val();
title(option);

\$( "#datepicker" ).datepicker({
    regional:"zh-TW",
    defaultDate: "+1w",
	changeYear: true,
    changeMonth: true,
    numberOfMonths: 1,
    showButtonPanel: true,
    onClose: function( selectedDate ) {
        \$( "#datepicker_1" ).datepicker( "option", "minDate", selectedDate );
    }
});
	
\$( "#datepicker_1" ).datepicker({
    regional:"zh-TW",
    defaultDate: "+1w",
    changeMonth: true,
    numberOfMonths: 1,
    showButtonPanel: true,
    onClose: function( selectedDate ) {      
        \$( "#datepicker" ).datepicker( "option", "maxDate", selectedDate );
    }
});

function Submit()
{
	\$("#load_gif").css('display','block'); 
	\$("#query").attr('disabled', true);
     var url = "search_data_local.pl";
     var start = \$("#datepicker").val();
     switch (\$("#report_type").val())
     {
         case '0':
             \$("#datepicker_1").val(\$("#datepicker").val());
         break;
         
         case '1':
             var tmp = new Array;
             tmp = start.split("/");
             tmp[2]++;
             if (tmp[2] < 10 ){tmp[2] = '0'+tmp[2];}
             \$("#datepicker_1").val(tmp[0] + "/" + tmp[1] + "/" + tmp[2]);
         break;
         
         case '2':
             var tmp = new Array;
             tmp = start.split("/");
             tmp[2] = (tmp[2]-0)+7;
             alert(tmp[2]);
             if (tmp[2] > 30)
             {
                 tmp[1]++
                 tmp[2] -= 30;
             }
             if (tmp[2] < 10 ){tmp[2] = '0'+tmp[2];}
             if (tmp[1] < 10 ){tmp[2] = '0'+tmp[1];}
             \$("#datepicker_1").val(tmp[0] + "/" + tmp[1] + "/" + tmp[2]);
         break;
         
         case '3':
             var tmp = new Array;
             tmp = start.split("/");
             tmp[1]++;
             if (tmp[1] > 12)
             {
                 tmp[0]++;
                 tmp[1] -= 12;
             }    
             if (tmp[2] < 10 ){tmp[2] = '0'+tmp[2];}
             if (tmp[1] < 10 ){tmp[2] = '0'+tmp[1];}
             \$("#datepicker_1").val(tmp[0] + "/" + tmp[1] + "/" + tmp[2]);
         break;
         
         case '4':
             var tmp = new Array;
             tmp = start.split("/");
             tmp[0]++;
             \$("#datepicker_1").val(tmp[0] + "/" + tmp[1] + "/" + tmp[2]);
         break;
         
         case '5':
             var tmp = new Array;
             tmp = start.split("/");
             tmp[1]=(tmp[1]-0) + 3;
             if (tmp[1] > 12)
             {
                 tmp[0]++;
                 tmp[1] -= 12;
             }    
             if (tmp[1] < 10 ){tmp[2] = '0'+tmp[1];}
             \$("#datepicker_1").val(tmp[0] + "/" + tmp[1] + "/" + tmp[2]);
         break;
         
         deafult :
         
         break;
     }
     var end = \$("#datepicker_1").val();
     var tmp = new Array;
     if (!start || !end)
     {
         alert("ERROR");
         return;
     }
     tmp=start.split("/");
     var time = "nfcapd." + tmp[0] + tmp[1] + tmp[2] + \$("#start_hr").val() + \$("#start_sec").val() + ":";
     tmp=end.split("/");
    // if (\$("#report_type").val().match("quert") != null)
    // {
        if ( \$("#report_type").val() == 0 )
		 {
			 var myhr = parseInt(\$("#start_hr").val())+1;
			 if(myhr < 10){myhr = '0'+myhr.toString();}
			 else{myhr.toString();}
             //\$("#end_hr").val(((\$("#start_hr").val()-0)+1));
			 \$("#end_hr").val(myhr);
         }
		 else
		 {
             \$("#end_hr").val(\$("#start_hr").val());
		 }
     //} 
        
     if (\$("#end_hr").val() < 10 ){\$("#end_hr").val('0'+tmp[2]);}
     time += "nfcapd." + tmp[0] + tmp[1] + tmp[2] + \$("#end_hr").val() + \$("#end_sec").val();
     var top = "-n " + \$("#top_1").val();
     var ip = \$("#ip_option").val();
     var unit ='';
     //if (\$("#ip_unit").val() != "all")
     	var unit =\$("#ip_unit").val();
     var limit=\$("#order").val();
     \$.get(url,{time:time,ip:ip,limit:limit,top:top,unit:unit,option:option,symd:start},function fno(data){
	\$("#table").html(data);
	var oTable =  \$('#tables').dataTable({
	    "bPaginate": false,
	    "bInfo": false
	});
	\$("label").attr("style","display:none");
        \$("#ip_search").keyup(function()
	{
    	    oTable.fnFilter(\$("#ip_search").val());
	});
	\$("#load_gif").css('display','none');
	\$("#query").attr('disabled', false);
     });
}

function search_flow(ip,time,option,symd)
{
	\$("#load_gif").css('display','block'); 
	var ip = ip;
	var time = time;
	var option = option;
	var symd = symd;
    var url = "search_flow.pl";
    \$.get(url,{ip:ip,time:time,option:option,symd:symd},function fno(data){
	\$("#table").html(data);
	var oTable =  \$('#tables').dataTable({
	    "bPaginate": false,
	    "bInfo": false
	});
	\$("label").attr("style","display:none");
        \$("#ip_search").keyup(function()
	{
    	    oTable.fnFilter(\$("#ip_search").val());
	});
	\$("#load_gif").css('display','none');
    });
}

</script>

QB_TRAFFIC

print qq (<div class="divframe" style="width:75%" id="table">);
print qq (</div></table>);
print qq(</form></div></body></html>);
