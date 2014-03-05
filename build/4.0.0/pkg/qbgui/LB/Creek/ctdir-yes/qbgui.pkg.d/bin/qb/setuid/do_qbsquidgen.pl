#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
my $QB_SQUID_XMLCONF="/usr/local/apache/qbconf/squidgen.xml";
my $QB_SQUID_CONF="/usr/local/squid/etc/squid.conf";
#my $QB_SQUID_CONF="/etc/squid/squid.conf";
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

#------------------------------------------------------------------
# Enable/Disable Schedule 
#------------------------------------------------------------------
$statement="acl blocktime time";
$statement1="http_access allow !blocktime";
if ( $squidgen->{schedule} eq '1' )
{
    my $time='';
    if ( $squidgen->{everyday} ne '1' )
    {
        if ( $squidgen->{sun} eq '1' ) { $time = 'S'.' '; }
        if ( $squidgen->{mon} eq '1' ) { $time .= 'M'.' '; }
        if ( $squidgen->{tue} eq '1' ) { $time .= 'T'.' '; }
        if ( $squidgen->{wed} eq '1' ) { $time .= 'W'.' '; }
        if ( $squidgen->{thu} eq '1' ) { $time .= 'H'.' '; }
        if ( $squidgen->{fri} eq '1' ) { $time .= 'F'.' '; }
        if ( $squidgen->{sat} eq '1' ) { $time .= 'A'.' '; }
    }
    $time .= $squidgen->{timehour1}.':'.$squidgen->{timemin1}.'-'.$squidgen->{timehour2}.':'.$squidgen->{timemin2};
    modifyfile($QB_SQUID_CONF,"^#*".$statement,$statement.' '.$time); # remove # character in the stateament
    modifyfile($QB_SQUID_CONF,"^#*".$statement1,$statement1); # remove # character in the stateament
}
elsif ( $squidgen->{schedule} eq '0' )
{
    modifyfile($QB_SQUID_CONF,$statement,"#".$statement); # Add # character in the stateament
    modifyfile($QB_SQUID_CONF,$statement1,"#".$statement1); # Add # character in the stateament
}
else
{
    print "ERROR: INVALID PARAMETER \n"; 
    exit;
}
