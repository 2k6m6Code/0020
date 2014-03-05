#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/inidns.lib");


#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my %action;
my $form = new CGI;

#--------------------------------------------------------------------------------------------------
$action{action}=$form->param('action');
$action{source}=$form->param('source');
$action{schedule}=$form->param('schedule');
$action{rulekey}=$form->param('rulekey');
$action{realip}=$form->param('realip');

#============================================================================================================================
if ( $action{viewpoint}=~m/^nat$/ && $action{service}=~m/:s$/ )
{
    my $ispid=findMyISP(subnet=>$action{source}); 
    
    #============================================================================================================================
    if ( $ispid ) { $action{isp}=$ispid; }

    $action{method}="none"; 
    $action{sip}=[]; 
}


#--------------------------------------------------------------------------------------------------
if ( $action{action} ) { maintianInidns(%action); }

#-----------------------------------------------------------------------------------------------
print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq (<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq (<script type="text/javascript" src="qb.js"></script>);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}
inidnsScript();

#-----------------------------------------------------------------------------------------------
print qq (<div class="myframe">);
#------- start to draw every form object to interact with users --------------------------------
print qq (<form name="inidnsform" method="post" action="inidns.cgi">);

show_inidns( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="rulekey" id="rulekey" value="$action{rulekey}">);
print qq (</form>);
print qq (</div>);

general_script();

#showResult();

print qq(</body>);
print qq(<head><META http-equiv="Pragma" content="no-cache"><head> );
print qq(</html>);
