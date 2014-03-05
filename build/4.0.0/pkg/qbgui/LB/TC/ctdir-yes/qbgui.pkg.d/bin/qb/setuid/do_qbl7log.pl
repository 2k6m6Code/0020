#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# --------------------------
#
# main program start routine
#
# --------------------------
my $QB_LAYER7_FILE="/usr/local/apache/qbconf/l7log.xml";
my $QB_LAYER7_CONF="/usr/local/apache/qbconf/l7log.sh";

my $l7log=XMLread($QB_LAYER7_FILE);

if(!$l7log) { print "$QBHA_LAYER7_FILE is NULL \n"; }#if the string is NULL
#------------------------------------------------------------------
if ( !open(LAYER7,">$QB_LAYER7_CONF") )
{
    print qq (Fail to Open LAYER7 Config file !!);
}
#------------------------------------------------------------------
foreach my $l7service ( sort  keys %gL7PROTOCOLHASH )
{
    if ( $l7log->{$l7service} )
    {
         if ( $l7service eq 'snmp' )
          { 
               print LAYER7 qq(iptables -t mangle -A PREROUTING  -m layer7 --l7proto snmp-trap -m limit --limit 1/s --limit-burst 1 -j LOG --log-level notice  --log-prefix snmp-trap: \n);
               print LAYER7 qq(iptables -t mangle -A PREROUTING  -m layer7 --l7proto snmp-mon -m limit --limit 1/s --limit-burst 1 -j LOG --log-level notice  --log-prefix snmp-monitor: \n);
          }
         elsif ( $l7service eq 'msnmessenger' )
          { 
               print LAYER7 qq(iptables -t mangle -A PREROUTING  -m layer7 --l7proto msn-filetransfer -m limit --limit 1/s --limit-burst 1 -j LOG --log-level notice  --log-prefix msn-filetransfer: \n);
          }
         elsif ( $l7service eq 'counterstrike' )
          { 
               print LAYER7 qq(iptables -t mangle -A PREROUTING  -m layer7 --l7proto counterstrike-source -m limit --limit 1/s --limit-burst 1 -j LOG --log-level notice  --log-prefix counterstrike: \n);
               next;
          }
         elsif ( $l7service eq 'halflife2' )
          { 
               print LAYER7 qq(iptables -t mangle -A PREROUTING  -m layer7 --l7proto halflife2-deathmatch -m limit --limit 1/s --limit-burst 1 -j LOG --log-level notice  --log-prefix halflife2-deathmatch: \n);
               next;
          }
         elsif ( $l7service eq 'dayofdefeat' )
          { 
               print LAYER7 qq(iptables -t mangle -A PREROUTING  -m layer7 --l7proto dayofdefeat-source -m limit --limit 1/s --limit-burst 1 -j LOG --log-level notice  --log-prefix dayofdefeat-source: \n);
               next;
          }
         elsif ( $l7service eq 'quake' )
          { 
               print LAYER7 qq(iptables -t mangle -A PREROUTING  -m layer7 --l7proto quake-halflife -m limit --limit 1/s --limit-burst 1 -j LOG --log-level notice  --log-prefix quake-halflife: \n);
               next;
          }
         my $params='';
         $params.=" -m layer7 --l7proto ".$l7service;
         $params.=" -m limit --limit 1/s --limit-burst 1 -j LOG --log-level notice  --log-prefix ".$l7service.":";
         print LAYER7 qq(iptables -t mangle -A PREROUTING $params \n);
    }
}
close(LAYER7);
