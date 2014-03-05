#!/usr/bin/perl
require ('/usr/local/apache/qb/qbmod.cgi');
#---------------------------------------------------------------
# main program start
#--------------------------------------------------------------
my $QB_SQUID_CONF="/usr/local/squid/etc/squid.conf";
my $QB_CATEGORY_XML="/usr/local/apache/qbconf/category.xml";
my $QB_SQUID_XML="/usr/local/apache/qbconf/squidgen.xml";
my $QB_SQUIDURL_XML="/usr/local/apache/qbconf/squidurl.xml";
my $QB_SQUIDGUARD_CONFIG="/usr/local/squidGuard/squidGuard.conf";

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/category.xml
#------------------------------------------------------------------
my $category=XMLread($QB_CATEGORY_XML);

if ( !$category ) #if the string is NULL
{
    print "$QB_CATEGORY_XML is NULL \n";
}

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/qsuidgen.xml
#------------------------------------------------------------------
my $squid=XMLread($QB_SQUID_XML);

if ( !$squid ) #if the string is NULL
{
    print "$QB_SQUID_XML is NULL \n";
}

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/squidurl.xml
#------------------------------------------------------------------
my $squidurl=XMLread($QB_SQUIDURL_XML);

if ( !$squidurl ) #if the string is NULL
{
    print "$QB_SQUIDURL_XML is NULL \n";
}
#------------------------------------------
# modify squid config to allow squidGuard
#------------------------------------------
my $statement="url_rewrite_program /usr/local/bin/squidGuard -c /usr/local/squidGuard/squidGuard.conf";
if ( $category->{block} ne '' )
{
    modifyfile($QB_SQUID_CONF,"^#*".$statement,$statement); # remove # character in the stateament
}
else
{
    modifyfile($QB_SQUID_CONF,$statement,"#".$statement); # Add # character in the stateament
    exit;
}

my $copyconfig = `cp -a /usr/local/squidGuard/squidGuard.conf.bak /usr/local/squidGuard/squidGuard.conf`;
if ( $copyconfig )
{
    print "copy squidGuard.conf error\n";
}

#------------------------------------------
# open squidGuard config
#------------------------------------------
if ( !open(SQUIDGUARD,">>$QB_SQUIDGUARD_CONFIG") )
{
     print qq (Fail to Open SQUIDGUARD Config file !!);
}

#------------------------------------------
# append exempt ip to squidGuard config.
#------------------------------------------
my $exempt = $squidurl->{exempt}[0]->{net};
my $exempt_size = scalar @$exempt;
if ( $exempt_size )
{
    print SQUIDGUARD qq "src exempt {\n";
    foreach my $net ( @$exempt )
    {
        print SQUIDGUARD qq "\tip $net->{ip}\n";
    }
    print SQUIDGUARD qq "}\n\n";
}

if ( $squid->{schedule} )
{
    print SQUIDGUARD qq "time blocktime {\n";
    print SQUIDGUARD qq "\tweekly ";
    my $time='';
    if ( $squid->{sun} eq '1' ) { $time = 's'; }
    if ( $squid->{mon} eq '1' ) { $time .= 'm'; }
    if ( $squid->{tue} eq '1' ) { $time .= 't'; }
    if ( $squid->{wed} eq '1' ) { $time .= 'w'; }
    if ( $squid->{thu} eq '1' ) { $time .= 'h'; }
    if ( $squid->{fri} eq '1' ) { $time .= 'f'; }
    if ( $squid->{sat} eq '1' ) { $time .= 'a'; }
    $time .= ' '.$squid->{timehour1}.':'.$squid->{timemin1}.'-'.$squid->{timehour2}.':'.$squid->{timemin2};
    print SQUIDGUARD qq "$time\n" ;
    print SQUIDGUARD qq "}\n\n";
}

print SQUIDGUARD qq "acl {\n";
if ( $exempt_size )
{
    print SQUIDGUARD qq "\texempt {\n";
    print SQUIDGUARD qq "\t\tpass all\n\t}\n";
}
if ( $squid->{schedule} )
{
    print SQUIDGUARD qq "\tallsource outside blocktime {\n";
    print SQUIDGUARD qq "\t\tpass all\n\t}\n";
}
print SQUIDGUARD qq "\tdefault {\n";
print SQUIDGUARD qq "\t\tpass ";
my @blockarray = split(/,/, $category->{block});
my $newstatement="";
foreach my $item ( @blockarray )
{
    print SQUIDGUARD qq "!$item ";
}
print SQUIDGUARD "all\n";
#print SQUIDGUARD qq "\t\tredirect http://www.creek.com.tw\n";
print SQUIDGUARD qq "\t\tredirect  http://172.31.3.1:4000/block.cgi?clientaddr=%a&clientname=%n&clientuser=%i&clientgroup=%s&targetgroup=%t&url=%u\n";
print SQUIDGUARD "\t}\n}\n";

=cut
my $statement="\t\tpass";
my $newstatement="";
foreach my $item ( @blockarray )
{
    $newstatement .= "!$item ";
}
#modifyfile($QB_SQUIDGUARD_CONFIG,"^$statement.*","\t\tpass $newstatement all"); # remove # character in the stateament
=cut



