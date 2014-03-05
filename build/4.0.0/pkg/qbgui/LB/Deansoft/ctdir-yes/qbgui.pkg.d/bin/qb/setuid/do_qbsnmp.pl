#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# --------------------------
#
# main program start routine
#
# --------------------------
my $QB_SNMP_FILE="/usr/local/apache/config/snmp.xml";
my $QB_SNMP_CONF="/mnt/conf/snmpd.con";
my $QB_FIRMWARE_VER="/mnt/conf/pkginfo";
open(FHD, "$QB_FIRMWARE_VER") || die "$!\n";
close(FHD);
my $snmp=XMLread($QB_SNMP_FILE);

if(!$snmp) #if the string is NULL
{
    print "$QBHA_SNMP_FILE is NULL \n";
}

#------------------------------------------------------------------
if ( !open(SNMP,">$QB_SNMP_CONF") )
{
    print qq (Fail to Open SNMP Config file !!);
}

#------------------------------------------------------------------
if( $snmp->{enablesnmp} )  
{
    print SNMP qq(#snmpd enable\n);
}
else
{
    print SNMP qq(#snmpd disable\n);
}


#------------------------------------------------------------------
if ( $snmp->{enabletrap} )
{
    print SNMP qq(#snmptrap enable\n);
}
else
{
    print SNMP qq(#snmptrap disable\n);
}


print SNMP qq(#manager $snmp->{snmpmgrip}\n);
print SNMP qq(#manager2 $snmp->{snmpmgrip2}\n);

#print SNMP qq(rocommunity public \n);
#For IPV4
print SNMP qq(rocommunity $snmp->{community} \n);
print SNMP qq(rwcommunity private \n);

#for IPV6
print SNMP qq(rocommunity6 $snmp->{community} \n);
print SNMP qq(rwcommunity6 private \n);

open(FW_ver, "$QB_FIRMWARE_VER") || die "$!\n";
my $version=<FW_ver>;
$version=~s/\n//g;
close(FW_ver);

open(QB_SN, '/mnt/conf/qbsn') || die "$!\n";
my $Serial=<QB_SN>;
$Serial=~s/\n//g;
close(QB_SN);

print SNMP qq(sysdescr QBalancer $gMODEL Firmware $version Serial Number : $Serial\n);

if ( $snmp->{sysname} )
{
    print SNMP qq(sysname $snmp->{sysname} \n);
}
else
{
    print SNMP qq(sysname Q-Balancer \n);
}

print SNMP qq(syslocation $snmp->{syslocation} \n);

print SNMP qq(syscontact $snmp->{syscontact} \n);

close(SNMP);
qbSync(); #20130419 To prevent DOM/CF become readonly
