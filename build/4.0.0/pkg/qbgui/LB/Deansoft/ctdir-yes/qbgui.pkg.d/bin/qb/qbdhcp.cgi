#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
print "Content-type:text/html\n\n";
my $form=new CGI;
my $natid=$form->param('natid');

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center"><form name="dhcp" method="post" action="qbdhcp.cgi">);

showDHCP($natid);  

showDHCPScript();

print qq(</form></div></body></html>);

