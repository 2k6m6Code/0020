#!/usr/bin/perl
print "Content-type:text/html\n\n";
require ("global.cgi");

use CGI;
use Data::Dumper;
use XML::Simple;

    my $form = new CGI;
    my $target_source	   = $form->param('source');
    my $target_service	   = $form->param('service');
    my $target_direction   = $form->param('direction');
    my $target_destination = $form->param('destination');
    my $target_method	   = $form->param('method');
    my $target_table	   = $form->param('table');
    my $enabled_or_not	   = $form->param('enabled_or_not');
    my $SelectAllMode;
    
    if ( $target_source eq 'system' ) { $target_source = '0.0.0.0/0' ; }
    
    if ( $enabled_or_not=~m/SelectAll/ )
    {
    	my @tmparray	= split(/:/, $enabled_or_not);
    	$enabled_or_not = $tmparray[1];
    	$SelectAllMode  = '1';
    }
    my $Iniroute_XML  = 'iniroute.xml';
    my $inirouteref = XMLin('/usr/local/apache/qbconf/'.$Iniroute_XML,forcearray=>1);
    my $Proute_XML  = 'proute.xml';
    my $prouteref = XMLin('/usr/local/apache/qbconf/'.$Proute_XML,forcearray=>1);
    my $Host_XML  = 'host.xml';
    my $hostref = XMLin('/usr/local/apache/qbconf/'.$Host_XML,forcearray=>1);
    my $Fwmark_XML  = 'fwmark.xml';
    my $fwmarkref = XMLin('/usr/local/apache/qbconf/'.$Fwmark_XML,forcearray=>1);
    
    my $hostlist = $hostref->{host};
    my $classes	    = $inirouteref->{nat}->[0]->{class};
    
   #####################################################################################
   ##
   ##  Process to target policy rules
   ## 
   ##  When user click checkbox(enable/disable) on policy route.
   ##  set 'enabled='1'{enabled) or 'enabled=0'(disabled) in iniroute.xml and proute.xml.
   ##  then call qbserv to do. ( add iptables or delete ) 
   ##
   #####################################################################################

    my @proute_value;
    foreach my $class ( @$classes )
    {
    	if ( $class->{source} eq 'system' ) {next;}
    	if ( $class->{source} eq $target_source && $class->{destination} eq $target_destination && $class->{service} eq $target_service && $class->{method} eq $target_method && !$SelectAllMode )
    	{
    	    $class->{enabled}=$enabled_or_not;
    	    $class->{process_me}='1';
    	    my @src_array;
    	    my @dest_array;
    	    my $src_type;
    	    my $dest_type;
    	    if ( grep(/^host-/, $class->{source}))
    	    {
    	    	foreach my $host ( @$hostlist )
    	    	{
    	    	    if ( $host->{hostname} eq $class->{source} )
    	    	    {
    	    	    	$src_type = $host->{hosttype};
    	    	    	@src_array = split(/,/, $host->{hostaddress});
    	    	    	last;
    	    	    }
    	    	}
    	    }
    	    else
            {
                $src_type = 'normal';
                push(@src_array, $class->{source});
                #$newclass{sourcetype}='normal';
            }
            if ( grep(/^host-/, $class->{destination}) )
            {
            	foreach my $host ( @$hostlist )
            	{
            	    if ( $host->{hostname} eq $class->{destination} )
            	    {
            	    	$dest_type = $host->{hosttype};
            	    	@dest_array = split(/,/, $host->{hostaddress});
            	    	last;
            	    }
            	}
            }
            else
            {
            	$dest_type = 'normal';
                push(@dest_array, $class->{destination});
            }
            foreach my $src ( @src_array )
            {
            	foreach my $dest ( @dest_array )
            	{
            	    my $proute_view;
            	    my $fwmark_view;
            	    # Will TODO
            	    #priority = 5000
            	    if ( $class->{source} eq "0.0.0.0/0"  && $class->{advance}==1 )
            	    {
            	    	$proute_view='to';
            	    	if ( $class->{service} eq "others" ) { $fwmark_view='to'; }
			elsif ( $class->{service} ne "others" ) { $fwmark_view='from_service_to'; }
            	    }
            	    #priority = 10000
            	    elsif ( $class->{service} ne "others" && $class->{advance}==1 )
            	    {
            	    	$proute_view='fwadv';
			$fwmark_view='from_service_to';
			#$dest='';
            	    }
            	    #priority = 15000
            	    elsif ( $class->{service} eq "others" && $class->{advance}==1 )
            	    {
            	    	$proute_view='subadv';
			$fwmark_view='from_to';
            	    }
            	    #priority = 20000
            	    elsif ( $class->{service} ne "others" && $class->{advance}==0 )
            	    {
            	    	$proute_view='fw';
            	    	$dest="";
			$fwmark_view='nat';
            	    }
            	    #priority = 25000
            	    elsif ( $class->{service} eq "others" && $class->{advance}==0 )
            	    {
            	    	$proute_view='sub';
            	    	$dest="";
			$fwmark_view='from';
            	    }
            	    
		    $prouteref->{$proute_view}->[0]->{class};
		    
		    my $qbclass = $prouteref->{$proute_view}->[0]->{class};
		    #foreach my $proute_class ( @$prouteref->{subnet}->[0]->{class} )
#`/usr/local/apache/qb/setuid/run /bin/echo $enabled_or_not > /tmp/garytest`;
		    foreach my $proute_class ( @$qbclass )
		    {
#`/usr/local/apache/qb/setuid/run /bin/echo $proute_class->{source} $src $proute_class->{service} $class->{service}  >> /tmp/garytest`;
		    	#if ( $proute_class->{source} eq $src && $proute_class->{service} eq $class->{service} && $proute_class->{destination} eq $dest)
		    	if ( $proute_class->{source} eq $src && $proute_class->{service} eq $class->{service} && $proute_class->{direction} eq $target_direction)
		    	{
		    	###################################################
		    	##  TODO   add enabled and process_me in proute.xml
		    	###################################################
    	    		    $proute_class->{enabled}=$enabled_or_not;
    	    		    $proute_class->{process_me}='1';
		    	}
		    }
		    my $fwmark = $fwmarkref->{$fwmark_view}->[0]->{mark};
#`/usr/local/apache/qb/setuid/run /bin/echo $fwmark_view >> /tmp/garytest`;
		    foreach my $fwmark_mark ( @$fwmark )
		    {
#`/usr/local/apache/qb/setuid/run /bin/echo $fwmark_mark->{source} $src $fwmark_mark->{destination} $dest $fwmark_mark->{service} $target_service >> /tmp/garytest`;
		    	if ( $dest eq '' ) { $dest="system"; }
		    	if ( $fwmark_mark->{source} eq $src && $fwmark_mark->{destination} eq $dest && $fwmark_mark->{service} eq $target_service)
		    	#if ( $fwmark_mark->{source} eq $src && $fwmark_mark->{destination} eq $dest)
		    	{
		    	###################################################
		    	## TODO    add enabled and process_me in fwmark.xml
		    	###################################################
		    	    #print qq ( $fwmark_mark->{value} );
		    	    $fwmark_mark->{enabled}=$enabled_or_not;
		    	    $fwmark_mark->{process_me}='1';
		    	}
		    }
            	}
            }
    	}
    	elsif ( $SelectAllMode eq '1' )  {   $class->{enabled}=$enabled_or_not; $class->{process_me}='1';   }
    	
    }
   #####################################################################################
   #
   # Save in XML Start...
   #
   #####################################################################################
    
    `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/$Iniroute_XML`;
    if ( !open(XMLLOCK, "> $gXMLLOCK") ) { exit; }
    flock(XMLLOCK, 2);
    if ( !open(XMLFILE, "> /usr/local/apache/qbconf/".$Iniroute_XML) )
    {
    	`/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/$Iniroute_XML`;
    	exit;
    }
    my $result=XMLout($inirouteref);
    print XMLFILE $result;
    close XMLFILE;
    flock(XMLLOCK, 8);
    close XMLLOCK;
    
    `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/$Proute_XML`;
    if ( !open(XMLLOCK, "> $gXMLLOCK") ) { exit; }
    flock(XMLLOCK, 2);
    if ( !open(XMLFILE, "> /usr/local/apache/qbconf/".$Proute_XML) )
    {
    	`/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/$Proute_XML`;
    	exit;
    }
    my $result=XMLout($prouteref);
    print XMLFILE $result;
    close XMLFILE;
    flock(XMLLOCK, 8);
    close XMLLOCK;
    
    `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/$Fwmark_XML`;
    if ( !open(XMLLOCK, "> $gXMLLOCK") ) { exit; }
    flock(XMLLOCK, 2);
    if ( !open(XMLFILE, "> /usr/local/apache/qbconf/".$Fwmark_XML) )
    {
    	`/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/$Fwmark_XML`;
    	exit;
    }
    my $result=XMLout($fwmarkref);
    print XMLFILE $result;
    close XMLFILE;
    flock(XMLLOCK, 8);
    close XMLLOCK;
   #####################################################################################
   #
   # Save in XML End.
   #
   #####################################################################################
    
    `/usr/local/apache/qb/setuid/run cp -a /usr/local/apache/qbconf/$Iniroute_XML /usr/local/apache/active/$Iniroute_XML`;
    `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/$Iniroute_XML`;
    `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/active/$Iniroute_XML`;
    
    `/usr/local/apache/qb/setuid/run cp -a /usr/local/apache/qbconf/$Proute_XML /usr/local/apache/active/$Proute_XML`;
    `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/$Proute_XML`;
    `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/active/$Proute_XML`;
    
    `/usr/local/apache/qb/setuid/run cp -a /usr/local/apache/qbconf/$Fwmark_XML /usr/local/apache/active/$Fwmark_XML`;
    `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/$Fwmark_XML`;
    `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/active/$Fwmark_XML`;
    
#    if ( $enabled_or_not eq '1' ) { `/usr/local/apache/qb/setuid/run /bin/echo 020 > /tmp/fifo.qbserv`; }
#    elsif ( $enabled_or_not eq '0' ) { `/usr/local/apache/qb/setuid/run /bin/echo 021 > /tmp/fifo.qbserv`; }
#
