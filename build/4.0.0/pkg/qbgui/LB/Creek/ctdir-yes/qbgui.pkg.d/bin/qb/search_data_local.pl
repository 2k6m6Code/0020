#!/usr/bin/perl

require ("qbmod.cgi");

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;

my $service=XMLread($gPATH.'flow_sec.xml');
my $flow=$service->{user};

my $nat=XMLread('/usr/local/apache/qbconf/zonecfg.xml');
my $natlist=$nat->{nat};

my $cgi = CGI-> new();
my $tm_time = $cgi->param("time");
my $tm_ip = $cgi->param("ip");
my $tm_limit = $cgi->param("limit");
my $tm_top = $cgi->param("top");
my $tm_option = $cgi->param("option");
my $tm_unit = $cgi->param("unit");
my $tm_symd = $cgi->param("symd");
my @limit = split(/,/,$tm_limit);
my $search='';

my $auth=XMLread('/usr/local/apache/qbconf/auth.xml');
my $auser=$auth->{user};
my $ipaddr=XMLread('/usr/local/apache/qbconf/ipaddr.xml');
my $iplist=$ipaddr->{ipaddress};
my $unit=XMLread('/usr/local/apache/qbconf/flow.xml');
my $unitlist=$unit->{user};


my $staticnet='';
my $nonet='';
foreach my $user (@$natlist)
{
	if($user->{network} eq ''){next;}
	$staticnet=$staticnet.'net '.$user->{network}.' or ';
	$nonet=$nonet.'not net '.$user->{network}.' or ';
}

foreach my $file (@$flow)
{
   	if ($file->{schname} eq 'system'){next;}
   	my $menber = $file->{member};
	foreach my $user (@$menber)
	{
		if($user->{ip} eq ''){next;}
		$staticnet=$staticnet.'host '.$user->{ip}.' or ';
		$nonet=$nonet.'not host '.$user->{ip}.' and ';
	}
}

if($tm_unit ne 'all')
{
	$staticnet='';
	#$nonet='';
	foreach my $file (@$unitlist)
	{
		if ($file->{schname} eq 'system'){next;}
		if ($file->{schname} eq $tm_unit)
		{
			my $menber = $file->{member};
			foreach my $user (@$menber)
			{
				if($user->{ip} eq ''){next;}
				$staticnet=$staticnet.'host '.$user->{ip}.' or ';
			}
		}
	}
}

$staticnet=~s/or $//g;

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
#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip '$staticnet' -o \"fmt:%ts %td %sa %pkt %byt %bps %bpp  %fl\"");
system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip 'SRC $staticnet' -o \"fmt:%ts %td %sa %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/test_nfdump");

my $file_check='0';
open(CHECKFILE,"/tmp/test_nfdump");
foreach my $rlt (<CHECKFILE>){$file_check=$rlt;}
close(CHECKFILE);
#my $file = -z "/tmp/test_nfdump";
if(grep(/No matched flows/,$file_check)||$file_check eq ''){print qq (<FONT SIZE=4>Query Completed : No Data</FONT>);}
else
{
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
	    if ($title eq '' || $title eq 'Date first seen' || $title eq 'Duration' || grep(/pps/,$title)){next;}
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

#foreach my $file (@$flow)
#{
    #if ($file->{schname} eq 'system'){next;}
    #my $menber = $file->{member};
    my $packets=0;
    my $bytes=0;
    my $bps=0;
    my $bpp=0;
    my $flows=0;
    my $index_all= 1;
    #$top='1';
    #foreach my $user (@$menber)
	foreach my $user (@$natlist)
    {
		if($user->{network} eq ''){next;}
		my ($sa,$sb,$sc,$sd)=split(/\./,$user->{network});
		#print qq(static $sa.$sb.$sc.$sd<br>);
        foreach my $database (@tmp_data)
        {
            if (grep(/(\d+)\.(\d+)\.(\d+)\.(\d+)/,$database))
            {
                $database=~s/(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)\.(\d+)\s+(\d+)\.(\d+)//g;
                $database=~s/\(\s*\d+\.\d+\)//g;
                $database=~s/any//g;
                my @traffic = split(/\s{2,}/,$database);
				my ($a,$b,$c,$d)=split(/\./,$traffic[1]);
				#print qq($a.$b.$c.$d<br>);
                if ( $sa.$sb.$sc eq $a.$b.$c)
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
					
					my $iii=$traffic[1];
					$iii=~s/\s+//g;
					print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
					print qq (<td width="200" align="center">$top</td>);
					print qq (<td width="200" align="center" $mytitle>$traffic[1]</td>);
					print qq (<td width="200" align="center">$traffic[2]</td>);
					print qq (<td width="200" align="center">$traffic[3]</td>);
					print qq (<td width="200" align="center">$traffic[4]</td>);
					print qq (<td width="200" align="center">$traffic[5]</td>);
					#$tm_time=~s/nfcapd\.//g;
					#my @YY=split(/(\d{2})/,$tm_time);
					#print qq (<td width="200" align="center"><a href="query.php?ip=$iii&time_Y=$YY[1]$YY[3]/$YY[5]/$YY[7]&time_h=$YY[9]&time_X=$YY[13]$YY[15]/$YY[17]/$YY[19]&time_z=$YY">$traffic[6]</a></td></tr>); 
					print qq (<td width="200" align="center"><a href="javascript:search_flow('$iii','$tm_time','$tm_ip','$tm_symd')">$traffic[6]</a></td>);
					$top++;
                }
            }
            $ary_index++;
        }
    }
#}
foreach my $file (@$flow)
{
    if ($file->{schname} eq 'system'){next;}
    my $menber = $file->{member};
    my $packets=0;
    my $bytes=0;
    my $bps=0;
    my $bpp=0;
    my $flows=0;
    my $index_all= 1;
    #$top='1';
    foreach my $user (@$menber)
	#foreach my $user (@$natlist)
    {
		if($user->{ip} eq ''){next;}
		my ($sa,$sb,$sc,$sd)=split(/\./,$user->{ip});
		#print qq(static $sa.$sb.$sc.$sd<br>);
        foreach my $database (@tmp_data)
        {
            if (grep(/(\d+)\.(\d+)\.(\d+)\.(\d+)/,$database))
            {
                $database=~s/(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)\.(\d+)\s+(\d+)\.(\d+)//g;
                $database=~s/\(\s*\d+\.\d+\)//g;
                $database=~s/any//g;
                my @traffic = split(/\s{2,}/,$database);
				my ($a,$b,$c,$d)=split(/\./,$traffic[1]);
				#print qq($a.$b.$c.$d<br>);
                if ( $sa.$sb.$sc eq $a.$b.$c)
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
					
					my $iii=$traffic[1];
					$iii=~s/\s+//g;
					print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
					print qq (<td width="200" align="center">$top</td>);
					print qq (<td width="200" align="center" $mytitle>$traffic[1]</td>);
					print qq (<td width="200" align="center">$traffic[2]</td>);
					print qq (<td width="200" align="center">$traffic[3]</td>);
					print qq (<td width="200" align="center">$traffic[4]</td>);
					print qq (<td width="200" align="center">$traffic[5]</td>);
					#$tm_time=~s/nfcapd\.//g;
					#my @YY=split(/(\d{2})/,$tm_time);
					#print qq (<td width="200" align="center"><a href="query.php?ip=$iii&time_Y=$YY[1]$YY[3]/$YY[5]/$YY[7]&time_h=$YY[9]&time_X=$YY[13]$YY[15]/$YY[17]/$YY[19]&time_z=$YY">$traffic[6]</a></td></tr>); 
					print qq (<td width="200" align="center"><a href="javascript:search_flow('$iii','$tm_time','$tm_ip','$tm_symd')">$traffic[6]</a></td>);
					$top++;
                }
            }
            $ary_index++;
        }
    }
}

print qq (<FONT SIZE=4>Query Completed (Time used $time Seconds) Data transfer completed (Total $title Records)</FONT>);
#system("/usr/local/apache/qb/setuid/run /bin/rm -rf /tmp/test_nfdump");
}