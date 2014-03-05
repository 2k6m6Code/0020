#!/usr/bin/perl
use CGI;
use Data::Dumper;
require ("qbmod.cgi");
require ("./qblib/3ginfo.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

my $form=new CGI;
my %action;
$action{action}=$form->param('action');

$action{refreshtime}=$form->param('refreshtime');

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body  bgcolor="#336699">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}


print qq (<div align="center">);
print qq (<form name="info_3G_form" method="post" action="3ginfo.cgi">);
showInfo_3G( %action );
print qq (<input type="hidden" name="action" id="action" value="$action{action}">);
print qq (<input type="hidden" name="freshtime" id="freshtime" value="">);
print qq (</form>);
print qq (</div>);
ispScript();

general_script();

print qq(</body></html> );  

