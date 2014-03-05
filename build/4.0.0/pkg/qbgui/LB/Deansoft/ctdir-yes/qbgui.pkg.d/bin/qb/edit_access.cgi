#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/access.lib");

print "Content-type:text/html\n\n";

my %action;
my $form=new CGI;

#=========================================================================================
$action{action}=$form->param('action');
$action{source}=$form->param('source');
$action{destination}=$form->param('dest');
$action{actiontype}=$form->param('action_type');
$action{focusedrule}=$form->param('focusedrule');
$action{default_status}=$form->param('default_status');
$action{service}=$form->param('service');
$action{schedule}=$form->param('schedule');
$action{rule_name}=$form->param('rule_name');

#=========================================================================================

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#------- start to draw every form object to interact with users ------------------------------------
print qq (<div class="myframe" align="center">);
print qq (<form name="access_control" method="post" action="edit_access.cgi">);

if ( $action{action} ne '' ){ maintainAccess(%action); }
edit_access( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="keyofrule" value="$keyofrule">);
print qq (<input type="hidden" name="focusedrule" value="">);
print qq (<input type="hidden" name="default_status" value="">);

print qq (</form></div>);


general_script();
access_script();

write_iptables_access_script();
print qq (</body>);
print qq(<head><META http-equiv="Pragma" content="no-cache"><head> );
print qq (</html>);

