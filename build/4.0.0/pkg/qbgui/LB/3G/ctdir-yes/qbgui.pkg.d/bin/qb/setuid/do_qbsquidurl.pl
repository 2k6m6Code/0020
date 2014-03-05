#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start
# --------------------------------------------------------------
my $QB_SQUID="/usr/local/squid/etc/";
my $QB_SQUID_XMLCONF="/usr/local/apache/qbconf/squidurl.xml";
my $QB_SQUID_CONF="/etc/squid/squid.conf";
my $QB_SQUID_EXEMPT=$QB_SQUID."exempt.txt";
my $QB_SQUID_KEYWORD=$QB_SQUID."keyword.txt";
my $QB_SQUID_BLKFILE=$QB_SQUID."blockfile.txt";
my $QB_SQUID_TRUST=$QB_SQUID."trust.txt";
my $QB_SQUID_FORBID=$QB_SQUID."forbid.txt";


my $statement;
my $namelist;
#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/squidgen.xml
#------------------------------------------------------------------
my $squid=XMLread($QB_SQUID_XMLCONF);

if( !$squid ) #if the string is NULL
{
    print "$QB_SQUID_XMLCONF is NULL \n";
}

my $exempt=$squid->{exempt}->[0]->{net};
my $trust=$squid->{trust}->[0]->{name};
my $forbid=$squid->{forbid}->[0]->{name};
my $keyword=$squid->{keyword}->[0]->{name};
#------------------------------------------------------------------
# allow exempt PC
#------------------------------------------------------------------
#$statement="acl exempt src";
#$namelist="";
#foreach my $net ( @$exempt )
#{
#    if ( $net->{ip} eq 'system' ) { next; }
#    $namelist .= " " . "$net->{ip}"."\/32";
#}    
#if ( $namelist ne "" )
#{
#     modifyfile($QB_SQUID_CONF, "$statement.*", $statement." ".$namelist);
#}
#else
#{
#     modifyfile($QB_SQUID_CONF, "$statement.*", $statement);
#}
if ( !open(EXEMPT,">$QB_SQUID_EXEMPT") )
{
    print qq (Fail to Open EXEMPT Config file !!);
}
foreach my $net ( @$exempt )
{
    if ( $net->{ip} eq 'system' ) { next; }
    print EXEMPT qq "$net->{ip}\/32\n";
}    




#------------------------------------------------------------------
# allow trust domain
#------------------------------------------------------------------
#$statement="acl myDomain dstdomain";
#$namelist="";
#foreach my $domain ( @$trust )
#{
#    if ( $domain->{trustname} eq 'system' ) { next; }
#    $namelist .= " " . ".$domain->{trustname}";
#}    
#if ( $namelist ne "" )
#{
#     modifyfile($QB_SQUID_CONF, "$statement.*", $statement." ".$namelist);
#}
#else
#{
#     modifyfile($QB_SQUID_CONF, "$statement.*", $statement);
#}
if ( !open(TRUST,">$QB_SQUID_TRUST") )
{
    print qq (Fail to Open TRUST Config file !!);
}
foreach my $domain ( @$trust )
{
    if ( $domain->{trustname} eq 'system' ) { next; }
    print TRUST qq "\.$domain->{trustname}\n";
}    




#------------------------------------------------------------------
# deny forbid domain
#------------------------------------------------------------------
#$statement="acl badDomain dstdomain";
#$namelist="";
#foreach my $domain ( @$forbid )
#{
#    if ( $domain->{forbidname} eq 'system' ) { next; }
#    $namelist .= " " . ".$domain->{forbidname}";
#}    
#if ( $namelist ne "" )
#{
#     modifyfile($QB_SQUID_CONF, "$statement.*", $statement." ".$namelist);
#}
#else
#{
#     modifyfile($QB_SQUID_CONF, "$statement.*", $statement);
#}
if ( !open(FORBID,">$QB_SQUID_FORBID") )
{
    print qq (Fail to Open FORBID Config file !!);
}
foreach my $domain ( @$forbid )
{
    if ( $domain->{forbidname} eq 'system' ) { next; }
    print FORBID qq "\.$domain->{forbidname}\n";
}

#------------------------------------------------------------------
# deny keyword
#------------------------------------------------------------------
#$statement="acl keyword url_regex -i";
#$namelist="";
#foreach my $word ( @$keyword )
#{
#    if ( $word->{keywordname} eq 'system' ) { next; }
#    $namelist .= " ".$word->{keywordname};
#}    
#if ( $namelist ne "" )
#{
#     modifyfile($QB_SQUID_CONF, "$statement.*", $statement." ".$namelist);
#}
#else
#{
#     modifyfile($QB_SQUID_CONF, "$statement.*", $statement);
#}
#if ( !open(KEYWORD,">$QB_SQUID_KEYWORD") )
#{
#    print qq (Fail to Open KEYWORD Config file !!);
#}
#foreach my $word ( @$keyword )
#{
#    if ( $word->{keywordname} eq 'system' ) { next; }
#    print KEYWORD qq "$word->{keywordname}\n";
#}


