#!/usr/bin/perl
require ("qbmod.cgi");
authenticate( action=>'RANDOMCHECK' );
print "Content-type:text/html\n\n";
use CGI;

#--Just for form to show available items of subnets and services ------------------
my %action;
my $form = new CGI;

#--------------------------------------------------------------------------------------------------
$action{viewpoint}=$form->param('viewpoint'); 

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body scroll="no" bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<script type="text/javascript" src="qb.js"></script>);
#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

print qq (<table border="0" width="100%" height="100%" cellspacing="0" cellpadding="0">);

my $TITLE=( $action{viewpoint} eq 'lvs' ) ? ('Server Mapping') : ('Internal Zone');

print qq (<tr><td height="5">);
print qq (<font class="bigtitle" align="center" >Subnet / Services<font> );
print qq (<a href="javascript:qbShowHelp('subnet_service')"><image src="image/help.gif" border="0" title="Help"></a><hr size=1></td></tr>);
print qq (</td></tr>);

print qq (<tr><td>);
my $frameSource='shownat.cgi'.'?'.'viewpoint='.$action{viewpoint};
print qq (<iframe name="show" frameborder="0" width="100%" src="$frameSource" height="100%" framespacing="NO"></iframe>);
print qq (</td></tr>);


print qq (<tr height="185"><td align="bottom">);
print qq (<hr size=1>);
my $frameSource='editnat.cgi'.'?'.'viewpoint='.$action{viewpoint};
print qq (<iframe name="edit" frameborder="0" src="$frameSource" height="100%" width="100%" framespacing="NO"></iframe>);
print qq (</td></tr>);

print qq (</table>);

print qq (</body>);
print qq (</html>);

