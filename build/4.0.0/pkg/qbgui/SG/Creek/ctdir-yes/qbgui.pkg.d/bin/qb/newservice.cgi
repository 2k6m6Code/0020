#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/newservice.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{SN} = $form->param('SN');
$action{saveSN} = $form->param('saveSN');
$action{newtcp} = $form->param('newtcp');
$action{newudp} = $form->param('newudp');
$action{newprotocol} = $form->param('newprotocol');
$action{newdescription} = $form->param('newdescription');
$action{exist} = $form->param('exist');


print qq (<html><head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainService( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------

print qq(<form name="serviceform" method="post" action="newservice.cgi">);
print qq (<table class="body" width="500" cellspacing="0" border="0">);
print qq (<tr><td>);
	print qq (<table class="body" width="500" cellspacing="0" border="0">);
    print qq (<tr><td class="bigtitle" colspan="3">Service Settings</td></tr>);
	print qq (<tr><td colspan="3"><hr size=1></td></tr>);
	print qq (<tr><td width="120" align="right">Service Name :</td>);
    print qq (<td width="230" align="center"><input type="text" class="qbtext" align="center" id="SN" name="SN" style="WIDTH:230" value="$action{SN}">);	
	print qq (<input type="hidden" id="saveSN" name="saveSN" value="$action{SN}"/>);
    print qq (</td><td width="150"></td></tr>);
    print qq (<tr><td align="right">TCP : </td>);
    print qq (<td align="center"><input type="text" class="qbtext" id="newtcp" name="newtcp" style="WIDTH:230" value="$action{newtcp}">);
    print qq (</td><td>(e.g. 3344,1234:2345)</td></tr>);
	print qq (<tr><td align="right">UDP :</td>);
    print qq (<td align="center"><input type="text" class="qbtext" id="newudp" name="newudp" style="WIDTH:230" value="$action{newudp}">);	
    print qq (</td><td>(e.g. 3344,1234:2345)</td></tr>);
	print qq (<tr><td align="right">Protocol defined :</td>);
    print qq (<td align="center"><input type="text" class="qbtext" id="newprotocol" name="newprotocol" style="WIDTH:230" value="$action{newprotocol}">);	
    print qq (</td><td></td></tr>);
	print qq (<tr><td align="right">Description :</td>);
	$action{newdescription} =~ s/<br>+/\r\n/g;
    print qq (<td align="center"><textarea class="qbtext" id="newdescription" name="newdescription" style="width:230;height:80">$action{newdescription}</textarea>);	
    print qq (</td></tr>);
	print qq (<tr><td colspan="3"><hr size=1></td></tr>);
	print qq (<tr><td colspan="3" align="center">);
	print qq (<input type="button" class="qb" align="center" value="Save" style="width:60" onClick="SaveService()">);
	print qq (<input type="button" class="qb" align="center" value="Cancel" style="width:60" onClick="window.close()">);
    print qq (</td></tr></table>);
	
scriptNewService();

print qq (</td></tr>);
print qq (</table>);
print qq (<input type="hidden" id="action" name="action" value="$action{action}">);
print qq (<input type="hidden" id="exist" name="exist" value="$action{exist}">);
print qq(</form></div>);

general_script();

print qq(</body></html>);
