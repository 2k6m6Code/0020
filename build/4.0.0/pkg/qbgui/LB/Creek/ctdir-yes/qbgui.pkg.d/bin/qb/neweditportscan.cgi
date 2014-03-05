#!/usr/bin/perl
use Data::Dumper;
use CGI;
require ("qbmod.cgi");
require ("./qblib/neweditportscan.lib");
require ("/usr/local/apache/qb/dos_make_shell.cgi");


#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{dosip} = $form->param('dosip');
$action{description} = $form->param('description');

$action{newtype} = $form->param('newtype');

$action{newenable} = $form->param('newenable');
$action{newAN} = $form->param('newAN');
$action{newSR} = $form->param('newSR');
$action{newSF} = $form->param('newSF');
$action{newNF} = $form->param('newNF');
$action{newAA} = $form->param('newAA');
$action{newNN} = $form->param('newNN');
$action{newXM} = $form->param('newXM');

$action{newlogset} = $form->param('newlogset');
$action{newtimenumber} = $form->param('newtimenumber');
$action{newtime} = $form->param('newtime');
$action{newlogprefix} = $form->param('newlogprefix');

print qq (<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainCOD( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="newdosform" method="post" action="neweditportscan.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);

#===========================================
showEditDos(%action);
scriptEditDos();
#===========================================

print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" id="action" value="$action{action}">);
print qq(<input type="hidden" name="newtype" id="newtype" value="">);
print qq(<input type="hidden" name="newenable" id="newnewenable" value="">);
print qq(<input type="hidden" name="newAN" id="newAN" value="">);
print qq(<input type="hidden" name="newSR" id="newSR" value="">);
print qq(<input type="hidden" name="newSF" id="newSF" value="">);
print qq(<input type="hidden" name="newNF" id="newNF" value="">);
print qq(<input type="hidden" name="newAA" id="newAA" value="">);
print qq(<input type="hidden" name="newNN" id="newNN" value="">);
print qq(<input type="hidden" name="newXM" id="newXM" value="">);
print qq(<input type="hidden" name="newlogset" id="newlogset" value="">);
print qq(<input type="hidden" name="newtimenumber" id="newtimenumber" value="">);
print qq(<input type="hidden" name="newtime" id="newtime" value="">);
print qq(<input type="hidden" name="newlogprefix" id="newlogprefix" value="">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

