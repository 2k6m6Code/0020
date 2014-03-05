#!/usr/bin/perl
 
require ('/usr/local/apache/qb/qbmod.cgi');

my $QB_L2TP = "/usr/local/apache/qbconf/l2tpinit.xml";
my $QB_IPSEC_CONF = "/etc/racoon/l2tpipsec.conf";
my $QB_DEL_IPSEC_CONF = "/etc/racoon/dell2tpipsec.conf";
my $QB_RACOON_CONF = "/etc/racoon/racoon.conf";
my $QB_L2TP_PSK = "/etc/racoon/l2tp.psk";
my $QB_IP_RULE = "/etc/racoon/iprule";
my $QB_CHAP_SECRET="/etc/ppp/chap-secrets";
my $QB_L2TP_CONF="/etc/xl2tpd/xl2tpd.conf";
my $QB_ZONE_XMLCONF="/usr/local/apache/qbconf/zonecfg.xml";

my $l2tp = XMLread($QB_L2TP);

#-----------------------------------------------------------------
# config for l2tp/ipsec vpn (setkey)
#-----------------------------------------------------------------
if ( !$l2tp ) #if the string is NULL
{
    print "$QB_BASIC_FILE is NULL \n";
}

if ( !open(IPSEC,">$QB_IPSEC_CONF") )
{
    print qq (Fail to Open IPSEC Config file !!);
}

if ( !open(DELIPSEC,">$QB_DEL_IPSEC_CONF") )
{
    print qq (Fail to Open IPSEC Config file !!);
}
# config for l2tp/ipsec vpn 
print IPSEC qq "#!/sbin/setkey -f\n";
#print IPSEC qq "flush;\n";
#print IPSEC qq "spdflush;\n";
print IPSEC qq "spdadd $l2tp->{serverip}\[1701] 0.0.0.0/0[0] any -P out ipsec esp/transport//require;\n";
print DELIPSEC qq "spddelete $l2tp->{serverip}\[1701] 0.0.0.0/0[0] any -P out ipsec esp/transport//require;\n";

close(IPSEC);
#------------------------------------------------------------------
# racoon.conf for l2tp/ipsec vpn
#------------------------------------------------------------------

my $islisten=runCommand(command=>"grep", params=>$l2tp->{serverip}.' '.'/etc/racoon/racoon.conf');
if ( $islisten eq '' )
{
    modifyfile($QB_RACOON_CONF,"listen {","listen {\n\tisakmp $l2tp->{serverip} [500];");
}


#my $isadd=runCommand(command=>"grep", params=>'anonymous'.' '.'/etc/racoon/racoon.conf');
#if ( $isadd eq '' )
#{
#    runCommand(command=>"cat", params=>'/etc/racoon/racoon.l2tp'.' '.'>>/etc/racoon/racoon.conf');
#}
#------------------------------------------------------------------
#iptables rule
#------------------------------------------------------------------
if ( !open(IP_RULE,">$QB_IP_RULE") )
{
    print qq (Fail to Open IPSEC iptables rule !!);
}
my @iparray=split(/\./, $l2tp->{iprange1});
my $subnet=$iparray[0]."\.".$iparray[1]."\.".$iparray[2]."\."."0/24";
my $fwto=44000;
my $fwtable=200;
my $fwmark= dec2hex( ( $fwtable << 16 ) | $fwto | 0x10000000 );
my $fwmarknew= dec2hex( ( $fwtable << 16 ) | $fwto | 0x50000000 );
#my $fwmark= ( ( $fwtable << 16 ) | $fwto | 0x40000000 );
#my $fwmarknew= ( $fwmark | 0x10000000 );

print IP_RULE qq "iptables -I INPUT -p 50 -d $l2tp->{serverip}  -j ACCEPT\n";
print IP_RULE qq "iptables -I INPUT -p udp -d $l2tp->{serverip} --dport 4500 -j ACCEPT\n";
print IP_RULE qq "iptables -I INPUT -p udp -d $l2tp->{serverip} --dport 500 -j ACCEPT\n";
print IP_RULE qq "iptables -I INPUT -p udp -d $l2tp->{serverip} --dport 1701 -j ACCEPT\n";


print IP_RULE qq "iptables -t mangle -A PREROUTING -s 0.0.0.0/0 -m iprange --dst-range $l2tp->{iprange1}\-$l2tp->{iprange2} -j MARK --set-mark 0x$fwmark\n";

close(IP_RULE);
chmod 0777, '/etc/racoon/iprule';
my $isaccept=runCommand(command=>"iptables", params=>'-L'.' '.'-vn|grep'.' '.'1701');
if ( $isaccept eq '' )
{
    runCommand(command=>"/etc/racoon/iprule", params=>'');
}
if ( !open(DELRULE,">$QB_IP_RULE") )
{
    print qq (Fail to Open IPSEC iptables rule !!);
}
print  DELRULE qq "iptables -D INPUT -p 50 -d $l2tp->{serverip}  -j ACCEPT\n";
print  DELRULE qq "iptables -D INPUT -p udp -d $l2tp->{serverip} --dport 4500 -j ACCEPT\n";
print  DELRULE qq "iptables -D INPUT -p udp -d $l2tp->{serverip} --dport 500 -j ACCEPT\n";
print  DELRULE qq "iptables -D INPUT -p udp -d $l2tp->{serverip} --dport 1701 -j ACCEPT\n";

print IP_RULE qq "iptables -t mangle -D PREROUTING -s 0.0.0.0/0 -m iprange --dst-range $l2tp->{iprange1}\-$l2tp->{iprange2} -j MARK --set-mark 0x$fwmark\n";

close(DELRULE);
chmod 0777, '/etc/racoon/iprule';


#---------------------------------------------------------------
# L2TP/ IPsec PSK /etc/racoon/l2tp.psk
#---------------------------------------------------------------
if ( !open(PSK,">$QB_L2TP_PSK") )
{
    print qq (Fail to Open L2TP/IPSEC PSK !!);
}

print PSK qq "$l2tp->{psk}\n";
close(PSK);
#---------------------------------------------------------------
# L2TP/ IPsec CHAP username / password
#---------------------------------------------------------------

#runCommand(command=>"cp", params=>'-a'.' '.'/etc/ppp/chap-secrets-bak'.' '.$QB_CHAP_SECRET);
#open IN, '<', $QB_CHAP_SECRET;
#my @contents = <IN>;
#close IN;
#@contents = grep !/$l2tp->{name}/, @contents;
#open OUT, '>', $QB_CHAP_SECRET;
#print OUT @contents;
#close OUT;

#if ( !open(CHAP,">>$QB_CHAP_SECRET") )
#{
#    print qq (Fail to Open CHAP_SECRET !!);
#}
#print CHAP "\"$l2tp->{name}\"\t*\t\"$l2tp->{password}\"\t*\n";
#close(CHAP);
runCommand(command=>"/usr/local/apache/qb/setuid/do_qbpppusr.pl", params=>'');

#-----------------------------------------------------------------
# L2TP conf
#-----------------------------------------------------------------
#runCommand(command=>"cp", params=>'-a'.' '.'/etc/xl2tpd/xl2tpd.conf.default'.' '.'/etc/xl2tpd/xl2tpd.conf');
if ( !open(L2TP,">$QB_L2TP_CONF") )
{
    print qq (Fail to Open L2TP CONF !!);
}
my $zone=XMLread($QB_ZONE_XMLCONF);

if( !$zone ) #if the string is NULL
{
    print "$QB_ZONE_XMLCONF is NULL \n";
}
my $natarray=$zone->{nat};
print L2TP qq "[global]\n";
print L2TP qq "auth file = /etc/ppp/chap-secrets\n";
print L2TP qq "listen-addr = $l2tp->{serverip}\n";
print L2TP qq "[lns default]\n";
print L2TP qq "ip range = $l2tp->{iprange1}-$l2tp->{iprange2}\n";

my @iparray=split(/\./, $l2tp->{iprange1});
my $subnet=$iparray[0]."\.".$iparray[1]."\.".$iparray[2]."\."."0/24";
#runCommand(command=>"echo", params=>$subnet.' '.'>/tmp/subnet');
my $ip1=$l2tp->{iprange1}.'/32';
my $ip2=$l2tp->{iprange2}.'/32';

foreach my $nat ( @$natarray )
{
    #if ( $nat->{network} eq $subnet )
    if ( subnet_belong_check($nat->{network}, $ip1) eq '2' && subnet_belong_check($nat->{network}, $ip2) eq '2' )
    {
	print L2TP qq "local ip = $nat->{ip}\n";
	last;
    }
}
close(L2TP);
runCommand(command=>"cat", params=>'/etc/xl2tpd/xl2tpd.tail'.' '.'>>/etc/xl2tpd/xl2tpd.conf');
    
#----------------------------------------------------------------
# enable L2TP / IPsec VPN
#----------------------------------------------------------------    
runCommand(command=>"/usr/sbin/xl2tpd", params=>'');
runCommand(command=>"/sbin/setkey", params=>'-f'.' '.'/etc/racoon/l2tpipsec.conf');
runCommand(command=>"ps", params=>'ax'.' '.'>/tmp/ps');
my $isrun=runCommand(command=>"grep", params=>'\"/usr/sbin/racoon\"'.' '.'/tmp/ps');
if ( $isrun eq '' )
{
    runCommand(command=>"/usr/sbin/racoon", params=>'');
}
elsif ( $islisten eq '' )
{
    runCommand(command=>"/usr/sbin/racoonctl", params=>'reload-config');    
}


#runCommand(command=>"/usr/sbin/racoonctl", params=>'reload-config');



