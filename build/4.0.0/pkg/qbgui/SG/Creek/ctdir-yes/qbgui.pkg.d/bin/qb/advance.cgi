#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/advance.lib";


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

#$action{sendarp}=$form->param('sendarp');
#$action{igwpermnt}=$form->param('igwpermnt');

#20090706 Brian Modify mss to 1428?
$action{mssmodify}=$form->param('mssmodify'); if ( !$action{mssmodify} ) { $action{mssmodify}=0; }
$action{mssmodify_value}=$form->param('mssmodify_value'); if ( !$action{mssmodify_value} && $action{mssmodify}==1 ) { $action{mssmodify_value}=1428; }
$action{udpmodify}=$form->param('udpmodify'); if ( !$action{udpmodify} ) { $action{udpmodify}=0; }
$action{udpmodify_value}=$form->param('udpmodify_value'); if ( !$action{udpmodify_value} && $action{udpmodify}==1 ) { $action{udpmodify_value}=5; }

#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

maintainOverview( %action );

#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="advanceform" method="post" action="advance.cgi">);

consoleScript();

showAdvance( %action ); 

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html>);

