#!/usr/bin/perl

use CGI;
require ("./qbmod.cgi");
require ("./qblib/quotawork.lib");
require ("./qblib/quota_status.lib");
print "Content-type:text/html\n\n";


my %action;
my  $form = new CGI;
$action{view} = $form->param('view');
$action{action} = $form->param('action');
$action{name} = $form->param('name');
$action{enable_value} = $form->param('enable_value');
$action{port} = $form->param('port');
my @quota=$form->param('quota');
$action{quota}=\@quota;

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"><script type="text/javascript" src="jquery-1.9.1.min.js"></script><script type="text/javascript" src="qb.js"></script>);
print qq(<style type="text/css">button.menu{width:70;height:18;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;margin-right: 5px;}</style></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

print qq (<button onclick="parent.mainFrame.location='quota_status.cgi?view=port'" style="width:200" hidefocus="true" class="menu">Quota by Link</button>);
print qq (<button onclick="parent.mainFrame.location='quota_status.cgi?view=policy'" style="width:200" hidefocus="true" class="menu">Quota by Policy</button>);
print qq (<button onclick="parent.mainFrame.location='quota_status.cgi?view=ip'" style="width:250" hidefocus="true" class="menu">Quota by Authenticated Users</button>);
#=================================================================================
#print '<button class="menu"  onclick="mainframe.location=\'rttraffic.cgi?page_now=1&amp;ispnum=10&amp;spool=ID\'"     style="width:120">'.$qblang[408].'</button>';
#print '<button class="menu"  onclick="mainframe.location=\'autoquery.htm\'"     style="width:200">'.$qblang[409].'</button>';
#print '<button class="menu"  onclick="mainframe.location=\'manualquery.htm\'"     style="width:160">'.$qblang[410].'</button>';
#print '<button class="menu"  onclick="mainframe.location=\'rate_status.php\'"     style="width:180">'.$qblang[411].'</button>';
#print '<button class="menu"  onclick="mainframe.location=\'sessions_status_src.php\'"     style="width:160">'.$qblang[412].'</button>';
#print '<button class="menu"  onclick="mainframe.location=\'sessions_status_nat.php\'"     style="width:180">'.$qblang[413].'</button>';
#================================================================================
print qq (<table width="100%" border="0"><tr><td class="qbCopy" align="center">);
print qq (Auto Refresh Per);
print qq (<select name="refreshtime" id="refreshtime">);
my @time=(5,10,15,20,25,30);
foreach my $tm ( @time )
{
    my $status = ( $action{refreshtime} eq $tm ) ? ( 'selected' ) : ( '' );
    print qq(<option value="$tm" $status>$tm</option>);
}
print qq (</select>seconds);
print qq (<input type="button" value="Stop" class="qb" style="width:60" id="switch" onclick="Switch(this.value)">);
print qq (</td></tr></table>);
print qq(<div class="divframe" align="center" id="main">);
print qq(<form name="quotaform" method="post" action="quota_status.cgi">);

showQuotaInfo(%action);
print qq (<input type="hidden" id="action" name="action" value=""/>);
print qq (<input type="hidden" id="name" name="name" value=""/>);
print qq (<input type="hidden" id="view" name="view" value=""/>);
print qq (<input type="hidden" id="enable_value" name="enable_value" value=""/>);
print qq(</form></div></body></html>);

print << "QB";
<script language="javascript">

var myform;
myform=window.document.forms[0];

function selenable(name,value,view)
{
	myform.view.value=view;
	myform.action.value='ENABLED';
	myform.name.value=name;
	myform.enable_value.value=value;
    myform.submit();
	for ( var i=0; i < myform.elements.length; i++)
   	{
       	var ctrlobj=myform.elements[i];
	   	ctrlobj.disabled=true;
	}
}

function delQuota(view)
{
	myform.view.value=view;
    myform.action.value='DELET';
    myform.submit();
}

function resetQuota(name,view)
{
	myform.view.value=view;
	myform.name.value=name;
	myform.action.value='RESETQUOTA';
    myform.submit();
	//alert(myform.gateway.value+' '+myform.action.value);
}

function myrefresh(view)
{
	parent.mainFrame.location='quota_status.cgi?view='+view;
    //window.location.replace('quota_status.cgi?view='+view);
}

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
	if(\$("#switch").val() == "Stop")
	{
    	setTimeout("refresh();",(parseInt(\$("#refreshtime").val()))*1000);
	}
}
function sleep( seconds ) {
	var timer = new Date();
	var time = timer.getTime();
	do
		timer = new Date();
	while( (timer.getTime() - time) < (seconds * 100) );
}
function refresh()
{
	var aa=new Array;
	var yy=new Array;
	var uu=new Array;
	if(\$("#postena").val() == 1)
	{
		\$.get("activequota.pl",{type:\$("#postquota").val()},function(da)
		{
			aa=da.split("-");
			yy=aa[0].split(":");
			uu=aa[1].split(":");
			for(var i = 0 ;yy[i] != null;i++)
			{
				var xx=new Array;
				var zz=new Array;
				xx=yy[i].split(",");
				zz=uu[i].split(",");
				for(var t=0;\$("#num" + t).val() != null;t++)
				{
					var asd = xx[0].split("/");
					if(asd[1] == '1')
					{
						\$("."+asd[0]).html(xx[1]);
					}
					else
					{
						\$("."+asd[0]).html(xx[1]+"/"+zz[1]);
					}
				}
			}
		});
	}
	auto_refresh();
}
auto_refresh();

</script>
QB

if ( $action{action} eq "RESETQUOTA" ) 
{
    quotawork(quotaaction=>'CREAT', LINK=>$action{name});
	print qq(<script>myrefresh('$action{view}')</script>);
}

if ( $action{action} eq "ENABLED" ) 
{
    quotawork(action=>'ENABLED', LINK=>$action{enable_value}, CHECK=>$action{name});
	print qq(<script>myrefresh('$action{view}')</script>);
}
if ( $action{action} eq "DELET" )
{
	my $dosref=XMLread($gPATH.'quota.xml');
	my $doslist=$dosref->{quota};
    my $delet=$action{quota};
    if( @$delet <= 0 )
    {
        $gMSGPROMPT.=qq (Please select some SUBNET first\\n\\n);
        return;
    }
    my @temparray;
    foreach my $item ( @$doslist )
    {
        if ( grep(/^$item->{name}$/, @$delet) )
		{
			LogUserAction( action=>'DELQUOTA', name=>$item->{name} );
			quotawork(action=>'ENABLED', LINK=>0, CHECK=>$item->{name});
			next;
		}
        push(@temparray, $item);
    }
    $dosref->{quota}=\@temparray;
	XMLwrite($dosref, $gPATH."quota.xml");
	print qq(<script>myrefresh('$action{view}')</script>);
}