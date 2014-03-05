#!/usr/bin/perl -w
print "Content-type:text/html\n\n";
use CGI;

#--Just for form to show available items of subnets and services ---------------
my %action;
my $form = new CGI;

#--------------------------------------------------------------------------------------------------
$action{viewpoint}=$form->param('viewpoint'); 

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body style="margin:0" bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

print qq (<table width="100%" height="100%" cellspacing="0" cellpadding="0">);

print qq (<tr><td height="10">);
print qq (<br><font class="bigtitle" align="center" >Transparent Zone &gt; Subnet / Services<font><hr size="1">);
print qq (</td></tr>);

print qq (<tr><td>);
my $frameSource='showdmz.cgi';
print qq (<iframe name="show" scrolling="NO" frameborder="0" frameSpacing="0" src="$frameSource" height="100%" width="100%" framespacing="NO"></iframe>);
print qq (</td></tr>);


print qq (<tr height="230"><td align="bottom">);
print qq (<hr size=1>);
my $frameSource='editdmz.cgi';
print qq (<iframe name="edit" frameborder="0" src="$frameSource" height="100%" width="100%" framespacing="NO"></iframe>);
print qq (</td></tr>);

print qq (</table>);

print qq (</html>);
