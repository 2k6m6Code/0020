#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start
# --------------------------------------------------------------
my $QB_SQUID="/usr/local/squid/etc/";
my $QB_SQUID_CONF="/usr/local/squid/etc/squid.conf";
my $statement;

#------------------------------------------------------------------
# save log
#------------------------------------------------------------------
$statement="cache_access_log /usr/local/squid/var/logs/";
sub gettime{
	my ($sec, $min, $hour, $day, $mon, $year) = localtime(time);
	$now_date=join("-",($year+1900,$mon+1,$day));
	$now_time=join(":",($hour,$min,$sec));
	return ($now_date, $now_time);
}
my ($now_date, $now_time) = &gettime();
modifyfile($QB_SQUID_CONF, "$statement.*", "$statement$now_date");

