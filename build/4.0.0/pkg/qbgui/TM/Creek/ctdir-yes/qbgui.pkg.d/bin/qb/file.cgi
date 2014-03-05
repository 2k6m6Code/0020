#!/usr/bin/perl
use Data::Dumper;
use CGI;
require ("qbmod.cgi");
require ("./qblib/file.lib");
require ("./qblib/editfile.lib");
#require ("./qblib/newschedule.lib");


#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
my @files=$form->param('files');
$action{files}=\@files;

my @block_files=$form->param('block_files');
$action{block_files}=\@block_files;

print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainFile( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="fileform" method="post" action="file.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showFile(%action);
scriptFile();
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

