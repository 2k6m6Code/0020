#!/usr/bin/perl

use CGI;
use CGI;
my $cgi = new CGI;
#my $name = $cgi->param("name");
my $type = $cgi->param("type");
my @test = split(/:/,$type);
print "Content-type:text/html\n\n";
foreach my $t (@test)
{
	my ($name,$bs) = split(/\//,$t);
	if($bs eq '1')
	{
		system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -L $name.total --line-numbers -vn|awk '/quota/' >>/tmp/quota_active");
		system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/quota_active");
		system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -L $name.total --line-numbers -vn|awk '/quota/' >>/tmp/quota_active2");
		system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/quota_active2");
	}
	else
	{
		system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -L $name.down --line-numbers -vn|awk '/quota/' >>/tmp/quota_active");
		system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/quota_active");
		system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -L $name.up --line-numbers -vn|awk '/quota/' >>/tmp/quota_active2");
		system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/quota_active2");
	}
}

open(FILE,'</tmp/quota_active');
open(FILEUP,'</tmp/quota_active2');
my @quota;
my @quotaUP;
my $i=0;
my $ii=0;
foreach my $line (<FILE>)
{
    my $quota;
    if (grep(/IMQ/,$line) || grep(/PREROUTING/,$line) || grep(/source/,$line) || grep(/CTDIRMARK/,$line) || grep(/MARK/,$line)){next;}
    my @quotaref=split(/\s+/,$line);
    if (!grep(/quota/,$line)){next;}
	if ($quotaref[11] <= "1024"||$quotaref[11] >= "1024" && $quotaref[11] < "1048576")
	{
		$quotaref[11]/=1024;
		$quotaref[11] = sprintf("%.2f", $quotaref[11]);
		$down = $quotaref[11]."KB";
	}
	if ($quotaref[11] >= "1048576" && $quotaref[11] < "1073741824")
	{
		$quotaref[11]/=1048576;
		$quotaref[11] = sprintf("%.2f", $quotaref[11]);
		$down = $quotaref[11]."MB";
	}
	if ($quotaref[11] >= "1073741824" && $quotaref[11] < "1099511627776")
	{
		$quotaref[11]/=1073741824;
		$quotaref[11] = sprintf("%.2f", $quotaref[11]);
		$down = $quotaref[11]."GB";
	}
	if ($quotaref[11] >= "1099511627776")
	{
		$quotaref[11]/=1099511627776;
		$quotaref[11] = sprintf("%.2f", $quotaref[11]);
		$down = $quotaref[11]."TB";
	}
	$down=~s/\n//;
	$quota[$i]=join(",",@test[$i],$down);
    $i++; 
}
close(FILE);

foreach my $lineUP (<FILEUP>)
{
	my $quotaUP;
	if (grep(/IMQ/,$lineUP) || grep(/POSTROUTING/,$lineUP) || grep(/source/,$lineUP) || grep(/CTDIRMARK/,$lineUP) || grep(/MARK/,$lineUP)){next;}
	my @quotarefUP=split(/\s+/,$lineUP);
	if (!grep(/quota/,$lineUP)){next;}
	if ($quotarefUP[11] <= "1024"||$quotarefUP[11] >= "1024" && $quotarefUP[11] < "1048576")
	{
		$quotarefUP[11]/=1024;
		$quotarefUP[11] = sprintf("%.2f", $quotarefUP[11]);
		$up = $quotarefUP[11]."KB";
	}
	if ($quotarefUP[11] >= "1048576" && $quotarefUP[11] < "1073741824")
	{
		$quotarefUP[11]/=1048576;
		$quotarefUP[11] = sprintf("%.2f", $quotarefUP[11]);
		$up = $quotarefUP[11]."MB";
	}
	if ($quotarefUP[11] >= "1073741824" && $quotarefUP[11] < "1099511627776")
	{
		$quotarefUP[11]/=1073741824;
		$quotarefUP[11] = sprintf("%.2f", $quotarefUP[11]);
		$up = $quotarefUP[11]."GB";
	}
	if ($quotarefUP[11] >= "1099511627776")
	{
		$quotarefUP[11]/=1099511627776;
		$quotarefUP[11] = sprintf("%.2f", $quotarefUP[11]);
		$up = $quotarefUP[11]."TB";
	}
	$up=~s/\n//;
	$quotaUP[$ii]=join(",",@test[$ii],$up);
	$ii++;
}
close(FILEUP);

my $data="";
for (my $z = 0 ; $z <= $i; $z++)
{
    $data.=$quota[$z].":";
	system("echo $quota[$z] >> /tmp/view_quotaDown");
}

my $data_up="";
for (my $z = 0 ; $z <= $i; $z++)
{
    $data_up.=$quotaUP[$z].":";
	system("echo $quotaUP[$z] >> /tmp/view_quotaUp");
}

$data=~s/:$//g;
$data_up=~s/:$//g;
system("cat /dev/null > /tmp/quota_active");
system("cat /dev/null > /tmp/quota_active2");
print $data.'-'.$data_up;
