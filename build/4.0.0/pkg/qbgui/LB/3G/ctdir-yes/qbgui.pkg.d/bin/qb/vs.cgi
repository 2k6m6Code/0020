#!/usr/bin/perl -w
print "Content-type:text/html\n\n";
use CGI;
require ("/usr/local/apache/qb/language/qblanguage.cgi");
@qblang = QBlanguage();
#--Just for form to show available items of subnets and services ------------------
my %action;
my $form = new CGI;
my $frameSource='';

#--------------------------------------------------------------------------------------------------
$action{viewpoint}=$form->param('viewpoint'); 

print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body  bgcolor="#336699" text="#ffffff" scroll="no">);
print qq(<script type="text/javascript" src="qb.js"></script>);

print qq (<table border="0" cellspacing="0" cellpadding="0" height="100%" width="100%">);

print qq (<tr height="10"><td>);
print qq (<font class="bigtitle" align="center" >$qblang[183]<font> );
print qq (<a href="javascript:qbShowHelp('server_mapping')"><image src="image/help.gif" border="0" title="Help"></a><hr size=1>);
print qq (</td></tr>);

print qq (<tr><td>);
$frameSource='showvs.cgi';
print qq (<iframe name="show" scrolling="no" frameborder="0" frameSpacing="0" src="$frameSource" height="100%" width="100%" framespacing="NO"></iframe>);
print qq (</td></tr>);

print qq (<tr height="190"><td>);
print qq (<hr size=1>);
$frameSource='editvs.cgi';
print qq (<iframe name="edit" scrolling="no" frameborder="0" src="$frameSource" height="100%" width="100%" framespacing="NO"></iframe>);
print qq (</td></tr>);

print qq (</table>);

print qq (</html>);

