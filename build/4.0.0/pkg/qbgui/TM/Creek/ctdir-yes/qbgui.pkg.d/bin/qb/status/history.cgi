#!/usr/bin/perl
use CGI;
use POSIX;
#use Data::Dumper;
push(@INC, "/usr/local/apache/qb/status");
require "nethis.lib";
require ("/usr/local/apache/qb/qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
# authenticate(action=>'RANDOMCHECK');
print "Content-type:text/html\n\n";

#read-in form information ------------------------------
my $form = new CGI;
# my %action;

sub printHeader()
{
print  <<HEADER;
    <html>
    <body>
HEADER

    print qq(<script>\n);
    print qq(window.parent.pmaster.clear\(\););
}

sub printFooter()
{
    print qq(window.parent.pmaster.show();\n);
    print qq(</script>\n);
    print qq(</body> </html>);
}


#--------------------------------------------------------------------------------
# $_[0]: pull-down menu option on oceanx's UI.
# $_[1]: resulting hash to print
sub printQueryResult
{
    my $item = $_[0];
    my $ans = $_[1];

    # inbound index is 1, outbound index is 2
    my $io_index = $item eq 'outbound' ? 0 : 1;

    my $firstentry = 1;
    print qq(window.parent.pmaster.add\("$item",");
    foreach my $key (sort keys %$ans)
    {
        if ($firstentry != 1) # if not the first entry, print
        {
           print ",";
        }

        # only want the bytes counts in kb, no packet counts
        #print "--- key: $key---- value: " . $ans->{$key}->{0} . "\n";
        #$ans->{$key}->{0} =~ m#,(.*)#;
        #print "dollar 1: $1\n";

        print $ans->{$key}->{$io_index}/1024.0;
        $firstentry++;
    }
    print qq("\););
}

# Add the result of the two answer hashes together
# This function is used to add traffic together, such as port 20 and 21
# and places result back in $_[0]
# $_[0]: one answer hash
# $_[1]: the other answer hash
sub addAnsHashes
{
    my $a = $_[0];
    my $b = $_[1];

    foreach my $key (keys %$a)
    {
        $a->{$key} += $b->{$key};
    }
}

#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
# main
# Note: if user has no specific query for proto, srcip and dstip, query, 
# fill in appropriate queries(all, 0.0.0.0/0)

if ($form->param('action') eq 'query')
{
    my %qhash;
    my %in_qhash;
    my $from_time = $form->param('from_year') . sprintf("%02d", $form->param('from_month')) .
                    sprintf("%02d", $form->param('from_date')) . '_' . 
                    sprintf("%02d", $form->param('from_hour')) . sprintf("%02d", $form->param('from_minute'));
    my $to_time = $form->param('to_year') . sprintf("%02d", $form->param('to_month')) .
                    sprintf("%02d", $form->param('to_date')) . '_' . 
                    sprintf("%02d", $form->param('to_hour')) . sprintf("%02d", $form->param('to_minute'));

    print $from_time . '<br>';
    print $to_time . '<br>';

    my @fields = split(';', $form->param('policy'));
    @policy = split('\|', $fields[0]);
    my $srcip = $policy[0];
    my $srcprt = $policy[1];
    my $dstip = $policy[2];
    my $dstprt = $policy[3];
    my $proto = $policy[4];

    $qhash{'proto'} = $proto if ($proto);
    $qhash{'srcip'} = $srcip ne '' ? $srcip : '0.0.0.0/0';
    $qhash{'dstip'} = $dstip ne '' ? $dstip : '0.0.0.0/0';
    $qhash{'icmp'} = '';

    if ($srcprt eq 'ping')
    {
        $qhash{'icmp'} = '0';
    }
    else
    {
        $qhash{'srcprt'} = $srcprt if (!($srcprt =~ /:/) && $srcprt ne '');
        $qhash{'sprts'} = $srcprt if ($srcprt =~ /:/ && $srcprt ne '');
    }

    if ($dstprt eq "ping")
    {
        $qhash{'icmp'} = '8';
    }
    else
    {
        $qhash{'dstprt'} = $dstprt if (!($dstprt =~ /:/) && $dstprt ne '');
        $qhash{'dprts'} = $dstprt if ($dstprt =~ /:/ && $dstprt ne '');
    }

    if ($qhash{'srcip'} eq 'localhost') { $qhash{'srcip'} = "172.31.3.1"; }

    # take out /32 if it exists(because when making query, no /32 allowed)
    if ($qhash{'srcip'} =~ m#(.*)/32#) { $qhash{'srcip'} = $1; }
    if ($qhash{'dstip'} =~ m#(.*)/32#) { $qhash{'dstip'} = $1; }

    $in_qhash{'proto'} = $qhash{'proto'} if (exists $qhash{'proto'});
    $in_qhash{'srcip'} = exists $qhash{'dstip'} ? $qhash{'dstip'} : '0.0.0.0/0';
    $in_qhash{'dstip'} = exists $qhash{'srcip'} ? $qhash{'srcip'} : '0.0.0.0/0';
    $in_qhash{'srcprt'} = $qhash{'dstprt'} if (exists $qhash{'dstprt'});
    $in_qhash{'dstprt'} = $qhash{'srcprt'} if (exists $qhash{'srcprt'});
    $in_qhash{'sprts'} = $qhash{'dprts'} if (exists $qhash{'dprts'});
    $in_qhash{'dprts'} = $qhash{'sprts'} if (exists $qhash{'sprts'});
    $in_qhash{'icmp'} = $qhash{'icmp'} if (exists $qhash{'icmp'});


    #print "qhash{'proto'}: -$qhash{'proto'}-<br>\n";
    #print "qhash{'srcip'}: -$qhash{'srcip'}-<br>\n";
    #print "qhash{'dstip'}: -$qhash{'dstip'}-<br>\n";
    #print "qhash{'srcprt'}: -$qhash{'srcprt'}-<br>\n";
    #print "qhash{'dstprt'}: -$qhash{'dstprt'}-<br>\n";
    #print "qhash{'sprts'}: -$qhash{'sprts'}-<br>\n";
    #print "qhash{'dprts'}: -$qhash{'dprts'}-<br>\n";
    #print "qhash{'icmp'}: -$qhash{'icmp'}-<br>\n";


    my %ans;
    my @total_ans;

    # FIXME: Everything except ICMP works. ICMP doesn't work because I'm not entirely sure of the logics in this file yet,
    # and in checker ICMP data grabbing is not working yet. Need to fix that.

    # assume not both dst prt and src prt are used
    if ($qhash{'icmp'} ne '')
    {
        my %queryHash;
        $queryHash{0} = \%qhash;
        $queryHash{1} = \%in_qhash;
        query($from_time, $to_time, \%queryHash, \%ans);
        push(@total_ans, \%ans);
    }
    elsif ($qhash{'srcprt'} ne 'others' && $qhash{'dstprt'} ne 'others')
    {
        # --- need to translate known ports to numerical
        my $service=XMLread($gACTIVEPATH.'service.xml');
        my $servicelist=$service->{service};
        foreach $service (@$servicelist)
        {
            #print "checking service: $service->{title}<br>\n";
            if ($qhash{'srcprt'} eq $service->{'title'})
            { 
                $portlist = $service->{port};
                foreach my $port (@$portlist)
                {
                    next if ($port->{value} eq 'system');
                    if ($qhash{'proto'} eq $port->{protocol})
                    {
                        $qhash{'srcprt'} = $port->{value};
			$in_qhash{'dstprt'} = $port->{value};

                        my %queryHash;
                        $queryHash{0} = \%qhash;
                        $queryHash{1} = \%in_qhash;

                        query($from_time, $to_time,\%queryHash, \%ans);

                        push(@total_ans, \%ans);
                    }
                }
                last;
            }
            if ($qhash{'dstprt'} eq $service->{title})
            {
                $portlist = $service->{port};
                foreach my $port (@$portlist)
                {
                    next if ($port->{value} eq 'system');
                    if ($qhash{'proto'} eq $port->{protocol})
                    {
                        $qhash{'dstprt'} = $port->{value};
			$in_qhash{'srcprt'} = $port->{value};

                        my %queryHash;
                        $queryHash{0} = \%qhash;
                        $queryHash{1} = \%in_qhash;

                        query($from_time, $to_time, \%queryHash, \%ans);
                        push(@total_ans, \%ans);
                    }          
                }
                last;
            }
        }
    }
    else
    {
        $qhash{'srcprt'} = '';
        $qhash{'dstprt'} = '';
        $qhash{'proto'} = 'all';

        $in_qhash{'srcprt'} = '';
        $in_qhash{'dstprt'} = '';
        $in_qhash{'proto'} = 'all';

        my %queryHash;

	# inbound index is 1, outbound index is 2
        $queryHash{0} = \%qhash;
        $queryHash{1} = \%in_qhash;
        query($from_time, $to_time, \%queryHash, \%ans);
        push(@total_ans, \%ans);
    }

    # if there are multiple ports, add these ports value together
    # print "size: " . scalar (@total_ans) . "<br>\n";
    if (scalar (@total_ans) > 1)
    {
        for (my $i = 1; $i < scalar (@total_ans); $i++) { addAnsHashes(\%{$total_ans[0]}, \%{$total_ans[$i]}); }
    }

#    print "=========\n";
#    foreach my $key (keys %{$total_ans[0]})
#    {
#        #print "$ans->{$key}<br>\n";
#        #print "$ans{$key}<br>\n";
#        # $test = %{$total_ans[0]};
#        # %{$total_ans[0]}->{$key} = 3;
#        print "key $key: " . %{$total_ans[0]}->{$key} . "<br>\n";;
#        # print "key $key: " . $test->{$key} . "<br>\n";;
#        $firstentry++;
#    }
#    print "=========\n";

    printHeader();
    printQueryResult('outbound',\%{$total_ans[0]});
    printQueryResult("inbound", \%{$total_ans[0]});
    printFooter();
}
elsif ($form->param('action') eq 'policy')
{
print <<HEADER2;
    <html>
    <body>
    <form>
HEADER2

    my $fwmark=XMLread($gACTIVEPATH.'fwmark.xml');

    my $service=XMLread($gACTIVEPATH.'service.xml');
    my $servicelist=$service->{service};

    my @tags = qw(from_to from nat dmz lvs to from_service_to);
    print qq(<script>);
    print qq(window.parent.pcmaster.clear();\n);
    foreach $tag (@tags)
    {
        my $marks = $fwmark->{$tag}->[0]->{mark};
        foreach my $mark ( @$marks )
        {
            my %m=%$mark;
	    next if ($m{'service'} eq 'system');
	    next if ($m{'direction'} eq '*');

            if ($m{'service'} ne 'others')
            {
                foreach $service (@$servicelist)
                {
                    next if ($service->{title} ne $m{'service'});

                    $portlist = $service->{port};
                    foreach $port (@$portlist)
                    {
                        next if ($port->{value} eq 'system');

                        #print qq(<input type='hidden' name='policy' value=');
                        print "window.parent.pcmaster.add(";
                        if ($m{'source'} ne 'system')
                        {
                            if ($m{'source'} ne '0.0.0.0/0')
                            {
                                print qq("$m{'source'}");
                            }
                            else
                            {
                                print qq("");
                            }
                        }
                        else { print qq(""); }
                        print qq(,);
                        if ($m{'direction'} eq 's')
                        {
                            print qq("$m{'service'}");
                        }
                        else { print qq(""); }
                    
                        print qq(,);
                        if ($m{'destination'} ne 'system')
                        {
                            print qq("$m{'destination'}") 
                        }
                        else { print qq(""); }
                        print qq(,);
                        if ($m{'direction'} eq 'd')
                        {
                            print qq("$m{'service'}") 
                        }
                        else { print qq(""); }
                        print qq(,);
                        print qq("$port->{protocol}");
                        print qq(\);\n);
                    }
                }
            }
            else
            {
                print "window.parent.pcmaster.add(";
                if ($m{'source'} ne 'system')
                {
                    if ($m{'source'} ne '0.0.0.0/0')
                    {
                        print qq("$m{'source'}");
                    }
                    else { print qq(""); }
                }
                else { print qq(""); }
                print qq(,);
                if ($m{'direction'} eq 's')
                {
                    print qq("$m{'service'}") 
                }
                else { print qq(""); }
                print qq(,);
                if ($m{'destination'} ne 'system')
                {
                    print qq("$m{'destination'}") 
                }
                else { print qq(""); }
                print qq(,);
                if ($m{'direction'} eq 'd')
                {
                    print qq("$m{'service'}") 
                }
                else { print qq(""); }
                print qq(,);
                print qq("all");
                print qq(\);\n);
            }
        }
    }

    print qq(</script>);
    print qq(</form> </body> </html>);
}
