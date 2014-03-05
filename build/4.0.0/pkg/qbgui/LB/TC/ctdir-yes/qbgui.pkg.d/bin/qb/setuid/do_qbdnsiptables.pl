#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
#my $QB_SQUID_XMLCONF="/usr/local/apache/qbconf/pxyinit.xml";
#my $QB_SQUID_CONF="/usr/local/squid/etc/squid.conf";
my $QB_ZONE_XMLCONF="/usr/local/apache/qbconf/zonecfg.xml";
my $QB_FWMARK_XMLCONF="/usr/local/apache/qbconf/fwmark.xml";
#my $QB_SQUID_CONF = "/usr/local/squid/etc/squid.conf";
my $QB_SCHEDULE_XML = "/usr/local/apache/qbconf/schedule.xml";
my $QB_SQUID_XML = "/usr/local/apache/qbconf/squidgen.xml";
my $QB_SQUIDURL_XML = "/usr/local/apache/qbconf/squidurl.xml";
##my $QB_SQUIDGUARD_CONFIG = "/usr/local/squidGuard/squidGuard.conf";
#my $QB_SQUID_CONF = "/usr/local/squid/etc/squid.conf";
my $QB_DNS_FILE = "/usr/local/apache/qbconf/overview.xml";
my $QB_DNS_XML = "/usr/local/apache/qbconf/inidns.xml";
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
# add udp_outgoing_address
#----------------------------------------------------------------
#if ( !open(ADD_UDPOUT,">>$QB_SQUID_CONF") )
#{
#    print qq (Fail to Open QB_SQUID_CONF Config file !!);
#}

#--------------------------------------------------------------------
# read the option from the file /usr/local/apache/qbconf/schedule.xml
#--------------------------------------------------------------------

#my $schedule = XMLread ( $QB_SCHEDULE_XML );
#my $schlist = $schref->{schedule};
my $schedule = XMLread ( $QB_SCHEDULE_XML );
my $schedulelist = $schedule->{schedule};

if ( !$schedule ) # if the string is NULL
{
    print " $QB_SCHEDULE_XML is NULL \n";
}

#--------------------------------------------------------------------
# read the option from the file /usr/local/apache/qbconf/overview.xml
#--------------------------------------------------------------------

my $relay = XMLread ( $QB_DNS_FILE );

if ( !$ relay )
{
    print "QB_DNS_FILE is NULL \n";
}

#--------------------------------------------------------------------
# read the option from the file /usr/local/apache/qbconf/inidns.xml
#--------------------------------------------------------------------

my $dnsrelay = XMLread ( $QB_DNS_XML );
my $dnsrelaylist = $dnsrelay->{class};

if ( !$dnsrelay ) #if the string is NULL
{
    print "$QB_DNS_XML is NULL \n";
}

#--------------------------------------------------------------------
# read the option from the file /usr/local/apache/qbconf/squidgen.xml
#--------------------------------------------------------------------

my $squid = XMLread ( $QB_SQUID_XML );

if ( !$squid ) # if the string is NULL
{
    print "QB_SQUID_XML is NULL \n";
}

#my $copyconfig = `cp -f /usr/local/squid/etc/squidGuard.conf.bak /usr/local/squidGuard/squidGuard.conf`;
#if ( $copyconfig )
#{
#    print "copy squidGuard.conf error\n";
#}

#------------------------------------------------------------------
# iptables proxy.sh 
#------------------------------------------------------------------

my $QB_DNSPROXY_CONF="/usr/local/bind/etc/dnsproxy.sh";
my $DELQB_DNSPROXY_CONF="/usr/local/bind/etc/deldnsproxy.sh";
if ( !open(DNSPROXY,">$QB_DNSPROXY_CONF") )
{
    print qq (Fail to Open DNSProxy Script Config file !!);
}
if ( !open(DELDNSPROXY,">$DELQB_DNSPROXY_CONF") )
{
    print qq (Fail to Open DNSProxy Script Config file !!);
}
my $dnsproxyport=runCommand(command=>'grep', params=>'dnsproxy_port /usr/local/bind/etc/dnspxy.conf|awk \'{print $2}\'');
$dnsproxyport=~s/\n//g;

#@$dnsrelaylist = sort ini_class_sort_by_realip ( @$dnsrelaylist );

foreach my $dnsrelay ( @$dnsrelaylist )
{
    my $addresslist;
    if ( $dnsrelay->{source} eq 'system' ) {  next; }

    if ( grep(/^host-/, $dnsrelay->{source}) ) 
    {
        my $tmpsource = $dnsrelay->{realip};
        $tmpsource =~ s/realip-//g;
        $addresslist = maintainHost ( action=>'GETADDRESSLIST', hostname=>$tmpsource);
        
#            my $address = get_rule_address('src', $dnsrelay->{realip});
            
#            print DNSPROXY qq "/usr/local/sbin/iptables -t nat -A PREROUTING -p udp --dport 53 $address -j REDIRECT --to-port $dnsproxyport\n";
#            print DELDNSPROXY qq "/usr/local/sbin/iptables -t nat -D PREROUTING -p udp --dport 53 $address -j REDIRECT --to-port $dnsproxyport\n";
        print qq ($dnsrelay->{realip}\n);
        if ( $dnsrelay->{schedule} eq 'All Week' )
        {

            my $address = get_rule_address('src', $dnsrelay->{realip});
            
            print DNSPROXY qq "/usr/local/sbin/iptables -t nat -A PREROUTING -p udp --dport 53 $address -j REDIRECT --to-port $dnsproxyport\n";
            print DELDNSPROXY qq "/usr/local/sbin/iptables -t nat -D PREROUTING -p udp --dport 53 $address -j REDIRECT --to-port $dnsproxyport\n";
        }
        else
        {
            foreach my $sch ( @$schedulelist )
            {
                 my $schedulelist;
                 if ( $sch->{schname} eq $dnsrelay->{schedule} )
                 {
                     print qq ($sch->{schname}\n);
                 
                     $time .= "timedns$count {\n";
                     my $subsch = $sch->{subsch};
                     foreach my $item ( @$subsch )
                     {
                         my $address = get_rule_address('src', $dnsrelay->{realip});
                         
                         print DNSPROXY qq "/usr/local/sbin/iptables -t nat -I PREROUTING -p udp --dport 53 $address -m time --timestart $item->{timestart} --timestop $item->{timestop} --days $item->{days} -j REDIRECT --to-port $dnsproxyport\n";
                         print DELDNSPROXY qq "/usr/local/sbin/iptables -t nat -D PREROUTING -p udp --dport 53 $address -m time --timestart $item->{timestart} --timestop $item->{timestop} --days $item->{days} -j REDIRECT --to-port $dnsproxyport\n";
                         
                     }
                 }
            }  
        }
    }
    else
    {
        $addresslist = $dnsrelay->{realip};
        print qq ($dnsrelay->{realip}\n);
        
        if ( $dnsrelay->{schedule} eq 'All Week' )
        {

            my $address = get_rule_address('src', $dnsrelay->{realip});
            
            print DNSPROXY qq "/usr/local/sbin/iptables -t nat -A PREROUTING -p udp --dport 53 $address -j REDIRECT --to-port $dnsproxyport\n";
            print DELDNSPROXY qq "/usr/local/sbin/iptables -t nat -D PREROUTING -p udp --dport 53 $address -j REDIRECT --to-port $dnsproxyport\n";
        }
        else
        {
            foreach my $sch ( @$schedulelist )
            {
                 my $schedulelist;
                 if ( $sch->{schname} eq $dnsrelay->{schedule} )
                 {
                     print qq ($sch->{schname}\n);
                 
                     my $subsch = $sch->{subsch};
                     foreach my $item ( @$subsch )
                     {
                         my $address = get_rule_address('src', $dnsrelay->{realip});

                         print DNSPROXY qq "/usr/local/sbin/iptables -t nat -I PREROUTING -p udp --dport 53 $address -m time --timestart $item->{timestart} --timestop $item->{timestop} --days $item->{days} -j REDIRECT --to-port $dnsproxyport\n";
                         print DELDNSPROXY qq "/usr/local/sbin/iptables -t nat -D PREROUTING -p udp --dport 53 $address -m time --timestart $item->{timestart} --timestop $item->{timestop} --days $item->{days} -j REDIRECT --to-port $dnsproxyport\n";
                     }
                  }
              } 
          } 
#        print DNSPROXY qq "/usr/local/sbin/iptables -t nat -A PREROUTING -p udp --dport 53 $address -j REDIRECT --to-port $dnsproxyport\n";
#        print DELDNSPROXY qq "/usr/local/sbin/iptables -t nat -D PREROUTING -p udp --dport 53 $address -j REDIRECT --to-port $dnsproxyport\n";

    }
    
}



#------------------------------------------------------------------
# accept dmz
#------------------------------------------------------------------
#my $ispref=XMLread($gPATH.'basic.xml');
#my $isplist=$ispref->{isp};
#my @dmz;
#my %dmzfakeip;
#foreach my $isp ( @$isplist )
#{

#   my @tempsubnet=split(/\//, $isp->{subnet});
#   if ( $tempsubnet[0] ne '' && $tempsubnet[1] ne '32' ) { push(@dmz, $isp->{subnet}); }
#}
#if ( $dmz ne '0' )
#{
#    if ( !open(ADDDMZ,">>$QB_SQUID_CONF") )
#    {
#        print qq (Fail to Open QB_SQUID_CONF Config file !!);
#    }
#    $statement="accept dmz";
#    my $newstatement=$statement."\n";
#    my @fakeip=("172.31.1.1", "172.31.1.2", "172.31.1.3", "172.31.1.4");
#    my $index=0;
#    foreach my $item ( @dmz )
#    {
#         if ( $index > 3) { last; }
#         $newstatement .= "acl localnet src ".$item."\n";
#         print ADDDMZ qq "acl dmz$index src $item\n";
#         print ADDDMZ qq "udp_outgoing_address $fakeip[$index] dmz$index\n";
#         $dmzfakeip{$item}=$fakeip[$index];
#         $index++;
#    }
#    modifyfile($QB_SQUID_CONF,$statement,$newstatement);
#    close(ADDDMZ);
#}
#------------------------------------------------------------------
# accept lan  
#------------------------------------------------------------------

#my $zone=XMLread($gPATH.'zonecfg.xml');
#my $natarray=$zone->{nat};
#$statement="accept lan";
#my $newstatement=$statement."\n";
#foreach my $nat ( @$natarray )
#{
#   if ( $nat->{network} ne '' )
#   {
       $newstatement .= "acl localnet src ".$nat->{network}."\n";
#   }
#}
#modifyfile($QB_SQUID_CONF,$statement,$newstatement);

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
  print ADD_UDPOUT qq "visible_hostname qb$host";
}

foreach my $from ( @$frommark )
{
    if ( $from->{direction} eq 'd' )
    {
#        print qq ($from->{source}\n);
        
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
            print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
            print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address  -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
            print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
        }else
        {
            print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
            print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address  -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
            print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
	}
        foreach my $nat ( @$natarray )
        {
            if ( $from->{source} eq $nat->{network} && $nat->{ip} ne '' )
            {
                print qq ($from->{source}\n);
                print qq ($nat->{network}\n);
                print qq ($nat->{ip}\n);
                
                
                print ADD_UDPOUT qq "acl subnet$num src $nat->{network}\n";
                print ADD_UDPOUT qq "udp_outgoing_address $nat->{ip} subnet$num\n";
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
        if( -e $IPSEC_FILE)
        {
            print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
            print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
            print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
        }else
        {
            print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
            print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
            print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
            print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
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
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --sport $dnsproxyport  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --sport $dnsproxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --sport $dnsproxyport  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --sport $dnsproxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m state --state NEW -j CONNMARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
            }else
            {
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --sport $dnsproxyport  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --sport $dnsproxyport  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --sport $dnsproxyport  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --sport $dnsproxyport  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m state --state NEW -j CTDIRMARK --set-mark_original 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m ctdirmark --mark_original 0x$remark -j MARK --set-mark 0x$remark\n";
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
            if(-e $IPSEC_FILE)
            {
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --sport $dnsproxyport  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --sport $dnsproxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --sport $dnsproxyport  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --sport $dnsproxyport  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m state --state REPLY -m connmark ! --mark 0x$remark -j CONNMARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m connmark --mark 0x$remark -j MARK --set-mark 0x$remark\n";
            }else
            { 
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --sport $dnsproxyport  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --sport $dnsproxyport  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --sport $dnsproxyport  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --sport $dnsproxyport  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print DNSPROXY qq "/sbin/iptables -t mangle -A OUTPUT -p udp --dport 53  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m state --state REPLY -m ctdirmark ! --mark_reply 0x$remark -j CTDIRMARK --set-mark_reply 0x$remark\n";
                print DELDNSPROXY qq "/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  $address -m ctdirmark --mark_reply 0x$remark -j MARK --set-mark 0x$remark\n";
            }
        }
    }

}
print ADD_UDPOUT qq "acl anysubnet src 0.0.0.0/0\n";
print ADD_UDPOUT qq "udp_outgoing_address 172.31.3.1 anysubnet\n";
close(DNSPROXY);
close(DELDNSPROXY);
close(ADD_UDPOUT);
chmod(0755, $QB_DNSPROXY_CONF);
chmod(0755, $DELQB_DNSPROXY_CONF);

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

