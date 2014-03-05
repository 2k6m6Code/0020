#!/usr/bin/perl
require ("/usr/local/apache/qb/language/qblanguage.cgi");
@qblang = QBlanguage();
print "Content-type:text/html\n\n";
use CGI;
#---------------- Just for form to show available items of subnets and services ------------------
my %action;
my $form = new CGI;

#--------------------------------------------------------------------------------------------------
$action{viewpoint}=$form->param('viewpoint'); 
$action{showqos}=$form->param('showqos'); 

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq (<body  style="margin:0" scroll="no" bgcolor="#336699">);
print qq(<script type="text/javascript" src="qb.js"></script>);

my $showTitle='';
#if ( $action{viewpoint} eq 'dmz' )    { $showTitle="Transparent Zone"; }
#elsif ( $action{viewpoint} eq 'nat' ) { $showTitle="Internal Zone"; }
#elsif ( $action{viewpoint} eq 'lvs' ) { $showTitle="Server Mapping"; }

if ( $action{viewpoint} eq 'nat' && $action{showqos} )    { $showTitle='Policy-based QoS'; }
elsif ( $action{viewpoint} eq 'nat' ) { $showTitle=$qblang[187]; }
elsif ( $action{viewpoint} eq 'lvs' ) { $showTitle=$qblang[188]; }

print qq (<table cellspacing="0" cellpadding="0" width="100%" height="100%" border="0">);

#==================================================================================================
# 1. Display Title 
#==================================================================================================
print qq (<tr><td height="5%">);
#print qq (<br><font class="bigtitle" align="center" >Outbound Policy<font> );
print qq (<br><font class="bigtitle" align="center" >$showTitle<font> );
print qq (<a href="javascript:qbShowHelp('policy')"><image src="image/help.gif" border="0" title="Help"></a><hr size=1>);
print qq (</td></tr>);

#==================================================================================================
# 2. Interface to edit the list of all rules in iniroute.xml
#==================================================================================================
print qq (<tr><td height="70%" valign="top" align="center">);
my $frameSource='editinirule.cgi'.'?'.'viewpoint='.$action{viewpoint}.'&amp;showqos='.$action{showqos};
print qq (<iframe name="editinirule" scrolling="no" frameborder="0" frameSpacing="0" src="$frameSource" height="100%" width="100%" framespacing="NO"></iframe>);
print qq (</td></tr>);


#==================================================================================================
# 3. Interface to edit selected rule in iniroute.xml
#==================================================================================================
#print qq (<tr><td height="250" align="bottom">);
print qq (<tr><td height="20%" align="bottom">);
print qq (<hr size=1>);
my $frameSource='iniroute.cgi'.'?'.'viewpoint='.$action{viewpoint}.'&amp;showqos='.$action{showqos};
print qq (<iframe name="iniroute" frameborder="0" src="$frameSource" height="100%" width="100%" framespacing="NO"></iframe>);
print qq (</td></tr>);

print qq (</table>);

print qq (</HTML>);

