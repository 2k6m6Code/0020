#!/usr/bin/perl
##!/usr/local/sbin/perl

my $ippath = "/usr/local/sbin/ip";
my $rulelist = "/var/log/rulelist";

system("$ippath rule > $rulelist");

unless (open FD, "<$rulelist")
{
    die "Couldn't open $rulelist\n";
}

while(<FD>)
{
    if ($_ =~ /(\d+):\s+from\s+([\d\.\/]+)\s+lookup\s+(\d+)/)
    #example: ip rule del from 192.168.3.0/24 table 3 prio 3000
    {
        print "$ippath rule del from $2 table $3 prio $1\n";
        system("$ippath rule del from $2 table $3 prio $1");
    }
    elsif ($_ =~ /(\d+):\s+from\s+([\d\.\/]+)\s+lookup\s+main blackhole/)
    {
        print "$ippath rule del from $2 blackhole prio $1\n";
        system("$ippath rule del from $2 blackhole prio $1");
    }
    elsif ($_ =~ /(\d+):\s+from\s([\d\.\/]+)\s+to\s+([\d\.\/]+)\s+lookup\s+(\d+)/)
    #example: ip rule add from 192.168.3.0/24 to 140.113.23.0/24 table 3
    {
        print "$ippath rule del from $2 to $3 table $4 prio $1\n";
        system("$ippath rule del from $2 to $3 table $4 prio $1");
    }
    elsif ($_ =~ /(\d+):\s+from\s([\d\.\/]+)\s+to\s+([\d\.\/]+)\s+lookup\s+main blackhole/)
    {
        print "$ippath rule del from $2 to $3 blackhole prio $1\n";
        system("$ippath rule del from $2 to $3 blackhole prio $1");
    }
    elsif ($_ =~ /(\d+):\s+from\s+all\s+to\s+(.+)\s+fwmark\s+(.+)\s+lookup\s+(\d+)/)
    {
        print "$ippath rule del fwmark $3 to $2 table $4 prio $1\n";
        system("$ippath rule del fwmark $3 to $2 table $4 prio $1");
    }
    elsif ($_ =~ /(\d+):\s+from\s+all\s+to\s+(.+)\s+fwmark\s+(.+)\s+lookup\s+main blackhole/)
    {
        print "$ippath rule del fwmark $3 to $2 blackhole prio $1\n";
        system("$ippath rule del fwmark $3 to $2 blackhole prio $1");
    }
    elsif ($_ =~ /(\d+):\s+from\s+all\s+fwmark\s+(.+)\s+lookup\s+(\d+)/)
    #ip rule add fwmark 1dc57 table 3 prio 3000
    {
        print "$ippath rule del fwmark $2 table $3 prio $1\n";
        system("$ippath rule del fwmark $2 table $3 prio $1");
    }
    elsif ($_ =~ /(\d+):\s+from\s+all\s+fwmark\s+(.+)\s+lookup\s+main blackhole/)
    #ip rule add fwmark 1dc57 table 3 prio 3000
    {
        print "$ippath rule del fwmark $2 blackhole prio $1\n";
        system("$ippath rule del fwmark $2 blackhole prio $1");
    }
}


#ip rule add from 192.168.3.0/24 table 3 prio 3000
#ip rule add from 192.168.3.0/24 to 140.113.23.0/24 table 3
#ip rule add from 192.168.3.0/24 to 140.113.0.0/24 table 3 prio 3000
#
#ip rule add from 192.168.3.0/24 to 140.113.0.0/24 table 3 prio 3000
#ip rule add fwmark 13492 to 140.113.0.0/24 table 3 prio 3000
#
#ip rule add fwmark 39716 to 140.113.0.0/24 table 3 prio 3000
#
#ip rule add fwmark 1dc57 table 3 prio 3000
#ip rule add fwmark 39716 table 3 prio 3000
#
#ip rule add from 192.168.2.0/24 table 3 prio 3000

close(FD);
