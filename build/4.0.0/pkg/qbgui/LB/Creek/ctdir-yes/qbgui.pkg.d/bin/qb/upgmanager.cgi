#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/upgmanager.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{number} = $form->param('number');
$action{upgid} = $form->param('upgid');
#$action{select} = $form->param('select');
#$action{qbtoupgrade} = $form->param('qbtoupgrade');
#$action{reboot_time} = $form->param('reboot_time');

my @qbtoupgrade = $form->param('qbtoupgrade');
$action{qbtoupgrade} = \@qbtoupgrade;

my @reboot_time = $form->param('reboot_time');
$action{reboot_time} = \@reboot_time;


print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainUPG( %action ); }
elsif ( !$gENABLECMS ) { noneFunctionExit('Upgrade Firmware is an Option');} #No PPTP server
print qq (<button  onclick="parent.mainFrame.location='cmsFrmconfig.cgi?viewpoint=managerUPG'" hidefocus="true" class="menu">Upload UPG</button>);
print qq (<button  onclick="parent.mainFrame.location='cmsPkg.cgi'" hidefocus="true" class="menu">Upload Image</button>);
print qq (<button  onclick="parent.mainFrame.location='upgmanager.cgi'" hidefocus="true" class="menu">Upgrade</button>);
print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="upgform" method="post" action="upgmanager.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showUPG(%action);
scriptUPG();
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" value="">);
print qq(<input type="hidden" name="select" value="">);
print qq(</form></div>);

general_script();
print qq(</body></html>);

