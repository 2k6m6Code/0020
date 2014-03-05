#!/usr/bin/perl
 
require ('/usr/local/apache/qb/qbmod.cgi');

my $QB_BASIC = "/usr/local/apache/active/basic.xml";
my $ispinfo = XMLread($QB_BASIC);
my $isplist = $ispinfo->{isp};
my $remote = $ARGV[0];
#-----------------------------------------------------------------
if ( $ispinfo ) #if the string is NULL
{
    print "$QB_BASIC_FILE is NULL \n";
}
#------------------------------------------------------------------    
       
foreach my $isp ( @$isplist )
{
    if ( $isp->{remote} eq $remote )
    {
        $isp->{dmpv} = "1";
    }
}
XMLwrite($ispinfo, $QB_BASIC);
