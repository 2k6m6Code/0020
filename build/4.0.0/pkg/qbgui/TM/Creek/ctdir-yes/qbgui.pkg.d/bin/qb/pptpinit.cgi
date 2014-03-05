#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/pptpinit.lib";


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

$action{enableppd}=($form->param('enableppd')) ? (1) : (0);
$action{bsdcompress}=($form->param('bsdcompress')) ? (1) : (0);
$action{deflatecompress}=($form->param('deflatecompress')) ? (1) : (0);
$action{encryption}=($form->param('encryption')) ? (1) : (0);
$action{compression}=($form->param('compression')) ? (1) : (0);
$action{pptpauthmethod}=$form->param('pptpauthmethod');
$action{maxclient}=$form->param('maxclient');
$action{rangelist}=$form->param('rangelist');
$action{idletime}=$form->param('idletime');if ( !$action{idletime} ) { $action{idletime}=0; }

$action{dnsip1}=$form->param('dnsip1');
$action{dnsip2}=$form->param('dnsip2');
$action{iprange1}=$form->param('iprange1');
$action{iprange2}=$form->param('iprange2');

my $ispcount=0; my @natsip; my @allnatip=$form->param('sip');
foreach my $natip ( @allnatip )
{
    my ($isp, $ip)=split(/j/, $natip);
    my $targetsip;
    foreach my $sip ( @natsip ) { if ( $sip->{isp} eq $isp ) { $targetsip=$sip; } }
    if ( $targetsip ) { $targetsip->{ip}.=','.$ip; }
    else  { $ispcount++; my %newsip=(isp=>$isp, ip=>$ip); push( @natsip, \%newsip); }
    }
$action{sip}=\@natsip;
            
#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainPptpinit( %action ); }
elsif ( !$gENABLEPPTPSERVER) { noneFunctionExit('PPTP Server is an Option');} #No PPTP server
#------- start to draw every form object to interact with users ------------------------------------
print qq (<button  onclick="parent.mainFrame.location='pptpinit.cgi'" hidefocus="true" class="menu">PPTP Server Configuration</button>);
print qq (<button  onclick="parent.mainFrame.location='ppdlogin.cgi'" hidefocus="true" class="menu">PPTP User Authentication</button>);
print qq (<div align="center">);
print qq (<form name="pptpinitform" method="post" action="pptpinit.cgi">);

pptpinitScript();

showPptpinit( %action ); 

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html>);

