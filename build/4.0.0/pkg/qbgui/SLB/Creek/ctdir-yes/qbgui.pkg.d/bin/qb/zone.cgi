#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
authenticate(action=>'RANDOMCHECK');
print "Content-type:text/html\n\n";

#read-in form information ------------------------------
#a hash structure to  package form info and then pass it as parameter to  subnet_maintain()  --------------            
my $form=new CGI;
my %action;

###############################################
$action{action}=$form->param('action');
$action{viewpoint}=$form->param('viewpoint');

###############################################
#DMZ
$action{dmzid}=$form->param('dmzid');
$action{dmzenabled}=$form->param('dmzenabled');
$action{dmznic}=$form->param('dmznic');

$action{dmzmode}=$form->param('dmzmode');


###############################################
#NAT
$action{ispid}=$form->param('ispid');
$action{nic_speed}=$form->param('nic_speed');
$action{natroute}=$form->param('natroute');
$action{natid}=$form->param('natid'); 
$action{natnic}=$form->param('natnic');
$action{natnet}=$form->param('natnet');
$action{natip}=$form->param('natip');
$action{version}=$form->param('version');
$action{natenabled}=$form->param('natenabled');
$action{natgateway}=$form->param('natgateway');
$action{natnote}=$form->param('natnote');
$action{type}=$form->param('type');
$action{batcrtdata}=$form->param('batcrtdata');

if ( $gENABLEDHCP )
{
    $action{dhcpinfo}=$form->param('dhcpinfo'); 
    $action{dhcpinfo}=~s/\s//g;
    $action{dhcpinfo}=~s/\n|\r/;/g;
    $action{dhcpinfo}=~s/;+/;/g;
}

my @zonetodel=$form->param('zonetodel');
$action{zonetodel}=\@zonetodel;

#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

#------- if submit pass form information to the procedure of updating  subnet.xml -----------------------------------
my $result;
$result=maintainZone( %action );

if ( $action{action}=~m/^CREATENATZONE$/) { $action{natid}=$result; }

#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center">);
print qq(<form name="zoneform" method="post" action="zone.cgi">);

zone_script();

showZone( %action ); 

print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

print qq(</body></html>);





