#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/sslportal.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');
print "Content-type:text/html\n\n";

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);

#假如認證失敗，就直接結束
#if ( !$gLOGINRESULT ) { general_script(); exit;}

# start to draw every form object to interact with users ------------------------------------
print qq (<button  onclick="parent.mainFrame.location='sslinit.cgi'" hidefocus="true" class="menu">SSL Server Configuration</button>);
print qq (<button  onclick="parent.mainFrame.location='ssllogin.cgi'" hidefocus="true" class="menu">SSL User Authentication</button>);
print qq (<button  onclick="parent.mainFrame.location='sslportal.cgi'" hidefocus="true" class="menu">SSL Portal Setting</button>);
print qq(<div align="center">);
print qq(<form enctype="multipart/form-data" name="sslportalform" method="post" action="./setuid/upload.cgi" target="result" >);
print qq (<table cellspacing="0" border="0">);

showSslportal( %action );  

sslportalScript();

print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();


print qq(</body></html>);
