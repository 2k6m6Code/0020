#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
print "Content-type:text/html\n\n";

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center"><form name="mxform" method="post" action="qbsetdate.cgi">);

showDate();  

showDateScript();

print qq(</form></div></body></html>);

