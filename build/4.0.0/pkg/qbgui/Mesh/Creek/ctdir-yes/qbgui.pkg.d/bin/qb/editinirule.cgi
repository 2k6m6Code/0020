#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

my $form=new CGI;
my %action;
$action{action}=$form->param('action');
$action{sortingkey}=$form->param('sortingkey');
$action{viewpoint}=$form->param('viewpoint');
$action{keyofrule}=$form->param('keyofrule');
$action{rule_priority}=$form->param('rule_priority');
$action{focusedrule}=$form->param('focusedrule');
$action{showqos}=$form->param('showqos');

my @rule=$form->param('rule'); 
$action{rule}=\@rule;

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body style="margin:0" bgcolor="#336699" text="#ffffff" link="#ffffff" vlink="#ffffff">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainIniroute( %action ); }
# maintainIniroute(action=>'JUDGEDIRTYVALUEOFPOLICY'); #nancy 040916
maintainIniroute(action=>'JUDGEDIRTYVALUEOFPOLICY'); #nancy 041029 

prepareServiceInfo();

prepareTableInfo();

list_ini_rule_script();

#print qq(<div style="background-color:#223344>);
print qq(<div style="myframe">);
print qq (<form name="editpruleform" method="post" action="editinirule.cgi">);

showPolicyTitle( %action );

list_ini_rule( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="focusedrule" value="$focusedrule">);
print qq (<input type="hidden" name="rule_priority" value="">);
print qq (<input type="hidden" name="viewpoint" value="$action{viewpoint}">);
print qq (<input type="hidden" name="sortingkey" value="">);
print qq (<input type="hidden" id="showqos" name="showqos" value="$action{showqos}">);

print qq (</form></div>);

general_script();

print qq(</body></html> );  

