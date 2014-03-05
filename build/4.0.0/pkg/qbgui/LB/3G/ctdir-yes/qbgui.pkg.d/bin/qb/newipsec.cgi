#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/newipsec.lib");

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
$action{ispname} = $form->param('ispname');
$action{local} = $form->param('local');
$action{remote} = $form->param('remote');
$action{remotename} = $form->param('remotename');
$action{systemip} = $form->param('systemip');
$action{gateway} = $form->param('gateway');
$action{download} = $form->param('download');
$action{upload} = $form->param('upload');
$action{mtu} = $form->param('mtu');
$action{mss} = $form->param('mss');
$action{mtu_value} = $form->param('mtu_value');
$action{mss_value} = $form->param('mss_value');
$action{mpv_nat}=($form->param('mpv_nat')) ? (1) : (0);if ( !$action{mpv_nat} ) { $action{mpv_nat}=0; }
$action{mpv_nat_ip}=$form->param('mpv_nat_ip');
$action{exchange}=$form->param('exchange');
$action{lifetime1}=$form->param('lifetime1');
$action{ph1alg}=$form->param('ph1alg');
$action{ph1hash}=$form->param('ph1hash');
$action{dhgroup}=$form->param('dhgroup');
$action{protocol}=$form->param('protocol');
$action{lifetime2}=$form->param('lifetime2');
$action{ph2alg}=$form->param('ph2alg');
$action{ph2auth}=$form->param('ph2auth');
$action{localsubnet}=$form->param('localsubnet');
$action{remotesubnet}=$form->param('remotesubnet');
$action{type}=$form->param('type');
$action{localid}=$form->param('localid');
$action{localdata}=$form->param('localdata');
$action{remotedata}=$form->param('remotedata');
$action{timeformat1}=$form->param('timeformat1');
$action{timeformat2}=$form->param('timeformat2');
$action{remoteid}=$form->param('remoteid');
$action{dial_num}=$form->param('dial_num');
$action{subnet}=$form->param('subnet');
$action{pfgroup}=$form->param('pfgroup');
$action{presharekey}=$form->param('presharekey');
print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainIPSec( %action ); }

$action{iid} = $gIid;

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="newipsecform" method="post" action="newipsec.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showNewIPSec(%action);
scriptNewIPSec();
print qq (</td></tr>);
print qq (</table>);
print qq (<input type="hidden" class="qbtext" name="action" id="action" value="$action{action}">);
print qq (<input type="hidden" class="qbtext" name="isp" id="isp" value="$action{iid}">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

