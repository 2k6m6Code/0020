#!/usr/bin/perl 
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";
use CGI;

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;

$action{action} = $form->param('action');

$action{focusedfilter} = $form->param('focusedfilter');

$action{classid} = $form->param('classid');
$action{srcip} = $form->param('srcip');
$action{srcnetnet} = $form->param('srcnetnet');
$action{srcprt} = $form->param('srcprt');
$action{dstip} = $form->param('dstip');
$action{dstnetnet} = $form->param('dstnetnet');
$action{dstprt} = $form->param('dstprt');

#20070823 Brian for Layer7 QOS
$action{l7service} = $form->param('l7service');

$action{tos} = $form->param('tos');
$action{priority} = $form->param('priority');
$action{area} = $form->param('area');
$action{burst} = $form->param('burst');
$action{oc} = $form->param('oc'); if ( !$action{oc} ) { $action{oc}=''; }

my @classtodel = $form->param('classtodel');
$action{classtodel}=\@classtodel;

my @filtertodel = $form->param('filtertodel');
$action{filtertodel}=\@filtertodel;

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);


#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainTC( %action ); }
# 2006/11/28 Brian for S200Lite
if ( $action{action} ) { maintainTC( %action ); }
elsif ( !$gENABLEQOS ) { noneFunctionExit('Service-based Filter is an Option'); }

createClassNicMap();

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="tcform" method="post" action="tcfilter.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
editFilterScript();
editFilter( %action );
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

#showResult();

print qq(</body></html>);
