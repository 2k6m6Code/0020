#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/weburl.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my %action;
my $form = new CGI;

#--------------------------------------------------------------------------------------------------
$action{action}=$form->param('action');
$action{source}=$form->param('source');
$action{isp}=$form->param('isp');
$action{focusedrule}=$form->param('focusedrule');
$action{destination}=$form->param('dest');

$action{filtertype}=$form->param('filter_type');
$action{listname}=$form->param('listname');
$action{schedule}=$form->param('schedule');


#--------------------------------------------------------------------------------------------------
# collect NAT IP information and Judge NAT Method
# important 
#$action{method}=$form->param('method');
#$action{sipstatus}=$form->param('sipstatus');

#my $ispcount=0; my @natsip; my @allnatip=$form->param('sip'); 
#foreach my $natip ( @allnatip ) 
#{ 
#    my ($isp, $ip)=split(/j/, $natip); 
#    my $targetsip; 
#    foreach my $sip ( @natsip ) { if ( $sip->{isp} eq $isp ) { $targetsip=$sip; } }
#    if ( $targetsip ) { $targetsip->{ip}.=','.$ip; }
#    else  { $ispcount++; my %newsip=(isp=>$isp, ip=>$ip); push( @natsip, \%newsip); }
#}
#$action{sip}=\@natsip;


#$action{method}=$form->param('method');
#if ( $action{method} eq 'ls' && $ispcount > 0 )             { $action{sip}=[]; }
#if ( $action{method} eq 'none' && $ispcount > 0 )           { $action{method}='none'; $action{sip}=[]; }

#if ( $action{method} ne 'ls' && $ispcount==0 )             { $action{method}='none'; }
#if ( $action{method} ne 'ls' && $ispcount > 1 )            { $action{method}='ms'; }
#if ( $action{method} ne 'ls' && $ispcount == 1 )           { $action{method}='ss'; }

#============================================================================================================================
# Pre-processing : when viewpoint is set to nat and service set to *:s, we do as follows

#--------------------------------------------------------------------------------------------------

#$action{table}=$form->param('table');
#$action{priority}=$form->param('priority');
#$action{priority}=1;
#my @schedule=$form->param('schedule'); $action{time}=\@schedule;
#$action{advance}=$form->param('advance');

#schedule object
#$action{schedule}=$form->param('schedule');

#-----------------------------------------------------------------------------------------------
# Important : creating key of policy rule  to highlight  matched  rule
my $keyofrule='';
if ( !$action{destination} ) 
{ 
    #$keyofrule=$action{source}.$action{service}.'system'.':'.$action{table};
    $keyofrule=$action{source}.'system'.':'.$action{table};
} 
else
{
    #$keyofrule=$action{source}.$action{service}.$action{destination}.':'.$action{table};
    $keyofrule=$action{source}.$action{destination};
}

#-----------------------------------------------------------------------------------------------
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

#-----------------------------------------------------------------------------------------------
maintainWeburl( %action );


#prepareServiceInfo();

#prepareTableInfo();

print qq(<div class="myframe">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="weburlform" method="post" action="editweburl.cgi">);

edit_weburl( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="keyofrule" value="$keyofrule">);
print qq (<input type="hidden" name="focusedrule" value="">);
print qq(</form>);
print qq(</div>);

general_script();


weburl_script();

#showResult();

print qq(</body>);
print qq(<head><META http-equiv="Pragma" content="no-cache"><head> );
print qq(</html>);
