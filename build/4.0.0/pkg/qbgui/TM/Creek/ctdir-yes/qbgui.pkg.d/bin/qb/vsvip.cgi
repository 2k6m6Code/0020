#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{focusedvip} = $form->param('focusedvip');

my @publiciptodel=$form->param('publiciptodel');
$action{publiciptodel}=\@publiciptodel;

$action{isp_of_vip}=$form->param('isp_of_vip');

$action{viptoappend}=$form->param('set'.$action{isp_of_vip});

print qq (<html><head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainVS( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form id="vsform" name="vsform" method="post" action="vsvip.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
editVIPScript();
editVIP( %action );
print qq (</td></tr>);
print qq (</table>);


print qq(<input type="hidden" id="focusedvip_f" name="focusedvip_f" value="">);
print qq(<input type="hidden" id="isp_of_vip" name="isp_of_vip" value="">);
print qq(<input type="hidden" id="action" name="action" value="">);
print qq(</form></div>);

general_script();

#showResult();

print qq(</body></html>);
