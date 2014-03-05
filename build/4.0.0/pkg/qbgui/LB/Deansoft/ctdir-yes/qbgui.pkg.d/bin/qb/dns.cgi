#!/usr/bin/perl

use CGI;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- read-in form information ------------------------------
my $form=new CGI;
my %action;
$action{action}=$form->param('action'); 

#read mode
$action{mode}=$form->param('mode');
if ( !$action{mode} ) { $action{mode}="FAILOVER"; }

# read selected isp
$action{isp}=$form->param('isp');

# read GSLB enable and country name
$action{enablegslb}=$form->param('enablegslb');
$action{countryname}=$form->param('countryname');
$action{ns_gslb}=$form->param('ns_gslb');
$action{mx_gslb}=$form->param('mx_gslb');

# read  ttl
$action{ttl}=$form->param('ttl');

# read  weight
$action{weight}=$form->param('weight');

# read priority
$action{priority}=$form->param('priority');

# read new domain information
$action{newdomain}=$form->param('newdomain');

# read  forwarding
$action{forward}=$form->param('forward');

# read domain information
$action{d_name}=$form->param('d_name');

# read domain ip
$action{domainip}=$form->param('domainip');

# read MX information
$action{mx}=$form->param('mx');

# read NS information
$action{ns}=$form->param('ns');

# read host information
$action{hostinfo}=$form->param('dnshostinfo');

#-------------------------- send html header --------------------------------------
print qq (<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq (<body  text="white" bgcolor="#336699">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

#------- pass form information to the procedure of updating  dns.xml -----------------------------------
if ( $action{action} ) { maintainDNS( %action ); }
elsif ( !$gENABLEINBOUND ) { noneFunctionExit('Inbound Load Balance is an Option'); }
# nancy, for S400Lite...041014
 
print qq(<div align="center">);

#------- start to draw every form object to interact with users ------------------------------------
print qq(<form name="dnsform" method="post" action="dns.cgi">);

print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);

dnsScript();

showDNS( %action );

print qq (</td></tr>);
print qq (</table>);
print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

print qq(</body></html>);

