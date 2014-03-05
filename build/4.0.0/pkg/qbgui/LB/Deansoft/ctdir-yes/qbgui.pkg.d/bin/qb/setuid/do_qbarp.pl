#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# --------------------------
#
# main program start routine
#
# --------------------------
my $QB_NEIGHBOR="/usr/local/apache/active/ipneigh.xml";
my $QB_BASIC="/usr/local/apache/active/basic.xml";

my $neighbor=XMLread($QB_NEIGHBOR);
my $neighborList=$neighbor->{ipneigh};
my $ispinfo=XMLread($QB_BASIC);
my $allisp=$ispinfo->{isp};
my $zone=XMLread($gACTIVEPATH.'zonecfg.xml');
my $dmzarray=$zone->{dmz};
if(!$neighbor) { print "$QB_NEIGHBOR is NULL \n"; }#if the string is NULL
if(!$ispinfo) { print "$QB_BASIC is NULL \n"; }#if the string is NULL
#------------------------------------------------------------------
foreach my $neighbor ( @$neighborList )
{
    #Arping from DMZIP to WAN's gateway
    if ( $neighbor->{ip} eq 'system' ) { next; }
    runCommand(command=>'sysctl', params=>qq(-w net.ipv4.ip_nonlocal_bind=1));
    foreach my $isp ( @$allisp ) 
    { 
       if ( $isp->{iid} eq $neighbor->{isp} && $isp->{gateway} ne $neighbor->{ip}) 
       {
          my $params='';
          $params.="-I $neighbor->{nic} -s $neighbor->{ip} $isp->{gateway} -c 1 -w 1";
          #print "$params \n";
          runCommand(command=>"/sbin/arping", params=>qq($params));
       } 
    }
=cut
    #Arping from Systemip to LAN
    foreach my $isp ( @$allisp ) 
    { 
       if ( $isp->{iid} eq $neighbor->{isp} && $isp->{gateway} ne $neighbor->{ip}) 
       {
          my $dmzzonenic=maintainZone( action=>"GETDMZNIC", isp=>$isp->{iid} );
          my $params='';
          $params.="-I $dmzzonenic -s $isp->{systemip} $neighbor->{ip} -c 1 -w 1";
          #print "$params \n";
          runCommand(command=>"/sbin/arping", params=>qq($params));
       } 
    }
=cut
    runCommand(command=>'sysctl', params=>qq(-w net.ipv4.ip_nonlocal_bind=0));
}

foreach my $dmz ( @$dmzarray )
{ 
  if ( $dmz->{enabled} eq '1' && $dmz->{isp} ne 'system' && $dmz->{mode} eq 'ARPPROXY') 
  { 
     foreach my $item ( @$allisp )
     {
       if( $item->{iid} eq $dmz->{isp} )
       { 
          $item->{subnet}=~s/^.*\//$item->{systemip}\//g;
          #print "addr $item->{subnet} add broadcast 255.255.255.255 dev $dmz->{nic} \n";
          runCommand(command=>'/sbin/ip', params=>qq(addr add $item->{subnet} broadcast 255.255.255.255 dev $dmz->{nic} ));
       }
     }
                                          
  }
}

