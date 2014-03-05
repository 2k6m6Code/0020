#!/usr/bin/perl
use Data::Dumper;
use CGI;
require ("qbmod.cgi");
require ("./qblib/qoslan.lib");


#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;

$action{action} = $form->param('action');
$action{edit} = $form->param('edit');
$action{source} = $form->param('source');
#$action{download} = $form->param('download');
#$action{upload} = $form->param('upload');
$action{uploadmin} = $form->param('uploadmin');
$action{uploadmax} = $form->param('uploadmax');
$action{downloadmin} = $form->param('downloadmin');
$action{downloadmax} = $form->param('downloadmax');
$action{priority} = $form->param('priority');
$action{qostype} = $form->param('qostype');


my @qosrule;
if ( defined($form->param('qosrule')) ) { @qosrule = $form->param('qosrule'); $action{qosrule} = \@qosrule; }

print qq (<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainQoSLAN( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="qoslanform" method="post" action="qoslan.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showqoslan(%action);
scriptqoslan();
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" value="$action{action}">);
print qq(<input type="hidden" name="lan" value="">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

