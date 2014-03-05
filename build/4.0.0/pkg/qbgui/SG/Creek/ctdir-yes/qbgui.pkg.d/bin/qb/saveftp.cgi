#!/usr/bin/perl
use CGI;
use Data::Dumper;
require ("qbmod.cgi");

print "Content-type:text/html\n\n";

my $_TEMP=$ENV{'QUERY_STRING'};
#print qq($_TEMP);

my @allvalue=split(/&/,$_TEMP);


my %action;

$action{action}="SAVE";

$action{enablecfgftpserver}=$allvalue[0];
$action{enablecfgftpserver}=~s/enablecfgftpserver=//;

$action{ftpmode}=$allvalue[1];
$action{ftpmode}=~s/ftpmode=//;

$action{cfgftpserverip}=$allvalue[2];
$action{cfgftpserverip}=~s/cfgftpserverip=//;

$action{cfgftpusername}=$allvalue[3];
$action{cfgftpusername}=~s/cfgftpusername=//;

$action{cfgftppassword}=$allvalue[4];
$action{cfgftppassword}=~s/cfgftppassword=//;

$action{cfgftpdirectory}=$allvalue[5];
$action{cfgftpdirectory}=~s/cfgftpdirectory=//;

$action{autofile}=$allvalue[6];
if ($action{autofile} eq 'ture'){$action{autofile}="on"}
$action{autofile}=~s/autofile=//;

maintainOverview( %action );

