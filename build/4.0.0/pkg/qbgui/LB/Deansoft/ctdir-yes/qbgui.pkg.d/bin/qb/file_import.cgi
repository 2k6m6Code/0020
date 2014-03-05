#!/usr/bin/perl

require("/usr/local/apache/qb/qbmod.cgi");
my $cgi = new CGI;
my $aa;
my $sel = $cgi->param("sel");

$action{action} = $cgi->param("action");
$action{file} = $cgi->param("filename");
#$action{group} = $cgi->param("group");
$action{sel} = $cgi->param("sel");

$aa=XMLread("/usr/local/apache/qbconf/flow.xml");
if($sel eq 'tp'){$aa=XMLread("/usr/local/apache/qbconf/flow_sec.xml");}
my $flow=$aa->{user};

print "Content-type:text/html\n\n";
print qq (<!DOCTYPE html><html><head><meta charset="UTF-8"><link rel="stylesheet" href="../gui.css" type="text/css"></head>);
print qq (<body bgcolor="#336699" text="#ffffff" link="#000040" >);
print qq (<div align="center" style="width: 100%; margin: 12px auto 5px auto;">);

if ( $action{action} ) { maintainImport( %action ); }
#print qq(action:$action{action}  sel:$action{sel});

print qq (<form enctype="multipart/form-data" method="post" action="file_import.cgi" style="width:100%">);
print qq (<input type="hidden" name="sel" id="sel"  value="$sel">);
print qq (<input type="hidden" name="action" id="action"  value="SAVE">);
print qq (<fieldset class="fieldset">);
print qq (<legend class="subtitle">File Import</legend>);
print qq (<table class="body">);
print qq (<tr><td align="center">);
print qq (<input type="file" class="qbtext" id="filename" name="filename" style="width:50">);
#print qq ( to );
#print qq (<select id="group" name="group" value="">);
#foreach my $oo (@$flow)
#{
#	if ($oo->{schname} eq 'system'){next;}
#	print qq (<option value="$oo->{schname}">$oo->{schname}</option>);
#}
#print qq (</select>);
print qq (</td></tr>);
print qq (<tr><td align="center"><input type="submit" value="Submit"></td></tr>);
print qq (</table>); 
print qq (</fieldset>);
print qq (</form>);
#print qq (<script language="javascript"> document.getElementById('group').onchange();</script>);
print qq (</div></body></html>);


sub maintainImport
{
    my (%action)=@_;
	if(!$action{file}){return;}
	my $aa;
	my $file = $action{file};
	my $sel = $action{sel};
	$aa="flow.xml";
	if($sel eq 'tp'){$aa="flow_sec.xml";}
	
    my $schref=XMLread($gPATH.$aa);
    my $schlist=$schref->{user};
    my $exist=0;
    my @subscharrary;
    my %newschedule;

    #$action{schname}=~s/^\s*|\s*$//g;
    
    if ( !$action{action} ) { return; }
    
    if ( $action{action}=~m/^SAVE$/ )
    {
		$basedir = '/tmp';
		$fileName = 'tmp_import';		
		if ($file ne "") 
		{
			open (OUTFILE, ">$basedir/$fileName");
			binmode(OUTFILE);
			while (my $bytesread = read($file, my $buffer, 1024)) {
				print OUTFILE $buffer;
			}
			close (OUTFILE);
		}
		system("cat $basedir/$fileName | tr -d '\r' > $basedir/$fileName.test");
		system("rm -rf $basedir/$fileName");
		
		my %newschedule;
		my $unitname='Default';
		my $unit_description='Default';
		
		open (FILE, "<$basedir/$fileName.test");
		foreach my $outlist( <FILE> ) 
        {
			my @list;
			if(grep(/,/,$outlist)){@list = split(/,/,$outlist);}
			elsif(grep(/;/,$outlist)){@list = split(/;/,$outlist);}
			my %newschedule1;
			$list[1]=~s/\n//g;
			if($list[0] eq '' && $list[1] eq ''){next;}
			elsif($list[0] eq 'Title' && $list[1] ne ''){$unitname=$list[1];}
			elsif($list[0] eq 'Title_description' && $list[1] ne ''){$unit_description=$list[1];}
			elsif($list[0] eq 'IP' && $list[1] eq 'IP_description'){next;}
			else
			{
				my @ip = split(/\./,$list[0]);
				if($ip[0]+0 > 255||$ip[1]+0 > 255||$ip[2]+0 > 255||$ip[0]+0 < 0||$ip[1]+0 < 0||$ip[2]+0 < 0){next;}
				if($ip[3]=~m/\//)
				{
					my @network=split(/\//,$ip[3]);
					if($network[0] > 255||$network[0] < 0){next;}
					if($network[1] > 32||$network[1] < 24){next;}
				}
				elsif($ip[3] > 255 || $ip[3] < 0){next;}
				
				$newschedule1{ip}=$list[0];
				$newschedule1{mail}=$list[1];
				push(@subscharray, \%newschedule1);
			}
		}
		close (FILE);
		
		$newschedule{member}=\@subscharray;
        $newschedule{schname}=$unitname;
		$newschedule{description}=$unit_description;
		
		foreach my $sh ( @$schlist )
        {
			if ( $sh->{schname} eq 'system'){next;}
            if ( $sh->{schname} eq $unitname )
            {
                $exist=1;
                #delete($action{action});
                $sh=\%newschedule;
            }
        }
        if ( $exist eq '0' )
        {
            #delete($action{action});
            push( @$schlist, \%newschedule); 
            @$schlist=sort byName @$schlist;
        }
    }
    XMLwrite($schref, $gPATH.$aa);
	my $callback = 'flow_user.cgi';
	if($sel eq 'tp'){$callback = 'flow_user_sec.cgi'}
	print qq (<script language="javascript">window.opener.location.replace('$callback');window.close();</script>);
}
