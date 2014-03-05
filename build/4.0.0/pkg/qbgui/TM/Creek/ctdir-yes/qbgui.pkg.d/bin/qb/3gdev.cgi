#!/usr/bin/perl
use CGI;
use Data::Dumper;
require ("qbmod.cgi");
require ("./qblib/3gdev.lib");

#認證是否是經過正常且標準的程序登入進來的
#authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

my $form=new CGI;
my %action;
$action{action}=$form->param('action');

$action{model_3g}=$form->param('model_3g');
$action{module_device_name_info}=$form->param('module_device_name_info');
$action{device_name}=$form->param('device_name');
$action{imei}=$form->param('imei');
$action{interface_name}=$form->param('interface_name');

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body  bgcolor="#336699">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

module_3gScript();

editModules( %action );

print qq (<div align="center">);
print qq (<form name="editModules" method="post" action="3gdev.cgi">);
listModules( %action );
print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="modules_3g" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html> );  

