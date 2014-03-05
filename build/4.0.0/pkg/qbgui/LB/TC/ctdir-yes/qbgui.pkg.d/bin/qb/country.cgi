#!/usr/bin/perl
use Data::Dumper;
use CGI;
require ("qbmod.cgi");
require ("./qblib/country.lib");
require ("./qblib/editcountry.lib");


#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{countryname} = $form->param('countryname');
my @country=$form->param('country');
$action{country}=\@country;

#print qq (<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#假如認證失敗，就直接結束
print qq(<html><head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);
if ( !$gLOGINRESULT ) { general_script(); exit;}
#print qq (<button  onclick="parent.mainFrame.location='host.cgi'" hidefocus="true" class="menu">Host Object</button>);
#print qq (<button  onclick="parent.mainFrame.location='country.cgi'" hidefocus="true" class="menu">Country Object</button>);
if ( $action{action} ) { maintainCountry( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="countryform" method="post" action="country.cgi">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showCountry(%action);
scriptCountry();
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" id="action" value="$action{action}">);
print qq(<input type="hidden" name="countryname" id="countryname" value="$action{countryname}">);
print qq(</form></div>);
general_script();
print qq(</body></html>);

