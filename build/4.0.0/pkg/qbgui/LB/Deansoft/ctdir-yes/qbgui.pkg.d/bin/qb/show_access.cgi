#!/usr/bin/perl
use CGI;
require ("/usr/local/apache/qb/language/qblanguage.cgi");
require ("qbmod.cgi");
require ("./qblib/access.lib");
@qblang = QBlanguage();

print "Content-type:text/html\n\n";
#---------------------------------------------------------

my $form=new CGI;
my %action;

#---------------------------------------------------------

$action{action}=$form->param('action');
$action{sortingkey}=$form->param('sortingkey');
$action{keyofrule}=$form->param('keyofrule');
$action{focusedrule}=$form->param('focusedrule');
#$action{setDefault}=$form->param('setDefault');
$action{default_status}=$form->param('default_status');
$action{rule_name}=$form->param('rule_name');

#$gMSGPROMPT.=qq ( setDefault:$action{action} \\n );
#$gMSGPROMPT.=qq ( Default:$action{default_status} \\n );
#$gMSGPROMPT.=qq ( $action{focusedrule},$action{sortingkey},$action{keyofrule} \\n );

my @rule=$form->param('rule'); 
$action{rule}=\@rule;

print qq (<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">);
print qq (<link rel="stylesheet" href="gui.css" type="text/css"></head>);
#print qq (<body style="margin:0" scroll="no" bgcolor="#336699">);

print qq (<body style="margin:0" bgcolor="#336699" text="#ffffff" link="#ffffff" vlink="#ffffff">);
print qq (<table bgcolor="#336699" cellspacing="3" border="0">);


#print qq (<tr><td class="body1">Set default : <select class="qbopt1" size="1" name="default_status" id="default_status" style="WIDTH:130">);
#print qq (<option value="all_allow" title= $status >All allow</option>);
#print qq (<option value="all_deny" title= $status >All deny</option>);
#print qq (</td></tr>);

if ( $action{action} ) { maintainAccess( %action ); }

list_access_script();

#print qq(<div style="background-color:#223344>);
print qq(<div style="myframe">);
print qq (<form name="showaccess" method="post" action="show_access.cgi">);

#---- print access control list ------------
print qq(</body></table>);

showAccessControl( %action );

print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="focusedrule" value="$focusedrule">);
#print qq (<input type="hidden" name="setDefault" value="">);
print qq (<input type="hidden" name="sortingkey" value="">);

print qq (</form></div>);

general_script();

#print qq(</body></html> );  
#print qq(</body></table>);
print qq (</html> );  

