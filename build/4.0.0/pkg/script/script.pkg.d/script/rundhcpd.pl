#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
#my $QB_ZONE_XML="/usr/local/apache/active/zonecfg.xml";
my $QB_ZONE_XML="/usr/local/apache/qbconf/zonecfg.xml";
my $QB_ARP_XML="/usr/local/apache/active/arp.xml";

my $DHCP_CONF_V6="/etc/radvd.conf";
my $DHCP_CONF="/etc/dhcpd.conf";

my $zone=XMLread($QB_ZONE_XML);
my $arp=XMLread($QB_ARP_XML);
my $natarray=$zone->{nat};
my $dmzarray=$zone->{dmz};
my $hostarray=$arp->{arp};
my %nicset;
my %bridgeset;

open(DHCPD, "> $DHCP_CONF" );
open(DHCPD_v6, "> $DHCP_CONF_V6" );
foreach $nat ( @$natarray )
{
    if ( ! $nat->{dhcp} ) { next; }
    if ( $nat->{gateway} ) { next; }

    $nicset{$nat->{nic}}=1;
    if ( !grep(/:/,$nat->{network}))
    {
    	my ( $subnetip, $bitcountmask )=split( /\//, $nat->{network});
    	my $ipmask=nummask2ipmask($bitcountmask);
    	print DHCPD qq(subnet $subnetip netmask $ipmask \{ \n);
    	print DHCPD qq(default-lease-time $nat->{dftlease}\;\n);
    	print DHCPD qq(max-lease-time $nat->{maxlease}\;\n);
    
    	print DHCPD qq(option subnet-mask $ipmask\;\n);
    	print DHCPD qq(option routers $nat->{ip}\;\n);
    	my $bcastip=get_bcast_ip($nat->{network});
    	print DHCPD qq(option broadcast-address $bcastip\;\n);
    
    	my @rangearray=split(/;/, $nat->{rangelist});
    
    	foreach my $range ( @rangearray )
    	{
            $range=~s/\s+|-+|~/ /g;
        
            my ($start, $end)=split(/\s/, $range);

            if ( isSubnetUsableIP($start, $nat->{network}) != 1 ) { next; }
            if ( isSubnetUsableIP($end, $nat->{network}) != 1 ) { next; }
        
            print DHCPD qq(     range $range\;\n);
        }
    
    	## for dhcp-DNS setting...nancy 20040901
    	if ($nat->{dnslist}) {
            my @dnsarray=split(/,/, $nat->{dnslist});
            print DHCPD qq(option domain-name-servers );
            my $dnsflag=0;
            foreach my $dns ( @dnsarray )
            {
            	if ($dnsflag) { print DHCPD qq(\, ); $dnsflag=0;}

            	$dnsflag=1; 
            	print DHCPD qq($dns);
            }
            print DHCPD qq(\;\n);
    	} 
    	if ($nat->{dname}) {
            print DHCPD qq(option domain-name "$nat->{dname}"\;\n);
    	} 

    	print DHCPD qq(\} \n);
    }else
    {
    	print DHCPD_v6 qq(interface $nat->{nic} \{ \n);
    	print DHCPD_v6 qq(AdvSendAdvert on;\n);
    	print DHCPD_v6 qq(MinRtrAdvInterval 5;\n);
    	print DHCPD_v6 qq(MaxRtrAdvInterval 15;\n);
    	print DHCPD_v6 qq(prefix $nat->{network} \{\n);
    	print DHCPD_v6 qq(AdvOnLink on;\n);
    	print DHCPD_v6 qq(AdvAutonomous on;\n);
    	print DHCPD_v6 qq(\};\n\};);
    }
}
if ( !grep(/:/,$nat->{network}))
{
    my $hostcount=1;
    foreach $host ( @$hostarray )
    {
    	if ( ! $host->{arpdhcpadd} ) { next; }
    	print DHCPD qq(host host$hostcount \{ \n);
    	print DHCPD qq(hardware ethernet $host->{mac} \;\n);
    	print DHCPD qq(fixed-address $host->{ip} \;\n);
    	print DHCPD qq(\} \n);
    	$hostcount++;
    }
}
close(DHCPD);
close(DHCPD_v6);

# restart dhcpd to load new dhcpd.conf
# step1 kill it
runCommand(command=>'killall', params=>' -9 dhcpd');
runCommand(command=>'killall', params=>' -9 radvd');

foreach $dmz ( @$dmzarray )
{
    if ( $dmz->{mode} ne 'BRIDGE' ) { next; }
    $bridgeset{$dmz->{nic}}=1;
}

# step2 restart it
if ( ! -z $DHCP_CONF )
{
    my $nic_with_dhcp='';
    #foreach my $nic ( keys %nicset ) { $nic_with_dhcp.=$nic.' '; }
    foreach my $nic ( keys %nicset )
    { 
      print "$nic => $nicset{$nic}\n";
      if (%bridgeset)
      {
       foreach my $dmz ( keys %bridgeset )
       { 
        if ( $dmz eq $nic ){$nic_with_dhcp.=' br0 ';};
        if ( $dmz ne $nic ){$nic_with_dhcp.=$nic.' ';};
       }
      }else{
      $nic_with_dhcp.=$nic.' '; 
      }
    }
    print "nic_with_dhcp => $nic_with_dhcp\n";
    runCommand(command=>'sleep', params=>'5'); # To wait qbmod.cgi when QB on booting.
    runCommand(command=>'dhcpd', params=>$nic_with_dhcp);
}
if( ! -z $DHCP_CONF_V6)
{
    runCommand(command=>'sleep', params=>'5'); # To wait qbmod.cgi when QB on booting.
    runCommand(command=>'/usr/local/sbin/radvd', params=>'-C /etc/radvd.conf');
}
