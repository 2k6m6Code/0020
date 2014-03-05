#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/syslog.lib";


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

$action{syslogserver}=($form->param('syslogserver') && $form->param('syslogserverip')) ? (1) : (0);
$action{syslogserverip}=($action{syslogserver}) ? ($form->param('syslogserverip')) : ('');
$action{ftpserver}=($form->param('ftpserver') && $form->param('ftpserverip')) ? (1) : (0);
$action{ftpserverip}=$form->param('ftpserverip');
$action{ftpusername}=$form->param('ftpusername');
$action{ftppassword}=$form->param('ftppassword');
$action{ftpfrequency}=$form->param('ftpfrequency');
$action{ftpdir}=$form->param('ftpdir');
$action{syslogdev}=$form->param('syslogdev');

$action{locallog}=($form->param('locallog')) ? (1) : (0);
$action{serverlog}=($form->param('serverlog')) ? (1) : (0);
$action{kernellog}=($form->param('kernellog')) ? (1) : (0);
$action{squidlog}=($form->param('squidlog')) ? (1) : (0);if ( !$action{squidlog} ) { $action{squidlog}=0; }

#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainSyslog( %action ); }

#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="syslogform" method="post" action="syslog.cgi">);

syslogScript();

showSyslog( %action ); 

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html>);





