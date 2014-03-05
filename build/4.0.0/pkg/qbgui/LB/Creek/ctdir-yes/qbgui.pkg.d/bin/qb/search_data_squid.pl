#!/usr/bin/perl
require ("qbmod.cgi");

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
my $cgi = CGI-> new();
my $tm_title = $cgi->param("title");
my $tm_ip = $cgi->param("ip");
my $tm_symd = $cgi->param("symd");
my $search='';
my $service=XMLread('/usr/local/apache/qbconf/flow.xml');
my $flow=$service->{user};
my $auth=XMLread('/usr/local/apache/qbconf/auth.xml');
my $auser=$auth->{user};
my $ipaddr=XMLread('/usr/local/apache/qbconf/ipaddr.xml');
my $iplist=$ipaddr->{ipaddress};
my ($y,$m,$d) = split(/\//,$tm_symd);
if($d < 10){$d=~s/^0//g;}
if($m < 10){$m=~s/^0//g;}
my %abbr = (Jan=>'1',Feb=>'2',Mar=>'3',Apr=>'4',May=>'5',Jun=>'6',Jul=>'7',Aug=>'8',Sep=>'9',Oct=>'10',Nov=>'11',Dec=>'12');
system ("/usr/local/apache/qb/setuid/run chmod 777 /tmp/");
print "Content-type: text/html\n\n";
if($tm_title eq 'webfilter')
{
	#/mnt/tclog/squid/log/filter.log
	system ("/usr/local/apache/qb/setuid/run /bin/cat /mnt/tclog/squid/log/$y-$m-$d | awk '/TCP_DENIED/ {print\$1 \" \" \$3 \" \" \$7}' > /tmp/$y-$m-$d.log");
	system ("/usr/local/apache/qb/setuid/run /usr/bin/perl -p -e 's/^\\d+\.\\d+/localtime \$&/e' < /tmp/$y-$m-$d.log > /tmp/tmp_squid.log");
	system ("sync");
}
if($tm_title eq 'webcache')
{
	system ("/usr/local/apache/qb/setuid/run /bin/cat /mnt/tclog/squid/log/$y-$m-$d | awk '{print\$1 \" \" \$3 \" \" \$7}' > /tmp/$y-$m-$d.log");
	system ("/usr/local/apache/qb/setuid/run /usr/bin/perl -p -e 's/^\\d+\.\\d+/localtime \$&/e' < /tmp/$y-$m-$d.log > /tmp/tmp_squid.log");
	#print qq ("/usr/local/apache/qb/setuid/run /bin/cat /mnt/tclog/squid/log/$y-$m-$d | awk '{print\$1 \" \" \$3 \" \" \$7}' > /tmp/$y-$m-$d.log"<br>);
        #print qq ("/usr/local/apache/qb/setuid/run /usr/bin/perl -p -e 's/^\\d+\.\\d+/localtime \$&/e' < /tmp/$y-$m-$d.log > /tmp/tmp_squid.log");
	system ("sync");
	#/mnt/tclog/squid/log/access.log
}

print qq (<table bgcolor="#332211" width="1000" border="0" id="tables">);
open(FILE,"/tmp/tmp_squid.log");
open(FILEE,"/tmp/tmp_squid.log");
my $lineCount = 0;
my $top = '1';
my $time = '0';
my $title='0';
my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
print qq (<thead><tr>);
print qq(<th style="width: 100px;">No</th>);
#print qq(<th style="width: 100px;">Time</th>);
#print qq(<th style="width: 100px;">IP</th>);
print qq(<th style="width: 800px;">Request</th>);
print qq(<th style="width: 100px;">Count</th>);
print qq (</tr></thead>);


$top='1';
my @array;
my $request="first_time_search";
t1:foreach my $database (<FILE>)
{
	foreach my $check (@array)
	{
		if (grep(/$check/,$database)){next t1;}
	}
	my $count=0;
    my @traffic = split(/\s+/,$database);
	#print qq([$y$m$d] $traffic[4].$abbr{$traffic[1]}.$traffic[2]<br>);
	if($y.$m.$d ne $traffic[4].$abbr{$traffic[1]}.$traffic[2]){next;}
	print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
	print qq (<td width="100" align="center">$top</td>);
	#print qq (<td width="100" align="center">$traffic[4]-$traffic[1]-$traffic[2]<br>$traffic[3]</td>);
	#print qq (<td width="100" align="center">$traffic[5]</td>);
	print qq (<td width="800" align="center" style="display:inline-block;overflow:hidden;text-overflow:ellipsis;white-space: nowrap;"><a href="$traffic[6]" target="_blank">$traffic[6]</a></td>);
	$request = $traffic[6];
	push @array, $request;
	#print qq ($request<br>);
	open(FILEE,"/tmp/tmp_squid.log");
	foreach my $database (<FILEE>)
	{
		my @trafficc = split(/\s+/,$database);
		if ($y.$m.$d eq $traffic[4].$abbr{$traffic[1]}.$traffic[2])
		{
			#print qq($request<br>);
			#print qq($traffic[6]<br>);
			if ($request eq $trafficc[6]){$count++;}
		}
	}
	close(FILEE);
	print qq (<td width="100" align="center"><a href="javascript:search_squid_detail('$tm_title','$tm_ip','$tm_symd','$request')">$count</a></td>);
	$top++;
}
close(FILE);

#system ("/usr/local/apache/qb/setuid/run rm -rf /tmp/$y-$m-$d.log /tmp/tmp_squid.log");
system ("sync");
=cut
print qq (<tfoot><tr><th>TOTAL:</th><th></th><th></th></tr></tfoot>);
	my $line;
=cut
