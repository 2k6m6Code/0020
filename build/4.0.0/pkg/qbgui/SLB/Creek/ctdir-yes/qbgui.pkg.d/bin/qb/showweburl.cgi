#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/weburl.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

my $form=new CGI;
my %action;
$action{action}=$form->param('action');
$action{sortingkey}=$form->param('sortingkey');
$action{keyofrule}=$form->param('keyofrule');
$action{focusedrule}=$form->param('focusedrule');
my $enable=$form->param('enable');
$action{enable}=$enable;
#$gMSGPROMPT.=qq ( $action{focusedrule} \\n );

my @rule=$form->param('rule'); 
$action{rule}=\@rule;

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css">);
print qq (</head>);
print qq(<body style="margin:0" bgcolor="#336699" text="#ffffff" link="#ffffff" vlink="#ffffff">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainWeburl( %action ); }
# maintainIniroute(action=>'JUDGEDIRTYVALUEOFPOLICY'); #nancy 040916
#maintainIniroute(action=>'JUDGEDIRTYVALUEOFPOLICY'); #nancy 041029 

list_weburl_script();
#prepareServiceInfo();

#prepareTableInfo();

#list_ini_rule_script();

#print qq(<div style="background-color:#223344>);
print qq(<div style="myframe">);
print qq (<form name="showweburl" method="post" action="showweburl.cgi">);

showWeburlTitle( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="focusedrule" value="$focusedrule">);
print qq (<input type="hidden" name="sortingkey" value="">);

print qq (</form></div>);

general_script();

print qq(</body></html> );  

