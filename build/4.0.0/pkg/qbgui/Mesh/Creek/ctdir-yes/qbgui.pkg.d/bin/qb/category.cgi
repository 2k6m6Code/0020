#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/category.lib";
require "./qblib/editcategory.lib";


#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

use CGI;
use Data::Dumper;

#---------------- read-in form information ------------------------------
my $form=new CGI;
my %action;

###############################################
#GENERAL
$action{action}=$form->param('action');
$action{block}=$form->param('block');
my @categorys=$form->param('categorys');
$action{categorys}=\@categorys;

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

 
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainCategory( %action ); }


#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center">);
print qq(<form name="categoryform" method="post" action="category.cgi">);

print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);

#categoryScript();
scriptCategory();

showCategory( %action ); 

print qq (</td></tr>);
print qq (</table>);
print qq(<input type="hidden" name="action" value="">);
print qq(<input type="hidden" name="block" value="">);
print qq(</form></div>);

general_script();

print qq(</body></html>);

