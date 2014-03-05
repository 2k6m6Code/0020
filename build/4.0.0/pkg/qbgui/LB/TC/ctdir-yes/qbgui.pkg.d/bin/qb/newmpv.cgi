#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/newmpv.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;

$action{action} = $form->param('action');
$gIid = $action{iid} = $form->param('isp');
$action{state} = $form->param('state');
$action{nic} = $form->param('nic');
$action{alive} = 0;
#$action{downupspeed} = $form->param('downupspeed');
$action{ispname} = $form->param('ispname');
$action{local} = $form->param('local');
$action{remote} = $form->param('remote');
$action{remotename} = $form->param('remotename');
$action{systemip} = $form->param('systemip');
$action{gateway} = $form->param('gateway');
$action{download} = $form->param('download');
$action{port} = $form->param('port');
$action{dport} = 60000;
$action{upload} = $form->param('upload');
$action{mtu} = $form->param('mtu');
$action{mss} = $form->param('mss');
$action{mtu_value} = $form->param('mtu_value');
$action{mss_value} = $form->param('mss_value');
$action{mpv_nat}=($form->param('mpv_nat')) ? (1) : (0);if ( !$action{mpv_nat} ) { $action{mpv_nat}=0; }
$action{mpv_nat_ip}=$form->param('mpv_nat_ip');
$action{ipcom} = $form->param('ipcom') ? (1) : (0);
$action{enc} = $form->param('enc') ? (1) : (0);
$action{alg}= $form->param('algslt');
#$action{algslt}=$form->param('algslt');
$action{poolDownUp} = $form->param('poolDownUp');
$action{poolMtu} = $form->param('poolMtu');
$action{poolMss} = $form->param('poolMss');
$action{poolEnc} = $form->param('poolEnc');
$action{poolComp} = $form->param('poolComp');
$action{poolNaSup} = $form->param('poolNaSup');
$action{poolAlg} = $form->param('poolAlg');
$action{enabletb}=($form->param('enabletb')) ? (1) : (0);if ( !$action{enabletb} ) { $action{enabletb}=0; }

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainMPV( %action ); }

$action{iid} = $gIid;

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="newmpvform" method="post" action="newmpv.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showNewMPV(%action);
scriptNewMPV();
print qq (</td></tr>);
print qq (</table>);
print qq (<input type="hidden" class="qbtext" name="action" id="action" value="$action{action}">);
print qq (<input type="hidden" class="qbtext" name="isp" id="isp" value="$action{iid}">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

