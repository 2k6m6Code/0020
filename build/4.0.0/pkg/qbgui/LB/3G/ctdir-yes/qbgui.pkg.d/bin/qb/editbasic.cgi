#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/3gdev.lib");
require ("./qblib/editbasic.lib");
require ("./qblib/quotawork.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');
print "Content-type:text/html\n\n";

#read-in form information ------------------------------
#a hash structure to  package form info and then pass it as parameter to  subnet_maintain()  --------------            
my $form = new CGI;
my %action;
my @tmp_action;

$action{action} = $form->param('action');
@tmp_action = split( /\?/ ,$action{action} );
if ( $tmp_action[0] ) {$action{action} = $tmp_action[0]; }
$action{isptype} = $form->param('isptype');
if ( $tmp_action[1] ) { $action{isptype} = $tmp_action[1]; $action{isptype} =~s/isptype=//; }
if ( $tmp_action[2] )
{
    $action{flag_3g}=$form->param('flag_3g');
    $action{flag_3g} = $tmp_action[2];
    $action{flag_3g} =~s/flag_3g=//;
}
if ( $form->param('flag_3g') eq '1' )
{
    $action{flag_3g}=$form->param('flag_3g');
}
$action{apn_name}=$form->param('apn_name');
$action{interface_name}=$form->param('interface_name');
$action{imei}=$form->param('imei');
$action{dial_num}=$form->param('dial_num');if ( !$action{dial_num} ) { $action{dial_num}='*99#'; }

# 2005-0707 Hammer
$action{basetunnel}=$form->param('basetunnel');

if ( !$action{isptype} ) { $action{isptype}="normal"; }

$action{iid} = $form->param('isp');
$action{state} = $form->param('state');
$action{udmethod}=$form->param('udmethod');
$action{nic}=$form->param('eth');
$action{old_nic}=$form->param('orieth');
$action{algslt}=$form->param('algslt');
$action{alive}=0;     
$action{downupspeed} = $form->param('downupspeed');
$action{pppispid}=$form->param('pppispid');if ( !$action{pppispid} ) { $action{pppispid}=''; }
$action{encrypt_mppe}=($form->param('encrypt_mppe')) ? (1) : (0);if ( !$action{encrypt_mppe} ) { $action{encrypt_mppe}=0; }
$action{compression}=($form->param('compression')) ? (1) : (0);if ( !$action{compression} ) { $action{compression}=0; }
$action{stateless}=($form->param('stateless')) ? (1) : (0);if ( !$action{stateless} ) { $action{stateless}=0; }
$action{enc}=($form->param('enc')) ? (1) : (0);if ( !$action{enc} ) { $action{enc}=0; }
$action{pptpserver}=$form->param('pptpserver');if ( !$action{pptpserver} ) { $action{pptpserver}=''; }
$action{psk}=$form->param('psk');if ( !$action{psk} ) { $action{psk}=''; }
$action{alg}=($form->param('alg')) ? (1) : (0);if ( !$action{alg} ) { $action{alg}="";} 
$action{ipcom}=($form->param('ipcom')) ? (1) : (0);if ( !$action{ipcom} ) { $action{ipcom}=0; }
$action{mpv_nat}=($form->param('mpv_nat')) ? (1) : (0);if ( !$action{mpv_nat} ) { $action{mpv_nat}=0; }
$action{mpv_nat_ip}=$form->param('mpv_nat_ip');
$action{remotesubnet}=$form->param('remotesubnet');if ( !$action{remotesubnet} ) { $action{remotesubnet}=''; }

$action{alias_subnet1}=$form->param('alias_subnet1');if ( !$action{alias_subnet1} ) { $action{alias_subnet1}=''; }

$action{alias_subnet2}=$form->param('alias_subnet2');if ( !$action{alias_subnet2} ) { $action{alias_subnet2}=''; }



$action{localsubnet}=$form->param('localsubnet');if ( !$action{localsubnet} ) { $action{localsubnet}=''; }
$action{lifetime1}=$form->param('lifetime1');if ( !$action{lifteime1} ) { $action{lifteime1}=''; }
$action{lifetime2}=$form->param('lifetime2');if ( !$action{lifetime2} ) { $action{lifetime2}=''; }
$action{presharekey}=$form->param('presharekey');if ( !$action{presharekey} ) { $action{presharekey}=''; }
$action{ph1alg}=$form->param('ph1alg');if ( !$action{ph1alg} ) { $action{ph1alg}=''; }
$action{ph2alg}=$form->param('ph2alg');if ( !$action{ph2alg} ) { $action{ph2alg}=''; }
$action{ph1hash}=$form->param('ph1hash');if ( !$action{ph1hash} ) { $action{ph1hash}=''; }
$action{ph2auth}=$form->param('ph2auth');if ( !$action{ph2auth} ) { $action{ph2auth}=''; }
$action{dhgroup}=$form->param('dhgroup');if ( !$action{dhgroup} ) { $action{dhgroup}=''; }
$action{pfgroup}=$form->param('pfgroup');if ( !$action{pfgroup} ) { $action{pfgroup}=''; }
$action{exchange}=$form->param('exchange');if ( !$action{exchange} ) { $action{exchange}=''; }
$action{wanisp}=$form->param('wanisp');if ( !$action{wanisp} ) { $action{wanisp}=''; }
$action{localid}=$form->param('localid');if ( !$action{localid} ) { $action{localid}=''; }
$action{remoteid}=$form->param('remoteid');if ( !$action{remoteid} ) { $action{remoteid}=''; }
$action{protocol}=$form->param('protocol');if ( !$action{protocol} ) { $action{protocol}=''; }
$action{timeformat1}=$form->param('timeformat1');if ( !$action{timeformat1} ) { $action{timeformat1}=''; }
$action{timeformat2}=$form->param('timeformat2');if ( !$action{timeformat2} ) { $action{timeformat2}=''; }
$action{localdata}=$form->param('localdata');if ( !$action{localdata} ) { $action{localdata}=''; }
$action{remotedata}=$form->param('remotedata');if ( !$action{remotedata} ) { $action{remotedata}=''; }
$action{usbmodemtype}=$form->param('usbmodemtype');if ( !$action{usbmodemtype} ) { $action{usbmodemtype}=''; }
$action{mode_2G3G}=$form->param('mode_2G3G');
$action{band_2G3G}=$form->param('band_2G3G');
$action{traversal_port}=$form->param('traversal_port');
$action{tunnel_role}=$form->param('tunnel_role');
$action{modemaction}=$form->param('modemaction');if ( !$action{modemaction} ) { $action{modemaction}=''; }
$action{daily_3greset}=$form->param('daily_3greset');if ( !$action{daily_3greset} ) { $action{daily_3greset}=''; }
$action{nic_speed}=$form->param('nic_speed');if ( !$action{nic_speed} ) { $action{nic_speed}='Auto'; }
$action{version}=$form->param('version');
my @infoParams=('pppoename', 'pppoepasswd', 'pppoeportdev', 'enableproxy', 'proxyport', 'proxyip', 'proxyname', 'enableddns', 'ddnschoice', 'ddnsname', 'ddnspasswd', 'ddnsdomainname','ispname', 'local', 'remote', 'subnet','gateway','systemip', 'type', 'target', 'upload','download','username','password','enabled','remotename');

foreach my $item ( @infoParams  ) 
{ 
    $action{$item} = $form->param($item); 
    if ( !$action{$item} ) { $action{$item}=''; }  
}

$action{dsip}=1;
#$action{mtu}=( $form->param(mtu) ) ? 1:0;
#$action{mss}=( $form->param(mss) ) ? 1:0;
$action{mtu}= $form->param('mtu');
$action{mss}= $form->param('mss');
$action{mtu_value}= $form->param('mtu_value');
$action{mss_value}= $form->param('mss_value');
#$action{mtu_def}= $form->param('mtu_def');
#$action{mss_def}= $form->param('mss_def');
$action{sortingkey}=$form->param('sortingkey');

$action{newdmit} = $form->param('newdmit');
$action{newdbps} = $form->param('newdbps');
$action{newdown} = $form->param('newdown');

$action{newumit} = $form->param('newumit');
$action{newubps} = $form->param('newubps');
$action{newup} = $form->param('newup');

$action{newtime} = $form->param('newtime');
$action{newcycle} = $form->param('newcycle');
$action{newselectday} = $form->param('newselectday');
$action{newnumber} = $form->param('newnumber');
$action{newquotaport} = $form->param('newquotaport');
$action{DATA} = $form->param('DATA');
$action{enawrite} = $form->param('enawrite');
$action{newtest} = $form->param('newtest');



#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

$action{maintainResult}=1;
#print qq ( action:  $action{action} );
if ( $action{action} ) { $action{maintainResult}=maintainISP(%action); if($action{old_nic} eq '-1' && $action{newtest} eq ''){$action{action}='NEWISPp';} if ($action{maintainResult} eq '0') {$action{action}='GoBack';} }
#if ( $action{action} eq 'NEWISP' ) { $action{iid}=$gNEWISPID; }
if ( $action{action} eq 'DELISP' ) { $action{iid}=''; }

#------- start to draw every form object to interact with users ------------------------------------
basicScript();
print qq(<div align="center">);
print qq(<form name="ispinfoform" method="post" action="editbasic.cgi">);

showISPInfo( %action );

print qq(<input type="hidden" name="action" id="action" value="$action{action}">);
print qq(<input type="hidden" name="sortingkey" value="">);
print qq(<input type="hidden" name="newdmit" id="newdmit" value="">);
print qq(<input type="hidden" name="newdbps" id="newdbps" value="">);
print qq(<input type="hidden" name="newumit" id="newumit" value="">);
print qq(<input type="hidden" name="newubps" id="newubps" value="">);
print qq(<input type="hidden" name="newtime" id="newtime" value="">);
print qq(<input type="hidden" name="newcycle" id="newcycle" value="">);
print qq(<input type="hidden" name="newselectday" id="newselectday" value="">);
print qq(<input type="hidden" name="newnumber" id="newnumber" value="">);
print qq(<input type="hidden" name="newquotaport" id="newquotaport" value="">);
print qq(<input type="hidden" name="DATA" id="DATA" value="">);
print qq(<input type="hidden" name="enawrite" id="enawrite" value="$action{enawrite}">);
print qq(<input type="hidden" name="newtest" id="newtest" value="">);
print qq(</form></div>);

general_script();

print qq(</body></html>);


