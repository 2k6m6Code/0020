#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# --------------------------
#
# main program start routine
#
# --------------------------
my $QB_LAYER7_FILE="/usr/local/apache/qbconf/layer7.xml";
my $QB_LAYER7_CONF="/usr/local/apache/qbconf/layer7.sh";

my $layer7=XMLread($QB_LAYER7_FILE);
my $layer7List=$layer7->{layer7};
if(!$layer7) { print "$QBHA_LAYER7_FILE is NULL \n"; }#if the string is NULL
#------------------------------------------------------------------
if ( !open(LAYER7,">$QB_LAYER7_CONF") )
{
    print qq (Fail to Open LAYER7 Config file !!);
}
#------------------------------------------------------------------
foreach my $layer7 ( @$layer7List )
{
    if ( $layer7->{l7service} eq 'system' ) { next; }
    my $params='';
    if ( $layer7->{src_subnet}) { $params.=" -s ".$layer7->{src_subnet};}
    if ( $layer7->{dst_subnet}) { $params.=" -d ".$layer7->{dst_subnet};}
    if ( $layer7->{l7service}) { $params.=" -m layer7 --l7proto ".$layer7->{l7service};}
    if ( $layer7->{l7action} eq "Drop")
    { 
       $params.=" -j DROP";
    }
    elsif ( $layer7->{l7action} eq "Log")
    {
       $params.=" -m limit --limit 1/s --limit-burst 1 -j LOG --log-level notice  --log-prefix ".$layer7->{l7service}.":";
    }
    else
   {
       $layer7->{l7action}=~s/ISP//g;
       my $isp=$layer7->{l7action}; 
       my $mark='0x'.dec2hex(1000+$isp);
       $params.=" -j MARK --set-mark ".$mark;
   }
       print LAYER7 qq(iptables -t mangle -A PREROUTING $params \n);
}
close(LAYER7);
