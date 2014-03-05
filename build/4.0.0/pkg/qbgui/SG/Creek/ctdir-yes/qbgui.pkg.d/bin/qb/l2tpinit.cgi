#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/l2tpinit.lib";


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

$action{isenable}=($form->param('isenable')) ? (1) : (0);
$action{servername}=$form->param('servername');
$action{serverip}=$form->param('serverip');
$action{psk}=$form->param('psk');
$action{name}=$form->param('name');
$action{password}=$form->param('password');
$action{iprange1}=$form->param('iprange1');
$action{iprange2}=$form->param('iprange2');


            
#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}
print qq (<button  onclick="parent.mainFrame.location='l2tpinit.cgi'" hidefocus="true" class="menu">L2TP IPsec Configuration</button>);
print qq (<button  onclick="parent.mainFrame.location='l2tplogin.cgi'" hidefocus="true" class="menu">L2TP IPsec Authentication</button>);
  
if ( $action{action} ) { maintainl2tpinit( %action ); }
#elsif ( !$gENABLEPPTPSERVER) { noneFunctionExit('l2tp Server is an Option');} #No PPTP server
#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="l2tpinitform" method="post" action="l2tpinit.cgi">);

l2tpinitScript();

showl2tpinit( %action ); 

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html>);

