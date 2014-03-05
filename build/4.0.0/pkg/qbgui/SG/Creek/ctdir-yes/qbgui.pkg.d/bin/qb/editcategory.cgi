#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/editcategory.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{categoryname} = $form->param('categoryname');
$action{oldcategoryname} = $form->param('oldcategoryname');
$action{description} = $form->param('description');
$action{block} = $form->param('block');

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainCategory( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="editcategoryform" method="post" action="editcategory.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showEditCategory(%action);
scriptEditCategory();
print qq (</td></tr>);
print qq (</table>);
print qq (<input type="hidden" class="qbtext" name="action" value="$action{action}">);
print qq (<input type="hidden" class="qbtext" name="block" value="$action{block}">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

