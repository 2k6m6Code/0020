#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
print "Content-type:text/html\n\n";

my $form=new CGI;

my $action=$form->param('action');


#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

listConfigScript();

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center">);
print qq (<form name="configform" method="post" action="">);

listConfig( $action );  

print qq(<input type="hidden" name="action" value="">);
print qq(</form></div></body></html>);

