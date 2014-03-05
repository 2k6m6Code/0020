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

maintainOverview( %action );

#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="sysdnsform" method="post" action="sysdns.cgi">);

consoleScript();
showSysdns( %action ); 

print qq(<script type="text/javascript" src="qb.js"></script>);

print qq (</div>);

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();


print qq(</body></html>);

