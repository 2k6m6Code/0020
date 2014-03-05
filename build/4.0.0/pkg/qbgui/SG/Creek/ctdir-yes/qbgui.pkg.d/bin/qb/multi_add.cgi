#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{focusedvip} = $form->param('focusedvip');

my @publiciptodel=$form->param('publiciptodel');
$action{publiciptodel}=\@publiciptodel;

$action{isp_of_vip}=$form->param('isp_of_vip');

$action{viptoappend}=$form->param('set'.$action{isp_of_vip});

print qq (<html><head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainVS( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------

print qq(<form name="vsform" method="post" action="vsvip.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);

print qq (<tr><td class="bigtitle" colspan="2">Add multiple IPs);
print qq (<hr size=1>);

print qq (<tr>);
print qq (<td class="body" align="left" rowspan="2">);
my %isphash=maintainBasic( action=>'GETISPNAMEHASH' );
my @good_iid_list=maintainBasic(action=>'GETGOODNORMALIIDLIST');
print qq (<select sytle="width:80px" id="isp_of_vip" name="isp_of_vip" value="">);

foreach my $ispid ( @good_iid_list ) 
{ 
	print qq (<option value="$ispid">$isphash{$ispid}</option>);
}
print qq (</select>);
foreach my $ispid ( @good_iid_list ) 
{
	print qq (<input type="hidden" class="qbtext" id="set$ispid" name="set$ispid" value="">);
}
print qq (</td>);
print qq (<td class="body" align="left">FORMAT2 := start ip : number of ip<br>);
print qq (<input type="radio" name="sel_format" value="f2" onClick="change_format_radio('f2')">);
print qq (<input type="text" class="qbtext" id="start_ip1" name="start_ip1" onFocus="change_format_radio('f2');" style="WIDTH:150px"> : );
print qq (<input type="text" class="qbtext" id="ip_num" name="ip_num" onFocus="change_format_radio('f2');" style="WIDTH:50px">);
print qq (</td></tr>);

print qq (<tr>);
print qq (<td class="body" align="left">FORMAT3 := start ip - end ip<br>);
print qq (<input type="radio" name="sel_format" value="f3" onClick="change_format_radio('f3')">);
print qq (<input type="text" class="qbtext" id="start_ip" name="start_ip" onFocus="change_format_radio('f3');" style="WIDTH:150px"> - );
print qq (<input type="text" class="qbtext" id="end_ip" name="end_ip" onFocus="change_format_radio('f3');" style="WIDTH:150px">);
print qq (</td></tr>);

print qq (<tr><td colspan="2"><hr size=1></td></tr>);
print qq (<tr><td colspan="2">);
print qq (<div class="body" align="center">);
print qq (<input type="button" class="qb" align="center" value="Add" style="width:60" onClick="myalert()">);
print qq (<input type="button" class="qb" align="center" value="Cancel" style="width:60" onClick="window.close()">);
print qq (<div>);
print qq (</td></tr>);

editVIPScript();
#editVIP( %action );

print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

#showResult();



print qq(</body></html>);
