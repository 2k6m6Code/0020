#!/usr/bin/perl
require ('/usr/local/apache/qb/qbmod.cgi');
#---------------------------------------------------------------
# main program start
#--------------------------------------------------------------
my $QB_SQUID_CONF="/usr/local/squid/etc/squid.conf";
my $QB_CATEGORY_XML="/usr/local/apache/qbconf/category.xml";
my $QB_WEBFILTER_XML="/usr/local/apache/qbconf/iniweb.xml";
my $QB_SCHEDULE_XML="/usr/local/apache/qbconf/schedule.xml";
my $QB_SQUID_XML="/usr/local/apache/qbconf/squidgen.xml";
my $QB_SQUIDURL_XML="/usr/local/apache/qbconf/squidurl.xml";
my $QB_SQUIDGUARD_CONFIG="/usr/local/squidGuard/squidGuard.conf";

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/category.xml
#------------------------------------------------------------------
my $category=XMLread($QB_CATEGORY_XML);
my $categorylist=$category->{category};

if ( !$category ) #if the string is NULL
{
    print "$QB_CATEGORY_XML is NULL \n";
}



#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/schedule.xml
#------------------------------------------------------------------
my $schedule=XMLread($QB_SCHEDULE_XML);
my $schedulelist=$schedule->{schedule};

if ( !$schedule ) #if the string is NULL
{
    print "$QB_SCHEDULE_XML is NULL \n";
}

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/iniweb.xml
#------------------------------------------------------------------
my $webfilter = XMLread($QB_WEBFILTER_XML);
my $filterlist = $webfilter->{class};

if ( !$webfilter ) #if the string is NULL
{
    print "$QB_WEBFILTER_XML is NULL \n";
}

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/qsuidgen.xml
#------------------------------------------------------------------
my $squid=XMLread($QB_SQUID_XML);

if ( !$squid ) #if the string is NULL
{
    print "$QB_SQUID_XML is NULL \n";
}
my $copyconfig = `cp -f /usr/local/squid/etc/squidGuard.conf.bak /usr/local/squidGuard/squidGuard.conf`;
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
my $src = '';
my $time = '';
my $acl = '';
my $count = 1;
my %weekly = (
    Mon	=> 'm',
    Tue	=> 't',
    Wed	=> 'w',
    Thu	=> 'h',
    Fri => 'f',
    Sat => 'a',
    Sun => 's',
);

@$filterlist = sort ini_class_sort_by_realip ( @$filterlist );

foreach my $filter ( @$filterlist )
{
    my $addresslist;
    if ( $filter->{source} eq 'system' ) { next; }
    
    if ( grep(/^host-/, $filter->{source}) )
    {
        my $tmpsource = $filter->{source};
        $tmpsource =~ s/host-//g; 
        $addresslist = maintainHost( action=>'GETADDRESSLIST', hostname=>$tmpsource);
    }
    else
    {
        $addresslist = $filter->{source}; 
    }
    
    if ( grep(/,/, $addresslist) )
    {
        my @iplist = split(/,/, $addresslist);
        $src .= "src websrc$count {\n";
        foreach my $ip ( @iplist )
        {
            $src .= "\tip\t$ip\n";
        }
        $src .= "}\n\n";
    }
    else
    {
        $src .= "src websrc$count {\n\tip\t$addresslist\n}\n\n";
    }
    
    if ( $filter->{schedule}  eq 'All Week' )
    {
        $acl .= "\twebsrc$count {\n";
    }
    else 
    {
        foreach my $sch ( @$schedulelist )
        {
            if ( $sch->{schname} eq $filter->{schedule} )    
            {
                $time .= "time webtime$count {\n";
                my $subsch = $sch->{subsch};
                foreach my $item ( @$subsch )
                {
                    $time .= "\tweekly\t";
                    my $days = $item->{days};
                    my @dayarray = split(/,/, $days);
                    foreach my $day ( @dayarray )
                    {
                        $time .= "$weekly{$day}";
                        #$time .= "$day";
                    }
                    if ( $item->{timestart} =~ m/^\d:/ )
                    {
                        $item->{timestart} = "0".$item->{timestart};
                    }
                    if ( $item->{timestop} =~ m/^\d:/ )
                    {
                        $item->{timestop} = "0".$item->{timestop};
                    }
                    $time .= "\t$item->{timestart}-$item->{timestop}\n";
                }
                $time .= "}\n\n";
            }
        }
        $acl .= "\twebsrc$count within webtime$count {\n";
    }
    my $sign = ( $filter->{web_action} eq 'Deny' ) ? ( '!' ) : ( '' );
    
    $acl .= "\t\tpass ";  
    foreach my $category ( @$categorylist )  
    {
        if ( $category->{categoryname} eq $filter->{webfilter} )
        {
            #print "1111\n";
            my $block = $category->{block};
            my @blockarray = split(/,/, $block);
            foreach my $item ( @blockarray )
            {
                $acl .= "$sign$item ";
            }
        }
    }
    if ( $filter->{web_action} eq 'Deny' ) { $acl .=  "all"; }
    $acl .= "\n\t}\n\n";
    $count++;
}

my $statement="url_rewrite_program /usr/local/bin/squidGuard -c /usr/local/squidGuard/squidGuard.conf";
if ( $src ne '' && $acl ne '' )
{
    modifyfile($QB_SQUID_CONF,"^#*".$statement,$statement); # remove # character in the stateament
}
else
{
    modifyfile($QB_SQUID_CONF,$statement,"#".$statement);
    exit;
}

print SQUIDGUARD qq "$src";
print SQUIDGUARD qq "$time";
print SQUIDGUARD qq "acl {\n";
print SQUIDGUARD qq "$acl";
#print SQUIDGUARD qq "}\n";
print SQUIDGUARD qq "\tdefault {\n";
print SQUIDGUARD qq "\t\tpass ";
print SQUIDGUARD "all\n";
print SQUIDGUARD qq "\t\tredirect  http://172.31.3.1:4000/block.cgi?clientaddr=%a&clientname=%n&clientuser=%i&clientgroup=%s&targetgroup=%t&url=%u\n";

print SQUIDGUARD qq "\t}\n";
print SQUIDGUARD qq "}\n";
close(SQUIDGUARD);



=cut
print SQUIDGUARD "all\n";
#print SQUIDGUARD qq "\t\tredirect http://www.creek.com.tw\n";
print SQUIDGUARD qq "\t\tredirect  http://172.31.3.1:4000/block.cgi?clientaddr=%a&clientname=%n&clientuser=%i&clientgroup=%s&targetgroup=%t&url=%u\n";
print SQUIDGUARD "\t}\n}\n";
=cut
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

    #if ( $avalue == $bvalue )
    #{
    #    return $a->{schedule} cmp $b->{};
    #}
    #else
    #{
        #$avalue <=> $bvalue;
    #}
    $bvalue <=> $avalue;
}


