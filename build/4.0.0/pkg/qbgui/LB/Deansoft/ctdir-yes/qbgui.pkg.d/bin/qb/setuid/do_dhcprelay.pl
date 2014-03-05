#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# --------------------------
#
# main program start routine
#
# --------------------------
my $QB_ZONE_FILE="/usr/local/apache/active/zonecfg.xml";

my $zone=XMLread($QB_ZONE_FILE);
my $zoneList=$zone->{nat};
if(!$zone) { print "$QBHA_ZONE_FILE is NULL \n"; }#if the string is NULL
#------------------------------------------------------------------
foreach my $zone ( @$zoneList )
{
    #if ( !$zone->{dhcp} ) { next; }
    if ( $zone->{dhcprelayip} && $zone->{dhcprelayinterface} )
    {
        $zone->{dhcprelayip}=~s/\,/ /g;
        print qq ($zone->{dhcprelayinterface} $zone->{dhcprelayip});
        runCommand(command=>"/usr/sbin/dhcp-helper", params=>qq( -i $zone->{dhcprelayinterface} -s $zone->{dhcprelayip} ));
    }
}
