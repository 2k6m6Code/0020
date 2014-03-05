#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/auth_option.lib";


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

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css">);
print qq (<style>button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);
print qq(</head><body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#print qq (<button  onclick="parent.mainFrame.location='auth_server.cgi'" hidefocus="true" class="menu">Server</button>);
#print qq (<button  onclick="parent.mainFrame.location='auth_user.cgi'" hidefocus="true" class="menu">Group</button>);
#print qq (<button  onclick="parent.mainFrame.location='auth_option.cgi'" hidefocus="true" class="menu">Option</button>);
#print qq (<button  onclick="parent.mainFrame.location='auth_status.cgi'" hidefocus="true" class="menu">Status</button>);
 
if ( !$gLOGINRESULT ) { general_script(); exit;}

#elsif ( !$gENABLEPPTPSERVER) { noneFunctionExit('PPTP Server is an Option');} #No PPTP server

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center">);
print qq(<form enctype="multipart/form-data" name="rmupgrdform" method="post" action="./test.cgi" target="result">);

print qq (<table cellspacing="0" border="0" style="width:55%;">);
print qq (<tr><td>);

squidgenScript();

showSquidgen( %action ); 

print qq (</td></tr>);
print qq (</table>);
print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();
#squidScript();

print qq(</body></html>);

