#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }
use QB_Xml;

my $xml = new QB_Xml;
my $ispref = $xml->read('/usr/local/apache/qbconf/basic.xml');
my $isplist = $ispref->{isp};
my @fileref;

open(FILE,"</etc/crontab");
foreach my $data (<FILE>)
{
    if (grep(/pool_speed.pl/,$data)){next;}
    push(@fileref,$data);
}
close(FILE);


open(FILE_input,">/etc/crontab");
print FILE_input @fileref;
foreach my $isp (@$isplist)
{
    if ($isp->{iid} eq 'system' || $isp->{time} eq ''){next;}
    print FILE_input "*/$isp->{time}  * * * *  root      /usr/local/apache/qb/pool_speed.pl nic=$isp->{nic}\n";
}
close(FILE_input);
