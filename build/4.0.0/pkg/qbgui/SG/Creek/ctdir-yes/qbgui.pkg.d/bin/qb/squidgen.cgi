#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/squidgen.lib";


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

$action{isenable}=$form->param('isenable')  ? (1) : (0);
#$action{activex}=$form->param('activex')  ? (1) : (0);
#$action{javascript}=$form->param('javascript')  ? (1) : (0);
#$action{javaapplt}=$form->param('javaapplt')  ? (1) : (0);
#$action{cookies}=$form->param('cookies') ? (1) : (0);

$action{pclist}=$form->param('pclist');
$action{iprange1}=$form->param('iprange1');
$action{iprange2}=$form->param('iprange2');
$action{timehour1}=$form->param('timehour1');
$action{timemin1}=$form->param('timemin1');
$action{timehour2}=$form->param('timehour2');
$action{timemin2}=$form->param('timemin2');
$action{schedule}=$form->param('schedule') ? (1) : (0);
$action{everyday}=$form->param('everyday') ? (1) : (0);
$action{sun}=$form->param('sun') ? (1) : (0);
$action{mon}=$form->param('mon') ? (1) : (0);
$action{tue}=$form->param('tue') ? (1) : (0);
$action{wed}=$form->param('wed') ? (1) : (0);
$action{thu}=$form->param('thu') ? (1) : (0);
$action{fri}=$form->param('fri') ? (1) : (0);
$action{sat}=$form->param('sat') ? (1) : (0);

$action{denymessage}=$form->param('denymessage');

            
#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

 
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainSquidgen( %action ); }

#elsif ( !$gENABLEPPTPSERVER) { noneFunctionExit('PPTP Server is an Option');} #No PPTP server

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center">);
print qq(<form name="squidgenform" method="post" action="squidgen.cgi">);

print qq (<table width="700" cellspacing="0" border="0">);
print qq (<tr><td>);

squidgenScript();

print qq (<tr><td colspan="8" class="bigtitle">Gerenal Setting</td></tr>);
    
#********************************** General Setup*******************************************
print qq (<tr><td colspan="8" bgcolor="#332211" align="left" class="subtitle">[ General Setup ]</td></tr>);
#********************************** ***************************************************
my $squid=XMLread($gPATH.'squidgen.xml');
print qq (<tr>);
print qq (<td class="body" valign="center" align="left" style="height: 50pxi; width: 150px">Enable Web Filtering</td>);
print qq (<td class="body"  valign="center" align="left" style="height: 50px; width: 150px">);
my $status=( $squid->{isenable} ) ? ('checked') : ('');
print qq (<INPUT type="checkbox" name="isenable"  $status >);
print qq (</td></tr>);

showSquidgen( %action ); 

print qq (<tr>);
print qq (<td></td><td>);
print qq (<input class="qb" type="button" align="center" value="Apply" title="Apply All Parameters now !" onClick="goSubmit('SAVE')" style="width:80">);
#print qq (<input class="qb" type="button" align="center" value="Apply" title="Apply All Parameters now !" onClick="SAVE()" style="width:80">);
print qq (</td></tr>);
	
print qq (</td></tr>);
print qq (</table>);
print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();
#squidScript();

print qq(</body></html>);

