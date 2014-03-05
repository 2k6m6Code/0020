#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/dynroute.lib";


#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

use CGI;
use Data::Dumper;

#---------------- read-in form information ------------------------------
my $form=new CGI;
my %action;

###############################################
#GENERAL
$action{action}=$form->param('action');

$action{enabledynroute}=($form->param('enabledynroute')) ? (1) : (0);
$action{protocol}=$form->param('protocol');
$action{metric}=$form->param('metric');
$action{chgtime}=$form->param('chgtime');
#========================================================
# collect virtual mac interface
my @monportarray=$form->param('monport');
my $monport='';
foreach my $eth ( @monportarray ) { $monport.= $eth.':'; }
$monport=~s/:$//g;
$action{monport}=$monport;
 
#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainDynroute( %action ); }

#elsif ( !$gENABLEDYNROUTE) { noneFunctionExit('Dynamic routing is an Option');} #Not support dynamic routing

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center">);
print qq(<form name="dynrouteform" method="post" action="dynroute.cgi">);

print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);

dynrouteScript();

showDynroute( %action ); 

print qq (</td></tr>);
print qq (</table>);
print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

print qq(</body></html>);

