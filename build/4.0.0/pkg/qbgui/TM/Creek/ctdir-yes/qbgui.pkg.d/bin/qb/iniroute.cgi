#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/quotawork.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my %action;
my $form = new CGI;

#--------------------------------------------------------------------------------------------------
$action{action}=$form->param('action');
$action{viewpoint}=$form->param('viewpoint'); 
$action{source}=$form->param('source');
$action{service}=$form->param('service');
$action{isp}=$form->param('isp');
$action{focusedrule}=$form->param('focusedrule');
$action{quota}=$form->param('quota');
$action{rule_name}=$form->param('rule_name');
$action{showqos}=$form->param('showqos');

#add qos
$action{qos}=$form->param('qos');

#add DropURL
$action{dropurl}=$form->param('dropurl');
#--------------------------------------------------------------------------------------------------
# collect NAT IP information and Judge NAT Method
# important 
$action{method}=$form->param('method');
$action{sipstatus}=$form->param('sipstatus');

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


$action{method}=$form->param('method');
if ( $action{method} eq 'ls' && $ispcount > 0 )             { $action{sip}=[]; }
if ( $action{method} eq 'none' && $ispcount > 0 )           { $action{method}='none'; $action{sip}=[]; }

#if ( $action{method} ne 'ls' && $ispcount==0 )             { $action{method}='none'; }
#if ( $action{method} ne 'ls' && $ispcount > 1 )            { $action{method}='ms'; }
#if ( $action{method} ne 'ls' && $ispcount == 1 )           { $action{method}='ss'; }

#============================================================================================================================
# Pre-processing : when viewpoint is set to nat and service set to *:s, we do as follows
if ( $action{viewpoint}=~m/^nat$/ && $action{service}=~m/:s$/ )
{
    my $ispid=findMyISP(subnet=>$action{source}); 
    
    #============================================================================================================================
    # if the source belongs to a certain ISP, we set to "none" and $action{isp} set to $ispid
    if ( $ispid ) { $action{isp}=$ispid; }

    $action{method}="none"; 
    $action{sip}=[]; 
}


#--------------------------------------------------------------------------------------------------

$action{table}=$form->param('table');
#$action{priority}=$form->param('priority');
$action{priority}=1;
my @schedule=$form->param('schedule'); $action{time}=\@schedule;
$action{advance}=$form->param('advance');
$action{destination}=$form->param('dest');

#schedule object
$action{schedule}=$form->param('schedule');

#-----------------------------------------------------------------------------------------------
# Important : creating key of policy rule  to highlight  matched  rule
my $keyofrule='';
if ( !$action{destination} ) 
{ 
    #$keyofrule=$action{source}.$action{service}.'system'.':'.$action{table};
    $keyofrule=$action{source}.$action{service}.'system'.':'.$action{table}.$action{schedule};
} 
else
{
    #$keyofrule=$action{source}.$action{service}.$action{destination}.':'.$action{table};
    $keyofrule=$action{source}.$action{service}.$action{destination}.':'.$action{table}.$action{schedule};
}

#-----------------------------------------------------------------------------------------------
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

#-----------------------------------------------------------------------------------------------
#if ( $action{action} ){ maintainIniroute( %action ); }
maintainIniroute( %action );

prepareServiceInfo();

prepareTableInfo();

print qq(<div class="myframe">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="prouteform" method="post" action="iniroute.cgi">);

show_iniroute( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="keyofrule" value="$keyofrule">);
print qq (<input type="hidden" name="quota" value="">);
print qq (<input type="hidden" id="rule_name" name="rule_name" value="">);
print qq (<input type="hidden" name="focusedrule" value="">);
print qq(</form>);
print qq(</div>);

general_script();

iniroute_script();

#showResult();

print qq(</body>);
print qq(<head><META http-equiv="Pragma" content="no-cache"><head> );
print qq(</html>);
