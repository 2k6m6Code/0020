#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

my $form=new CGI;
my %action;

###############################################
$action{action}=$form->param('action');
$action{configname}=$form->param('configname');
$action{cms}=$form->param('cmsname');

#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html;charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#3399CC" leftmargin="0" topmargin="0" text="#FFFFFF">);
#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} eq 'UPDATE' )
{
    maintainOverview ( %action );
}
else
{
    maintainConfig( %action );
}

configScript();

showConfig( %action ); 

general_script();

print qq(</body></html>);
