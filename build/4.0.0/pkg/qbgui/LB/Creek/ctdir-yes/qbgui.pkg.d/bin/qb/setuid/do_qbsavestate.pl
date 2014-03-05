#!/usr/bin/perl
 
require ('/usr/local/apache/qb/qbmod.cgi');

my $QB_BASIC = "/usr/local/apache/active/basic.xml";
my $ispinfo = XMLread($QB_BASIC);
my $isplist = $ispinfo->{isp};
my $isplist = $ispinfo->{isp};
#-----------------------------------------------------------------
if ( !$ispinfo ) #if the string is NULL
{
    print "$QB_BASIC_FILE is NULL \n";
}
#------------------------------------------------------------------    

my $sn=@ARGV[0];
my $state=@ARGV[1];
my $time=@ARGV[2];

foreach my $isp ( @$isplist )
{
    if ( $isp->{qbsn} eq $sn )
    {
    	$isp->{upgradestate} = $state;
    	$isp->{reboot_time} = $time;
    }
}

XMLwrite($ispinfo, $gACTIVEPATH."basic.xml");
