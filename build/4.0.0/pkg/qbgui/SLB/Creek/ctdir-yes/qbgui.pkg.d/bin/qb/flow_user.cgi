#!/usr/bin/perl
use Data::Dumper;
use CGI;
require ("./qbmod.cgi");
require ("./qblib/flow_user.lib");
require ("./qblib/newsflow_user.lib");


#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
my @schedule=$form->param('schedule');
$action{schedule}=\@schedule;

print qq (<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css">);
print qq (<style>button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);
print qq (</head><body bgcolor="#336699" text="#ffffff" link="#000040" >);
print qq (<button  onclick="parent.mainFrame.location='l7log.cgi'" style="width:170" hidefocus="true" class="menu">Log Configuration</button>);
print qq (<button  onclick="parent.mainFrame.location='flow_user.cgi'" style="width:170" hidefocus="true" class="menu">Unit</button>);
print qq (<button  onclick="parent.mainFrame.location='flow_user_sec.cgi'" style="width:170" hidefocus="true" class="menu">Transparent Subnets</button>);
print qq (<button  onclick="parent.mainFrame.location='storage_set.cgi'" style="width:170" hidefocus="true" class="menu">Storage</button>);
#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainSchedule( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="scheduleform" method="post" action="flow_user.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showSchedule(%action);
scriptSchedule();
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" id="action" value="">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

