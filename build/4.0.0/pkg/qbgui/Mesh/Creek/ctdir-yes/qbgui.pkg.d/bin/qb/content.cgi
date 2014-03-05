#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/content.lib";


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

$action{keywordname}=$form->param('keywordname');
$action{keywordlist}=$form->param('keywordlist');
            
$action{activex}=$form->param('activex')  ? (1) : (0);
$action{javascript}=$form->param('javascript')  ? (1) : (0);
$action{javaapplet}=$form->param('javaapplet')  ? (1) : (0);
$action{cookies}=$form->param('cookies') ? (1) : (0);
$action{proxy}=$form->param('proxy') ? (1) : (0);
$action{prohibitmulti}=$form->param('prohibitmulti') ? (1) : (0);

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

 
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainContent( %action ); }

#elsif ( !$gENABLEPPTPSERVER) { noneFunctionExit('PPTP Server is an Option');} #No PPTP server

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center">);
print qq(<form name="contentform" method="post" action="content.cgi">);

print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);

contentScript();

showContent( %action ); 

print qq (</td></tr>);
print qq (</table>);
print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

print qq(</body></html>);

