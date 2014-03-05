#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/admin.lib";

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

$action{httpsport}=$form->param('httpsport'); #20080925 Brian support user define https port
$action{hostname}=$form->param('hostname'); #20080925 Brian support user define hostname
$action{hostname_lcm}=$form->param('hostname_lcm'); #20110425 Brian hostname on LCM
$action{numofuser}=$form->param('maximumuser');

#$action{rmlogserver}=$form->param('rmlogserver');
#$action{rmusername}=$form->param('rmusername');
#$action{rmpassword}=$form->param('rmpassword');

#20081226 Brian Export config file to ftp server
$action{enablecfgftpserver}=($form->param('enablecfgftpserver') && $form->param('cfgftpserverip')) ? (1) : (0);
$action{ftpmode}=$form->param('ftpmode');if ( !$action{ftpmode} ) { $action{ftpmode}=0; }
$action{cfgftpserverip}=$form->param('cfgftpserverip');
$action{cfgftpusername}=$form->param('cfgftpusername');
$action{cfgftppassword}=$form->param('cfgftppassword');
$action{cfgftpdirectory}=$form->param('cfgftpdirectory');


##############################################
# Set TIMEZONE

##############################################
# Set DATE

my @maillist;
for my $mailcount (1..5)
{
    my $mail=$form->param('mail'.$mailcount);
    if ( !$mail ) { $mail='system'; }
    my %mailhash=(value=>$mail);
    push( @maillist, \%mailhash );
}

$action{mail}=\@maillist;

#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

maintainOverview( %action );
#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="adminform" method="post" action="admin.cgi">);
consoleScript();
showAdmin( %action ); 
print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html>);





