#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
my $QB_WIRELESS_XMLCONF="/usr/local/apache/qbconf/wireless.xml";
my $QB_WIRELESS_CONF="/etc/Wireless/RT2860AP/RT2860AP.dat";
my $QB_ZONE_XMLCONF="/usr/local/apache/qbconf/zonecfg.xml";


#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/wireless.xml
#------------------------------------------------------------------
my $wirelessinit=XMLread($QB_WIRELESS_XMLCONF);

if( !$wirelessinit ) #if the string is NULL
{
    print "$QB_WIRELESS_XMLCONF is NULL \n";
}

#------------------------------------------------------------------
# Enable Wireless or not
#------------------------------------------------------------------
if ( $wirelessinit->{enablewirelesslan})
{
    print "Enable Wireless LAN.\n";
    runCommand(command=>"/sbin/ifconfig", params=>qq(ra0 up));
    runCommand(command=>"sleep", params=>'5');
}
else
{
    print "Disable Wireless LAN.\n";
    runCommand(command=>"/sbin/ifconfig", params=>qq(ra0 down));
}

#------------------------------------------------------------------
# Add SSID
#------------------------------------------------------------------
if ( $wirelessinit->{ssid} )
{
    print "Adding SSID $wirelessinit->{ssid}\n";
    runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set SSID=$wirelessinit->{ssid}));
}
else
{
    print "SSID is NULL \n";
}

#------------------------------------------------------------------
# Hide SSID or not 
#------------------------------------------------------------------
if ( $wirelessinit->{hidessid} eq 'Enabled' )
{
    print "Hide SSID $wirelessinit->{hidessid}\n";
    runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set HideSSID=1));
}
else
{
    print "Don't Hide SSID .\n";
    runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set HideSSID=0));
}

#------------------------------------------------------------------
# Set Wireless Mode : "0"=>"802.11 B/G", "1"=>"802.11 B", "4"=>"802.11 G", "6"=>"802.11 N", "7"=>"802.11 G/N", "9"=>"802.11 B/G/N"
#------------------------------------------------------------------
if ( $wirelessinit->{wirelessmode})
{
    print "Set Wireless Mode.\n";
    runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set WirelessMode=$wirelessinit->{wirelessmode}));
}
else
{
    runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set WirelessMode=$wirelessinit->{wirelessmode}));
}

#------------------------------------------------------------------
# Set ChannelMode 
#------------------------------------------------------------------
if ( $wirelessinit->{channelmode} eq 'Auto')
{
    print "Set Channel Mode=Auto.\n";
    runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set AutoChannelSelect=1));
}
else
{
    print "Set Channel Mode=$wirelessinit->{channelmode}.\n";
    runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set Channel=$wirelessinit->{channelmode}));
}

#------------------------------------------------------------------
# Security
#------------------------------------------------------------------
if ( $wirelessinit->{encryptmode} eq 'WEP')
{
   print "Adding EncryptType=$wirelessinit->{encryptmode}\n";
   runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set EncrypType=WEP));
   runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set AuthMode=$wirelessinit->{authmode}));
   #runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set IEEE8021X=0));

 if ( $wirelessinit->{authmode} ne 'OPEN')
 {
   if ( $wirelessinit->{wep_key_num} eq '1' )
   {
        runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set DefaultKeyID=1));
        runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set Key1=$wirelessinit->{wepkey1}));
   }
   elsif ( $wirelessinit->{wep_key_num} eq '2' )
   {
        print "Adding DefaultKeyID=$wirelessinit->{wep_key_num}\n";
        runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set DefaultKeyID=2));
        print "Adding Key2=$wirelessinit->{wepkey2}\n";
        runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set Key2=$wirelessinit->{wepkey2}));
   }
   elsif ( $wirelessinit->{wep_key_num} eq '3' )
   {
        runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set DefaultKeyID=3));
        runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set Key3=$wirelessinit->{wepkey3}));
   }
   elsif ( $wirelessinit->{wep_key_num} eq '4' )
   {
        runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set DefaultKeyID=4));
        runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set Key4=$wirelessinit->{wepkey4}));
   }
 }
}
elsif ( $wirelessinit->{encryptmode} eq 'TKIP' || $wirelessinit->{encryptmode} eq 'AES' )
{
   print "Adding EncryptType=$wirelessinit->{encryptmode}\n";
   runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set EncrypType=$wirelessinit->{encryptmode}));
   runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set AuthMode=$wirelessinit->{authmode}));
   #runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set IEEE8021X=0));
   runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set WPAPSK=$wirelessinit->{wpakey}));
}
elsif ( $wirelessinit->{encryptmode} eq 'NONE' )
{
   print "Adding EncryptType=$wirelessinit->{encryptmode}\n";
   runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set EncrypType=$wirelessinit->{encryptmode}));
   print "Adding AuthMode=OPEN\n";
   runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set AuthMode=OPEN));
   #print "Adding  IEEE8021X=0\n";
   #runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set IEEE8021X=0));

}
#------------------------------------------------------------------
# Add SSID
#------------------------------------------------------------------
if ( $wirelessinit->{ssid} )
{
    print "Adding SSID $wirelessinit->{ssid}\n";
    runCommand(command=>"/sbin/iwpriv", params=>qq(ra0 set SSID=$wirelessinit->{ssid}));
}
else
{
    print "SSID is NULL \n";
}

