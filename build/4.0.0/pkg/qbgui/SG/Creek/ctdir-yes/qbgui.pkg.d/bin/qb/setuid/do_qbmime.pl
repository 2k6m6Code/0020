#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start
# --------------------------------------------------------------
my $QB_SQUID="/usr/local/squid/etc/";
my $QB_SQUID_CONF="/etc/squid/squid.conf";
my $QB_mime_XMLCONF="/usr/local/apache/qbconf/mime.xml";
my $QB_SQUID_BLKMIME=$QB_SQUID."blockmime.txt";

#------------------------------------------------------------------
# read the option from the mime  
#------------------------------------------------------------------
my $mimeref=XMLread($QB_mime_XMLCONF);

if ( !$mimeref ) #if the string is NULL
{
    print "$QB_SQUID_mime_XMLCONF is NULL \n";
}

if ( !open(BLKMIME,">$QB_SQUID_BLKMIME") )
{
   print qq (Fail to Open BLKmime Config mime !!);
}
$mimelist = $mimeref->{mime};
my $blockmime = '';
foreach my $item ( @$mimelist ) 
{
    if ( $item->{block} eq '1' )
    {
        $blockmime .= "\^$item->{mimetype}\$\n";
    }
}
print BLKMIME qq "$blockmime";
close(BLKMIME);
