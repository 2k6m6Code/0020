#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/extroute.lib";

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
$action{extrouteinfo}=$form->param('extrouteinfo');
#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainEXTROUTE(%action); }

#------- start to draw every form object to interact with users ------------------------------------
showEXTROUTEScript();
print qq (<button  onclick="parent.mainFrame.location='zone10.cgi'" hidefocus="true" class="menu">Subnet on DMZ</button>);
print qq (<button  onclick="parent.mainFrame.location='extroute.cgi'" hidefocus="true" class="menu">Subnet on WAN</button>);
  
print qq (<div align="center">);
print qq (<form name="extrouteform" method="post" action="extroute.cgi">);

showEXTROUTE();

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html>);
