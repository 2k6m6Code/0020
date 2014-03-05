#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");

#judge if the user should be kicked out
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#============================================================================
my $form = new CGI;
my %action;
$action{action}=$form->param('action');
$action{destination}=$form->param('destination');

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#003366" text="#ffffff" link="#000040" vlink="#400040" onBlur="window.focus()">);


#------- pass form information to updating  destinations in overview.xml --------------------------
if ( $action{action} ) { maintainOverview( %action); }

#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="editdestform" method="post" action="editdest.cgi">);

print qq(<div align="center">);

print qq(<table border="1" bordercolor="#003366">);

#----------------------------------------
my @destinations=maintainOverview(action=>'GETDESTINATION');

print qq(<tr><td class="body"  bordercolor="#ffffff">);
print qq(<select size="10" class="qbopt" style="width:120" name="destination">\n);
foreach my $dest ( sort @destinations ) 
{ 
  ( $dest eq $action{dest_list} )?( print qq(<option selected value="$dest">$dest\n) ):( print qq(<option value="$dest">$dest\n) ); 
}
print qq(</select></td>);

#--------- 4 different submit button for user do specify which action to take -------
print qq(<td class="body"  bordercolor="#ffffff">);

print << "COMMANDTABLE";
 <table>
  <tr><td class="body"  align="left"><input type="button"  class="qb" value="NEW"    onClick="new_dest()"    style="width:60px"></td></tr>
  <tr><td class="body"  align="left"><input type="button"  class="qb" value="DELETE" onClick="delete_dest()" style="width:60px"></td></tr>
  <tr><td class="body"  align="left"><input type="button"  class="qb" value="EXIT"   onClick="go_to_exit()"  style="width:60px"></td></tr>
  </table>
COMMANDTABLE

print qq(</td></tr></table>);

print qq(</div>);
print qq(<input type="hidden" name="action" value="">);
print qq(</form>);

general_script();

editdest_script();

print qq(</body></html>);


