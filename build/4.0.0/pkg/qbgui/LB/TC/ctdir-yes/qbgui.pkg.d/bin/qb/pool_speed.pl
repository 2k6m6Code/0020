#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
use QB_Xml;

my $cgi = new CGI;
my $xml = new QB_Xml;
my $nic = $cgi->param("nic");
my $ispref = $xml->read("/usr/local/apache/qbconf/basic.xml");
my $isplist = $ispref->{isp};
my ($sec, $min, $hour, $day, $mon, $year) = localtime(time);
my $now_date=join("-",($year+1900,$mon+1,$day));
my $now_time=join(":",($hour,$min,$sec));
my $download;
my $upload;
my $name;
my $down;
my $up;
my $result;
foreach my $isp (@$isplist)
{
    if ($isp->{nic} ne $nic || $isp->{isptype} eq 'fixed'){next;}
    `/usr/local/apache/qb/setuid/run /usr/local/apache/qb/tunnel_speed.sh $isp->{target} $isp->{systemip} 1 &`;
    $down = "/tmp/download-$isp->{systemip}";
    $up = "/tmp/upload-$isp->{systemip}";
    $name = $isp->{ispname};
    if ((-e $down) && (-e $up))
    {
        $download = `/bin/cat $down|awk \'{print \$7}\'`;
        $upload = `/bin/cat $up|awk \'{print \$7}\'`;
        $download =~ s/\s//g;
        $upload =~ s/\s//g;
        $isp->{action_download}=($download*8/1024);
        $isp->{action_upload}=($upload*8/1024);
        `/usr/local/apache/qb/setuid/run echo "$now_date $now_time Tunnel Speed $isp->{systemip} -> $isp->{target} Upload: $upload  Download : $download  \n">> /tmp/tunnel_speed.log`;
        $result = 'Finish!!';
    }else
    {
        `/usr/local/apache/qb/setuid/run echo "$now_date $now_time Tunnel Speed $isp->{systemip} -> $isp->{target} Error \n">> /tmp/tunnel_speed.log`;
        $result = 'Failed';
    }
}
my $random_number = rand()*10+1;
sleep($random_number);
$download = $download/1024;
$upload = $upload/1024;
print "Content-type:text/html\n\n";
print $result;
`/usr/local/apache/qb/setuid/run /bin/rm -f $down $up`;
$xml->write($ispref,"/usr/local/apache/qbconf/basic.xml");

