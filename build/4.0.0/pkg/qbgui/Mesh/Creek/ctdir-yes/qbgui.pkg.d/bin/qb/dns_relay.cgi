#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/sysdns.lib";


#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

use CGI;
use Data::Dumper;

#---------------- read-in form information ------------------------------
my $form=new CGI;
my %action;

###############################################
#GENERAL
$action{action}=$form->param('action');
$action{resolve}=$form->param('resolve');
#$action{dnsserver}=( $form->param('dnsserver') && $form->param('dnsserverip') ) ? (1) : (0);
#$action{dnsserver}=( $form->param('dnsserver') && $form->param('relay') ) ? (1) : (0);
$action{dnsserver}= $form->param('dnsserver');
$action{relay}=($action{dnsserver}) ? ( $form->param('relay') ) : ('');
$action{dnsserverip}=($action{dnsserver}) ? ( $form->param('dnsserverip') ) : ('');
$action{dnsproxyport}=($action{dnsserver}) ? ( $form->param('dnsproxyport') ) : ('');
#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body sytle="margin:0" scroll="AUTO" bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="sysdnsform" method="post" action="sysdns.cgi">);
print qq(<script type="text/javascript" src="qb.js"></script>);


#===================================================================================================
# 1. Display Title
#===================================================================================================
print qq (<div style="margin: auto; text-align: center;" width="100%">);
print qq (<font class="bigtitle" align="center">DNS Relay</font>);
print qq (<br><hr size=1 style="width: 710px;">);
print qq (</div>);

#===================================================================================================
# 2. Interface to edit the list of all rules
#===================================================================================================
print qq (<div style="margin: auto; width: 100%;">);
my $frameSource='editdns.cgi'.'?'.'viewpoint=app';
print qq (<iframe name="editdns" scrolling="no" frameborder="0" frameSpacing="0" src="$frameSource" height="auto" width="60%" framespacing="NO"></iframe>);
print qq (</div>);

#===================================================================================================
# 3. Interface to edit selected rule
#===================================================================================================
print qq (<div style="margin: auto; width: 100%;">);
#print qq (<hr size=1 >);
my $frameSource='inidns.cgi';
print qq (<iframe name="inidns" frameborder="0" src="$frameSource" height="auto" width="60%" framespacing="NO"></iframe>);
print qq (</div>);

# print qq (</table>);

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();






print qq(</body></html>);





