#!/usr/bin/perl  
require ('/usr/local/apache/qb/qbmod.cgi'); 
my $QB_BASIC = "/usr/local/apache/qbconf/basic.xml";
my $QB_IPADDR="/usr/local/apache/qbconf/ipaddr.xml";
my $QB_IPSEC_CONF = "/etc/racoon/ipsec.conf";


my $ispinfo = XMLread($QB_BASIC);
my $isplist = $ispinfo->{isp};
my $ipaddr = XMLread($QB_IPADDR);
my $iplist = $ipaddr->{ipaddress};

my $transport = "ipsec esp/transport//require ah/transport//require";
my $transport_ipcomp = "ipsec ipcomp/transport//use esp/transport//require ah/transport//require";
my $ipsecrule = "/etc/racoon/ipsecrule";
my $delipsecrule = "/etc/racoon/delipsecrule";
my $IPSEC_FILE="/tmp/connmark.txt";

#-----------------------------------------------------------------
if ( $ispinfo ) #if the string is NULL
{
    print "$QB_BASIC_FILE is NULL \n";
}
#------------------------------------------------------------------
if ( !open(IPSEC,">$QB_IPSEC_CONF") )
{
    print qq (Fail to Open IPSEC Config file !!);
}
#------------------------------------------------------------------    
if ( !open(IPRULE,">$ipsecrule") )
{
    print qq (Fail to Open IPSEC rule file !!);
}
#------------------------------------------------------------------    
if ( !open(DELIPRULE,">$delipsecrule") )
{
    print qq (Fail to Open IPSEC rule file !!);
}
#------------------------------------------------------------------    

print IPSEC qq "#!/sbin/setkey -f\n";
print IPSEC qq "flush;\n";
print IPSEC qq "spdflush;\n";
 my $number=24995;
       
foreach my $isp ( @$isplist )
{
    if ( $isp->{enc} )
    {
        my $QB_IPSEC_DELCONF = "/etc/racoon/delipsec." . $isp->{ispname};
 	my $QB_IPSEC_ADDCONF = "/etc/racoon/addipsec." . $isp->{ispname};
        if ( !open(IPSECADD,">$QB_IPSEC_ADDCONF") )
        {
            print qq (Fail to Open IPSEC AddConfig file !!);
	}
        if ( !open(IPSECDEL,">$QB_IPSEC_DELCONF") )
        {
            print qq (Fail to Open IPSEC DelConfig file !!);
	}
	my $ipsecmode = ( $isp->{ipcom} ) ? ( $transport_ipcomp ) : ( $transport );
        print IPSEC qq "spdadd $isp->{local} $isp->{remote} any -P out $ipsecmode;\n";
        print IPSEC qq "spdadd $isp->{remote} $isp->{local} any -P in $ipsecmode;\n";
	print IPSECADD qq "#!/sbin/setkey -f\n";
        print IPSECADD qq "spdadd $isp->{local} $isp->{remote} any -P out $ipsecmode;\n";
        print IPSECADD qq "spdadd $isp->{remote} $isp->{local} any -P in $ipsecmode;\n";
	print IPSECDEL qq "#!/sbin/setkey -f\n";
        print IPSECDEL qq "spddelete $isp->{local} $isp->{remote} any -P out $ipsecmode;\n";
        print IPSECDEL qq "spddelete $isp->{remote} $isp->{local} any -P in $ipsecmode;\n";
        close(IPSECADD);
        close(IPSECDEL);
    }
    
    if ( $isp->{isptype} eq "ipsec" )
    {
        if ( $isp->{remote} ne "0.0.0.0" ) #Brian 20130906 Brian For unknown NATed source IP
        {
        my $QB_IPSEC_DELCONF = "/etc/racoon/delipsec." . $isp->{ispname};
        my $QB_IPSEC_ADDCONF = "/etc/racoon/addipsec." . $isp->{ispname};
        if ( !open(IPSECADD,">$QB_IPSEC_ADDCONF") )
        {
            print qq (Fail to Open IPSEC AddConfig file !!);
        }
        if ( !open(IPSECDEL,">$QB_IPSEC_DELCONF") )
        {
            print qq (Fail to Open IPSEC DelConfig file !!);
	}
     	my $out = $isp->{local} . "-" . $isp->{remote};
     	my $in = $isp->{remote} . "-" . $isp->{local};                            
     	print IPSEC qq "spdadd $isp->{localsubnet} $isp->{remotesubnet} any -P out ipsec ";
     	print IPSEC qq "$isp->{protocol}/tunnel/$out/unique;\n";
     	print IPSEC qq "spdadd $isp->{remotesubnet} $isp->{localsubnet} any -P in ipsec ";
     	print IPSEC qq "$isp->{protocol}/tunnel/$in/unique;\n";
     	print IPSECADD qq "#!/sbin/setkey -f\n";
     	print IPSECADD qq "spdadd $isp->{localsubnet} $isp->{remotesubnet} any -P out ipsec ";
     	print IPSECADD qq "$isp->{protocol}/tunnel/$out/unique;\n";
     	print IPSECADD qq "spdadd $isp->{remotesubnet} $isp->{localsubnet} any -P in ipsec ";
     	print IPSECADD qq "$isp->{protocol}/tunnel/$in/unique;\n";
     	print IPSECDEL qq "#!/sbin/setkey -f\n";
     	print IPSECDEL qq "spddelete $isp->{localsubnet} $isp->{remotesubnet} any -P out ipsec ";
     	print IPSECDEL qq "$isp->{protocol}/tunnel/$out/unique;\n";
     	print IPSECDEL qq "spddelete $isp->{remotesubnet} $isp->{localsubnet} any -P in ipsec ";
     	print IPSECDEL qq "$isp->{protocol}/tunnel/$in/unique;\n";
     	close(IPSECADD);
     	close(IPSECDEL);
     	}
     	my $num;
     	foreach my $ip ( @$iplist )
     	{
           if ( $ip->{ip} eq $isp->{local} )  
           {
              $num = $ip->{isp}; 
           }
     	}
     	my $table="10".$num;
     	my $fwmark= dec2hex( ( $table << 16 ) | $number ); 
     	my $fwmarkback= dec2hex( ( $table << 16 ) | $number | 0x40000000 ); 
       	
       	#request
     	print IPRULE qq "/usr/local/sbin/ip rule add fwmark 0x$fwmark table $table prio 15000\n";
     	print DELIPRULE qq "/usr/local/sbin/ip rule del fwmark 0x$fwmark table $table prio 15000\n";
     	if (-e $IPSEC_FILE)
     	{
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{remotesubnet} -d $isp->{localsubnet} -m connmark --mark 0x$fwmark -j MARK --set-mark 0x$fwmarkback\n";
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{localsubnet} -d $isp->{remotesubnet} -m state --state NEW -j CONNMARK --set-mark 0x$fwmark\n";
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{localsubnet} -d $isp->{remotesubnet} -m connmark --mark 0x$fwmark -j MARK --set-mark 0x$fwmark\n";
     	}else
     	{
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{remotesubnet} -d $isp->{localsubnet} -m ctdirmark --mark_original 0x$fwmark -j MARK --set-mark 0x$fwmarkback\n";
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{localsubnet} -d $isp->{remotesubnet} -m state --state NEW -j CTDIRMARK --set-mark_original 0x$fwmark\n";
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{localsubnet} -d $isp->{remotesubnet} -m ctdirmark --mark_original 0x$fwmark -j MARK --set-mark 0x$fwmark\n";
     	}
     	$number -= 5;
     	#reply
     	$fwmark= dec2hex( ( $table << 16 ) | $number ); 
     	$fwmarkback= dec2hex( ( $table << 16 ) | $number | 0x40000000 ); 
     	print IPRULE qq "/usr/local/sbin/ip rule add fwmark 0x$fwmark table $table prio 15000\n";
     	print DELIPRULE qq "/usr/local/sbin/ip rule del fwmark 0x$fwmark table $table prio 15000\n";
     	if (-e $IPSEC_FILE)
     	{
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{remotesubnet} -d $isp->{localsubnet} -m state --state NEW -j MARK --set-mark 0x$fwmarkback\n";
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{remotesubnet} -d $isp->{localsubnet} -m connmark --mark 0x$fwmark -j MARK --set-mark 0x$fwmarkback\n";
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{localsubnet} -d $isp->{remotesubnet} -m state --state REPLY -m connmark ! --mark 0x$fwmark -j CONNMARK --set-mark 0x$fwmark\n";
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{localsubnet} -d $isp->{remotesubnet} -m connmark --mark 0x$fwmark -j MARK --set-mark 0x$fwmark\n";
     	}else
     	{
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{remotesubnet} -d $isp->{localsubnet} -m state --state NEW -j MARK --set-mark 0x$fwmarkback\n";
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{remotesubnet} -d $isp->{localsubnet} -m ctdirmark --mark_reply 0x$fwmark -j MARK --set-mark 0x$fwmarkback\n";
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{localsubnet} -d $isp->{remotesubnet} -m state --state REPLY -m ctdirmark ! --mark_reply 0x$fwmark -j CTDIRMARK --set-mark_reply 0x$fwmark\n";
     	    print IPRULE qq "/sbin/iptables -t mangle -A PREROUTING -s $isp->{localsubnet} -d $isp->{remotesubnet} -m ctdirmark --mark_reply 0x$fwmark -j MARK --set-mark 0x$fwmark\n";
     	}
     	$number -= 5;
    }
}
close(IPSEC);
close(IPRULE);
chmod(0777, $ipsecrule);
chmod(0777, $delipsecrule);
