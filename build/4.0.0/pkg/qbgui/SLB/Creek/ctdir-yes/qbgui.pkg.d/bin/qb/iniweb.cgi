#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/iniweb.lib");


#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my %action;
my $form = new CGI;

#--------------------------------------------------------------------------------------------------
$action{action}=$form->param('action');
$action{source}=$form->param('source');
$action{webfilter}=$form->param('webfilter');
$action{schedule}=$form->param('schedule');
$action{web_action}=$form->param('web_action');
$action{rulekey}=$form->param('rulekey');
$action{realip}=$form->param('realip');

#add qos
#$action{qos}=$form->param('qos');


#$action{method}=$form->param('method');
#if ( $action{method} eq 'ls' && $ispcount > 0 )             { $action{sip}=[]; }
#if ( $action{method} eq 'none' && $ispcount > 0 )           { $action{method}='none'; $action{sip}=[]; }

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
=cut
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
=cut

if ( $action{action} ) { maintianIniweb(%action); }

#-----------------------------------------------------------------------------------------------
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}
iniwebScript();

#-----------------------------------------------------------------------------------------------
print qq(<div class="myframe">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="iniwebform" method="post" action="iniweb.cgi">);

show_iniweb( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="rulekey" value="$action{rulekey}">);
#print qq (<input type="hidden" name="keyofrule" value="$keyofrule">);
#print qq (<input type="hidden" name="focusedrule" value="">);
print qq(</form>);
print qq(</div>);

general_script();

#showResult();

print qq(</body>);
print qq(<head><META http-equiv="Pragma" content="no-cache"><head> );
print qq(</html>);
