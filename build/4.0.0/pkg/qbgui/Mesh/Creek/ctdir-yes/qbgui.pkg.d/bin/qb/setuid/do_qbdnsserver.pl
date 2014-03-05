#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

#--------------------------------------------------------------------
# main program start
#--------------------------------------------------------------------
my $QB_SQUID_CONF = "/usr/local/squid/etc/squid.conf";
my $QB_SCHEDULE_XML = "/usr/local/apache/qbconf/schedule.xml";
my $QB_SQUID_XML = "/usr/local/apache/qbconf/squidgen.xml";
my $QB_SQUIDURL_XML="/usr/local/apache/qbconf/squidurl.xml";
#my $QB_SQUIDGUARD_CONFIG = "/usr/local/squidGuard/squidGuard.conf";
my $QB_DNS_FILE = "/usr/local/apache/qbconf/overview.xml";
my $QB_DNS_CONF = "/usr/local/bind/named.conf";
my $QB_DNS_XML = "/usr/local/apache/qbconf/inidns.xml";
my $QB_DNSPROXY_IPTABLES = "/usr/local/apache/qb/setuid/do_qbdnsiptables.pl";
my $QB_DNSPROXY_CONF = "/usr/local/squid/etc/dnspxy.conf";
my $QB_DNSPROXY_SH = "/usr/local/squid/etc/dnsproxy.sh";

#--------------------------------------------------------------------
# read the option from the file /usr/local/apache/qbconf/overview.xml
#--------------------------------------------------------------------

my $relay = XMLread ( $QB_DNS_FILE );

if ( !$relay )
{
    print "QB_DNS_FILE is NULL \n";
}

print qq ($relay->{relay}\n);

if ( $relay->{relay} )
{
    modifyfile ( $QB_DNS_CONF, "^.*forwarders.*", "       forwarders{ $relay->{relay}; };");
    modifyfile ( $QB_DNS_CONF, "^#.*forwarders.*", "       forwarders{ $relay->{relay}; };");
}

#--------------------------------------------------------------------
# modify dnsproxy_port
#--------------------------------------------------------------------

if ( $overview->{dnsproxyport} )
{
    modifyfile ( $QB_DNSPROXY_CONF, "dnsproxy_port.*","dnsproxy_port ".$overview->{dnsproxyport}." transparent"); # refresh dns proxy port No.
    #modifyfile ( $QB_DNSPROXY_CONF,"^#*"."dnsproxy_port","dnsproxy_port"); #remove # character in the stateament
}
else
{
    modifyfile ( $QB_DNSPROXY_CONF, "^#*"."dnsproxy_port","#"."dnsproxy_port"); # Disable dns proxy function
}

#--------------------------------------------------------------------
# read the option from the file /usr/local/apache/qbconf/schedule.xml
#--------------------------------------------------------------------

my $schedule = XMLread ( $QB_SCHEDULE_XML );
my $schedulelist = $schedule->{schedule};

if ( !$schedule ) #if the string is NULL
{
    print " $QB_SCHEDULE_XML is NULL \n";
}


#---------------------------------------------------------------------
# read the option from the file /usr/local/apache/qbconf/inidns.xml
#---------------------------------------------------------------------

my $dnsrelay = XMLread ( $QB_DNS_XML );
my $dnsrelaylist = $dnsrelay->{class};

if ( !$dnsrelay ) #if the string is NULL
{
    print "$QB_DNS_XML is NULL \n";
}

#---------------------------------------------------------------------
# read the option from the file /usr/local/apache/qbconf/squidgen.xml
#---------------------------------------------------------------------

#my $squid = XMLread ( $QB_SQUID_XML );

#if ( !$squid ) #if the string is NULL
#{
#    print "QB_SQUID_XML is NULL \n";
#}

#my $copyconfig = `cp -f /usr/local/squid/etc/squidGuard.conf.bak /usr/local/squidGuard/squidGuard.conf`;
#if ( $copyconfig )
#{
#    print "copy squidGuard.conf error\n";
#}

#------------------------------------------
# open squidGuard config
#------------------------------------------

#if ( !open(SQUIDGUARD,">>$QB_SQUIDGUARD_CONFIG") )
#{
#     print qq (Fail to Open SQUIDGUARD Config file !!);
#}
#     my $src = '';
#     my $time = '';
#     my $acl = '';
#     my $count = 1;
#     my %weekly = (
#         Mon => 'm',
#         Tue => 't',
#         Wed => 'w',
#         Thu => 'h',
#         Fri => 'f',
#         Sat => 'a',
#         Sun => 's',
#         );
                                 
#@$dnsrelaylist = sort ini_class_sort_by_realip ( @$dnsrelaylist );

#foreach my $dnsrelay ( @$dnsrelaylist )
#{

#    my $addresslist;
#    if ( $dnsrelay->{source} eq 'system' ) { next; }
#    if ( grep(/^host-/, $dnsrelay->{source}) )
#    {

#        my $tmpsource = $dnsrelay->{source};
#        $tmpsource =~ s/host-//g;
#        $addresslist = maintainHost ( action=>'GETADDRESSLIST', hostname=>$tmpsource);
#        print qq ($dnsrelay->{realip}\n);
        
#    }
#    else
#    {
#        $addresslist = $dnsrelay->{source};
#        print qq ($dnsrelay->{source}\n);
        
#    }
    
#    if ( grep(/,/, $addresslist) )
#    {
#        my @iplist = split(/,/, $addresslist);
#        $src .= "src dnssrc$count {\n";
#        foreach my $ip ( @iplist )
#        {
#            $src .= "\tip\t$ip\n";
#        }
#        $src .= "}\n\n";
#    }
#    else
#    {
#        $src .= "src dnssrc$count {\n\tip\t$adresslist\n}\n\n";
#    }
    
#    if ( $dnsrelay->{schedule} eq 'All Week' )
#    {
#        $acl .= "\tdnssrc$count {\n";
#    }
#    else
#    {
#        foreach my $sch ( @$schedulelist )
#        {
#            if ( $sch->{schname} eq $dnsrelay->{schedule} )
#            {
#                $time .= "timedns$count {\n";
#                my $subsch = $sch->{subsch};
#                foreach my $item ( @$subsch )
#                {
#                    $time .= "\tweekly\t";
#                    my $days = $item->{days};
#                    my @dayarray = split(/,/, $days);
#                    foreach my $day ( @dayarray )
#                    {
#                        $time .= "$weekly{$day}";
#                    }
#                    if ( $item->{timestart} =~ m/^\d:/ )
#                    {
#                        $item->{timestart} = "0".$item->{timestart};
#                    }
#                    if ( $item->{timestop} =~ m/^\d:/ )
#                    {
#                        $item->{timestop} = "0".$item->{timestop};
#                    }
#                    $time .= "\t$item->{timestart}-$item->{timestop}\n";
#                }
#                $time .= "}\n\n";
#            }
#        }
#        $acl .= "\tdnssrc$count within dnstime$count {\n";
#    }
#}

#my $statement ="url_rewrite_program /usr/local/bin/squidGuard -c /usr/local/squidGuard/squidGuard.conf";
#if ( $src ne '' && $acl ne '' )
#{
#    modifyfile ($QB_SQUID_CONF,"^#*".$statement,$statement); # remove # character in the statement
#}
#else 
#{
#    modifyfile ($QB_SQUID_CONF,$statement,,"#".$statement);
#    exit;
#}

#print SQUIDGUARD qq "$src";
#print SQUIDGUARD qq "$time";
#print SQUIDGUARD qq "acl {\n";
#print SQUIDGUARD qq "$acl";
#print SQUIDGUARD qq "\tdefault {\n";
#print SQUIDGUARD qq "\t\tpass ";
#print SQUIDGUARD "all \n";
#print SQUIDGUARD qq "\t\tredirect  http://172.31.3.1:4000/block.cgi?clientaddr=%a&clientname=%n&clientuser=%i&clientgroup=%s&targetgroup=%t&url=%u\n";

#print SQUIDGUARD qq "\t}\n";
#print SQUIDGUARD qq "}\n";
#print (SQUIDGUARD);
#print SQUIDGUARD

#=cut 
#print SQUIDGUARD "all\n";
#print SQUIDGUARD qq "\t\tredirect  http://172.31.3.1:4000/block.cgi?clientaddr=%a&clientname=%n&clientuser=%i&clientgroup=%s&targetgroup=%t&url=%u\n";
#print SQUIDGUARD "\t}\n}\n";
#=cut

sub ini_class_sort_by_realip
{
    my @afields=split(/\.|\/|\-|\,/,$a->{realip});
    my @bfields=split(/\.|\/|\-|\,/,$b->{realip});
    
    foreach my $index ( 0..4 )
    {
        $avalue=int($afields[$index]);
        $bvalue=int($bfields[$index]);
        if ( $avalue != $bvalue ) { last; }
    }
    $bvalue <=> $avalue;
}
