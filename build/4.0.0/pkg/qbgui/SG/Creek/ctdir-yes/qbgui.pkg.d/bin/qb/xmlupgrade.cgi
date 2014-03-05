#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

# start to draw every form object to interact with users ------------------------------------
xmlupgScript();

print qq(<div align="center">);

print qq(<form name="xmlupgform" method="post" action="./setuid/runxmlupgrade.cgi" target="result">);

showXMLupg( %action );  

print qq(<input type="hidden" name="action" value="">);

print qq(</form></div>);

general_script();


print qq(</body></html>);
