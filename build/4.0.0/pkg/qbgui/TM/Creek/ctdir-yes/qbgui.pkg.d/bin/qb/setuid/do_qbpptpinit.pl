#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
my $QB_PPTPD_XMLCONF="/usr/local/apache/qbconf/pptpinit.xml";
my $QB_BASIC="/usr/local/apache/qbconf/basic.xml";
my $QB_PPTPD_CONF="/etc/pptpd.conf";
my $QB_PPTPD_OPTION="/etc/ppp/options.pptpd";
my $QB_IP_RULE="/etc/pptpd.iprule";
my $QB_ZONE_XMLCONF="/usr/local/apache/qbconf/zonecfg.xml";
my $new_str;
my $statement;
my $statement1;


#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/pptpinit.xml
#------------------------------------------------------------------
my $pptpinit=XMLread($QB_PPTPD_XMLCONF);

if( !$pptpinit ) #if the string is NULL
{
    print "$QB_PPTPD_XMLCONF is NULL \n";
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
# Support Bsdcompress
#------------------------------------------------------------------
if ( !$pptpinit->{bsdcompress})
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."nobsdcomp","nobsdcomp"); # remove # character in the stateament
}
else
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."nobsdcomp","#"."nobsdcomp"); # Enable BSD compress function
}

#------------------------------------------------------------------
# Support Deflate Compression 
#------------------------------------------------------------------
if ( !$pptpinit->{deflatecompress})
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."nodeflate","nodeflate"); # remove # character in the stateament
}
else
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."nodeflate","#"."nodeflate"); # Enable Deflate compress function
}

#------------------------------------------------------------------
# Max Client Connections
#------------------------------------------------------------------
if ( $pptpinit->{maxclient})
{
    modifyfile($QB_PPTPD_CONF,"connections.*","connections ".$pptpinit->{maxclient}); # refresh Max Client Connection
    modifyfile($QB_PPTPD_CONF,"^#*"."connections","connections"); # remove # character in the stateament
}
else
{
    modifyfile($QB_PPTPD_CONF,"^#*"."connections","#"."connections"); # Disable Max Client Option
}

#------------------------------------------------------------------
# PPTP idle time to prevent DOS attack
#------------------------------------------------------------------
if ( $pptpinit->{idletime})
{
    modifyfile($QB_PPTPD_CONF,"stimeout.*","stimeout ".$pptpinit->{idletime}); # refresh Max Client Connection
    modifyfile($QB_PPTPD_CONF,"^#*"."stimeout","stimeout"); # remove # character in the stateament
}
else
{
    modifyfile($QB_PPTPD_CONF,"^#*"."stimeout","#"."stimeout"); # Disable Max Client Option
}

#------------------------------------------------------------------
# Authenticate Method
#------------------------------------------------------------------
if ( $pptpinit->{pptpauthmethod} eq 'CHAP')
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."require-","#"."require-"); # Disable require-xxx Option
    modifyfile($QB_PPTPD_OPTION,"^#*"."require-chap","require-chap"); # remove # character in the stateament
}
elsif ( $pptpinit->{pptpauthmethod} eq 'MSCHAP')
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."require-","#"."require-"); # Disable require-xxx Option
    modifyfile($QB_PPTPD_OPTION,"^#*"."require-mschap","require-mschap"); # remove # character in the stateament
    modifyfile($QB_PPTPD_OPTION,"^#*"."require-mschap-v2","#"."require-mschap-v2"); # Disable require-mschap-v2 Option
}
elsif ( $pptpinit->{pptpauthmethod} eq 'MSCHAPV2')
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."require-","#"."require-"); # Disable require-xxx Option
    modifyfile($QB_PPTPD_OPTION,"^#*"."require-mschap-v2","require-mschap-v2"); # remove # character in the stateament
}
elsif ( $pptpinit->{pptpauthmethod} eq 'PAP')
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."require-","#"."require-"); # Disable require-xxx Option
    modifyfile($QB_PPTPD_OPTION,"^#*"."require-pap","require-pap"); # remove # character in the stateament
}

#------------------------------------------------------------------
# Support MPPE Encryption
#------------------------------------------------------------------
if ( $pptpinit->{encryption} )
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."mppe required","mppe required,stateless"); # remove # character in the stateament
}
else
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."mppe required,stateless","#"."mppe required,stateless"); # Disable require-mppe-128 Option
    modifyfile($QB_PPTPD_OPTION,"^#*"."mppe required","#"."mppe required"); # Disable require-mppe-128 Option
}

#------------------------------------------------------------------
# DNS IP 1
#------------------------------------------------------------------
if ( $pptpinit->{dnsip1})
{
    modifyfile($QB_PPTPD_OPTION,"ms-dns.*DNS1","ms-dns ".$pptpinit->{dnsip1}." #DNS1"); # refresh DNS IP
    modifyfile($QB_PPTPD_OPTION,"^#*"."ms-dns","ms-dns"); # remove # character in the stateament
}
else
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."ms-dns.*DNS1","#"."ms-dns        #DNS1"); # Disable DNS IP
}

#------------------------------------------------------------------
# DNS IP 2
#------------------------------------------------------------------
if ( $pptpinit->{dnsip2})
{
    modifyfile($QB_PPTPD_OPTION,"ms-dns.*DNS2","ms-dns ".$pptpinit->{dnsip2}." #DNS2"); # refresh DNS IP
    modifyfile($QB_PPTPD_OPTION,"^#*"."ms-dns","ms-dns"); # remove # character in the stateament
}
else
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."ms-dns.*DNS2","#"."ms-dns        #DNS2"); # Disable DNS IP
}

#------------------------------------------------------------------
# Support MPPC Compression
#------------------------------------------------------------------
if ( $pptpinit->{compression})
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."-mppc","#"."-mppc"); # Mark -mppc=enable mppc
}
else
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."-mppc","-mppc"); # remove # character in the stateament=disable mppc
}

#------------------------------------------------------------------
# Write PPTP IP Range List 
#------------------------------------------------------------------
@range2=split(/\./, $pptpinit->{iprange2});

if ( $pptpinit->{iprange1})
{
    modifyfile($QB_PPTPD_CONF,"remoteip.*","remoteip ".$pptpinit->{iprange1}."-".$range2[3]); # refresh Max Client Connection
    modifyfile($QB_PPTPD_CONF,"^#*"."remoteip","remoteip"); # remove # character in the stateament
}
else
{
    modifyfile($QB_PPTPD_OPTION,"^#*"."remoteip","#"."remoteip"); # Disable require-mppe-128 Option
}


#------------------------------------------------------------------
# iptables rule for RRG 
#------------------------------------------------------------------
#my @iparray=split(/\./, $pptpinit->{rangelist});
#my $subnet=$iparray[0]."\.".$iparray[1]."\.".$iparray[2]."\."."0/24";
my $zone=XMLread($QB_ZONE_XMLCONF);
if( !$zone ) #if the string is NULL
{
    print "$QB_ZONE_XMLCONF is NULL \n";
}
my $natarray=$zone->{nat};


if ( !open(IP_RULE,">$QB_IP_RULE") )
{
    	print qq ("fail to open pptpd.iprule\n");
}
runCommand(command=>"/etc/pptpd.iprule", params=>'');

my $fwto=43000;
my $fwtable=200;
my $fwmark= dec2hex( ( $fwtable << 16 ) | $fwto | 0x10000000 );
my $fwmarknew= dec2hex( ( $fwtable << 16 ) | $fwto | 0x50000000 );

foreach my $nat ( @$natarray )
{
    if ( $nat->{network} ne '' )
    {
        print IP_RULE qq "iptables -t mangle -A PREROUTING -s $nat->{network} -m iprange --dst-range $pptpinit->{iprange1}\-$pptpinit->{iprange2} -j MARK --set-mark 0x$fwmark\n";
    }
}

close(IP_RULE);
chmod 0777, $QB_IP_RULE;

if ( $pptpinit->{enableppd} eq '1' )
{
    runCommand(command=>"/etc/pptpd.iprule", params=>'');
}

if ( !open(DELIP_RULE,">$QB_IP_RULE") )
{
    	print qq ("fail to open pptpd.iprule\n");
}
foreach my $nat ( @$natarray )
{
    if ( $nat->{network} ne '' )
    {
        print DELIP_RULE qq "iptables -t mangle -D PREROUTING -s $nat->{network} -m iprange --dst-range $pptpinit->{iprange1}\-$pptpinit->{iprange2} -j MARK --set-mark 0x$fwmark\n";
    }
}

#print DELIP_RULE qq "iptables -t mangle -D PREROUTING -s 0.0.0.0/0 -m iprange --dst-range $pptpinit->{iprange1}\-$pptpinit->{iprange2} -j MARK --set-mark 0x$fwmark\n";


close(DELIP_RULE);
chmod 0777, $QB_IP_RULE;

#------------------------------------------------------------------
# Write Server Local IP 
#------------------------------------------------------------------
#my $siplist=$pptpinit->{sip};
#my @iidlist=maintainBasic(action=>'GETGOODIIDLIST');
#my $allisp=$ispinfo->{isp};
my $newlocalip='';
=cut
my $zone=XMLread($QB_ZONE_XMLCONF);

if( !$zone ) #if the string is NULL
{
    print "$QB_ZONE_XMLCONF is NULL \n";
}
my $natarray=$zone->{nat};
=cut

# local ip is lan interface ip
my $ip1=$pptpinit->{iprange1}.'/32';
my $ip2=$pptpinit->{iprange2}.'/32';
my $newlocalip;
foreach my $nat ( @$natarray )
{
     if ( subnet_belong_check($nat->{network}, $ip1) eq '2' && subnet_belong_check($nat->{network}, $ip2) eq '2' )
     #if ( $nat->{network} eq $subnet )
     {
         $newlocalip = $nat->{ip};
         last;
     }
}    
#foreach my $iid ( @iidlist)
#{
#    my $targetsip;
#    foreach my $sip ( @$siplist ) { if ( $sip->{isp} eq $iid ) { $targetsip=$sip; } }
#    foreach my $isp ( @$allisp ) { if ( $isp->{iid} eq $iid ) { $targetsip->{ip}=~s/systemip/$isp->{systemip}/g;}}
#    if ($targetsip->{ip} && $newlocalip eq '')
#    {
#       $newlocalip.="$targetsip->{ip}";
#    }
#    elsif ($targetsip->{ip})
#    {
#       $newlocalip.=",$targetsip->{ip}";
#    }
#}
    
    modifyfile($QB_PPTPD_CONF,"localip.*","localip ".$newlocalip); # refresh Server Local IP
    #modifyfile($QB_PPTPD_CONF,"^#*"."localip","localip"); # remove # character in the stateament

