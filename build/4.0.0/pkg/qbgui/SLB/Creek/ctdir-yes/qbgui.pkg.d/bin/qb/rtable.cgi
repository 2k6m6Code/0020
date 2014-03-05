#!/usr/bin/perl

use CGI;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#============================================================================
my $form=new CGI;
my %action;

$action{action}=$form->param('action');

$action{focused_rtable}=$form->param('focused_rtable');

$action{backup_table}=$form->param('backup_table');
$action{level}=$form->param('level');
$action{measure_time}=$form->param('measure_time');

$action{wltegress}=$form->param('wltegress'); 

$action{redirect}=$form->param('redirect');
if ( !$action{redirect} ) { $action{redirect}=''; }

$action{vtlc}=( $form->param('vtlc') ) ? 1 : 0; 

$action{equalize}=$form->param('equalize'); 

$action{aggregate}=$form->param('aggregate');

$action{mode}=$form->param('mode');

## Gary test ##############################################################

#$action{tolerance_latency}=$form->param('tolerance_latency');
#$action{latency_diff}=$form->param('latency_diff');

$action{bbl_pool}=$form->param('bbl_pool');
$action{bbl_pool2}=$form->param('bbl_pool2');

#$action{latency_hand}=$form->param('latency_hand');
#$action{latency_hand2}=$form->param('latency_hand2');

if ($action{bbl_pool} eq "latency")
{
    if ($action{bbl_pool2} ne "latency_hand2")
    {
	$action{latency_diff}=$form->param('latency_hand2');
    }
	$action{tolerance_latency}=$form->param('tolerance_latency');
}
if ($action{bbl_pool2} eq "latency")
{
    if ($action{bbl_pool} ne "latency")
    {
	$action{tolerance_latency}=$form->param('latency_hand');
    }
	$action{latency_diff}=$form->param('latency_diff');
}
if ($action{bbl_pool} eq "latency_hand")
{
    if ($action{bbl_pool2} ne "latency")
    {
	$action{latency_diff}=$form->param('latency_hand2');
    }
	$action{tolerance_latency}=$form->param('latency_hand');
}
if ($action{bbl_pool2} eq "latency_hand2")
{
    if ($action{bbl_pool} ne "latency")
    {
	$action{tolerance_latency}=$form->param('latency_hand');
    }
	$action{latency_diff}=$form->param('latency_hand2');
}

$action{enable_latency_tolerance}    =   ($form->param('enable_latency_tolerance'))? 1 : 0;
$action{enable_latency_difference}   =   ($form->param('enable_latency_difference'))? 1 : 0;
$action{enable_pktloss_rate}         =   ($form->param('enable_pktloss_rate'))? 1 : 0;
$action{latency_tolerance}           =   $form->param('latency_tolerance'); if ( !$action{latency_tolerance} && $action{enable_latency_tolerance} == 1 ) { $action{latency_tolerance}=200; }
$action{latency_difference}          =   $form->param('latency_difference'); if ( !$action{latency_difference} && $action{enable_latency_difference} == 1 ) { $action{latency_difference}=50; }
$action{pktloss_rate}                =   $form->param('pktloss_rate'); if ( !$action{pktloss_rate} && $action{enable_pktloss_rate} == 1 ) { $action{pktloss_rate}=20; } 
$action{latency_tolerance_keeptime}  =   $form->param('latency_tolerance_keeptime'); if ( !$action{latency_tolerance_keeptime} ) { $action{latency_tolerance_keeptime}=20; }
$action{latency_difference_keeptime} =   $form->param('latency_difference_keeptime'); if ( !$action{latency_difference_keeptime} ) { $action{latency_difference_keeptime}=20; }
$action{pktloss_rate_keeptime}       =   $form->param('pktloss_rate_keeptime'); if ( !$action{pktloss_rate_keeptime} ) { $action{pktloss_rate_keeptime}=20; }

###########################################################################

$action{tablenote}=$form->param('tablenote');

my @tablestodel=$form->param('tablestodel');
$action{tablestodel}=\@tablestodel;

my @path;
my @iidlist=maintainBasic(action=>'GETIIDLIST');
foreach my $isp (@iidlist) 
{ 
    my $weight=$form->param("weight"."$isp"); if ( !$weight ) { next };
    my %pathitem=(subnet=>$form->param("subnet"."$isp"), isp=>$isp, weight=>$weight, dsip=>$form->param("dsip"."$isp"));
    push(@path,\%pathitem)
}
$action{path}=\@path;

#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}


#------- pass form information to the procedure of updating  rtable.xml -------------------------
if ( $action{action} ) { maintainRtable(%action); }

# Special for "DELETETTABLES"
if ( $action{action} eq "DELETETABLES" &&  grep(/^$action{focused_rtable}$/, @tablestodel) ) { $action{focused_rtable}=''; }

# Special for "CREATETABLE"
if ( $action{action} eq "CREATETABLE" ) { $action{focused_rtable}=$gNEWTABLEID; } 

print qq(<div align="center">);

print qq(<form name="rtableform" method="post" action="rtable.cgi">);

#----------------------------------------------------------------------------------------------
rtable_script();
showRtable( $action{focused_rtable} );

print qq(<input type="hidden" name="action" value="$action{action}">);
print qq(</div>);
print qq(</form>);

general_script();

#showResult();

print qq(</body></html>);


