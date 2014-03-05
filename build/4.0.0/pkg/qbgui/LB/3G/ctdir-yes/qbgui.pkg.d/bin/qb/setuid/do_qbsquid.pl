#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
my $QB_SQUID_XMLCONF="/usr/local/apache/qbconf/squidgen.xml";
my $QB_SQUID_CONF="/etc/squid/squid.conf";
my $statement;
my $statement1;
my $statement2;

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/squidgen.xml
#------------------------------------------------------------------
my $squidgen=XMLread($QB_SQUID_XMLCONF);

if( !$squidgen ) #if the string is NULL
{
    print "$QB_SQUID_XMLCONF is NULL \n";
}
    
#------------------------------------------------------------------
# Enable/Disable activex
#------------------------------------------------------------------
$statement="http_access deny activex";
if ( $squidgen->{activex} eq '1' )
{
    modifyfile($QB_SQUID_CONF,"^#*".$statement,$statement); # remove # character in the stateament
}
elsif ( $squidgen->{activex} eq '0' )
{
    modifyfile($QB_SQUID_CONF,$statement,"#".$statement); # Add # character in the stateament
}
else
{
    print "ERROR: INVALID PARAMETER \n"; 
    exit;
}

#------------------------------------------------------------------
# Enable/Disable javascript
#------------------------------------------------------------------
$statement="http_access deny javaapplt";
if ( $squidgen->{javaapplet} eq '1' )
{
    modifyfile($QB_SQUID_CONF,"^#*".$statement,$statement); # remove # character in the stateament
}
elsif ( $squidgen->{javaapplet} eq '0' )
{
    modifyfile($QB_SQUID_CONF,$statement,"#".$statement); # Add # character in the stateament
}
else
{
    print "ERROR: INVALID PARAMETER \n"; 
    exit;
}
#------------------------------------------------------------------
# Enable/Disable cookies
#------------------------------------------------------------------
$statement="request_header_access Cookie deny all";
$statement1="request_header_access Cookie allow mydomain";
$statement2="request_header_access Cookie allow exempt";
if ( $squidgen->{cookies} eq '1' )
{
    modifyfile($QB_SQUID_CONF,"^#*".$statement,$statement); # remove # character in the stateament
    modifyfile($QB_SQUID_CONF,"^#*".$statement1,$statement1); # remove # character in the stateament
    modifyfile($QB_SQUID_CONF,"^#*".$statement2,$statement2); # remove # character in the stateament
}
elsif ( $squidgen->{cookies} eq '0' )
{
    modifyfile($QB_SQUID_CONF,$statement,"#".$statement); # Add # character in the stateament
    modifyfile($QB_SQUID_CONF,$statement1,"#".$statement1); # Add # character in the stateament
    modifyfile($QB_SQUID_CONF,$statement2,"#".$statement2); # Add # character in the stateament
}
else
{
    print "ERROR: INVALID PARAMETER \n"; 
    exit;
}
#------------------------------------------------------------------
# Enable/Disable javascript
#------------------------------------------------------------------
$statement="http_access deny js";
if ( $squidgen->{javascript} eq '1' )
{
    modifyfile($QB_SQUID_CONF,"^#*".$statement,$statement); # remove # character in the stateament
}
elsif ( $squidgen->{javascript} eq '0' )
{
    modifyfile($QB_SQUID_CONF,$statement,"#".$statement); # Add # character in the stateament
}
else
{
    print "ERROR: INVALID PARAMETER \n"; 
    exit;
}

#------------------------------------------------------------------
# Enable/Disable Prohibit multi-thread download
#------------------------------------------------------------------
$statement="http_reply_access deny partial maxcon";
if ( $squidgen->{prohibitmulti} eq '1' )
{
    modifyfile($QB_SQUID_CONF,"^#*".$statement,$statement); # remove # character in the stateament
}
elsif ( $squidgen->{prohibitmulti} eq '0' )
{
    modifyfile($QB_SQUID_CONF,$statement,"#".$statement); # Add # character in the stateament
}
else
{
    print "ERROR: INVALID PARAMETER \n";
    exit;
}

