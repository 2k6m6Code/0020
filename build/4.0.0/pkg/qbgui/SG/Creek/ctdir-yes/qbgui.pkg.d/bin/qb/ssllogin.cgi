#!/usr/bin/perl
use CGI;
use Data::Dumper;
require ("qbmod.cgi");
require "./qblib/ssllogin.lib";

#認證是否是經過正常且標準的程序登入進來的
#authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

my $form=new CGI;
my %action;
$action{action}=$form->param('action');

$action{user}=$form->param('user');
$action{newusername}=$form->param('newusername');
$action{newpassword}=$form->param('newpassword');
$action{newassignip}=$form->param('newassignip');
$action{key}=$form->param('key');
$action{value}=$form->param('value');

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body  bgcolor="#336699">);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}
#elsif ( !$gENABLEPPTPSERVER) { noneFunctionExit('SSL Server is an Option');} 
userScript();
print qq (<button  onclick="parent.mainFrame.location='sslinit.cgi'" hidefocus="true" class="menu">SSL Server Configuration</button>);
print qq (<button  onclick="parent.mainFrame.location='ssllogin.cgi'" hidefocus="true" class="menu">SSL User Authentication</button>);
print qq (<button  onclick="parent.mainFrame.location='sslportal.cgi'" hidefocus="true" class="menu">SSL Portal Setting</button>);
editsslUsers( %action );
print qq (<div align="center">);
print qq (<form name="editUser" method="post" action="ssllogin.cgi">);
listsslUsers( %action );
print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="user" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html> );  

