#!/usr/bin/perl
use Data::Dumper;
use CGI;
require ("qbmod.cgi");
require ("./qblib/neweditdos.lib");
require ("/usr/local/apache/qb/dos_make_shell.cgi");

authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;

$action{option} = $form->param('option');
$action{action} = $form->param('action');
$action{dosip} = $form->param('dosip');
$action{description} = $form->param('description');

$action{newtype} = $form->param('newtype');

$action{newenable} = $form->param('newenable');
$action{newipnum} = $form->param('newipnum');
$action{newportnum} = $form->param('newportnum');
$action{newport} = $form->param('newport');
$action{cls} = $form->param('cls');

$action{newlogset} = $form->param('newlogset');
$action{newtimenumber} = $form->param('newtimenumber');
$action{newtime} = $form->param('newtime');
$action{newlogprefix} = $form->param('newlogprefix');

print qq (<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainCOD( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="newdosform" method="post" action="neweditdos.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);

print qq(<input type="hidden" name="option" id="option" value="$action{option}">);
#===========================================
showEditDos(%action);
scriptEditDos();
#===========================================

print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" id="action" value="$action{action}">);
print qq(<input type="hidden" name="newtype" id="newtype" value="">);
print qq(<input type="hidden" name="newenable" id="newnewenable" value="">);
print qq(<input type="hidden" name="newipnum" id="newipnum" value="">);
print qq(<input type="hidden" name="newportnum" id="newportnum" value="">);
print qq(<input type="hidden" name="newport" id="newport" value="">);
print qq(<input type="hidden" name="newlogset" id="newlogset" value="">);
print qq(<input type="hidden" name="newtimenumber" id="newtimenumber" value="">);
print qq(<input type="hidden" name="newtime" id="newtime" value="">);
print qq(<input type="hidden" name="cls" id="cls" value="">);
print qq(<input type="hidden" name="newlogprefix" id="newlogprefix" value="">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

