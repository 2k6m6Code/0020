#!/usr/bin/perl
 
require ('/usr/local/apache/qb/qbmod.cgi');

my $QB_BASIC = "/usr/local/apache/qbconf/basic.xml";
my $QB_IPSECROUTE_CONF = "/etc/racoon/ipsecroute";
my $ispinfo = XMLread($QB_BASIC);
my $isplist = $ispinfo->{isp};
#-----------------------------------------------------------------
if ( $ispinfo ) #if the string is NULL
{
    print "$QB_BASIC_FILE is NULL \n";
}
#------------------------------------------------------------------
if ( !open(ROUTE,">$QB_IPSECROUTE_CONF") )
{
    print qq (Fail to Open IPSECROUTE!!);
}
#------------------------------------------------------------------    
       
foreach my $isp ( @$isplist )
{
    if ( $isp->{isptype} eq "ipsec" )
    {
        if($isp->{enabled} eq "0"){next;}
    	print ROUTE qq "ip route del $isp->{gateway}\n";
    	print ROUTE qq "ip route add $isp->{remotesubnet} via $isp->{systemip} src $isp->{systemip}\n";
    	#print ROUTE qq "/usr/local/sbin/iptables -t filter -D INPUT -d $isp->{systemip} -s $isp->{gateway} -m state --state NEW  -j ACCEPT\n";
    	#print ROUTE qq "/usr/local/sbin/iptables -t filter -I INPUT -d $isp->{systemip} -s $isp->{gateway} -m state --state NEW  -j ACCEPT\n";
    	print ROUTE qq "/usr/local/sbin/iptables -D INPUT -p tcp -d $isp->{systemip} -m state --state NEW  -j DROP\n";
    }
}
close(ROUTE);
chmod 0777, '/etc/racoon/ipsecroute';
