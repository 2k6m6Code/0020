#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/newsergroup.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{sergroup} = $form->param('sergroup');
#my @sltser=$form->param('sltser');
#$action{sltser}=\@sltser;
#$action{sltser}= $form->param('sltser');
$action{serlist} = $form->param('serlist');
$action{description} = $form->param('description');

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainSerGroup( %action ); }
#elsif ( !$gENABLECMS ) { noneFunctionExit('UPG Managemnt is an Option');} #No PPTP server

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="newsergroupform" method="post" action="newsergroup.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showNewSerGroup(%action);
scriptNewSerGroup();
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" id="action" value="$action{action}">);
print qq(<input type="hidden" name="serlist" id="serlist" value="">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

