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
my $focuseddmz=$action{focuseddmz}=$form->param('focuseddmz');

my @sservices=$form->param('sservices');
push ( @sservices, 'system' );
$action{sservices}=\@sservices;

my @dservices=$form->param('dservices');
push ( @dservices, 'system' );
$action{dservices}=\@dservices;

$action{isp}=$form->param('isp_radio');
$action{dmz_bind_sub}=$form->param($action{isp}.'_seed')."/".$form->param($action{isp}.'_netmask');

if ( $action{action}=~m/^APPENDSUBNET$|^UPDATE$/ ) { $focuseddmz=$action{dmz_bind_sub}; }

#------- send html header --------------------------------------
print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body  style="margin:0" bgcolor="#336699" text="#ffffff" link="#2030dd" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainDMZ( %action ); }

#------- pass form information to the procedure of updating  subnet.xml -----------------------------------
print qq(<div class="myframe">);
print qq (<form name="dmznetform" action="editdmz.cgi" method="post">);

editDMZ( %action );

print qq(<input type="hidden" name="action" value="$action{action}">);
print qq(<input type="hidden" name="focuseddmz" value="$focuseddmz">);
print qq(</form></div>);

general_script();

editDMZScript();

print qq(</body></html>);
