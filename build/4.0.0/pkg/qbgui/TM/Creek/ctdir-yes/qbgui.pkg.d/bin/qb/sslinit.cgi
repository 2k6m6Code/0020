#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/sslinit.lib";


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

$action{enablessl}=($form->param('enablessl')) ? (1) : (0);
$action{serverip}=$form->param('serverip');
$action{servername}=$form->param('servername');
$action{protocol}=$form->param('protocol');
$action{port}=$form->param('port');
$action{vpnnet}=$form->param('vpnnet');
$action{netmask}=$form->param('netmask');
$action{max}=$form->param('max');
$action{pridns}=$form->param('pridns');
$action{secdns}=$form->param('secdns');
$action{priwins}=$form->param('priwins');
$action{secwins}=$form->param('secwins');

$action{sltava}=$form->param('sltava');
$action{sltlea}=$form->param('sltlea');
            
#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainSslinit( %action ); }

#elsif ( !$gENABLEPPTPSERVER) { noneFunctionExit('PPTP Server is an Option');} #No PPTP server

#------- start to draw every form object to interact with users ------------------------------------
print qq (<button  onclick="parent.mainFrame.location='sslinit.cgi'" hidefocus="true" class="menu">SSL Server Configuration</button>);
print qq (<button  onclick="parent.mainFrame.location='ssllogin.cgi'" hidefocus="true" class="menu">SSL User Authentication</button>);
print qq (<button  onclick="parent.mainFrame.location='sslportal.cgi'" hidefocus="true" class="menu">SSL Portal Setting</button>);
print qq(<div align="center">);
print qq(<form name="sslinitform" method="post" action="sslinit.cgi">);

print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);

sslinitScript();

showSslinit( %action ); 

print qq (</td></tr>);
print qq (</table>);
print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

print qq(</body></html>);

