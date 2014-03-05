#!/usr/bin/perl

require("/usr/local/apache/qb/qbmod.cgi");
my $cgi = new CGI;
my $aa;
my $sel = $cgi->param("sel");

$action{action} = $cgi->param("action");
$action{file} = $cgi->param("filename");
$action{group} = $cgi->param("group");
$action{sel} = $cgi->param("sel");

$aa=XMLread("/usr/local/apache/qbconf/flow.xml");
if($sel eq 'tp'){$aa=XMLread("/usr/local/apache/qbconf/flow_sec.xml");}
my $flow=$aa->{user};

print "Content-type:text/html\n\n";
print qq (<!DOCTYPE html><html><head><meta charset="UTF-8"><link rel="stylesheet" href="../gui.css" type="text/css"></head>);
print qq (<body bgcolor="#336699" text="#ffffff" link="#000040" >);
print qq (<div align="center" style="width: 100%; margin: 12px auto 5px auto;">);

if ( $action{action} ) { maintainExport( %action ); }
#print qq(action:$action{action}  sel:$action{sel});

print qq (<form enctype="multipart/form-data" method="post" action="file_export.cgi" style="width:100%">);
print qq (<input type="hidden" name="sel" id="sel"  value="$sel">);
print qq (<input type="hidden" name="action" id="action"  value="SAVE">);
print qq (<fieldset class="fieldset">);
print qq (<legend class="subtitle">File Export</legend>);
print qq (<table class="body">);
print qq (<tr><td align="center">File Export :);
print qq (<select id="group" name="group" value="">);
print qq (<option value="Example">Example</option>);
foreach my $oo (@$flow)
{
	if ($oo->{schname} eq 'system'){next;}
	print qq (<option value="$oo->{schname}">$oo->{schname}</option>);
}
print qq (</select>);
print qq (</td></tr>);
print qq (<tr><td align="center"><input type="submit" value="Submit"></td></tr>);
print qq (</table>); 
print qq (</fieldset>);
print qq (</form>);
#print qq (<script language="javascript"> document.getElementById('group').onchange();</script>);
print qq (</div></body></html>);


sub maintainExport
{
    my (%action)=@_;
	if(!$action{group}){return;}
	my $aa;
	my $file = $action{file};
	my $sel = $action{sel};
	$aa="flow.xml";
	if($sel eq 'tp'){$aa="flow_sec.xml";}
	
    my $schref=XMLread($gPATH.$aa);
    my $schlist=$schref->{user};
	
    #$action{schname}=~s/^\s*|\s*$//g;
    
    if ( !$action{action} ) { return; }
    
    if ( $action{action}=~m/^SAVE$/ )
    {
    	system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp");
    	$basedir = '/tmp';
    	$fileName = $action{group}.'.csv';
    	if($action{group} eq 'Example')
    	{
    		system("echo -e 'Title,Example' >> $basedir/tmp_export.csv");
                system("echo -e 'Title_description,Example' >> $basedir/tmp_export.csv");
                system("echo -e ',' >> $basedir/tmp_export.csv");
                system("echo -e 'IP,IP_description' >> $basedir/tmp_export.csv");
                system("/usr/local/apache/qb/setuid/run mv $basedir/tmp_export.csv $basedir/Example.csv");
                print qq (<script language="javascript"> location.replace("unitexport.cgi?file=Example.csv");</script>);
    	}
    	else
    	{
	foreach my $sh ( @$schlist )
        {
		if ($sh->{schname} eq 'system'){next;}
        	if ( $sh->{schname} eq $action{group} )
            	{
			my $member = $sh->{member};
			system("echo -e 'Title,$sh->{schname}' >> $basedir/tmp_export.csv");
			system("echo -e 'Title_description,$sh->{description}' >> $basedir/tmp_export.csv");
			system("echo -e ',' >> $basedir/tmp_export.csv");
			system("echo -e 'IP,IP_description' >> $basedir/tmp_export.csv");
			foreach my $user (@$member)
			{
				if($user->{ip} eq ''){next;}
				system("echo -e '$user->{ip},$user->{mail}' >> $basedir/tmp_export.csv");
			}
            	}
        }
	system("/usr/local/apache/qb/setuid/run mv $basedir/tmp_export.csv $basedir/$fileName");
	print qq (<script language="javascript"> location.replace("unitexport.cgi?file=$fileName");</script>);
	}
    }
}
