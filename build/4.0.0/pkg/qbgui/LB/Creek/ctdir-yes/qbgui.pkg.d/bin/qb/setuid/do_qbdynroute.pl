#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# -----------------------------------------------
# build config file 
# -----------------------------------------------
my $RIPD_FILE="/opt/qb/quagga/etc/quagga/ripd.conf";
my $OSPFD_FILE="/opt/qb/quagga/etc/quagga/ospfd.conf";
my $OVERVIEW='/usr/local/apache/qbconf/overview.xml';
my $overview_opt=XMLread($OVERVIEW);
my $QBDYNROUTE_XML_FILE="/usr/local/apache/qbconf/dynroute.xml";

#------------------------------------------------------------------
# read the dynamic route option from the file 
#------------------------------------------------------------------
my $dynroute_opt=XMLread($QBDYNROUTE_XML_FILE);

if( !$dynroute_opt ) #if the string is NULL
{
    print "$QBDYNROUTE_XML_FILE is NULL \n";
}

#------------------------------------------------------------------
# read the hostname option from the file 
#------------------------------------------------------------------
my $overview_opt=XMLread($OVERVIEW);

if( !$overview_opt ) #if the string is NULL
{
    print "$OVERVIEW is NULL \n";
}
if ( $dynroute_opt->{protocol} ne 'OSPF' )
{
#------------------------------------------------------------------
# write the config file 
#------------------------------------------------------------------

open(OUT,">$RIPD_FILE");

if ( $overview_opt->{hostname} )
{ 
      print OUT "hostname $overview_opt->{hostname} \n";
      print OUT "password $overview_opt->{hostname} \n";
}else{
      print OUT "hostname QB_Router \n";
      print OUT "password QB_Router \n";
}

print OUT "router rip \n";

# config monitor port on selected interfaces
my @monportarray=split(/:/, $dynroute_opt->{monport});
foreach my $nic ( sort @monportarray )
{
    print OUT qq(network $nic \n);
}

if ( $dynroute_opt->{protocol} )
{
      my $version=$dynroute_opt->{protocol}; 
      $version=~s/RIP//g;
      print OUT "version $version \n";
}else{
      print OUT "version 2 \n";
}

if ( $dynroute_opt->{matric} )
{ 
      print OUT "redistribute connected metric $dynroute_opt->{matric} \n";
}else{
      print OUT "redistribute connected metric 15 \n";
}

if ( $dynroute_opt->{chgtime} )
{ 
      print OUT "timers basic $dynroute_opt->{chgtime} 180 120 \n";
}else{
      print OUT "timers basic 30 180 120\n";
}

print OUT "log stdout \n";

close(OUT);

chmod(0755,$RIPD_FILE);
}else{

#------------------------------------------------------------------
# write the OSPF config file 
#------------------------------------------------------------------

open(OUT,">$OSPFD_FILE");

if ( $overview_opt->{hostname} )
{ 
      print OUT "hostname $overview_opt->{hostname} \n";
      print OUT "password $overview_opt->{hostname} \n";
}else{
      print OUT "hostname QB_Router \n";
      print OUT "password QB_Router \n";
}

print OUT "router ospf \n";

print OUT "log stdout \n";

close(OUT);

chmod(0755,$OSPFD_FILE);
}
