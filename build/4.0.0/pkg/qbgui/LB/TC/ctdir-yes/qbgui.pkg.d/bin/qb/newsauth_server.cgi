#!/usr/bin/perl
use CGI;
require ("./qbmod.cgi");
require ("./qblib/newsauth_server.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{schname} = $form->param('schname');
$action{description} = $form->param('description');

$action{d_ip} = $form->param('d_ip');
$action{d_port} = $form->param('d_port');
$action{d_group} = $form->param('d_group');
$action{d_domain} = $form->param('d_domain');

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainSchedule( %action ); }
#elsif ( !$gENABLECMS ) { noneFunctionExit('UPG Managemnt is an Option');} #No PPTP server

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="newscheduleform" method="post" action="newsauth_server.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showNewSchedule(%action);
scriptNewSchedule();
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" id="action" name="action" value="$action{action}">);
print qq(<input type="hidden" id="d_ip" name="d_ip" value="">);
print qq(<input type="hidden" id="d_port" name="d_port" value="">);
print qq(<input type="hidden" id="d_group" name="d_group" value="">);
print qq(<input type="hidden" id="d_domain" name="d_domain" value="">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

