#!/usr/bin/perl
use CGI;
use Data::Dumper;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

my $form=new CGI;
my %action;
$action{action}=$form->param('action');

$action{user}=$form->param('user');
$action{newusername}=$form->param('newusername');
$action{newpassword}=$form->param('newpassword');
$action{privilege}=$form->param('privilege');
$action{key}=$form->param('key');
$action{value}=$form->param('value');

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body  bgcolor="#336699">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

userScript();

editUsers( %action );

print qq (<div align="center">);
print qq (<form name="editUser" method="post" action="edituser.cgi">);
listUsers( %action );
print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="user" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html> );  

