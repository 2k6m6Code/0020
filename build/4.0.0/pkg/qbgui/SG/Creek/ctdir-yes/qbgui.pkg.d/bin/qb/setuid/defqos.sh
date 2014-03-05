#!/usr/bin/perl
require ("/usr/local/apache/qb/qbmod.cgi");
my $isplist = XMLread("/usr/local/apache/active/basic.xml");
my $ispref = $isplist->{isp};
my $interface;
my @face;
open ( FILE, '</opt/qb/registry');
foreach my $line (<FILE>) 
{ 
    if(grep(/^MAXETHBW/,$line))
    {
       $line=~s/^MAXETHBW\s//g;
       $line=~s/\n//g;
       $line=~s/\s//g;
       $max=$line.'mbit';
    }
}
close(FILE);

foreach my $isp (@$ispref)
{
    if ($isp->{nic} eq "" || $isp->{dtunnel} || $isp->{tunnel}){next;}
    $interface .= $isp->{nic}.',';
}
$interface=~ s/,$//g;
@face = split(/,/,$interface);
open ( QOSFILE, '>/usr/local/apache/qb/setuid/mainqos.sh');
print QOSFILE "\#!/bin/bash\n";
print QOSFILE "/usr/local/sbin/tc qdisc del dev imq60 root 2>/dev/null\n";
print QOSFILE "/usr/local/sbin/tc qdisc add dev imq60 root handle 10: htb default 10\n";
print QOSFILE "/usr/local/sbin/tc class add dev imq60 parent 10: classid 10:1 htb rate $max ceil $max\n";
print QOSFILE "/usr/local/sbin/tc class add dev imq60 parent 10:1 classid 10:10 htb rate $max ceil $max prio 0\n";
print QOSFILE "/usr/local/sbin/tc qdisc add dev imq60 parent 10:10 handle 101: sfq perturb 10\n";
print QOSFILE "/usr/local/sbin/tc filter add dev imq60 parent 10: protocol ip prio 100 handle 10 fw classid 10:10\n";
foreach my $inter (@face)
{
    print QOSFILE "/usr/local/sbin/iptables -t mangle -A PREROUTING -i $inter -j IMQ --todev 60\n";
    print QOSFILE "/usr/local/sbin/iptables -t mangle -A POSTROUTING -o $inter -j IMQ --todev 60\n";
}
print QOSFILE "/usr/local/sbin/ip link set imq60 up\n";
close (QOSFILE);
runCommand(command=>'chmod' , params=>'777 /usr/local/apache/qb/setuid/mainqos.sh');
runCommand(command=>'/usr/bin/perl' , params=>'/usr/local/apache/qb/setuid/mainqos.sh');
