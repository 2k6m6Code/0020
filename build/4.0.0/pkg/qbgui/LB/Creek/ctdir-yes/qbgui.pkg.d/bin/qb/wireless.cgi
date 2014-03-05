#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/wireless.lib";


#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

use CGI;
use Data::Dumper;

#---------------- read-in form information ------------------------------
my $form=new CGI;
my %action;

###############################################
#GENERAL
$action{action}=$form->param('action');

$action{enablewirelesslan}=($form->param('enablewirelesslan')) ? (1) : (0);
$action{ssid}=$form->param('ssid');
$action{hidessid}=$form->param('hidessid');
$action{wirelessmode}=$form->param('wirelessmode');
$action{channelmode}=$form->param('channelmode');
#$action{encryptmode}=$form->param('encryptmode');if ( !$action{encryptmode} ) { $action{encryptmode}='NONE'; }
$action{encryptmode}=$form->param('encryptmode');
#$action{authmode}=$form->param('authmode');if ( !$action{authmode} ) { $action{authmode}='OPEN'; }
$action{authmode}=$form->param('authmode');
$action{key_ascii}=$form->param('key_ascii');if ( !$action{key_ascii} ) { $action{key_ascii}='0'; }
$action{wepkey1}=$form->param('wepkey1');
$action{wepkey2}=$form->param('wepkey2');
$action{wepkey3}=$form->param('wepkey3');
$action{wepkey4}=$form->param('wepkey4');
$action{wep_key_num}=$form->param('wep_key_num');
$action{wpakey}=$form->param('wpakey');
$action{wpa_key_ascii}=$form->param('wpa_key_ascii');if ( !$action{wpa_key_ascii} ) { $action{wpa_key_ascii}='0'; }

#=========================================================================================
print qq(<html><head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainWirelessinit( %action ); }
elsif ( !$gENABLEWIRELESS) { noneFunctionExit('Wireless LAN is an Option');} #No Wireless LAN card
#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="wirelessinitform" method="post" action="wireless.cgi">);

wirelessinitScript();

showWirelessinit( %action ); 

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html>);

