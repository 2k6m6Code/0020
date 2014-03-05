#!/usr/bin/perl
use Data::Dumper;
use CGI;
require ("qbmod.cgi");
require ("./qblib/newflood.lib");
require ("./qblib/neweditflood.lib");
require ("/usr/local/apache/qb/dos_make_shell.cgi");


authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{option} = $form->param('option');
$action{action} = $form->param('action');
my @newflood=$form->param('newflood');
$action{newflood}=\@newflood;
my @enable=$form->param('enable');
$action{enable}=\@enable;

print qq (<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainCOD( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="scheduleform" method="post" action="newflood.cgi?option=$action{option}">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
$action{option}= uc($action{option});
print qq(<input type="hidden" name="option" id="option" value="$action{option}">);
#===========================================
showDos(%action);
scriptDos();
#===========================================

print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" id="action" value="">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

