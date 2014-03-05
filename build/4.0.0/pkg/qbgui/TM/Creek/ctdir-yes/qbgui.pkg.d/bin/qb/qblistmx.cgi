#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
print "Content-type:text/html\n\n";
my $form=new CGI;
my $domain=$form->param('domain');
my $countryname=$form->param('countryname');

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center"><form name="mxform" method="post" action="qblistmx.cgi">);

if ( $countryname ){ listMX($domain,$countryname); }
else { listMX($domain); }

listMXScript();

print qq(</form></div></body></html>);

