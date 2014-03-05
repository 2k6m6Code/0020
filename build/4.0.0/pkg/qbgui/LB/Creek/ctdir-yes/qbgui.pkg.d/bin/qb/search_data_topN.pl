#!/usr/bin/perl

require ("qbmod.cgi");

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
my $service=XMLread($gPATH.'flow.xml');
my $flow=$service->{user};
my $cgi = CGI-> new();
my $tm_time = $cgi->param("time");
my $tm_ip = $cgi->param("ip");
my $tm_limit = $cgi->param("limit");
my $tm_top = $cgi->param("top");
my $tm_symd = $cgi->param("symd");
my @limit = split(/,/,$tm_limit);
my $search='';

my $auth=XMLread('/usr/local/apache/qbconf/auth.xml');
my $auser=$auth->{user};
my $ipaddr=XMLread('/usr/local/apache/qbconf/ipaddr.xml');
my $iplist=$ipaddr->{ipaddress};

if ($limit[1] ne '')
{
    if ($limit[0] eq 'packets')
    {
        $search="-l $limit[1]";
    }elsif ($limit[0] eq 'traffic')
    {
        $search="-L $limit[1]";
    }
}        
print "Content-type: text/html\n\n";
system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp");
system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip > /tmp/test_nfdump");
system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/test_nfdump");

print qq (<table bgcolor="#332211" width="100%" border="0" id="tables">);
open(FILE,"/tmp/test_nfdump");
my $lineCount = 0;
my $top = '1';
my $time = '0';
my $title='0';
my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
my @tmp_data;
foreach my $data (<FILE>)
{
    if (grep(/Top/,$data) || grep(/Blocks/,$data) || grep(/Time/,$data)){next;}
    if (grep(/Summary/,$data)|| grep(/Aggregated/,$data)){next;}
    elsif (grep(/Date/,$data))
    {
        my @tmp = split(/\s{2}/,$data);
	print qq (<thead><tr>);
	print qq(<th style="width: 200px;">Top</th>);
	foreach my $title (@tmp)
	{
	    if ($title eq '' || $title eq 'Date first seen' || $title eq 'Duration Proto' || grep(/pps/,$title)){next;}
	    #$title=~s/Src||Dst//g;
	    $title=~s/\(%\)//g;
	    if (grep(/IP Addr/,$title))
	    {
	        print qq(<th style="width: 200px;">IP addr</th>);
	    }
	    elsif (grep(/Bpp Flows/,$title))
	    {
	        my @tmp = split(/ /,$title);
	        print qq(<th style="width: 200px;">$tmp[0]</th>);
	        print qq(<th style="width: 200px;">$tmp[1]</th>);
	    }
	    else
	    {
	        print qq(<th style="width: 200px;">$title</th>);
	    }
	}
	print qq (</tr></thead>);
    }
    elsif (grep(/Sys/,$data))
    {
    	$data =~ s/^.*Wall://g;
    	$data =~ s/flows\/second:.*$//g;
    	$time = $data;
    	if (grep(/0.000s/,$data))
    	{
    	    $time = '0.001s';
    	}
    	$title = $top - 1;
    }else
    {
        if (grep(/No matched flows/,$datai)){next;}
        if (!grep(/\w+/,$data)){next;}
        push(@tmp_data,$data);
    }
    
}
close(FILE);

foreach my $file (@$flow)
{
    if ($file->{schname} eq 'system'){next;}
    print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
    print qq (<td width="200" align="center" colspan=7>$file->{schname}<td>);
    my $menber = $file->{member};
    my $packets=0;
    my $bytes=0;
    my $bps=0;
    my $bpp=0;
    my $flows=0;
    $top='1';
    foreach my $user (@$menber)
    {
    	my $ary_index="0";
        foreach my $database (@tmp_data)
        {
            if (grep(/(\d+)\.(\d+)\.(\d+)\.(\d+)/,$database))
            {
                $database=~s/(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)\.(\d+)\s+(\d+)\.(\d+)//g;
                $database=~s/\(\s*\d+\.\d+\)//g;
                $database=~s/any//g;
                my @traffic = split(/\s{2,}/,$database);
                if ( $user->{ip} eq $traffic[1])
                {
					my $mystatus='';
					system("/usr/local/apache/qb/setuid/run /sbin/arp -an | awk \"/$traffic[1]/\" > /tmp/tmp_arp");
					system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_arp");
					open(FILE,'</tmp/tmp_arp');
					foreach my $line (<FILE>)
					{
						my @macref=split(/\s/,$line);
						if("($traffic[1])" eq $macref[1])
						{
							$mystatus="MAC: $macref[3]&#10;";
						}
					}
					close(FILE);
					foreach my $userlist (@$auser)
					{
						if ($userlist->{schname} eq 'system'){next;}
						my $menber = $userlist->{member};
						foreach my $user (@$menber)
						{
							if($user->{iip} eq $traffic[1]){$mystatus=$mystatus."Auth: $user->{idd}";}
						}
					}
					$mytitle="title=\"$mystatus\"";
					print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
					print qq (<td width="200" align="center">$top</td>);
					print qq (<td width="200" align="center" $mytitle>$traffic[1]</td>);
					print qq (<td width="200" align="center">$traffic[2]</td>);
					print qq (<td width="200" align="center">$traffic[3]</td>);
					print qq (<td width="200" align="center">$traffic[4]</td>);
					print qq (<td width="200" align="center">$traffic[5]</td>);
					print qq (<td width="200" align="center">$traffic[6]</td></tr>); 
					$top++;
					#delete $tmp_data[$ary_index];
					splice(@tmp_data,$ary_index,1);
                }
            }
            $ary_index++;
        }
    }
}
print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
print qq (<td width="200" align="center" colspan=7>Other<td>);
$top=1;
foreach my $database (@tmp_data)
{
    $database=~s/(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)\.(\d+)\s+(\d+)\.(\d+)\s+//g;
    my @traffic = split(/\s{2,}/,$database);
	if($traffic[1] eq '127.0.0.1'||$traffic[1] eq '0.0.0.0'){next;}
	if (grep(/(172)\.(31)\.(\d+)\.(\d+)/,$traffic[1]))
	{
		my $pass = '0';
		system("/usr/local/apache/qb/setuid/run /sbin/ip addr | awk \"/$traffic[1]/\" > /tmp/tmp_ipaddr");
		system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_ipaddr");
		my $file = -z "/tmp/tmp_ipaddr";
		if(file){next;}
		open(FILE,'</tmp/tmp_ipaddr');
		foreach my $line (<FILE>)
		{
			my @ipref=split(/\s+/,$line);
			foreach my $ip (@$iplist)
			{
				if($ip->{nic} eq $ipref[5])
				{
					$traffic[1] = $ip->{ip};
					$pass='1';
				}else{next;}
			}
		}
		close(FILE);
		if($pass='0'){next;}
	}

	my $mystatus='';
	system("/usr/local/apache/qb/setuid/run /sbin/arp -an | awk \"/$traffic[1]/\" > /tmp/tmp_arp");
	system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_arp");
	open(FILE,'</tmp/tmp_arp');
	foreach my $line (<FILE>)
	{
		my @macref=split(/\s/,$line);
		if("($traffic[1])" eq $macref[1])
		{
			$mystatus="MAC: $macref[3]&#10;";
		}
	}
	close(FILE);
	foreach my $userlist (@$auser)
	{
		if ($userlist->{schname} eq 'system'){next;}
		my $menber = $userlist->{member};
		foreach my $user (@$menber)
		{
			if($user->{iip} eq $traffic[1]){$mystatus=$mystatus."Auth: $user->{idd}";}
		}
	}
	$mytitle="title=\"$mystatus\"";
	
    print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
    print qq (<td width="200" align="center">$top</td>);
    print qq (<td width="200" align="center" $mytitle>$traffic[1]</td>);
    print qq (<td width="200" align="center">$traffic[2]</td>);
    print qq (<td width="200" align="center">$traffic[3]</td>);
    print qq (<td width="200" align="center">$traffic[4]</td>);
    print qq (<td width="200" align="center">$traffic[5]</td>);
    print qq (<td width="200" align="center">$traffic[6]</td></tr>); 
    $top++;
}

print qq (<FONT SIZE=4>Query Completed (Time used $time Seconds) Data transfer completed (Total $title Records)</FONT>);
#system("/usr/local/apache/qb/setuid/run /bin/rm -rf /tmp/test_nfdump");
