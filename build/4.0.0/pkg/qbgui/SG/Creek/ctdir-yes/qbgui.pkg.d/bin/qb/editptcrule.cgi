#!/usr/bin/perl
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
use CGI;
my %action;
my $form = new CGI;

#--------------------------------------------------------------------------------------------------
$action{action}=$form->param('action');
$action{viewpoint}=$form->param('viewpoint'); 
$action{source}=$form->param('source');
$action{service}=$form->param('service');
$action{destination}=$form->param('dest');
$action{table}=$form->param('table');
$action{advance}=$form->param('advance');
$action{isp}=$form->param('isp');


#--------------------------------------------------------------------------------------------------
# QoS setting ...
my @iidlist=maintainBasic(action=>'GETIIDLIST');
my @qossetting;
foreach my $iid ( @iidlist )
{   
    my $imqvalue=nicTranslate('ISP'.$iid.'-OUT');
    my $classid=$form->param($imqvalue);
    my %imqtc=(area=>$imqvalue, classid=>"$classid");
    push( @qossetting, \%imqtc);

    my $imqvalue=nicTranslate('ISP'.$iid.'-IN');
    my $classid=$form->param($imqvalue);
    my %imqtc=(area=>$imqvalue, classid=>"$classid");
    push( @qossetting, \%imqtc);
}

$action{qos}=\@qossetting;
#--------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------
# Important : creating key of policy rule  to highlight  matched  rule
my $keyofrule='';
if ( !$action{destination} ) 
{ 
    $keyofrule=$action{source}.$action{service}.'system'.':'.$action{table};
} 
else
{
    $keyofrule=$action{source}.$action{service}.$action{destination}.':'.$action{table};
}

#-----------------------------------------------------------------------------------------------
$action{keyofrule}=( $form->param('keyofrule') ) ?  ( $form->param('keyofrule') ) : ( $keyofrule ) ; 


#-----------------------------------------------------------------------------------------------
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"><META http-equiv="Pragma" content="no-cache"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

#-----------------------------------------------------------------------------------------------
maintainIniPtc( %action );

print qq(<div class="myframe" align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="prouteform" method="post" action="editptcrule.cgi">);

showIniPtc( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="viewpoint" value="$action{viewpoint}">);
print qq (<input type="hidden" name="keyofrule" value="$action{keyofrule}">);
print qq(</form>);
print qq(</div>);

general_script();

showIniPtcScript();

#showResult();

print qq(</body>);
print qq(</html>);
