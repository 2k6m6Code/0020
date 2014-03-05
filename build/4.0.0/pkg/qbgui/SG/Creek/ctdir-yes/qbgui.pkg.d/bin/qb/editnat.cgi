#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

#read-in form information ------------------------------
#a hash structure to  package form info and then pass it as parameter to  natnet_maintain()  ----
my $form=new CGI;
my %action;

$action{action}=$form->param('action'); 

$action{viewpoint}=$form->param('viewpoint');

my @dservices=$form->param('dservices');
push (@dservices, 'system');
$action{dservices}=\@dservices;

my @sservices=$form->param('sservices');
push (@sservices, 'system');
$action{sservices}=\@sservices;

my $focusednat=$action{focusednat}=$form->param('focusednat'); 

$action{nat_bind_sub}=$form->param('nat_bind_sub');

if ( $action{action}=~m/^APPENDSUBNET$|^UPDATE$/ ) { $focusednat=$action{nat_bind_sub}; }

#------- send html header --------------------------------------
print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq (<body  style="overflow:hidden;margin:0" bgcolor="#336699" text="#ffffff" link="#2030dd" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainNAT( %action ); }

#------- pass form information to the procedure of updating  subnet.xml -----------------------------------
print qq(<div class="myframe">);
print qq (<form name="natnetform" action="editnat.cgi" method="post">);

editNAT( %action );

print qq(<input type="hidden" name="action" value="$action{action}">);
print qq(<input type="hidden" name="focusednat" value="$focusednat">);
print qq(<input type="hidden" name="viewpoint" value="$action{viewpoint}">);
print qq(</form></div>);

general_script();

editNATScript();

print qq(</body></html>);
