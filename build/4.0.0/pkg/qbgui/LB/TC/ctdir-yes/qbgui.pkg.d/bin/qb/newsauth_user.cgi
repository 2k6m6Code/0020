#!/usr/bin/perl
use CGI;
require ("./qbmod.cgi");
require ("./qblib/newsauth_user.lib");
require ("./qblib/quotawork.lib");

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
$action{d_pwd} = $form->param('d_pwd');
$action{d_mail} = $form->param('d_mail');
$action{d_time} = $form->param('d_time');
$action{d_quota} = $form->param('d_quota');
$action{group_quota} = $form->param('group_quota');
$action{group_name} = $form->param('group_name');
$action{d_qn} = $form->param('d_qn');
$action{d_ql} = $form->param('d_ql');

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"><script type="text/javascript" src="jquery-1.9.1.min.js"></script></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainSchedule( %action ); }
#elsif ( !$gENABLECMS ) { noneFunctionExit('UPG Managemnt is an Option');} #No PPTP server

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="newscheduleform" method="post" action="newsauth_user.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showNewSchedule(%action);
scriptNewSchedule();
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" id="action" name="action" value="$action{action}">);
print qq(<input type="hidden" id="d_ip" name="d_ip" value="">);
print qq(<input type="hidden" id="d_port" name="d_port" value="">);
print qq(<input type="hidden" id="d_pwd" name="d_pwd" value="">);
print qq(<input type="hidden" id="d_mail" name="d_mail" value="">);
print qq(<input type="hidden" id="d_time" name="d_time" value="">);
print qq(<input type="hidden" id="d_quota" name="d_quota" value="">);
print qq(<input type="hidden" id="d_qn" name="d_qn" value="">);
print qq(<input type="hidden" id="d_ql" name="d_ql" value="">);
print qq(<input type="hidden" id="group_name" name="group_name" value="">);
print qq(<input type="hidden" id="group_quota" name="group_quota" value="">);
print qq(</form></div>);
general_script();
print qq(</body></html>);