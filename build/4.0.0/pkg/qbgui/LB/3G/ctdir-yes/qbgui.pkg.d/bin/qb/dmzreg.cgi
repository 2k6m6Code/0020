#!/usr/bin/perl

use CGI;
use Data::Dumper;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

#---------------- a hash structure to  package form info and then pass it as parameter to  subnet_maintain()  --------------            
my %action;
$form=new CGI;
$action{action} = $form->param('action');
$action{isp} = $form->param('isp'); if ( !$action{isp} ) { $action{isp}=0; }
$action{newhostip}=$form->param('newhostip');
my @hostlist = $form->param('dmzhostlist');
$action{hostlist} = \@hostlist;
$action{mode}=$form->param('mode');

##############################################################################################
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

#------- if submit pass form information to the procedure of updating  subnet.xml -----------------------------------

if ( $action{action}=~m/^DELETEHOST$|^ADDHOST$/) { maintainDMZreg( %action ); }

#------- start to draw form object to interact with users ------------------------------------
print qq(<form name="dmzregform" method="post" action="dmzreg.cgi">);

#------ extract subnet information in dmzreg.xml and display them in the format of form object 
#------ to be interact with our users

print qq (<div align="center"><table cellspacing="0" border="0">);

print qq (<tr><td>);

showDMZreg( %action ); 

print qq (</td></tr>);
print qq (</table></div>);

general_script();

dmzreg_script();

print qq(<input type="hidden" name="action" value="">);
print qq(<input type="hidden" name="mode" value="$action{mode}">);
print qq(</form>);
print qq(</body></html>);


