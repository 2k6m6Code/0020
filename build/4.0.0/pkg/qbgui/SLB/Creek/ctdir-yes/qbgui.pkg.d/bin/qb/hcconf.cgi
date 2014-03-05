#!/usr/bin/perl
use CGI;
use Data::Dumper;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- read-in form information ------------------------------
#---------------- a hash structure to  package form info and then pass it as parameter to  subnet_maintain()  --------------            
my $form=new CGI;
my %action;

#==========================================================================================
$action{action}=$form->param('action');

#$action{hcmode}=$form->param('hcmode');
$action{hcmode}="HEALTHYACTION";

$action{hctype}=$form->param('hctype');

#$action{target}=$form->param('target');
$action{target}='';

$action{port}=$form->param('port');

#$action{nospeed}=$form->param('nospeed'); if ( !$action{nospeed} ) { $action{nospeed}=0; }
$action{nospeed}=0; 

$action{nopassive}=$form->param('nopassive'); if ( !$action{nopassive} ) { $action{nopassive}=0; }
#$action{nopassive}=$form->param('nopassive'); if ( !$action{nopassive} ) { $action{nopassive}=1; }#20080414 Brian Disable Passive Line Check By default

#$action{deadnode}=$form->param('deadnode');
$action{deadnode}=3;

#$action{failnode}=$form->param('failnode');
$action{failnode}=3;

#$action{dodfdtime}=$form->param('dodfdtime');
$action{dodfdtime}=0;

#$action{rfddefault}=$form->param('rfddefault');
$action{rfddefault}=7;

$action{timeout}=$form->param('timeout');
$action{connecttimeout}=$form->param('connecttimeout');
$action{traceroutetimeout}=$form->param('traceroutetimeout');
$action{interhctime}=$form->param('interhctime');
$action{pktloss_base_time}=$form->param('pktloss_base_time');if ( !$action{pktloss_base_time} ) { $action{pktloss_base_time}=30; }
$action{enable_latencychk}=$form->param('enable_latencychk');if ( !$action{enable_latencychk} ) { $action{enable_latencychk}=0; }
$action{latency_rate}=$form->param('latency_rate');if ( !$action{latency_rate} ) { $action{latency_rate}=300; }
$action{latency_time}=$form->param('latency_time');if ( !$action{latency_time} ) { $action{latency_time}=30; }
$action{enable_pktlosschk}=$form->param('enable_pktlosschk');if ( !$action{enable_pktlosschk} ) { $action{enable_pktlosschk}=0; }
$action{pktloss_rate}=$form->param('pktloss_rate');if ( !$action{pktloss_rate} ) { $action{pktloss_rate}=50; }
$action{pktloss_time}=$form->param('pktloss_time');if ( !$action{pktloss_time} ) { $action{pktloss_time}=60; }

#=========================================================================================
print qq(<html><head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#------- if submit pass form information to the procedure of updating  subnet.xml --------
maintainHCconf( %action );

#------- start to draw every form object to interact with users --------------------------
print qq(<div align="center">);
print qq(<form name="consoleform" method="post" action="hcconf.cgi">);

showHCconf( %action ); 

print qq(<input type="hidden" name="action" value="">);

print qq(</form></div>);

general_script();

hcconfScript();

print qq(</body></html>);
