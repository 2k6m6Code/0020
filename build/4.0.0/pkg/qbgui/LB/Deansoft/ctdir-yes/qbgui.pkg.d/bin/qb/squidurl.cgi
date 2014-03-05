#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/squidurl.lib";


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

$action{trustname}=$form->param('trustname');
$action{trustlist}=$form->param('trustlist');
$action{forbidname}=$form->param('forbidname');
$action{forbidlist}=$form->param('forbidlist');
$action{keywordname}=$form->param('keywordname');
$action{keywordlist}=$form->param('keywordlist');

#$action{facebook}=$form->param('facebook') ? (1) : (0);
#$action{plurk}=$form->param('plurk')? (1) : (0);
#$action{twitter}=$form->param('twitter')? (1) : (0);
#$action{game}=$form->param('game')? (1) : (0);
#$action{ebay}=$form->param('ebay')? (1) : (0);
#$action{shopping}=$form->param('shopping')? (1) : (0);
#$action{sex}=$form->param('porno')? (1) : (0);
#$action{pussy}=$form->param('pussy')? (1) : (0);
#$action{youtobe}=$form->param('youtobe')? (1) : (0);
#$action{blog}=$form->param('blog')? (1) : (0);
#$action{porno}=$form->param('porno')? (1) : (0);

            
#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainSquidurl( %action ); }

#elsif ( !$gENABLEPPTPSERVER) { noneFunctionExit('PPTP Server is an Option');} #No PPTP server

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center">);
print qq(<form name="squidurlform" method="post" action="squidurl.cgi">);

print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);

squidurlScript();

showSquidurl( %action ); 

print qq (</td></tr>);
print qq (</table>);
print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

print qq(</body></html>);

