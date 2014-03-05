#!/usr/bin/perl
use CGI;

require ('../qbmod.cgi');
require ('isphis.lib');

my $form=new CGI;
my %namehash=maintainBasic( action=>"GETACTIVEISPNAMEHASH" );
my %gwhash=maintainBasic( action=>"GETACTIVEISPGWHASH" );
my %nichash=maintainBasic( action=>"GETACTIVEISPNICHASH" );
print "Content-type:text/html\n\n";

# $_[0], gateway to search for
# $_[1], an array of gateway to search from 
# returns 1 if its in the list, else 0


sub make_query()
{
    print "In make_query<br>";
    my $fromYY = sprintf "%04d", $form->param('from_yy');
    my $fromMM = sprintf "%02d", $form->param('from_mm')+1;
    my $fromDD = sprintf "%02d", $form->param('from_dd');
    my $fromhh = sprintf "%02d", $form->param('from_hh');
    my $frommm = sprintf "%02d", $form->param('from_min');


    my $toYY = sprintf "%04d", $form->param('to_yy');
    my $toMM = sprintf "%02d", $form->param('to_mm')+1;
    my $toDD = sprintf "%02d", $form->param('to_dd');
    my $tohh = sprintf "%02d", $form->param('to_hh');
    my $tomm = sprintf "%02d", $form->param('to_min');

    my %ans;
    query("$fromYY$fromMM$fromDD" . '_' . "$fromhh$frommm",
          "$toYY$toMM$toDD" . '_' . "$tohh$tomm", \%ans);
    #print(Dumper(\%ans));
    #print(Dumper(%namehash));

    print qq(<html><head></head><body><script>);
	
	# while (my ($key, $value) = each (%nichash)) {  	
      # 取出雜湊中的每一對鍵值，並且分別放入$key, $value
      # print "$key => $value\n";
	# }
	@qtt;@ctt;
    print "\nwindow.parent.pmaster.clear()\n";
#######################################total_chart start
	for my $ispid (sort num_sort keys %namehash)
    {
        my $ispname = $namehash{$ispid};
        #my $ispgw = $gwhash{$ispid};
		
        # ---- now traverse through time, find the right ISP by gateway IP
        # ---- inbound
        # print "window.parent.pmaster.add(\"$ispname-inbound\", \"";
        my $count = 1;
        for my $time ( sort num_sort keys %ans)
        {
            # sometimes it's not empty, but new isp configured may not have past histories
            my $foundflag = 0;
            for my $gw (keys %{$ans{$time}})
            {
                # --- get the right ISP
                #if ($ispgw eq $gw)
                if ($ispid eq $gw)
                {
                    # --- This get the final hash: $ans{$time}->{$gw}
                    $ans{$time}->{$gw} =~ m#(.*),(.*)#;
                    my $outbound = $1/128; # translate from Bytes to KBits
                    my $inbound = $2/128;  # translate from Bytes to KBits
                    # --- we only want inbound
                    if (!grep(/tmv/,$nichash{$ispid})) {
						if (!grep(/mpv/,$nichash{$ispid})){
						$qtt[$count]+=$inbound; 
						}
					}
                    
                    $count = $count + 1;
                    $foundflag = 1;
                }
		elsif ($gw eq 'empty')
		{
            $qtt[$count]=0;
                    $count = $count + 1;
                    $foundflag = 1;
		    last;
		}
            }

            if ($foundflag == 0) {$qtt[$count]=0; $count = $count + 1;}
        }
        # print "\", \"in\");\n";

        # ---- outbound
        
        my $count = 1;
        for my $time ( sort num_sort keys %ans)
        {
            # sometimes it's not empty, but new isp configured may not have past histories
            my $foundflag = 0;
            for my $gw (keys %{$ans{$time}})
            {
                # --- get the right ISP
                #if ($ispgw eq $gw)
                if ($ispid eq $gw)
                {
                    # --- This get the final hash: $ans{$time}->{$gw}
                    $ans{$time}->{$gw} =~ m#(.*),(.*)#;
                    my $outbound = $1/128; # translate from Bytes to KBits
                    my $inbound = $2/128;  # translate from Bytes to KBits
                    # --- we only want outbound
                    if (!grep(/tmv/,$nichash{$ispid})) {
						if (!grep(/mpv/,$nichash{$ispid})){
						$ctt[$count]+=$outbound; 
						}
					}
                    $count = $count + 1;
                    $foundflag = 1;
                }
		elsif ($gw eq 'empty')
		{
            $ctt[$count] =0;
                    $count = $count + 1;
                    $foundflag = 1;
		    last;
		}
            }
            if ($foundflag == 0) { $ctt[$count] =0; $count = $count + 1;}
        }
        # print "\", \"out\");\n";
    }
	shift @qtt;
	shift @ctt;
	print "window.parent.pmaster.add(\"Aggregated-inbound\", \"";
	print join(",",@qtt);
	print "\", \"in\");\n";
	# print "\n";
	print "window.parent.pmaster.add(\"Aggregated-outbound\", \"";
	print join(",",@ctt);
	print "\", \"out\");\n";
	# print "\n";
#######################################total_chart End
    #-----------------
    # looping through ISP
    # looping through ispids
    for my $ispid (sort num_sort keys %namehash)
    {
        my $ispname = $namehash{$ispid};
        #my $ispgw = $gwhash{$ispid};
    
        # ---- now traverse through time, find the right ISP by gateway IP
        # ---- inbound
        print "window.parent.pmaster.add(\"$ispname-inbound\", \"";
        my $count = 1;
        for my $time ( sort num_sort keys %ans)
        {
            # sometimes it's not empty, but new isp configured may not have past histories
            my $foundflag = 0;
            for my $gw (keys %{$ans{$time}})
            {
                # --- get the right ISP
                #if ($ispgw eq $gw)
                if ($ispid eq $gw)
                {
                    # --- This get the final hash: $ans{$time}->{$gw}
                    $ans{$time}->{$gw} =~ m#(.*),(.*)#;
                    my $outbound = $1/128; # translate from Bytes to KBits
                    my $inbound = $2/128;  # translate from Bytes to KBits
                    # --- we only want inbound
                    if ($count eq '1') { print qq($inbound); }
                    else { print qq(,$inbound);}
                    $count = $count + 1;
                    $foundflag = 1;
                }
		elsif ($gw eq 'empty')
		{
                    if ($count eq '1') {print qq(0) }
		    else { print qq(,0); }
                    $count = $count + 1;
                    $foundflag = 1;
		    last;
		}
            }

            if ($foundflag == 0) { print qq(,0); $count = $count + 1;}
        }
        print "\", \"in\");\n";

        # ---- outbound
        print "window.parent.pmaster.add(\"$ispname-outbound\", \"";
        my $count = 1;
        for my $time ( sort num_sort keys %ans)
        {
            # sometimes it's not empty, but new isp configured may not have past histories
            my $foundflag = 0;
            for my $gw (keys %{$ans{$time}})
            {
                # --- get the right ISP
                #if ($ispgw eq $gw)
                if ($ispid eq $gw)
                {
                    # --- This get the final hash: $ans{$time}->{$gw}
                    $ans{$time}->{$gw} =~ m#(.*),(.*)#;
                    my $outbound = $1/128; # translate from Bytes to KBits
                    my $inbound = $2/128;  # translate from Bytes to KBits
                    # --- we only want outbound
                    if ($count eq '1') { print qq($outbound); }
                    else { print qq(,$outbound);}
                    $count = $count + 1;
                    $foundflag = 1;
                }
		elsif ($gw eq 'empty')
		{
                    if ($count eq '1') {print qq(0) }
		    else { print qq(,0); }
                    $count = $count + 1;
                    $foundflag = 1;
		    last;
		}
            }
            if ($foundflag == 0) { print qq(,0); $count = $count + 1;}
        }
        print "\", \"out\");\n";
    }

#   print "window.parent.pmaster.show()\n";

    print qq(</script></body></html>);
}

# ------- main -------
make_query();
