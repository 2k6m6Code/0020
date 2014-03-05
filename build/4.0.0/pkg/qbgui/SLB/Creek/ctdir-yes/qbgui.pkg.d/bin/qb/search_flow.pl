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
my $tm_symd = $cgi->param("symd");
my $tm_proto = $cgi->param("proto");
my $tm_cd = $cgi->param("tm_ip");
my @limit = split(/,/,$tm_limit);
my $search='';
my $service=XMLread('/usr/local/apache/qbconf/flow.xml');
my $flow=$service->{user};
my $auth=XMLread('/usr/local/apache/qbconf/auth.xml');
my $auser=$auth->{user};
my $ipaddr=XMLread('/usr/local/apache/qbconf/ipaddr.xml');
my $iplist=$ipaddr->{ipaddress};

if($tm_proto ne ''){$tm_proto='proto '.$tm_proto.' and';}
print "Content-type: text/html\n\n";
system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp");
if(grep(/srcip/,$tm_option))
{
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time '$tm_proto dst ip $tm_ip' -o long -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump");
	#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time '$tm_proto dst ip $tm_ip' -o long -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump");
}
elsif(grep(/dstip/,$tm_option))
{
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time '$tm_proto dst ip $tm_ip' -o long -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump");
	#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time '$tm_proto dst ip $tm_ip' -o long -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump");
}
elsif($tm_option eq 'bd_tr')
{
	my @tmp_ip = split(/,/,$tm_ip);
	my @src_ip = split(/:/,$tmp_ip[0]);
	my @dst_ip = split(/:/,$tmp_ip[1]);
	#print qq(/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time '(src ip $src_ip[0] and src port $src_ip[1] and dst ip $dst_ip[0] and dst port $dst_ip[1]) or (src ip $dst_ip[0] and src port $dst_ip[1] and dst ip $src_ip[0] and dst port $src_ip[1])'<br>);
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time '(src ip $src_ip[0] and src port $src_ip[1] and dst ip $dst_ip[0] and dst port $dst_ip[1]) or (src ip $dst_ip[0] and src port $dst_ip[1] and dst ip $src_ip[0] and dst port $src_ip[1])' -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump");
}
elsif($tm_option eq 'realtime')
{
	if(grep(/-B /,$tm_cd))
	{
		my @tmp_ip = split(/,/,$tm_ip);
		my @src_ip = split(/:/,$tmp_ip[0]);
		my @dst_ip = split(/:/,$tmp_ip[1]);
		#print qq(/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time '(src ip $src_ip[0] and src port $src_ip[1] and dst ip $dst_ip[0] and dst port $dst_ip[1]) or (src ip $dst_ip[0] and src port $dst_ip[1] and dst ip $src_ip[0] and dst port $src_ip[1])'<br>);
		system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time '(src ip $src_ip[0] and src port $src_ip[1] and dst ip $dst_ip[0] and dst port $dst_ip[1]) or (src ip $dst_ip[0] and src port $dst_ip[1] and dst ip $src_ip[0] and dst port $src_ip[1])' -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump");
	}
	else
	{
		my @tmp_ip = split(/,/,$tm_ip);
		system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time '(src ip $tmp_ip[0] and dst ip $tmp_ip[1])' -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump");
		#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time '(src ip $tmp_ip[0] and dst ip $tmp_ip[1])' -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump");
	}
}
elsif($tm_option eq 'service')
{
	my @tmp_ip = $tm_ip;
	my $search_port='';
	foreach my $portlist (@tmp_ip)
	{
		my @port = split(/-/,$portlist);
	    $search_port = $search_port.'dst port '.$port[1].' and ';
	}
	$search_port=~s/and $//g;
	#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time -A proto,srcip,dstip,srcport,dstport '$search_port' -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump"<br>);
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time -A proto,srcip,dstip,srcport,dstport '$search_port' -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump");
}
elsif($tm_option eq 'otherservice')
{
	my $search_port='';
	my @port = split(/,/,$tm_ip);
	foreach my $portlist (@port)
	{
		my @portt = split(/-/,$portlist);
	    $search_port = $search_port.'not dst port '.$portt[1].' and ';
	}
	$search_port=~s/and $//g;
	#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time -A proto,srcip,dstip,srcport,dstport 'not $search_port' -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump"<br>);
	system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time -A proto,srcip,dstip,srcport,dstport '$search_port' -o \"fmt:%ts %td  %pr %sap %dap %pkt %byt  %fl\" > /tmp/test_nfdump");
}

#print qq ("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time 'src ip $tm_ip' > /tmp/test_nfdump"<br>);
#system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time 'dst ip $tm_ip' -o \"fmt:%ts %td  %pr %sa %da %pkt %byt  %fl\" > /tmp/test_nfdump");
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
	    if ($title eq '' || grep(/pps/,$title)){next;}
	    $title=~s/\(%\)//g;
	    if (grep(/IP Addr/,$title))
	    {
			$title=~s/IP Addr/IP addr/g;
	        print qq(<th style="width: 200px;">$title</th>);
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

my $packets=0;
    my $bytes=0;
    my $bps=0;
    my $bpp=0;
    my $flows=0;
    my $index_all= 1;
    my $top='1';
foreach my $database (@tmp_data)
{
    if (grep(/(\d+)\.(\d+)\.(\d+)\.(\d+)/,$database))
    {
        my @traffic = split(/\s{2,}/,$database);					
			my $iii=$traffic[1];
			$iii=~s/\s+//g;
			print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
			print qq (<td width="200" align="center">$top</td>);
			print qq (<td width="200" align="center">$traffic[0]</td>);
			print qq (<td width="200" align="center">$traffic[1]</td>);
			print qq (<td width="200" align="center">$traffic[2]</td>);
			print qq (<td width="200" align="center" $mytitle>$traffic[3]</td>);
			print qq (<td width="200" align="center">$traffic[4]</td>);
			print qq (<td width="200" align="center">$traffic[5]</td>);
			print qq (<td width="200" align="center">$traffic[6]</td>);
			print qq (<td width="200" align="center">$traffic[7]</td></tr>); 
			$top++;
        
    }
	$ary_index++;
}

print qq (<FONT SIZE=4>Query Completed (Time used $time Seconds) Data transfer completed (Total $ary_index Records)</FONT>);
#system("/usr/local/apache/qb/setuid/run /bin/rm -rf /tmp/test_nfdump");
=cut
print qq (<tfoot><tr><th>TOTAL:</th><th></th><th></th></tr></tfoot>);
	my $line;
=cut
