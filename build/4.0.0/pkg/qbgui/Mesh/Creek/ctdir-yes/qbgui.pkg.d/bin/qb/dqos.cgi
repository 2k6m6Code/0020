#!/usr/bin/perl
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );
print "Content-type:text/html\n\n";

use CGI;

#---------------- read-in form information ------------------------------
my $form=new CGI;
my %action;

###############################################
#GENERAL
$action{action}=$form->param('action');
$action{topic}=$form->param('topic');
$action{enable}=$form->param('enable') eq "1"?1:0;

$action{lograte}="";
if($form->param('log_enable') eq "1") { $action{lograte} = ( $form->param('lograte') ne "" ? $form->param('lograte')."/".$form->param('lograteunit') :"" ); }

$action{drop}=($form->param('drop')) ? (1) : (0);

$action{logprefix}=$form->param('logprefix');
$action{exception}="";foreach my $item ($form->param('exception')){$action{exception}.=$item.":";} $action{exception}=~s/:$//g;

#QoD
$action{level}='';
foreach my $level ('0x02', '0x04', '0x08', '0x10', '0xff') { $action{level}.=$form->param('level'.$level).':'.$level.';'; }
$action{level}=~s/;$//g;

#PFD
$action{upper}=$form->param('upper');
$action{lower}=$form->param('lower');
if ( $action{upper} < $action{lower} ) { ( $action{upper}, $action{lower} ) = ( $action{lower}, $action{upper} ); }


#PSD
$action{highport}=$form->param('highport');
$action{lowport}=$form->param('lowport');
if ( $action{lowport} < $action{highport} ) { ( $action{lowport}, $action{highport} )=( $action{highport}, $action{lowport} ); }
$action{threshold}=$form->param('threshold');
$action{delay}=$form->param('delay');

#iplimit
$action{above}=$form->param('above');

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>\n);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040" style="text-align:center">\n);

# if the authentication failed, jump to end right now !!
if ( !$gLOGINRESULT ) { general_script(); exit;}

maintainDQOS( %action );

dqosScript( %action );

showDQOS( %action );

#showResult();

general_script();

print qq(</body></html>);

