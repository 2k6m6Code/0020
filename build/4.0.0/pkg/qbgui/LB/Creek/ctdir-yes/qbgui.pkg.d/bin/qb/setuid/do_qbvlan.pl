#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# --------------------------
#
# main program start routine
#
# --------------------------
my $QB_VLAN_FILE="/usr/local/apache/qbconf/vlan.xml";
my $QB_VLAN_CONF="/mnt/conf/vlan.con";

my $vlan=XMLread($QB_VLAN_FILE);
my $vlanList=$vlan->{vlan};
if(!$vlan) { print "$QBHA_VLAN_FILE is NULL \n"; }#if the string is NULL
#------------------------------------------------------------------
if ( !open(VLAN,">$QB_VLAN_CONF") )
{
    print qq (Fail to Open VLAN Config file !!);
}
#------------------------------------------------------------------
foreach my $vlan ( @$vlanList )
{
    if ( $vlan->{vlannic} eq 'system' ) { next; }
    if ( $vlan->{enablevlan} )
    {
        print VLAN qq(vconfig add $vlan->{portnum} $vlan->{vid} \n);
        if ( $vlan->{mac_addr} )
        {
        print VLAN qq(ifconfig $vlan->{portnum}.$vlan->{vid} hw ether $vlan->{mac_addr} \n); #20110624 user add mac
        }
        print VLAN qq(ifconfig $vlan->{portnum}.$vlan->{vid} up \n); #20080911 Brian need to wake up the device
    }
    else
    {
        print VLAN qq(vconfig rem $vlan->{portnum}.$vlan->{vid} \n);
    }
}
close(VLAN);
qbSync(); #20130419 To prevent DOM/CF become readonly
