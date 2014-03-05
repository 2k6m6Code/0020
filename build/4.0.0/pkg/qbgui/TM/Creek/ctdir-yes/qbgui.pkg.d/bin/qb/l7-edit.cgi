#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/l7-edit.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{AN} = $form->param('AN');
$action{saveAN} = $form->param('saveAN');
$action{newpattern} = $form->param('newpattern');
$action{newdescription} = $form->param('newdescription');
$action{exist} = $form->param('exist');
$action{fromgroup} = $form->param('fromgroup');

my $viewdata = '';
my $status = '';
if($action{AN} ne ''){$status = 'disabled'}
if($action{AN} ne '' && $action{exist} eq '1')
{
	my $path='/usr/local/apache/qbconf/l7-object/';
	find( { wanted => sub { push(@FileList, $_) }, no_chdir => 1 }, $path );
	foreach my $aa (@FileList)
    {
        $aa =~ s/$path//g;
		if (!grep(/\.pat/,$aa)||!grep(/$action{AN}\.pat/,$aa)){next;}
		$aa =~ s/\.pat//g;
		my $aa2 = $aa;
		$aa2 =~ s/_UD//g;
		open(FILE,"<$path$aa\.pat");
		foreach my $data (<FILE>)
		{
			if (grep(/\#/,$data) || $data eq "\n" || grep(/^$aa\n$/,$data)){next;}			
			$viewdata = $data;
		}
		close(FILE);
	}
	
}


print qq (<html><head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainApplication( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------

print qq(<form name="applicationform" method="post" action="l7-edit.cgi">);
print qq (<table class="body" width="300" cellspacing="0" border="0">);
print qq (<tr><td>);
	print qq (<table class="body" width="300" cellspacing="0" border="0">);
    print qq (<tr><td class="bigtitle" colspan="3">Application Setting</td></tr>);
	print qq (<tr><td colspan="3"><hr size=1></td></tr>);
	print qq (<tr><td width="100" align="right">Name :</td>);
    print qq (<td width="200" align="left"><input type="text" class="qbtext" align="center" id="AN" name="AN" style="WIDTH:200" value="$action{AN}" $status>);	
	print qq (<input type="hidden" id="saveAN" name="saveAN" value="$action{AN}"/>);
    print qq (</td></tr>);
	print qq (<tr><td align="right">Pattern :</td>);
    print qq (<td align="left"><input type="text" class="qbtext" align="center" id="newpattern" name="newpattern" style="WIDTH:200" value="$viewdata">);	
    print qq (</td></tr>);
	print qq (<tr><td align="right">Description :</td>);
    print qq (<td align="left"><textarea class="qbtext" id="newdescription" name="newdescription" style="width:200;height:80"></textarea>);	
    print qq (</td></tr>);
	print qq(<tr><td colspan="2"><p align="left" style="border: 5px double rgb(109, 2, 107); cellpadding="1" cellspacing="1" frame="border" rules="none">
        Pattern is a regular expression used to define a software or protocol<br><br>
	An example to define your own pattern:<br>
	To define the HTML Patten.<br>
	1\)Use the <a href="http://www.wireshark.org/">Wireshark</a> or some other softwares which support to catch a certain number of packets.<br>
	2\)Find out the rule from the packets.<br>
	In this example, it is "&lt;html .*&gt;&lt;head&gt;".<br>
	You can type "&lt;html .*&gt;&lt;head&gt;" on the pattern field and give it a name.
</p></td>);
	print qq (<tr><td colspan="2"><hr size=1></td></tr>);
	print qq (<tr><td colspan="2" align="center">);
	print qq (<input type="button" class="qb" align="center" value="Save" style="width:60" onClick="SaveApplication()">);
	print qq (<input type="button" class="qb" align="center" value="Cancel" style="width:60" onClick="appcancel()">);
    print qq (</td></tr></table>);
	
scriptNewApplication();

print qq (</td></tr>);
print qq (</table>);
print qq (<input type="hidden" id="action" name="action" value="$action{action}">);
print qq (<input type="hidden" id="exist" name="exist" value="$action{exist}">);
print qq (<input type="hidden" id="fromgroup" name="fromgroup" value="$action{fromgroup}">);
print qq(</form></div>);

general_script();

print qq(</body></html>);
