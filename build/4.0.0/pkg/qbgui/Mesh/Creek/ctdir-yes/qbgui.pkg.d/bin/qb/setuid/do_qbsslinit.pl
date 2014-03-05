#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');
sub netmask_convert
{
    my ($string)=@_;
    my $CIDIR=0; 
    
    @mask=split('\.', $string);
    
    foreach my $num ( @mask )
    {
        while ( $num & 0x80 )
        {
            $CIDIR++;
            $num = $num << 1;
        }
        if ( $CIDIR % 8 ) { last; }
    }
    return $CIDIR;
}

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
my $QB_SSL_XMLCONF="/usr/local/apache/qbconf/sslinit.xml";
#my $QB_AVA_XMLCONF="/usr/local/apache/qbconf/avanet.xml";
my $QB_LEA_XMLCONF="/usr/local/apache/qbconf/leanet.xml";
my $QB_BASIC="/usr/local/apache/qbconf/basic.xml";
my $QB_SSL_DIR="/etc/ssl";
my $QB_SSL_CONF=$QB_SSL_DIR."/ssl.conf";
my $QB_SSL_CLIENT_CONF=$QB_SSL_DIR."/client.ovpn";
my $QB_SSL_START=$QB_SSL_DIR."/sslstart";
my $QB_SSL_STOP=$QB_SSL_DIR."/sslstop";

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/sslinit.xml
#------------------------------------------------------------------
my $ssl=XMLread($QB_SSL_XMLCONF);
if( !$ssl ) #if the string is NULL
{
    print "$QB_SSL_XMLCONF is NULL \n";
}
#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/basic.xml
#------------------------------------------------------------------
my $ispinfo=XMLread($QB_BASIC);
if( !$ispinfo ) #if the string is NULL
{
    print "$QB_BASIC is NULL \n";
}
#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/leanet.xml
#------------------------------------------------------------------
my $lea=XMLread($QB_LEA_XMLCONF);
if( !$ispinfo ) #if the string is NULL
{
    print "$QB_LEA_XMLCONF is NULL \n";
}
#------------------------------------------------------------------
if ( !open(SSL,">$QB_SSL_CONF") )
{
    print qq (Fail to Open SSL Config file !!);
}
#-----------------------------------------------------------------
if ( !open(CLI,">$QB_SSL_CLIENT_CONF") )
{
    print qq (Fail to Open SSL CLIENT Config file !!);
}
#------------------------------------------------------------------
if ( !open(SSLSTART,">$QB_SSL_START") )
{
    print qq (Fail to Open SSLSTART file !!);
}
#------------------------------------------------------------------
if ( !open(SSLSTOP,">$QB_SSL_STOP") )
{
    print qq (Fail to Open SSLSTART file !!);
}
#------------------------------------------------------------------
my $leasubnet=$lea->{subnet};
my $ispinfo = XMLread($QB_BASIC);
my $isplist = $ispinfo->{isp};
my @RRGarray;
my $fwto=60005;
my $fwtable=200;
my $fwmark= dec2hex( ( $fwtable << 16 ) | $fwto | 0x10000000 );

print SSL qq "local $ssl->{serverip}\n";
print SSL qq "port $ssl->{port}\n";
print SSL qq "proto $ssl->{protocol}\n";
print SSL qq "dev tun\n";
print SSL qq "ca $QB_SSL_DIR/ca.crt\n";
print SSL qq "cert $QB_SSL_DIR/server.crt\n";
print SSL qq "key $QB_SSL_DIR/server.key\n";
print SSL qq "dh $QB_SSL_DIR/dh1024.pem\n";
print SSL qq "server $ssl->{vpnnet} $ssl->{netmask}\n";
print SSL qq "ifconfig-pool-persist $QB_SSL_DIR/ipp.txt\n";
my $CIDIR=netmask_convert($ssl->{netmask});
foreach my $lea ( @$leasubnet )
{
    if ( $lea->{network} eq "system" ) { next; }
    my $fwmark= dec2hex( ( $fwtable << 16 ) | $fwto | 0x10000000 );
    
    my $argument='-s'.' '.$lea->{network}.' '.'-d'.' '.$ssl->{vpnnet}.'/'.$CIDIR.' -j MARK --set-mark 0x'.$fwmark;
  
    push(@RRGarray, $argument);
    $fwto += 5;
    $lea->{network}=~s/\/24//g;
    print SSL qq "push \"route $lea->{network} 255.255.255.0\"\n";
}
print SSL qq "keepalive 10 30\n";
print SSL qq "tls-auth $QB_SSL_DIR/ta.key 0\n";
print SSL qq "comp-lzo\n";
print SSL qq "max-clients $ssl->{max}\n";
print SSL qq "persist-key\n";
print SSL qq "persist-tun\n";
print SSL qq "status /var/log/sslvpn-status.log 60\n";
print SSL qq "inactive 120\n";
print SSL qq "verb 3\n";
print SSL qq "log\t/var/log/sslvpn.log\n";
print SSL qq "auth-user-pass-verify /usr/local/apache/qb/setuid/do_qbcheckssl.pl  via-env\n";
print SSL qq "client-cert-not-required\n";
print SSL qq "username-as-common-name\n";
#-----------------------------------------------------------------------------------------------------
print SSLSTART qq "#!/bin/bash\n";
foreach my $isp ( @$isplist )
{
    if ( $isp->{systemip} eq $ssl->{serverip} )
    {
    	my $nic=$isp->{nic};
        print SSLSTART qq "/sbin/iptables -I INPUT -i $nic -p $ssl->{protocol} --dport $ssl->{port} -j ACCEPT \n";
        print SSLSTART qq "/usr/local/sbin/iptables -t nat -A PREROUTING -d $ssl->{serverip} -p tcp --dport 5000 -j DNAT --to-destination 172.31.3.1\n";
	print SSLSTART qq "/sbin/iptables -t mangle -A OUTPUT -s 172.31.3.1 -p tcp --sport 5000 -j MARK --set-mark 0x4647535\n";
        print SSLSTOP qq "/usr/local/sbin/iptables -t nat -D PREROUTING -d $ssl->{serverip} -p tcp --dport 5000 -j DNAT --to-destination 172.31.3.1\n";
        print SSLSTOP qq "/sbin/iptables -D INPUT -i $nic -p $ssl->{protocol} --dport $ssl->{port} -j ACCEPT \n";
	print SSLSTOP qq "/sbin/iptables -t mangle -D OUTPUT -s 172.31.3.1 -p tcp --sport 5000 -j MARK --set-mark 0x4647535\n";
        foreach my $rrg ( @RRGarray )
        {
            print SSLSTART qq "/sbin/iptables -t mangle -A PREROUTING $rrg\n";
            print SSLSTOP qq "/sbin/iptables -t mangle -D PREROUTING $rrg\n";
        }
        last;
    }
}
print SSLSTART qq "/usr/sbin/openvpn /etc/ssl/ssl.conf &\n";
print SSLSTART qq "cp -a /etc/ssl/client.ovpn /usr/local/apache/sslportal/\n";

print CLI qq "client\n";
print CLI qq "dev tun\n";
print CLI qq "proto $ssl->{protocol}\n";
print CLI qq "remote $ssl->{serverip} $ssl->{port}\n";
print CLI qq "resolv-retry infinite\n";
print CLI qq "nobind\n";
print CLI qq "persist-key\n";
print CLI qq "ca ca.crt\n";
print CLI qq "tls-auth ta.key 1\n";
print CLI qq "comp-lzo\n";
print CLI qq "verb 3\n";
print CLI qq "auth-user-pass\n";


close(SSL);
close(CLI);
close(SSLSTART);
close(SSLSTOP);
chmod 0777, '/etc/ssl/sslstart';
chmod 0777, '/etc/ssl/sslstop';
