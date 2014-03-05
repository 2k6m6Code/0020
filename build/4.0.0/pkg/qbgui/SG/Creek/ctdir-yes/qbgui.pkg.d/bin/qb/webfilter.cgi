#!/usr/bin/perl
print "Content-type:text/html\n\n";
use CGI;

#---------------- Just for form to show available items of subnets and services ------------------
my %action;
my $form = new CGI;

#--------------------------------------------------------------------------------------------------
print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq (<body  style="margin:0" scroll="no" bgcolor="#336699">);
print qq (<script type="text/javascript" src="qb.js"></script>);

print qq (<table cellspacing="0" cellpadding="0" width="100%" height="100%" border="0">);

#==================================================================================================
# 1. Display Title 
#==================================================================================================
print qq (<tr><td height="10">);
print qq (<br><font class="bigtitle" align="center" >Category Filtering<font> );
print qq (<hr size=1>);
print qq (</td></tr>);

#==================================================================================================
# 2. Interface to edit the list of all rules 
#==================================================================================================
print qq (<tr><td valign="top" align="center">);
my $frameSource='editweb.cgi'.'?'.'viewpoint=app';
print qq (<iframe name="editweb" scrolling="no" frameborder="0" frameSpacing="0" src="$frameSource" height="100%" width="100%" framespacing="NO"></iframe>);
print qq (</td></tr>);


#==================================================================================================
# 3. Interface to edit selected rule 
#==================================================================================================
print qq (<tr><td height="160" align="bottom">);
print qq (<hr size=1>);
#my $frameSource='iniroute.cgi'.'?'.'viewpoint=app';
#my $frameSource='iniroute.cgi\?viewpoint=nat';
my $frameSource='iniweb.cgi';
print qq (<iframe name="iniweb" frameborder="0" src="$frameSource" height="100%" width="100%" framespacing="NO"></iframe>);
print qq (</td></tr>);

print qq (</table>);

print qq (</HTML>);

