#!/usr/bin/perl

my $SQUIDCFG=XMLread('/usr/local/apache/qbconf/pxyinit.xml');
my $FILTERCFG=XMLread("/usr/local/apache/qbconf/squidgen.xml");
my $enablesquidpxy;
my $enablesquidfilter;
foreach my $line ($SQUIDCFG)
{
	$enablesquidpxy=$line->{enablepxy};
}
foreach my $line ($FILTERCFG)
{
	$enablesquidfilter=$line->{isenable};
}
if($enablesquidpxy eq '1'||$enablesquidfilter eq '1'){system("/usr/local/squid/sbin/squid -k reconfigure");}