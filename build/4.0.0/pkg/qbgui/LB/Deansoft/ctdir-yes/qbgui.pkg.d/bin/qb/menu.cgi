#!/usr/bin/perl
use CGI;

require ("qbmod.cgi");

authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

#---------------- read-in form information ------------------------------
my $form=new CGI;
my %action;

#=========================================================================================
$action{action}=$form->param('action');

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff">);

maintainOverview( %action ); 

print qq (<form name="menuform" method="post" action="menu.cgi">);

show_menu(); 

general_script();

print qq(<input type="hidden" name="action" value="">);

print qq (</form>);

print qq(</body></html>);
