#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use QB_Xml;

my $mode = @ARGV[0];
my $nic = @ARGV[1];
my $xml=new QB_Xml;
my $ispref = QB_Xml->read('/usr/local/apache/qbconf/basic.xml');
my $service_ref = QB_Xml->read('/usr/local/apache/qbconf/service.xml');
my $service_list = $service_ref->{service};
my $isplist = $ispref->{isp};
open(FILE, ">/usr/local/apache/qbconf/do_tunnel_speed.sh");
foreach my $isp (@$isplist)
{
    if ($isp->{iid} eq 'system'){next;}
    if ($mode eq 'action' && $isp->{time} eq '' && $isp->{nic} ne $nic){next;}
    print FILE "/usr/local/sbin/tc qdisc del dev $isp->{nic} root 2>/dev/null\n";
    print FILE "/usr/local/sbin/tc qdisc add dev $isp->{nic} root handle 1: htb default 50\n";
    
    my $remote_speed = ($isp->{action_upload})?($isp->{action_upload}):($isp->{upload});
    my $unit = "kbit";
    print FILE "/usr/local/sbin/tc class add dev $isp->{nic} parent 1: classid 1:1 htb rate ".($remote_speed*10/10)."$unit ceil $remote_speed$unit prio 5\n";
    
    print FILE "/usr/local/sbin/tc class add dev $isp->{nic} parent 1:1 classid 1:100 htb rate ".($remote_speed*10/10)."$unit ceil $remote_speed$unit prio 0\n";
    print FILE "/usr/local/sbin/tc qdisc add dev $isp->{nic} parent 1:100 handle 100: sfq perturb 10\n";
    foreach (1..8)
    {
        my $class = 10 - $_;
        print FILE "/usr/local/sbin/tc class add dev $isp->{nic} parent 1:1 classid 1:".($_*10)." htb rate ".($remote_speed*$class/10)."$unit ceil $remote_speed$unit prio $_\n";
        print FILE "/usr/local/sbin/tc qdisc add dev $isp->{nic} parent 1:".($_*10)." handle ".($_*10).": sfq perturb 10\n";
    }
    
    my $servicelist = $isp->{service};
    print FILE "/usr/local/sbin/tc filter add dev $isp->{nic} parent 1:0 protocol ip prio 11 u32 match ip protocol 1 0xff flowid 1:100\n";
    print FILE "/usr/local/sbin/tc filter add dev mpv0 parent 1:0 prio 17 protocol ip rsvp session 0.0.0.0 flowid 1:40\n";
    
    foreach my $service (@$servicelist)
    {
        foreach my $ser (@$service_list)
        {
            if ($ser->{title} ne $service->{service}){next;}
            my $portlist = $ser->{port};
            foreach my $port (@$portlist)
            {
                if ($port->{protocol} eq 'system'){next;}
                print FILE "/usr/local/sbin/tc filter add dev $isp->{nic} parent 1: prio 18 protocol ip rsvp ipproto $port->{protocol} session 0.0.0.0/$port->{value} classid 1:".($service->{priority}*10)."\n";
            }
        }
    }

}
close(FILE);
