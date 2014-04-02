#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
my $QB_SQUID_XMLCONF="/usr/local/apache/qbconf/pxyinit.xml";
my $QB_SQUID_CONF="/usr/local/squid/etc/squid.conf";
my $QB_ZONE_XMLCONF="/usr/local/apache/qbconf/zonecfg.xml";
my $QB_FWMARK_XMLCONF="/usr/local/apache/qbconf/fwmark.xml";
my $IPSEC_FILE="/tmp/connmark.txt";


#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/pxyinit.xml
#------------------------------------------------------------------
my $pxyinit=XMLread($QB_SQUID_XMLCONF);

if( !$pxyinit ) #if the string is NULL
{
    print "$QB_SQUID_XMLCONF is NULL \n";
}

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/zonecfg.xml
#------------------------------------------------------------------
my $zone=XMLread($QB_ZONE_XMLCONF);

if( !$zone ) #if the string is NULL
{
    print "$QB_ZONE_XMLCONF is NULL \n";
}
my $natarray=$zone->{nat};

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/fwmark.xml
#------------------------------------------------------------------
my $fwmark=XMLread($QB_FWMARK_XMLCONF);

if( !$fwmark ) #if the string is NULL
{
    print "$QB_FWMARK_XMLCONF is NULL \n";
}

#---------------------------------------------------------------
# add tcp_outgoing_address
#----------------------------------------------------------------
if ( !open(ADD_TCPOUT,">>$QB_SQUID_CONF") )
{
    print qq (Fail to Open QB_SQUID_CONF Config file !!);
}
#------------------------------------------------------------------
# iptables proxy.sh 
#------------------------------------------------------------------

my $QB_PROXY_CONF="/usr/local/squid/etc/proxy.sh";
my $DELQB_PROXY_CONF="/usr/local/squid/etc/delproxy.sh";
if ( !open(PROXY,">$QB_PROXY_CONF") )
{
    print qq (Fail to Open Proxy Script Config file !!);
}
if ( !open(DELPROXY,">$DELQB_PROXY_CONF") )
{
    print qq (Fail to Open Proxy Script Config file !!);
}
my $proxyport=runCommand(command=>'grep', params=>'http_port /usr/local/squid/etc/squid.conf|awk \'{print $2}\'');
$proxyport=~s/\n//g;
my $sproxyport=runCommand(command=>'grep', params=>'https_port /usr/local/squid/etc/squid.conf|awk \'{print $2}\'');
$sproxyport=~s/\n//g;

print PROXY qq "/usr/local/sbin/iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port $proxyport\n";
print DELPROXY qq "/usr/local/sbin/iptables -t nat -D PREROUTING -p tcp --dport 80 -j REDIRECT --to-port $proxyport\n";
#print PROXY qq "/usr/local/sbin/iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port $sproxyport\n";
#print DELPROXY qq "/usr/local/sbin/iptables -t nat -D PREROUTING -p tcp --dport 443 -j REDIRECT --to-port $sproxyport\n";
#------------------------------------------------------------------
# accept dmz
#------------------------------------------------------------------
my $ispref=XMLread($gPATH.'basic.xml');
my $isplist=$ispref->{isp};
my @dmz;
my %dmzfakeip;
foreach my $isp ( @$isplist )
{
   my @tempsubnet=split(/\//, $isp->{subnet});
   if ( $tempsubnet[0] ne '' && $tempsubnet[1] ne '32' ) { push(@dmz, $isp->{subnet}); }
}
if ( $dmz ne '0' )
{
    if ( !open(ADDDMZ,">>$QB_SQUID_CONF") )
    {
        print qq (Fail to Open QB_SQUID_CONF Config file !!);
    }
    $statement="accept dmz";
    my $newstatement=$statement."\n";
    my @fakeip=("172.31.1.1", "172.31.1.2", "172.31.1.3", "172.31.1.4");
    my $index=0;
    foreach my $item ( @dmz )
    {
         if ( $index > 3) { last; }
         $newstatement .= "acl localnet src ".$item."\n";
         print ADDDMZ qq "acl dmz$index src $item\n";
         print ADDDMZ qq "tcp_outgoing_address $fakeip[$index] dmz$index\n";
         $dmzfakeip{$item}=$fakeip[$index];
         $index++;
    }
    modifyfile($QB_SQUID_CONF,$statement,$newstatement);
    close(ADDDMZ);
}
#------------------------------------------------------------------
# accept lan  
#------------------------------------------------------------------

my $zone=XMLread($gPATH.'zonecfg.xml');
my $natarray=$zone->{nat};
$statement="accept lan";
my $newstatement=$statement."\n";
foreach my $nat ( @$natarray )
{
   if ( $nat->{network} ne '' )
   {
       $newstatement .= "acl localnet src ".$nat->{network}."\n";
   }
}
#print $newstatement;
modifyfile($QB_SQUID_CONF,$statement,$newstatement);

#--------------------------------------------------
# remark 
#-------------------------------------------------
my $num=0;
my $frommark=$fwmark->{from}->[0]->{mark};
my $tomark=$fwmark->{to}->[0]->{mark};
my $host=runCommand(command=>"cat", params=>'/mnt/conf/qbsn');
my $dmzpolicy=0;
if ( $host ne '' )
{
  print ADD_TCPOUT qq "visible_hostname qb$host";
}

foreach my $from ( @$frommark )
{
    if ( $from->{direction} eq 'd' )
    {
        if ( $dmzfakeip{$from->{source}} )
        {
            $from->{source}=$dmzfakeip{$from->{source}};
            $dmzpolicy=1;
        }
        
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
        if ( -e $IPSEC_FILE)
        {
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address  -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
			
			print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address  -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
        }else
        {
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address  -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
			
			print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address  -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
	}
        foreach my $nat ( @$natarray )
        {
            if ( $from->{source} eq $nat->{network} && $nat->{ip} ne '' )
            {
                print ADD_TCPOUT qq "acl subnet$num src $nat->{network}\n";
                print ADD_TCPOUT qq "tcp_outgoing_address $nat->{ip} subnet$num\n";
                $num++;
            }
        }
    }
}

foreach my $from ( @$frommark )
{
    if ( $dmzfakeip{$from->{source}} )
    {
        $from->{source}=$dmzfakeip{$from->{source}};
        $dmzpolicy=1;
    }
    if ( $from->{direction} eq 's' )
    {
        my $remark;
        my $table = (hex($from->{value}) & 0x00ff0000) >> 16;
        #if ( $table < 100 )
        if ( (hex($from->{value}) & 0x01000000) || (hex($from->{value}) & 0x02000000) || (hex($from->{value}) & 0x20000000) )
        {
            $remark = dec2hex(hex($from->{value}) | 0x80000000);
        }
        else
        {
            $remark = dec2hex(hex($from->{value}));
        }
        my $address = get_rule_address('src', $from->{source});
        if (-e $IPSEC_FILE)
        {
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
			
			print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
        }else
        {
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
			
			print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
            print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
            print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
        }
    }
}

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
            if (-e $IPSEC_FILE)
            {
               print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $proxyport  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
               print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $proxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
               print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $proxyport  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
               print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $proxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
			   
			   print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $sproxyport  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
               print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $sproxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
               print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $sproxyport  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
               print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $sproxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
			   
			   print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
               print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
               print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
               print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
			   
			   print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
               print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
               print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
               print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
            }else
            {
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $proxyport  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $proxyport  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $proxyport  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $proxyport  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
				
				print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $sproxyport  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $sproxyport  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $sproxyport  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $sproxyport  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
				
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
				
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
            }
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
            if (-e $IPSEC_FILE)
            {
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $proxyport  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
           	print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $proxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
           	print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $proxyport  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
           	print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $proxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
			
			print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $sproxyport  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
           	print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $sproxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
           	print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $sproxyport  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
           	print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $sproxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
			
           	print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
           	print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
           	print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
           	print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
			
			print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
           	print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
           	print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
           	print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
            }else
            {
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $proxyport  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $proxyport  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $proxyport  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $proxyport  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
				
				print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $sproxyport  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --sport $sproxyport  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $sproxyport  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --sport $sproxyport  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
				
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 80  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 80  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
				
				print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print PROXY qq "/sbin/iptables -t mangle -A OUTPUT -p tcp --dport 443  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print DELPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p tcp --dport 443  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
            }
        }
    }

}
print ADD_TCPOUT qq "acl anysubnet src all\n";
print ADD_TCPOUT qq "tcp_outgoing_address 172.31.3.1 anysubnet\n";
close(PROXY);
close(DELPROXY);
close(ADD_TCPOUT);
chmod(0755, $QB_PROXY_CONF);
chmod(0755, $DELQB_PROXY_CONF);

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

