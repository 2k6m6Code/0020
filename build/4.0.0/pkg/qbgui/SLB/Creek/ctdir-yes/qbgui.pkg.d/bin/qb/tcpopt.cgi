#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/tcpopt.lib";


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
$action{tcp_opt}=$form->param('tcp_opt');
$action{tcp_source}=$form->param('tcp_source');
#$action{tcp_destination}=$form->param('tcp_destination');
#$action{tcp_dest_port}=$form->param('tcp_dest_port');
$action{enabletcpopt}=($form->param('enabletcpopt')) ? (1) : (0);
$action{tcp_destination}=($action{enabletcpopt}) ? ($form->param('tcp_destination')) : ('');
$action{tcp_dest_port}=($action{enabletcpopt}) ? ($form->param('tcp_dest_port')) : ('');

#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

maintainOverview( %action );

#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="tcpoptform" method="post" action="tcpopt.cgi">);

TCPoptScript();
showTCPopt( %action ); 

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);
general_script();

print qq(</body></html>);

