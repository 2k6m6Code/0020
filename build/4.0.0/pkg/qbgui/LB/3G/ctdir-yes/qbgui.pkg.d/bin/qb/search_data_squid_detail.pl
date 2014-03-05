#!/usr/bin/perl
require ("qbmod.cgi");

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
use URI::Escape;
my $cgi = CGI-> new();
my $tm_title = $cgi->param("title");
my $tm_ip = $cgi->param("ip");
my $tm_symd = $cgi->param("symd");
my $request = $cgi->param("request");
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

print "Content-type: text/html\n\n";

print qq (<table bgcolor="#332211" width="1100" border="0" id="tables">);
open(FILE,"/tmp/tmp_squid.log");
my $lineCount = 0;
my $top = '1';
my $time = '0';
my $title='0';
my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
print qq (<thead><tr>);
print qq(<th style="width: 100px;">Top</th>);
print qq(<th style="width: 100px;">Time</th>);
print qq(<th style="width: 100px;">IP</th>);
print qq(<th style="width: 800px;">Request</th>);
print qq (</tr></thead>);


$top='1';
foreach my $database (<FILE>)
{
    my @traffic = split(/\s+/,$database);
	if ($request ne uri_unescape($traffic[6])){next;}
	#print qq([$y$m$d] $traffic[4].$abbr{$traffic[1]}.$traffic[2]<br>);
	if($y.$m.$d ne $traffic[4].$abbr{$traffic[1]}.$traffic[2]){next;}
	if($tm_ip ne '')
	{
		if($traffic[5] ne $tm_ip){next;}
	}
	my $mystatus='';
	system("/usr/local/apache/qb/setuid/run /sbin/arp -an | awk \"/$traffic[5]/\" > /tmp/tmp_arp");
	system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/tmp_arp");
	open(FILE,'</tmp/tmp_arp');
	foreach my $line (<FILE>)
	{
		my @macref=split(/\s/,$line);
		if("($traffic[5])" eq $macref[1])
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
			if($user->{iip} eq $traffic[5]){$mystatus=$mystatus."Auth: $user->{idd}";}
		}
	}
	$mytitle="title=\"$mystatus\"";
	
	my $iii=$traffic[1];
	$iii=~s/\s+//g;
	print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
	print qq (<td width="100" align="center">$top</td>);
	print qq (<td width="100" align="center">$traffic[4]-$traffic[1]-$traffic[2]<br>$traffic[3]</td>);
	print qq (<td width="100" align="center" $mytitle>$traffic[5]</td>);
	print qq (<td width="800" align="center" style="display:inline-block;overflow:hidden;text-overflow:ellipsis;white-space: nowrap;"><a href="$traffic[6]" target="_blank">$traffic[6]</a></td>);
	$top++;
}
close(FILE);
#system ("/usr/local/apache/qb/setuid/run rm -rf /tmp/$y-$m-$d.log /tmp/tmp_squid.log");
system ("sync");
=cut
print qq (<tfoot><tr><th>TOTAL:</th><th></th><th></th></tr></tfoot>);
	my $line;
=cut
