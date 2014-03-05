#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

my $form=new CGI;
my %action;
$action{viewpoint}=$form->param('viewpoint');
$action{action}=$form->param('action'); 
$action{focusednat}=$form->param('focusednat');
my @natnets=$form->param('natnets');
$action{natnets}=\@natnets;
$action{sortingkey}=$form->param('sortingkey');

#-------------------------- send html header --------------------------------------
print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq (<body  style="overflow:hidden"  bgcolor="#336699" text="#ffffff" link="#ffffff" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainNAT( %action ); }

#------- pass form information to the procedure of upd;ating  subnet.xml -----------------------------------
print qq(<div class="myframe" style="background-color:#223344;width:100%;height:100%"><form action="shownat.cgi" method="post">);
showNATScript();
showNAT( %action );
print qq(<input type="hidden" name="action"     value="">);
print qq(<input type="hidden" name="focusednat" value="">);
print qq(<input type="hidden" name="sortingkey" value="">);
print qq(<input type="hidden" name="viewpoint"  value="$action{viewpoint}">);
print qq(</form></div>);

general_script();

print qq(</body></html>);
