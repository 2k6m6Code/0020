#!/usr/bin/perl
require ("qbmod.cgi");

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
my $cgi = CGI-> new();
my $tm_time = $cgi->param("time");
my $tm_ip = $cgi->param("ip");
my $tm_limit = $cgi->param("limit");
my $tm_top = $cgi->param("top");
my $tm_option = $cgi->param("option");
my $tm_unit = 'all';
if($cgi->param("unit") ne ''||$cgi->param("unit") ne 'all'){
$tm_unit = $cgi->param("unit");}
my $tm_symd = $cgi->param("symd");
my @limit = split(/,/,$tm_limit);
my $search='';
my $unit=XMLread('/usr/local/apache/qbconf/flow.xml');
my $unitlist=$unit->{user};
my $service=XMLread('/usr/local/apache/qbconf/flow_sec.xml');
my $flow=$service->{user};
my $skip=1;

my $nat=XMLread('/usr/local/apache/qbconf/zonecfg.xml');
my $natlist=$nat->{nat};

my $auth=XMLread('/usr/local/apache/qbconf/auth.xml');
my $auser=$auth->{user};
my $ipaddr=XMLread('/usr/local/apache/qbconf/ipaddr.xml');
my $iplist=$ipaddr->{ipaddress};

my $staticnet='';
my $nonet='';
foreach my $user (@$natlist)
{
	my $choose='not ';
	#if($tm_option eq 'query_host'&&$tm_ip eq '-A proto,dstip'){$choose='not '}
	if($user->{network} eq ''){next;}
	$staticnet=$staticnet.'net '.$user->{network}.' or ';
	$nonet=$nonet.$choose.'net '.$user->{network}.' and ';
}

foreach my $file (@$flow)
{
	my $choose='not ';
	#if($tm_option eq 'query_host'&&$tm_ip eq '-A proto,dstip'){$choose='not '}
   	if ($file->{schname} eq 'system'){next;}
   	my $menber = $file->{member};
	foreach my $user (@$menber)
	{
		if($user->{ip} eq ''){next;}
		$staticnet=$staticnet.'host '.$user->{ip}.' or ';
		$nonet=$nonet.$choose.'host '.$user->{ip}.' and ';
	}
}

if($tm_unit ne 'all')
{
	my $choose;
	if ($tm_option eq 'in_dst' || $tm_option eq 'out_dst'){$choose = 'SRC';}
	if ($tm_option eq 'in_src' || $tm_option eq 'out_src'){$choose = 'DST';}
	$nonet=$nonet.'(';
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
				$nonet=$nonet.$choose.' host '.$user->{ip}.' or ';
			}
		}
	}
	$nonet=$nonet.')';
}

$staticnet=~s/or $/and /g;
#$nonet=~s/and $/and /g;
if($tm_unit ne 'all'){$nonet=~s/or \)$/\)and /g;}

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

if($tm_option eq 'bd_tr')
{
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip 'not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %pr %sap <-> %dap %ipkt %opkt %ibyt  %obyt  %fl \" > /tmp/test_nfdump");
	#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip -o \"fmt:%ts %td  %pr %sap <-> %dap %ipkt %opkt %ibyt  %obyt  %fl \" > /tmp/test_nfdump");
}
if($tm_option eq 'realtime')
{
	if(grep(/-B /,$tm_ip))
	{
		system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip 'not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %pr %sap <-> %dap %ipkt %opkt %ibyt  %obyt  %fl \" > /tmp/test_nfdump");
		#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip -o \"fmt:%ts %td  %pr %sap <-> %dap %ipkt %opkt %ibyt  %obyt  %fl \" > /tmp/test_nfdump");
	}
	elsif(grep(/local/,$tm_ip))
	{
		system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit '$staticnet not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %sa %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
		#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit '$staticnet not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %sa %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
	}
	else
	{
		system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip 'not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %sa %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
		#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip -o \"fmt:%ts %td  %pr %sa %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
	}
}
elsif($tm_option eq 'query_host')
{
	if($tm_ip eq '-A proto,srcip')
	{
		system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip 'SRC $staticnet not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %pr %sa %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
		#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip 'SRC $staticnet not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %pr %sa %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
	}
	else
	{
		system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip '$nonet not host 127.0.0.1 and not host 0.0.0.0 and not net 172.31.3.0/24' -o \"fmt:%ts %td  %pr %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
		#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip '$nonet not host 127.0.0.1 and not host 0.0.0.0 and not net 172.31.3.0/24' -o \"fmt:%ts %td  %pr %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
	}
}
elsif($tm_option eq 'in_dst')
{
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip 'SRC $staticnet not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %pr %sa %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
	#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip 'SRC $staticnet not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %pr %sa %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
}
elsif($tm_option eq 'out_src')
{
	#system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip -o \"fmt:%ts %td  %pr %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip 'DST $staticnet not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %pr %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
	#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip 'DST $staticnet not host 127.0.0.1 and not host 0.0.0.0' -o \"fmt:%ts %td  %pr %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
}
elsif($tm_option eq 'in_src')
{
	#system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip -o \"fmt:%ts %td  %pr %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip '$nonet not host 127.0.0.1 and not host 0.0.0.0 and not net 172.31.3.0/24' -o \"fmt:%ts %td  %pr %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
	#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip '$nonet not host 127.0.0.1 and not host 0.0.0.0 and not net 172.31.3.0/24' -o \"fmt:%ts %td  %pr %da %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
}
elsif($tm_option eq 'out_dst')
{
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip '$nonet not host 127.0.0.1 and not host 0.0.0.0 and not net 172.31.3.0/24' -o \"fmt:%ts %td  %pr %sa %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
	#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip '$nonet not host 127.0.0.1 and not host 0.0.0.0 and not net 172.31.3.0/24' -o \"fmt:%ts %td  %pr %sa %pkt %byt %bps %bpp  %fl\" > /tmp/test_nfdump");
}
else
{
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip > /tmp/test_nfdump");
	#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip > /tmp/test_nfdump");
}
system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/test_nfdump");
#system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip > /tmp/mytest");
#system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip -o \"fmt:%ts %td %pr %sap %dap %ipkt %opkt %ibyt %obyt %fl \" > /tmp/mytest");
#system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/test_nfdump");
#print qq (/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip<br>);
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
test1: foreach my $data (<FILE>)
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
	    if ($title eq ''){next;}
		if (!grep(/bd_tr/,$tm_option)&&!grep(/realtime/,$tm_option))
		{
			$title=~s/Src||Dst//g;
		}
	    if (grep(/IP Addr/,$title) && grep(/Pt/,$title))
	    {
	        my @tmp_1 = split(/ /,$title);
	        my @tmp_2;
	        foreach my $yy (@tmp_1)
	        {
	            if ($yy eq ''){next;}
				if ($yy eq 'IP Addr'){$yy=~s/IP Addr/IP addr/g;}
	            push(@tmp_2,$yy);
	        }
	        print qq(<th style="width: 200px;">$tmp_2[0] $tmp_2[1]</th>);
	        print qq(<th style="width: 200px;">$tmp_2[2]</th>);
	    }elsif (grep(/Duration/,$title) && grep(/Proto/,$title))
	    {
	        my @tmp_1 = split(/ /,$title);
	        print qq(<th style="width: 200px;">$tmp_1[0]</th>);
	        print qq(<th style="width: 200px;">$tmp_1[1]</th>);
	    }
		elsif (grep(/Bpp/,$title) && grep(/Flows/,$title))
	    {
	        my @tmp_1 = split(/ /,$title);
	        print qq(<th style="width: 200px;">$tmp_1[0]</th>);
	        print qq(<th style="width: 200px;">$tmp_1[1]</th>);
	    }
	    elsif (grep(/Byte/,$title) && grep(/Flows/,$title) && grep(/In/,$title))
	    {
	        my @tmp_1 = split(/ /,$title);
	        print qq(<th style="width: 200px;">$tmp_1[0] $tmp_1[1]</th>);
	        print qq(<th style="width: 200px;">$tmp_1[2]</th>);
	    }
	    elsif (grep(/Byte/,$title) && grep(/Pkt/,$title))
	    {
	        my @tmp_1 = split(/ /,$title);
	        print qq(<th style="width: 200px;">$tmp_1[1] $tmp_1[2]</th>);
	        print qq(<th style="width: 200px;">$tmp_1[3] $tmp_1[4]</th>);
	    }
	    elsif (grep(/Byte/,$title) && grep(/Flows/,$title))
	    {
	        my @tmp_1 = split(/ /,$title);
	        print qq(<th style="width: 200px;">$tmp_1[0]</th>);
	        print qq(<th style="width: 200px;">$tmp_1[1]</th>);
	    }else
	    {
			if (grep(/IP Addr/,$title)){$title=~s/IP Addr/IP addr/g;}
	        print qq(<th style="width: 200px;">$title</th>);
	    }
	}
	print qq (</tr></thead>);
    }
    #elsif (grep(/Summary/,$data))
    #{
   #	$data=~s/Summary://g;
   #	my @total = split(/,/,$data); 
   #     print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
   #     print qq (<td width="200" align="center"></td>);
   #     print qq (<td width="200" align="center">Total</td>);
   #     print qq (<td width="200" align="center">Total</td>);
   #     print qq (<td width="200" align="center">Total</td>);
   #     foreach my $db (@total)
   #     {
   #         if ($db eq ''){next;}
   #         $db=~s/^.*://g;
   #         print qq (<td width="200" align="center">$db</td>);
   #     }
   # 	$lineCount++;
   # }
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
    }
    else
    {
        if (grep(/No matched flows/,$data)){next;}
        if (!grep(/\w+/,$data)){next;}
		my $con = '1';
		my @tmp = split(/\s+/,$data);
		my ($a,$b,$c,$d) = split(/\./,$tmp[4]);
		#if (grep(/127.0.0.1/,$tmp[4])||grep(/0.0.0.0/,$tmp[4])){next;}
		if($tm_option eq 'in_dst'||$tm_option eq 'out_src'||($tm_option eq 'query_host'&&$tm_ip eq '-A proto,srcip')){$con='0';}
		#print qq ($tmp[4]<br>);
=cut
		if (grep(/(172)\.(31)\.(\d+)\.(\d+)/,$tmp[4])||grep(/(172)\.(31)\.(\d+)\.(\d+):(\d+)/,$tmp[4]))
		{
			my $pass = '0';
			#print qq ($tmp[4]);
			#print qq("/usr/local/apache/qb/setuid/run /sbin/ip addr | awk \"/$db/\" > /tmp/tmp_ipaddr"<br>);
			system("/usr/local/apache/qb/setuid/run /sbin/ip addr | awk \"/$tmp[4]/\" > /tmp/tmp_ipaddr");
			system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_ipaddr");
			my $file = -z "/tmp/tmp_ipaddr";
			if(file){next;}
			open(FILE,'</tmp/tmp_ipaddr');
			foreach my $line (<FILE>)
			{
				my @ipref=split(/\s+/,$line);
				foreach my $ip (@$iplist)
				{
					if($ip->{nic} ne $ipref[5])
					{
						next;
					}else{$pass='1';}
				}
			}
			close(FILE);
			#if($pass='0'){next;}
		}
=cut
		my($a,$b,$c,$d)=split(/\./,$tmp[4]);
		#print qq($a  $b  $c  $d<br>);
        #foreach my $file (@$flow)
        #{
        	#if ($file->{schname} eq 'system'){next;}
			#print qq(aaa$data<br>);
        	#my $menber = $file->{member};
        	#foreach my $user (@$menber)
			foreach my $user (@$natlist)
        	{
				if($user->{network} eq ''){next;}
				my ($sa,$sb,$sc,$d)=split(/\./,$user->{network});
				if($tm_option eq 'in_dst'||$tm_option eq 'out_src'||($tm_option eq 'query_host'&&$tm_ip eq '-A proto,srcip'))
				{
					$con = '0';
					if($a.$b.$c ne $sa.$sb.$sc){next;}
					else
					{
						#print qq($tmp[4] $user->{ip}<br>);
						my @traffic = split(/\s{2}/,$data);
						#print qq($traffic[2]<br>);
						print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
						print qq (<td width="200" align="center">$top</td>);
						my $tt='0';
						foreach my $db (@traffic)
						{
							$tt++;
							if ($db eq ''){next;}
							if (grep(/(\d+)\.(\d+)\.(\d+)\.(\d+)/,$db))
							{
								$iii=$db;
								$iii=~s/\s+//g;
								$mystatus='';
								my @test = split(/:/,$iii);
								system("/usr/local/apache/qb/setuid/run /sbin/arp -an | awk \"/\($test[0]\)/\" > /tmp/tmp_arp");
								system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_arp");
								open(FILE,'</tmp/tmp_arp');
								foreach my $line (<FILE>)
								{
									my @macref=split(/\s/,$line);
									if("($test[0])" eq $macref[1])
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
										if($user->{iip} eq $test[0]){$mystatus=$mystatus."Auth: $user->{idd}";}
									}
								}
								$mytitle="title=\"$mystatus\"";
							}
							if (grep(/-/,$db) && grep(/:/,$db)&& grep(/\./,$db))
							{
								$db =~ s/<->//g;
								my @tmp =split(/\s+/,$db);
								if ($tmp[0] eq '' &&  $tmp[1] eq ''){next;}
								print qq (<td width="200" align="center">$tmp[0] $tmp[1]</td>);
								if ($tmp[2] eq ''){next;}
								print qq (<td width="200" align="center">$tmp[2]</td>);
							}elsif (grep(/-/,$db) )
							{
								$db =~ s/->//g;
								$db =~ s/<//g;
								my @tmp =split(/\s+/,$db);
								if ($tmp[0] eq '' &&  $tmp[1] eq ''){next;}
								print qq (<td width="200" align="center">$tmp[0] $tmp[1]</td>);
								if ($tmp[2] eq '' || $tmp[3] eq ''){next;}
								print qq (<td width="200" align="center">$tmp[2] $tmp[3]</td>);    
							}elsif ($tt > $#traffic)
							{
								#$tm_time=~s/nfcapd\.//g;
								#my @YY=split(/(\d{2})/,$tm_time);
								#print qq (<td width="200" align="center"><a href="query.php?ip=$iii&time_Y=$YY[1]$YY[3]/$YY[5]/$YY[7]&time_h=$YY[9]&time_X=$YY[13]$YY[15]/$YY[17]/$YY[19]&time_z=$YY">$db</a></td>);
								print qq (<td width="200" align="center"><a href="javascript:search_flow('$iii','$tm_time','$tm_ip','$tm_symd','$traffic[2]')">$db</a></td>);
							}
							elsif (grep(/\.(\d+)(\s+)(M)/,$db)||grep(/\.(\d+)(\s*)(G)(\s)/,$db))
							{
								$db=~s/^\s+//g;
								$db=~s/\s+$//g;
								#print qq (<td width="200" align="center" $mytitle>$db</td>);
								my @tmp_1 = split(/\s+/,$db);
								if($tmp_1[1] eq 'M'){$tmp_1[0]*=1000000;}
								if($tmp_1[1] eq 'G'){$tmp_1[0]*=1000000000;}
								print qq(<td width="200" align="center" $mytitle>$tmp_1[0]</td>);
								#print qq(<td width="200" align="center" $mytitle></td>);
							}
							else
							{
								if (grep(/(172)\.(31)\.(\d+)\.(\d+)/,$db))
								{
									#print qq("/usr/local/apache/qb/setuid/run /sbin/ip addr | awk \"/$db/\" > /tmp/tmp_ipaddr"<br>);
									system("/usr/local/apache/qb/setuid/run /sbin/ip addr | awk \"/$db/\" > /tmp/tmp_ipaddr");
									system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_ipaddr");
									open(FILE,'</tmp/tmp_ipaddr');
									foreach my $line (<FILE>)
									{
										my @ipref=split(/\s+/,$line);
										#print qq ($db 5:$ipref[5]<br>);
										foreach my $ip (@$iplist)
										{
											if($ip->{nic} eq $ipref[5])
											{
												$db=$ip->{ip};
												#print qq ($db $ipref[5] $ip->{ip}&#10;);
											}
										}
									}
									close(FILE);
									print qq (<td width="200" align="center" $mytitle>$db</td>);
								}
								else
								{
									print qq (<td width="200" align="center" $mytitle>$db</td>);
								}
							}
						}
						print qq (</tr>);
						$lineCount++;
						$top++;
					}
				}
				#if($test_next='1'){$test_next='0';next;}
				#if($tm_option eq 'in_src'||$tm_option eq 'out_dst'||($tm_option eq 'query_host'&&$tm_ip eq '-A proto,dstip'))
				#{
				#	if($a.$b.$c eq $sa.$sb.$sc){next test1;}
				#	#if($tmp[4] eq $user->{ip}){next test1;}
				#	$con='1';
				#	#print qq($data<br>);
				#}
			}
		#}
		#print qq($a  $b  $c  $d<br>);
        foreach my $file (@$flow)
        {
        	if ($file->{schname} eq 'system'){next;}
			#print qq(aaa$data<br>);
        	my $menber = $file->{member};
        	foreach my $user (@$menber)
			#foreach my $user (@$natlist)
        	{
				if($user->{ip} eq ''){next;}
				my ($sa,$sb,$sc,$d)=split(/\./,$user->{ip});
				if($tm_option eq 'in_dst'||$tm_option eq 'out_src'||($tm_option eq 'query_host'&&$tm_ip eq '-A proto,srcip'))
				{
					$con = '0';
					if($a.$b.$c ne $sa.$sb.$sc){next;}
					else
					{
						#print qq($tmp[4] $user->{ip}<br>);
						my @traffic = split(/\s{2}/,$data);
						print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
						print qq (<td width="200" align="center">$top</td>);
						my $tt='0';
						foreach my $db (@traffic)
						{
							$tt++;   
							if ($db eq ''){next;}
							if (grep(/(\d+)\.(\d+)\.(\d+)\.(\d+)/,$db))
							{
								$iii=$db;
								$iii=~s/\s+//g;
								$mystatus='';
								my @test = split(/:/,$iii);
								system("/usr/local/apache/qb/setuid/run /sbin/arp -an | awk \"/\($test[0]\)/\" > /tmp/tmp_arp");
								system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_arp");
								open(FILE,'</tmp/tmp_arp');
								foreach my $line (<FILE>)
								{
									my @macref=split(/\s/,$line);
									if("($test[0])" eq $macref[1])
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
										if($user->{iip} eq $test[0]){$mystatus=$mystatus."Auth: $user->{idd}";}
									}
								}
								$mytitle="title=\"$mystatus\"";
							}
							if (grep(/-/,$db) && grep(/:/,$db)&& grep(/\./,$db))
							{
								$db =~ s/<->//g;
								my @tmp =split(/\s+/,$db);
								if ($tmp[0] eq '' &&  $tmp[1] eq ''){next;}
								print qq (<td width="200" align="center">$tmp[0] $tmp[1]</td>);
								if ($tmp[2] eq ''){next;}
								print qq (<td width="200" align="center">$tmp[2]</td>);
							}elsif (grep(/-/,$db) )
							{
								$db =~ s/->//g;
								$db =~ s/<//g;
								my @tmp =split(/\s+/,$db);
								if ($tmp[0] eq '' &&  $tmp[1] eq ''){next;}
								print qq (<td width="200" align="center">$tmp[0] $tmp[1]</td>);
								if ($tmp[2] eq '' || $tmp[3] eq ''){next;}
								print qq (<td width="200" align="center">$tmp[2] $tmp[3]</td>);    
							}elsif ($tt > $#traffic)
							{
								#$tm_time=~s/nfcapd\.//g;
								#my @YY=split(/(\d{2})/,$tm_time);
								#print qq (<td width="200" align="center"><a href="query.php?ip=$iii&time_Y=$YY[1]$YY[3]/$YY[5]/$YY[7]&time_h=$YY[9]&time_X=$YY[13]$YY[15]/$YY[17]/$YY[19]&time_z=$YY">$db</a></td>);
								print qq (<td width="200" align="center"><a href="javascript:search_flow('$iii','$tm_time','$tm_ip','$tm_symd','$traffic[2]')">$db</a></td>);
							}
							elsif (grep(/\.(\d+)(\s+)(M)/,$db)||grep(/\.(\d+)(\s*)(G)(\s)/,$db))
							{
								$db=~s/^\s+//g;
								$db=~s/\s+$//g;
								#print qq (<td width="200" align="center" $mytitle>$db</td>);
								my @tmp_1 = split(/\s+/,$db);
								if($tmp_1[1] eq 'M'){$tmp_1[0]*=1000000;}
								if($tmp_1[1] eq 'G'){$tmp_1[0]*=1000000000;}
								print qq(<td width="200" align="center" $mytitle>$tmp_1[0]</td>);
								#print qq(<td width="200" align="center" $mytitle></td>);
							}
							else
							{
								if (grep(/(172)\.(31)\.(\d+)\.(\d+)/,$db))
								{
									#print qq("/usr/local/apache/qb/setuid/run /sbin/ip addr | awk \"/$db/\" > /tmp/tmp_ipaddr"<br>);
									system("/usr/local/apache/qb/setuid/run /sbin/ip addr | awk \"/$db/\" > /tmp/tmp_ipaddr");
									system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_ipaddr");
									open(FILE,'</tmp/tmp_ipaddr');
									foreach my $line (<FILE>)
									{
										my @ipref=split(/\s+/,$line);
										#print qq ($db 5:$ipref[5]<br>);
										foreach my $ip (@$iplist)
										{
											if($ip->{nic} eq $ipref[5])
											{
												$db=$ip->{ip};
												#print qq ($db $ipref[5] $ip->{ip}&#10;);
											}
										}
									}
									close(FILE);
									print qq (<td width="200" align="center" $mytitle>$db</td>);
								}
								else
								{
									print qq (<td width="200" align="center" $mytitle>$db</td>);
								}
							}
						}
						print qq (</tr>);
						$lineCount++;
						$top++;
					}
				}
			}
		}
		if($tm_option eq 'in_src'||$tm_option eq 'out_dst'||($tm_option eq 'query_host'&&$tm_ip eq '-A proto,dstip'))
				{
					if($a.$b.$c eq $sa.$sb.$sc){next test1;}
					#if($tmp[4] eq $user->{ip}){next test1;}
					$con='1';
					#print qq($data<br>);
				}
		if($con eq '1')
		{
		my @traffic = split(/\s{2}/,$data);
		my @testtraffic = split(/\s+/,$data);
		print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
		print qq (<td width="200" align="center">$top</td>);
		my $tt='0';
		foreach my $db (@traffic)
		{
			$tt++;   
			if ($db eq ''){next;}
			if (grep(/(\d+)\.(\d+)\.(\d+)\.(\d+)/,$db))
			{
				$iii=$db;
				$iii=~s/\s+//g;
				$mystatus='';
				my @test = split(/:/,$iii);
				system("/usr/local/apache/qb/setuid/run /sbin/arp -an | awk \"/\($test[0]\)/\" > /tmp/tmp_arp");
				system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_arp");
				open(FILE,'</tmp/tmp_arp');
				foreach my $line (<FILE>)
				{
					my @macref=split(/\s/,$line);
					if("($test[0])" eq $macref[1])
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
						if($user->{iip} eq $test[0]){$mystatus=$mystatus."Auth: $user->{idd}";}
					}
				}
				$mytitle="title=\"$mystatus\"";
			}
			if (grep(/-/,$db) && grep(/:/,$db)&& grep(/\./,$db))
			{
				$db =~ s/<->//g;
				my @tmp =split(/\s+/,$db);
				if ($tmp[0] eq '' &&  $tmp[1] eq ''){next;}
				print qq (<td width="200" align="center">$tmp[0] $tmp[1]</td>);
				if ($tmp[2] eq ''){next;}
				print qq (<td width="200" align="center">$tmp[2]</td>);
			}elsif (grep(/-/,$db) )
			{
				$db =~ s/->//g;
				$db =~ s/<//g;
				my @tmp =split(/\s+/,$db);
				if ($tmp[0] eq '' &&  $tmp[1] eq ''){next;}
				print qq (<td width="200" align="center">$tmp[0] $tmp[1]</td>);
				if ($tmp[2] eq '' || $tmp[3] eq ''){next;}
				print qq (<td width="200" align="center">$tmp[2] $tmp[3]</td>);    
			}elsif ($tt > $#traffic)
			{
				#$tm_time=~s/nfcapd\.//g;
				#my @YY=split(/(\d{2})/,$tm_time);
				#print qq (<td width="200" align="center"><a href="query.php?ip=$iii&time_Y=$YY[1]$YY[3]/$YY[5]/$YY[7]&time_h=$YY[9]&time_X=$YY[13]$YY[15]/$YY[17]/$YY[19]&time_z=$YY">$db</a></td>);
				#print qq (<td width="200" align="center"><a href="javascript:search_flow('$iii','$tm_time','$tm_ip')">$db</a></td>);
				if($tm_option eq 'bd_tr')
				{
					$iii = $testtraffic[4].','.$testtraffic[6];
					print qq (<td width="200" align="center"><a href="javascript:search_flow('$iii','$tm_time','$tm_option','$tm_symd','$traffic[2]')">$db</a></td>);
				}
				elsif($tm_option eq 'realtime')
				{
					if($tm_option eq 'realtime'&&!grep(/-B /,$tm_ip))
					{
						$iii = $testtraffic[3].','.$testtraffic[4];
					}
					else
					{
						$iii = $testtraffic[4].','.$testtraffic[6];
					}
					print qq (<td width="200" align="center"><a href="javascript:search_flow('$iii','$tm_time','$tm_option','$tm_symd','$tm_ip','$traffic[2]')">$db</a></td>);
				}
				else
				{print qq (<td width="200" align="center"><a href="javascript:search_flow('$iii','$tm_time','$tm_ip','$tm_symd','$traffic[2]')">$db</a></td>);}
			}
			elsif (grep(/\.(\d+)(\s+)(M)/,$db)||grep(/\.(\d+)(\s*)(G)(\s)/,$db))
			    {
					$db=~s/^\s+//g;
					$db=~s/\s+$//g;
					#print qq (<td width="200" align="center" $mytitle>$db</td>);
					my @tmp_1 = split(/\s+/,$db);
					if($tmp_1[1] eq 'M'){$tmp_1[0]*=1000000;}
					if($tmp_1[1] eq 'G'){$tmp_1[0]*=1000000000;}
					print qq(<td width="200" align="center" $mytitle>$tmp_1[0]</td>);
					#print qq(<td width="200" align="center" $mytitle></td>);
				}
			else
			{
				if (grep(/(172)\.(31)\.(\d+)\.(\d+)/,$db))
			    {
					#print qq("/usr/local/apache/qb/setuid/run /sbin/ip addr | awk \"/$db/\" > /tmp/tmp_ipaddr"<br>);
			    	system("/usr/local/apache/qb/setuid/run /sbin/ip addr | awk \"/$db/\" > /tmp/tmp_ipaddr");
					system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_ipaddr");
					open(FILE,'</tmp/tmp_ipaddr');
					foreach my $line (<FILE>)
					{
						my @ipref=split(/\s+/,$line);
						#print qq ($db 5:$ipref[5]<br>);
						foreach my $ip (@$iplist)
						{
							if($ip->{nic} eq $ipref[5])
							{
								$db=$ip->{ip};
								#print qq ($db $ipref[5] $ip->{ip}&#10;);
							}
						}
					}
					close(FILE);
					print qq (<td width="200" align="center" $mytitle>$db</td>);
				}
				elsif (grep(/\.(\d+)(\s+)(\w+)/,$db))
			    {
					$db=~s/^\s+//g;
					$db=~s/\s+$//g;
					#print qq (<td width="200" align="center" $mytitle>$db</td>);
					my @tmp_1 = split(/\s+/,$db);
					print qq(<td width="200" align="center" $mytitle>$tmp_1[0]</td>);
					print qq(<td width="200" align="center" $mytitle>$tmp_1[1]</td>);
				}
			    else
			    {
					print qq (<td width="200" align="center" $mytitle>$db</td>);
				}
			}
		}
		print qq (</tr>);
		$lineCount++;
		$top++;
		}
	}
}
close(FILE);
print qq (<FONT SIZE=4>Query Completed (Time used $time Seconds) Data transfer completed (Total $title Records)</FONT>);
}
#system("/usr/local/apache/qb/setuid/run /bin/rm -rf /tmp/test_nfdump");
=cut
print qq (<tfoot><tr><th>TOTAL:</th><th></th><th></th></tr></tfoot>);
	my $line;
=cut
