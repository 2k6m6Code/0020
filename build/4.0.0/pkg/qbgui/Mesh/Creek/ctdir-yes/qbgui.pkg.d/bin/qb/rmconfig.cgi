#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
my  $form = new CGI;

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');
print "Content-type:text/html\n\n";

#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

$action{viewpoint} = $form->param('viewpoint');

#if not enable cms show 'UPG is an Otion'
if ( $action{viewpoint} eq 'managerUPG' && !$gENABLECMS ){ noneFunctionExit('Upload Firmware is an Option'); }
elsif ( $action{viewpoint} eq 'managerconfig' && !$gENABLECMS ){ noneFunctionExit('Upload Config is an Option'); }

#假如認證失敗，就直接結束
#if ( !$gLOGINRESULT ) { general_script(); exit;}

# start to draw every form object to interact with users ------------------------------------
rmupgrdScript();

print qq(<div align="center">);
print qq(<form enctype="multipart/form-data" name="rmupgrdform" method="post" action="./setuid/runrmconfig.cgi" target="result" >);

showRmupgrd( %action );  

print qq(<input type="hidden" name="action" id="action" value="">);
print qq(<input type="hidden" name="viewpoint"  id="viewpoint" value="$action{viewpoint}">);
print qq(</form></div>);

general_script();


print qq(</body></html>);
