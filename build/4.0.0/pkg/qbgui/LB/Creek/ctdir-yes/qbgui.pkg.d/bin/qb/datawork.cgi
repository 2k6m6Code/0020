#!/usr/bin/perl              
use CGI;
use Data::Dumper;
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type: text/html\n\n";
$cgi=CGI->new();
$data = $cgi->param("data");
$option = "-o StrictHostKeyChecking=no -o TCPKeepAlive=no -o ServerAliveInterval=5 -o ServerAliveCountMax=3 -o ConnectTimeout=30";
@tmp = split(/,/,$data);
#if ($tmp[1] ne ($#tmp - 1)){return;}
$filehome = "/mnt/qb/conf/set/";
$fileclient = "/mnt/qb/conf/cms/";
my $ispref=XMLread('/usr/local/apache/active/basic.xml');
my $check=runCommand(command=>'cat', params=>"/mnt/conf/qbsn");
my $isplist=$ispref->{isp};
my $y = 0;
foreach $isp (@$isplist)
{
    if ($isp->{qbsn} eq $tmp[0])
    {    	
    	foreach $isp (@$isplist)
    	{
            if ($isp->{qbsn} eq $tmp[0] && $isp->{alive} eq "1" && $isp->{tunnel_role} eq "1")
    	    {
                $ip = $isp->{target};
    	        for (my $y = 2; $y < ($#tmp + 1) ; $y++)
    	        {
    	            runCommand(command=>'scp', params=>"-i /etc/.ssh/qlogin $option -r $fileclient$tmp[0]/$tmp[$y] $ip:$filehome");
    	        }
    	    }
    	    next;
    	 }
    }
    if ($isp->{remote} eq $tmp[0])
    {
        if ($isp->{remote} eq $tmp[0] && $isp->{alive} eq "1" && $isp->{tunnel_role} eq "0")
        {
            
            for (my $y = 1; $y < ($#tmp + 1) ; $y++)
            {
                runCommand(command=>'scp', params=>"-i /etc/.ssh/qlogin $option -r $filehome$tmp[$y] $tmp[0]:$fileclient$check/");
            }
            next;
        }
    }
}    
