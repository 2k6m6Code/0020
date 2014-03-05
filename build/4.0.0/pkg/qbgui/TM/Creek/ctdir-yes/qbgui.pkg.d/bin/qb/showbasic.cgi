#!/usr/bin/perl
use Data::Dumper;
use CGI;
require ("qbmod.cgi");
require ("./qblib/showbasic.lib");
require ("./qblib/editbasic.lib");


#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');

my @selectisp=$form->param('selectisp');
$action{selectisp}=\@selectisp;

$action{iid} = $form->param('isp');

#print qq ( $action{action} );
#print qq (cgi : iid  action{iid}: $action{iid} );


print qq (<html><head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} eq 'DELISP' ) 
{
    maintainISP( %action );
}
elsif ( $action{action} eq 'TEST' ) 
{
    maintainISP( %action );
}
elsif ( $action{action} eq 'ON' |$action{action} eq 'OFF' ) 
{
    maintainShowbasic( %action );
}

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------

print qq(<form name="ispform" method="post" action="showbasic.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showISPList();
basicScript_1();
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" value="$action{action}">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

