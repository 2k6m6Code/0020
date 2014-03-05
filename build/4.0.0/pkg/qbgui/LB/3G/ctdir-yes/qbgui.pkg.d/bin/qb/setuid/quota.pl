#!/usr/bin/perl

use CGI;

require ("/usr/local/apache/qb/qbmod.cgi");
#print "Content-type:text/html\n\n";

my $cgi = new CGI;
my $action = $cgi->param("action");

if ($action eq "date")
{
    my $quotaref = XMLread($gPATH.'quota.xml');
    my $quotalist = $quotaref->{quota};
    open(FILE,"/usr/local/apache/qb/Log_file/quota_Dynamic");
    ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday) = localtime(time);
    foreach my $quota (@$quotalist)
    {
        if ($quota->{gateway} eq "system"){next;}
        foreach my $line (<FILE>)
        {
            my ($num,$dev,$gate,$size)=split(/,/,$line);
            if ($gate ne $quota->{gateway_16} || $dev ne $quota->{port}){next;}
            if ($num ne $quota->{num})
            {
                $quota->{num} = $num;
            }
            
            #if ($gate eq $quota->{gateway_16} && $dev eq $quota->{port} && $size ne "0" && $quota->{alert} ne "0")
            #{
            #    my ($num,$oo)=(":",$quota->{down});
            #    my $max = $num*$oo;
            #    if(($size/$max) < ($quota->{alert}/100))
            #    {
            #    }
            #}
        }
        close(FILE); 
        my $time = $hour.":".$min;
        if ($quota->{cycle} eq "1")
        {
            if ($time eq $quota->{date})
            {
                system("/usr/local/apache/qb/setuid/run /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=CREAT LINK=$quota->{gateway}");
            }
        }
        elsif ($quota->{cycle} eq "7")
        {
            if ($wday eq $quota->{chose} && $time eq $quota->{date})
            {
            	system("/usr/local/apache/qb/setuid/run /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=CREAT LINK=$quota->{gateway}");
            }
        }
        elsif ($quota->{cycle} eq "30")
        {
            if ($yday eq $quota->{chose} && $time eq $quota->{date})
            {
            	system("/usr/local/apache/qb/setuid/run /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=CREAT LINK=$quota->{gateway}");
            }
        }
    }
    XMLwrite($quotaref, $gPATH."quota.xml");
}
