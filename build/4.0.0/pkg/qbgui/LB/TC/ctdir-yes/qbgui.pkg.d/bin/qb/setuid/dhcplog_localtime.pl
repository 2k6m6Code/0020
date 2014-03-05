#!/usr/bin/perl
# Converts dhcpd.lease to show local time
use English;
use Time::localtime;
use Time::Local;  # for timegm()
print "Usage: $PROGRAM_NAME dhcpd.lease\n" if ($#ARGV < 0);
$file = shift(@ARGV);
open(IN,"<$file") || die "Can't open input file \"$file\" $!";

while (<IN>) 
{
    if (/^(\s+(starts|ends)\s+\d+\s+)([^;]+)/) 
	{
		my $beforeTimeStr=$2.' ';
		my $gmtStr = $3;
		print $beforeTimeStr,convertToLocalTime($gmtStr),$POSTMATCH;
    } 
	else 
	{
		print;
    }
}

sub convertToLocalTime 
{
	my($gmtStr) = shift(@_);    # time in GMT in fmt YYYY/MM/DD HH:MM:SS
	($Y,$M,$D,$h,$m,$s) = split(/[ :\/]/,$gmtStr);
	my $localtime = ctime(timegm($s,$m,$h,$D, $M-1, $Y-1900));
	return "$localtime";
	#return "$gmtStr GMT, Localtime: $localtime";
}
