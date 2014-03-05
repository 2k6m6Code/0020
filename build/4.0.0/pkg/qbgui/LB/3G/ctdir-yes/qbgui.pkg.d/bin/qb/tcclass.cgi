#!/usr/bin/perl 
require ("qbmod.cgi");


#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

use CGI;
use Data::Dumper;


#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;

$action{action} = $form->param('action');

$action{focusedclass} = $form->param('focusedclass');
$action{min} = $form->param('min');
$action{max} = $form->param('max');
$action{priority} = $form->param('priority');
$action{area2change} = $form->param('area2change');
$action{default} = $form->param('default');
$action{area} = $form->param('area');
$action{bw} = $form->param('bw');
$action{classid} = $form->param('classid');

my @classtodel = $form->param('classtodel');
$action{classtodel}=\@classtodel;

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);


#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}
# 2006/11/28 Brian for S200Lite
if ( $action{action} ) { maintainTC( %action ); }
elsif ( !$gENABLEQOS ) { noneFunctionExit('QOS Class Definition is an Option'); }

#---- IMPORTANT: if adding a class, need to show on screen the eth that's added. Not the current eth.
if ( $action{action} eq 'APPENDCLASS' && $action{area2change} ne "-1") { $action{area} = $action{area2change}; }


print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="tcform" method="post" action="tcclass.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
editClassScript();
editClass( %action );
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

#showResult();

print qq(</body></html>);
