#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/editweb.lib");
require ("./qblib/iniweb.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

my $form=new CGI;
my %action;
$action{action}=$form->param('action');

my @rule=$form->param('rule'); 
$action{rule}=\@rule;

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body style="margin:0" bgcolor="#336699" text="#ffffff" link="#ffffff" vlink="#ffffff">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

#maintainIniroute( %action );
#prepareServiceInfo();
#prepareTableInfo();
if ( $action{action} ) { maintianIniweb( %action ); }

list_ini_rule_script();

#print qq(<div style="background-color:#223344>);
print qq(<div style="myframe">);
print qq (<form name="editewebform" method="post" action="editweb.cgi">);

showWebPolicyTitle( %action );

list_webini_rule( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
#print qq (<input type="hidden" name="focusedrule" value="$focusedrule">);
#print qq (<input type="hidden" name="viewpoint" value="$action{viewpoint}">);
#print qq (<input type="hidden" name="sortingkey" value="">);

print qq (</form></div>);

general_script();

print qq(</body></html> );  

