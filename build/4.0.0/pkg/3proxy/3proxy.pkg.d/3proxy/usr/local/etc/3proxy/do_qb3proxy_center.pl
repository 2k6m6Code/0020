#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');
my $source = get_subnet($ARGV[0]);
my $remotegateway = $ARGV[1];
my $port = $ARGV[2];
my $QB_3PROXY_CONF = "/usr/local/etc/3proxy/3proxy.cfg";
my $QB_FWMARK_XMLCONF = "/usr/local/apache/qbconf/fwmark.xml";

if ( $source eq '' || !isValidIP($remotegateway) )
{
    print "Bad argument!!!\n";
}

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/fwmark.xml
#------------------------------------------------------------------
my $fwmark=XMLread($QB_FWMARK_XMLCONF);

if( !$fwmark ) #if the string is NULL
{
    print "$QB_FWMARK_XMLCONF is NULL \n";
}

#---------------------------------------------------------------
# to modify 3proxy.cfg
#----------------------------------------------------------------
my $zone=XMLread($gPATH.'zonecfg.xml');
my $natarray=$zone->{nat};
my $interface_ip;
foreach my $nat ( @$natarray )
{
    if ( $nat->{network} eq $source )
    {
        $interface_ip = $nat->{ip};
        last;
    }
}

modifyfile($QB_3PROXY_CONF, "^external.*", "external $interface_ip"); 
modifyfile($QB_3PROXY_CONF, "^internal.*", "internal 172.31.3.1"); 
modifyfile($QB_3PROXY_CONF, "^tcppm.*", "tcppm $port $remotegateway $port"); 


#------------------------------------------------------------------
# iptables proxy.sh 
#------------------------------------------------------------------

my $QB_PROXY_CONF="/tmp/proxy.sh";
#my $DELQB_PROXY_CONF="/usr/local/squid/etc/delproxy.sh";
if ( !open(PROXY,">$QB_PROXY_CONF") )
{
    print qq (Fail to Open Proxy Script Config file !!);
}

print PROXY qq "/usr/local/sbin/iptables -t nat -A PREROUTING -s $source -d $remotegateway -p tcp --dport $port -j DNAT --to-dest 172.31.3.1:$port\n";
#-------------------------------------------------
# remark 
#-------------------------------------------------
my $num=0;
my $frommark=$fwmark->{from}->[0]->{mark};
my $fromtomark=$fwmark->{from_to}->[0]->{mark};
my $tomark=$fwmark->{to}->[0]->{mark};
foreach my $from ( @$frommark )
{
    if ( $from->{direction} eq 'd' && $from->{source} eq $source )
    #if ( $from->{direction} eq 'd' )
    {
        my $remark;
        my $table = (hex($from->{value}) & 0x00ff0000) >> 16;
        if ( (hex($from->{value}) & 0x01000000) || (hex($from->{value}) & 0x02000000) || (hex($from->{value}) & 0x20000000) )
        {
            $remark = dec2hex(hex($from->{value}) | 0x80000000);
        }
        else
        {
            $remark = dec2hex(hex($from->{value}));
        }
        my $address = get_rule_address('src', $from->{source});
        print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
        print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address  -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
    }
}

foreach my $from ( @$frommark )
{
    if ( $from->{direction} eq 's' && $from->{source} eq $source )
    #if ( $from->{direction} eq 's' )
    {
        my $remark;
        my $table = (hex($from->{value}) & 0x00ff0000) >> 16;
        if ( (hex($from->{value}) & 0x01000000) || (hex($from->{value}) & 0x02000000) || (hex($from->{value}) & 0x20000000) )
        {
            $remark = dec2hex(hex($from->{value}) | 0x80000000);
        }
        else
        {
            $remark = dec2hex(hex($from->{value}));
        }
        my $address = get_rule_address('src', $from->{source});
        print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
        print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
    }
}

foreach my $fromto ( @$fromtomark )
{
    if ( $fromto->{direction} eq 'd' && $fromto->{source} eq $source )
    #if ( $fromto->{direction} eq 'd' )
    {
        my $remark;
        my $table = (hex($fromto->{value}) & 0x00ff0000) >> 16;
        if ( (hex($fromto->{value}) & 0x01000000) || (hex($fromto->{value}) & 0x02000000) || (hex($fromto->{value}) & 0x20000000) )
        {
            $remark = dec2hex(hex($fromto->{value}) | 0x80000000);
        }
        else
        {
            $remark = dec2hex(hex($fromto->{value}));
        }
        my $address = get_rule_address('src', $fromto->{source});
        print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -d $fromto->{destination} -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
        print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -d $fromto->{destination} -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
    }
}

foreach my $fromto ( @$fromtomark )
{
    if ( $fromto->{direction} eq 's' && $fromto->{source} eq $source )
    #if ( $fromto->{direction} eq 's' )
    {
        my $remark;
        my $table = (hex($fromto->{value}) & 0x00ff0000) >> 16;
        if ( (hex($fromto->{value}) & 0x01000000) || (hex($fromto->{value}) & 0x02000000) || (hex($fromto->{value}) & 0x20000000) )
        {
            $remark = dec2hex(hex($fromto->{value}) | 0x80000000);
        }
        else
        {
            $remark = dec2hex(hex($fromto->{value}));
        }
        my $address = get_rule_address('src', $fromto->{source});
        print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -d $fromto->{destination} -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
        print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -d $fromto->{destination} -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
    }
}
=cut
foreach my $to ( @$tomark )
{
    if ( $to->{value} ne '' )
    {
        if ( $to->{direction} eq 'd' )
        {
            #my $remark = dec2hex(hex($to->{value}) | 0x80000000);
            my $remark;
            my $table = (hex($to->{value}) & 0x00ff0000) >> 16;
            #if ( $table < 100 )
            if ( (hex($to->{value}) & 0x01000000) || (hex($to->{value}) & 0x02000000) || (hex($to->{value}) & 0x20000000) )
            {
                $remark = dec2hex(hex($to->{value}) | 0x80000000);
            }
            else
            {
                $remark = dec2hex(hex($to->{value}));
            }
            my $address = get_rule_address('dst', $to->{destination});
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
        }
    }
}
foreach my $to ( @$tomark )
{
    if ( $to->{value} ne '' )
    {
        if ( $to->{direction} eq 's' )
        {
            #my $remark = dec2hex(hex($to->{value}) | 0x80000000);
            my $remark;
            my $table = (hex($to->{value}) & 0x00ff0000) >> 16;
            #if ( $table < 100 )
            if ( (hex($to->{value}) & 0x01000000) || (hex($to->{value}) & 0x02000000) || (hex($to->{value}) & 0x20000000) )
            {
                $remark = dec2hex(hex($to->{value}) | 0x80000000);
            }
            else
            {
                $remark = dec2hex(hex($to->{value}));
            }
            my $address = get_rule_address('dst', $to->{destination});
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
        }
    }

}
=cut

close(PROXY);
chmod(0755, $QB_PROXY_CONF);

sub get_rule_address
{
	my ($direction, $ipaddress) = ($_[0], $_[1]);
	my $rule_address;
	#print "$ipaddress\n";
	if (grep(/-/, $ipaddress))
	{
	    $rule_address = "-m iprange --$direction-range $ipaddress";
	   
	}
	else
	{
	    my $direct = ( $direction eq 'src' ) ? ( 's' ) : ( 'd' );
	    $rule_address = "-$direct $ipaddress";
	}
	return $rule_address;
}
