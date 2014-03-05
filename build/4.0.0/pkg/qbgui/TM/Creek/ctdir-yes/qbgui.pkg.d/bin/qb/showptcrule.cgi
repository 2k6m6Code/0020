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
$action{focusedrule}=$form->param('focusedrule');

my @rule=$form->param('rule'); 
$action{rule}=\@rule;

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq (<body  bgcolor="#336699">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

maintainIniroute( %action );

maintainIniroute(action=>'JUDGEDIRTYVALUEOFPOLICY');

prepareServiceInfo();

prepareTableInfo();

showPtcRuleScript();

print qq (<div align="center" class="myframe">);
print qq (<form name="editpruleform" method="post" action="showptcrule.cgi">);

showPtcPolicyTitle( %action );

showPtcRules( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="focusedrule" value="$focusedrule">);
print qq (<input type="hidden" name="viewpoint" value="$action{viewpoint}">);
print qq (<input type="hidden" name="sortingkey" value="">);

print qq (</form></div>);

general_script();

print qq(</body></html>);  

