#!/usr/bin/perl
print "Content-type:text/html\n\n";
use CGI;

#---------------- Just for form to show available items of subnets and services ------------------
my %action;
my $form = new CGI;

#--------------------------------------------------------------------------------------------------
$action{viewpoint}=$form->param('viewpoint'); 

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq (<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<script type="text/javascript" src="qb.js"></script>);


#==================================================================================================
# 1. Display Title 
#==================================================================================================
print qq (<font class="bigtitle" align="center" >Policy-based Filter Configuration<font> );
print qq (<a href="javascript:qbShowHelp('ptc')"><image src="image/help.gif" border="0" title="Help"></a><hr size=1>);


#==================================================================================================
# 2. Interface to edit the list of all rules in iniroute.xml
#==================================================================================================
my $frameSource='showptcrule.cgi';
print qq (<iframe name="editinirule" frameborder="0" frameSpacing="0" src="$frameSource" height="250" width="100%" framespacing="NO"></iframe>);

print qq (<hr size=1>);

#==================================================================================================
# 3. Interface to edit selected rule in iniroute.xml
#==================================================================================================
my $frameSource='editptcrule.cgi';
print qq (<iframe name="iniroute" frameborder="0" src="$frameSource" height="200" width="100%" framespacing="NO"></iframe>);

print qq (</HTML>);

