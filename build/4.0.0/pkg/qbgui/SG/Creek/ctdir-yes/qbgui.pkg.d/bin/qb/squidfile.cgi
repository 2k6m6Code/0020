#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/squidfile.lib";


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

$action{prohibitmulti}=$form->param('prohibitmulti') ? (1) : (0);

$action{mp3}=$form->param('mp3') ? (1) : (0);
$action{mp4}=$form->param('mp4') ? (1) : (0);
$action{wma}=$form->param('wma') ? (1) : (0);
$action{wmv}=$form->param('wmv') ? (1) : (0);
$action{mpg}=$form->param('mpg') ? (1) : (0);
$action{mpeg}=$form->param('mpeg') ? (1) : (0);
$action{rm}=$form->param('rm') ? (1) : (0);
$action{rmvb}=$form->param('rmvb') ? (1) : (0);
$action{avi}=$form->param('avi') ? (1) : (0);
$action{mov}=$form->param('mov') ? (1) : (0);
$action{zip}=$form->param('zip') ? (1) : (0);
$action{rar}=$form->param('rar') ? (1) : (0);
$action{tgz}=$form->param('tgz') ? (1) : (0);
$action{gz}=$form->param('gz') ? (1) : (0);
$action{z7z}=$form->param('z7z') ? (1) : (0);
$action{exe}=$form->param('exe') ? (1) : (0);
$action{bin}=$form->param('bin') ? (1) : (0);
$action{dll}=$form->param('dll') ? (1) : (0);
$action{msi}=$form->param('msi') ? (1) : (0);
$action{bat}=$form->param('bat') ? (1) : (0);
$action{iso}=$form->param('iso') ? (1) : (0);
$action{doc}=$form->param('doc') ? (1) : (0);
$action{pdf}=$form->param('pdf') ? (1) : (0);
$action{ppt}=$form->param('ppt') ? (1) : (0);
$action{reg}=$form->param('reg') ? (1) : (0);
$action{pif}=$form->param('pif') ? (1) : (0);
$action{chm}=$form->param('chm') ? (1) : (0);
$action{vbs}=$form->param('vbs') ? (1) : (0);
$action{scr}=$form->param('scr') ? (1) : (0);
$action{hta}=$form->param('hta') ? (1) : (0);

            
#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

 
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainSquidfile( %action ); }

#elsif ( !$gENABLEPPTPSERVER) { noneFunctionExit('PPTP Server is an Option');} #No PPTP server

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center">);
print qq(<form name="squidfileform" method="post" action="squidfile.cgi">);

print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);

squidfileScript();

showSquidfile( %action ); 

print qq (</td></tr>);
print qq (</table>);
print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

print qq(</body></html>);

