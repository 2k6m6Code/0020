#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/regist.lib";


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

$action{registername}=$form->param('registername');
$action{registersn}=$form->param('registersn');
$action{registermail}=$form->param('registermail');

#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

#if ( $action{action} ) { maintainTime( %action ); }
maintainOverview( %action );

#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="registform" method="post" action="regist.cgi">);

#RegistScript();
consoleScript();

showRegist( %action ); 

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html>);





