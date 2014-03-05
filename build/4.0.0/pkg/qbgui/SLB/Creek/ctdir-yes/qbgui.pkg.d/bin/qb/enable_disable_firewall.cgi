#!/usr/bin/perl

#require ("/usr/local/apache/qb/global.cgi");
require ("global.cgi");

print "Content-type:text/html\n\n";

use CGI;
use Data::Dumper;
use XML::Simple;

my $form = new CGI;
my $target_name=$form->param('name');
my $tmp_target_name='tmp_'.$target_name;
my $status=$form->param('status');
    
    #my $firewallref = XMLin($gPATH.'access.xml',forcearray=>1);    my $firewall_list = $firewallref->{access};
    my $accessref   = XMLin($gPATH.'access.xml',forcearray=>1);     my $access_access = $accessref->{access};
    my $ispref      = XMLin($gPATH."basic.xml",forcearray=>1);      my $isplist       = $ispref->{isp};
    my $zoneref     = XMLin($gPATH."zonecfg.xml",forcearray=>1);    my $zonelist      = $zoneref->{nat};
    my $hostref     = XMLin($gPATH."host.xml",forcearray=>1);       my $hostlist      = $hostref->{host};
    my $serviceref  = XMLin($gPATH.'service.xml',forcearray=>1);    my $servicelist   = $serviceref->{service};
    my $scheduleref = XMLin($gPATH.'schedule.xml',forcearray=>1);   my $schedulelist  = $scheduleref->{schedule};
    
	# Debug function    
	# `/usr/local/apache/qb/setuid/run /bin/echo "$target_name $status" > /tmp/garytest`;
    my $iptables_access = "/tmp/".$target_name;
    if ( !open(IPTABLES_ACCESS, ">$iptables_access") ) { print "open qosinit fail!!\n"; return; }

    foreach my $item (@$access_access)
    {
      if ( $item->{service} eq 'system' && $item->{service} eq 'system' ) { next; }
      if ( $item->{name} eq $target_name )
      {
        if 	( $status eq 'true'  ) 	{   $item->{dirty}='0';   }
        elsif 	( $status eq 'false' ) 	{   $item->{dirty}='1';   }
        
        #####################################################################################################
        ##
        ##    Start to process realtime iptables rule when press enable/disable checkbox
        ##
        #####################################################################################################
	my $allport;
	my @service_and_direction=split(/:/,$item->{service});
	my $type_of_service=$service_and_direction[0];         #service type
	my $direction=$service_and_direction[1];	       #rule direction "d" or "s"
	
	# begin search service port info
	foreach $service ( @$servicelist )
	{
	    if ( $service->{type} eq 'layer7' || $service->{type} eq 'system' ) { next; }
	    $portlist=$service->{port};
	    if ( $service->{title} eq $type_of_service )
	    {
	    	foreach my $port ( @$portlist )
	    	{
	    	    if ( $port->{protocol} eq 'system' ) { next; }
	    	    if ( $port->{value} eq '' ) { $allport = $port->{protocol};next; } 
	    	    $allport .= $port->{protocol}.':'.$port->{value}.',';
	    	}
	    }
	}
	
    	if ( $item->{source} eq 'all' && $item->{destination} eq 'all' ) {next;}
    	my $sourceip = ( $item->{source} eq 'all' ) ? ('0.0.0.0/0') : ($item->{source}) ;
    	my $destinationip = ( $item->{destination} eq 'all' ) ? ('0.0.0.0/0') : ($item->{destination}) ;
    	my $muti_source=0;
    	my $muti_dest=0;
    	my $dir_port;
    	my $had_schedule='0';
    	if ( $direction eq 's' ) { $dir_port='--sport'; }
    	else { $dir_port='--dport';; }
    	
    	my $action_allow = ( $item->{actiontype} eq 'Allow' ) ? ('ACCEPT'):('DROP');
    	
    	my @portinfo=split(/,/,$allport);
    	if ( $type_of_service eq 'others' ) { $portinfo[0]='1'; }
    	
    	foreach my $schedule ( @$schedulelist ) {   if ( $schedule->{schname} eq $item->{schedule} ) { $had_schedule='1'; }   }
    	
    	###############################################################################
    	#
    	##     if had use schedule object enter this condition
    	##
    	###############################################################################
    	if ( $had_schedule eq '1' )
    	{
		foreach my $schedule ( @$schedulelist )
    	  	{
    	    	    if ( $schedule->{schname} eq $item->{schedule} )
    	    	    {
    	    		my $scheduledays=$schedule->{subsch};
    	    		foreach my $scheduleday ( @$scheduledays )
    	    		{
    	    	    	    $scheduletime='-m time --timestart '.$scheduleday->{timestart}.' --timestop '.$scheduleday->{timestop}.' --weekdays '.$scheduleday->{days};
    	
    		    	    foreach my $protocolandport ( @portinfo )
    		    	    {
    	    			if ( $protocolandport eq '1' ) {  $protocol_parameter='';  }
    	    			else
    	    			{
	    		    	    my @protocolandport2=split(/:/,$protocolandport); # protocolandport2 array [0] is protocol , [1] is port number
	    
	    		    	    my $iptables_rule;
	    		    	    if ( $protocolandport2[1] eq '' ) { $protocol_parameter='-p '.$protocolandport2[0]; }
	    		    	    else { $protocol_parameter='-p '.$protocolandport2[0].' '.$dir_port.' '.$protocolandport2[1]; }
    	    			}
    	    			if ( grep(/host-/, $item->{source}) || grep(/host-/, $item->{destination}) ) 
    	    			{
    	    		    	    foreach my $host (@$hostlist)
    	    		    	    {
    	    	    			if ( $host->{hostname} eq $item->{source} )      { $sourceip=$host->{hostaddress}; 	$muti_source=1; }
    	    	    			if ( $host->{hostname} eq $item->{destination} ) { $destinationip=$host->{hostaddress}; $muti_dest=1; }
    	    		    	    }
    	    		    	    if ( $muti_source && !$muti_dest )
    	    		    	    {
    	    	    			my @splitsource=split(/,/, $sourceip);
    	    	    			foreach my $muti_sourceip ( @splitsource )
					{
    	    	    		    	    my $my_src_ip ;
    	    	        	    	    if( grep(/-/, $muti_sourceip) ){ $my_src_ip='-m iprange --src-range '.$muti_sourceip; }
    	    	        	    	    else { $my_src_ip='-s '.$muti_sourceip; }
    	     	        	    	    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT $my_src_ip -d $destinationip $protocol_parameter $scheduletime -j $action_allow \n";
    	    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT $my_src_ip -d $destinationip $protocol_parameter $scheduletime -j $action_allow \n";
    	    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD $my_src_ip -d $destinationip $protocol_parameter $scheduletime -j $action_allow \n";
    	    	    	
    	    	        	    	    if( grep(/-/, $muti_sourceip) ){ $my_src_ip='-m iprange --dst-range '.$muti_sourceip; }
    	    	        	    	    else { $my_src_ip='-d '.$muti_sourceip;}
    	     	        	    	    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT $my_src_ip -s $destinationip $protocol_parameter $scheduletime -j $action_allow \n";
    	    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT $my_src_ip -s $destinationip $protocol_parameter $scheduletime -j $action_allow \n";
    	    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD $my_src_ip -s $destinationip $protocol_parameter $scheduletime -j $action_allow \n";
    	    	    			}
	    		    	    }
    	    		    	    elsif ( !$muti_source && $muti_dest )
    	    		    	    {
    	    	    			my @splitdestination=split(/,/, $destinationip);
    	    	    			foreach my $muti_destip ( @splitdestination )
    	    	    			{
					    my $my_dest_ip;
					    if( grep(/-/, $muti_destip) ){ $my_dest_ip='-m iprange --dst-range '.$muti_destip; }
					    else { $my_dest_ip='-d '.$muti_destip; }
					    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT -s $sourceip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
					    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT -s $sourceip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
					    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD -s $sourceip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
    	    	    	
					    if( grep(/-/, $muti_destip) ){ $my_dest_ip='-m iprange --src-range '.$muti_destip; }
    	    	        	    	    else { $my_dest_ip='-s '.$muti_destip; }
    	    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT -d $sourceip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
    	    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT -d $sourceip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
					    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD -d $sourceip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
    	    	    			}
	    		    	    }
    	    		    	    else
    	    		    	    { 
    	    	    			my @splitsource=split(/,/, $sourceip);
    	    	    			my @splitdestination=split(/,/, $destinationip);

    	    	    			foreach my $muti_sourceip ( @splitsource )
    	    	    			{
    	    	    		    	    foreach my $muti_destip ( @splitdestination ) 
    	    	    		    	    {
    	    	    	    			my $my_src_ip, $my_dest_ip;
    	    	            			if( grep(/-/, $muti_sourceip) ) {   $my_src_ip='-m iprange --src-range '.$muti_sourceip;   }
    	    	            			else 				{   $my_src_ip='-s '.$muti_sourceip;   }
    	    	            			if( grep(/-/, $muti_destip) )   {   $my_dest_ip='-m iprange --dst-range '.$muti_destip;   }
    	    	            			else 				{   $my_dest_ip='-d '.$muti_destip;   }
    	    	            			
    	    		    			print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT $my_src_ip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
    	    		    			print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT $my_src_ip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
    	    		    			print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD $my_src_ip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
    	    		    
    	    	            			if( grep(/-/, $muti_sourceip) ) {   $my_src_ip='-m iprange --dst-range '.$muti_sourceip;   }
    	    	            			else 				{   $my_src_ip='-s '.$muti_sourceip;   }
    	    	            			if( grep(/-/, $muti_destip) )   {   $my_dest_ip='-m iprange --src-range '.$muti_destip;    }
    	    	            			else 				{   $my_dest_ip='-d '.$muti_destip;   }
    	    	            			
    	    		    			print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT $my_src_ip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
    	    		    			print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT $my_src_ip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
    	    		    			print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD $my_src_ip $my_dest_ip $protocol_parameter $scheduletime -j $action_allow \n";
    	    	        	    	    }
    	    	    			}
	    		    	    }
    	    			}
    	    			else
    	    			{
    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT -s $sourceip -d $destinationip $protocol_parameter $scheduletime -j $action_allow \n"; 
    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT -s $sourceip -d $destinationip $protocol_parameter $scheduletime -j $action_allow \n"; 
    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD -s $sourceip -d $destinationip $protocol_parameter $scheduletime -j $action_allow \n"; 
    	    	
    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT -d $sourceip -s $destinationip $protocol_parameter $scheduletime -j $action_allow \n"; 
    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT -d $sourceip -s $destinationip $protocol_parameter $scheduletime -j $action_allow \n"; 
    	    		    	    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD -d $sourceip -s $destinationip $protocol_parameter $scheduletime -j $action_allow \n"; 
    	    			}
    		    	    }			    # foreach my $protocolandport  @portinfo 		End
			}			    # foreach my $scheduleday  @$scheduledays  		End
    
    	   	     }				    # if  $schedule->{schname} eq $item->{schedule}  	End
    	  	}				    # foreach my $schedule ( @$schedulelist )		End
    	}
    	###############################################################################
    	##
    	##     if had use schedule = "All Week" enter this condition
    	##
    	###############################################################################
    	else
    	{
    		    foreach my $protocolandport ( @portinfo )
    		    {
    	    		if ( $protocolandport eq '1' )
    	    		{
    	    		    $protocol_parameter='';
    	    		}
    	    		else
    	    		{
	    		    my @protocolandport2=split(/:/,$protocolandport); # protocolandport2 array [0] is protocol , [1] is port number
	    
	    		    my $iptables_rule;
	    		    if ( $protocolandport2[1] eq '' ) { $protocol_parameter='-p '.$protocolandport2[0]; }
	    		    else { $protocol_parameter='-p '.$protocolandport2[0].' '.$dir_port.' '.$protocolandport2[1]; }
    	    		}
    	    		if ( grep(/host-/, $item->{source}) || grep(/host-/, $item->{destination}) ) 
    	    		{
    	    		    foreach my $host (@$hostlist)
    	    		    {
    	    	    		if ( $host->{hostname} eq $item->{source} )      { $sourceip=$host->{hostaddress}; 	$muti_source=1; }
    	    	    		if ( $host->{hostname} eq $item->{destination} ) { $destinationip=$host->{hostaddress}; $muti_dest=1; }
    	    		    }
    	    		    if ( $muti_source && !$muti_dest )
    	    		    {
    	    	    		my @splitsource=split(/,/, $sourceip);
    	    	    		foreach my $muti_sourceip ( @splitsource )
    	    	    	    	{
    	    	    		    my $my_src_ip ;
    	    	        	    if( grep(/-/, $muti_sourceip) ){ $my_src_ip='-m iprange --src-range '.$muti_sourceip; }
    	    	        	    else { $my_src_ip='-s '.$muti_sourceip; }
    	     	        	    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT $my_src_ip -d $destinationip $protocol_parameter -j $action_allow \n";
    	    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT $my_src_ip -d $destinationip $protocol_parameter -j $action_allow \n";
    	    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD $my_src_ip -d $destinationip $protocol_parameter -j $action_allow \n";
    	    	    	
    	    	        	    if( grep(/-/, $muti_sourceip) ){ $my_src_ip='-m iprange --dst-range '.$muti_sourceip; }
    	    	        	    else { $my_src_ip='-d '.$muti_sourceip;}
    	     	        	    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT $my_src_ip -s $destinationip $protocol_parameter -j $action_allow \n";
    	    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT $my_src_ip -s $destinationip $protocol_parameter -j $action_allow \n";
    	    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD $my_src_ip -s $destinationip $protocol_parameter -j $action_allow \n";
    	    	    		}
	    		    }
    	    		    elsif ( !$muti_source && $muti_dest )
    	    		    {
    	    	    		my @splitdestination=split(/,/, $destinationip);
    	    	    		foreach my $muti_destip ( @splitdestination )
    	    	    		{
    	    	        	    my $my_dest_ip;
    	    	        	    if( grep(/-/, $muti_destip) ){ $my_dest_ip='-m iprange --dst-range '.$muti_destip; }
    	    	        	    else { $my_dest_ip='-d '.$muti_destip; }
    	    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT -s $sourceip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT -s $sourceip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD -s $sourceip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    	    	
    	    	        	    if( grep(/-/, $muti_destip) ){ $my_dest_ip='-m iprange --src-range '.$muti_destip; }
    	    	        	    else { $my_dest_ip='-s '.$muti_destip; }
    	    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT -d $sourceip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT -d $sourceip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD -d $sourceip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    	    		}
	    		    }
    	    		    else
    	    		    { 
    	    	    		my @splitsource=split(/,/, $sourceip);
    	    	    		my @splitdestination=split(/,/, $destinationip);

    	    	    		foreach my $muti_sourceip ( @splitsource )
    	    	    		{
    	    	    		    foreach my $muti_destip ( @splitdestination ) 
    	    	    		    {
    	    	    	    		my $my_src_ip, $my_dest_ip;
    	    	            		if( grep(/-/, $muti_sourceip) ){ $my_src_ip='-m iprange --src-range '.$muti_sourceip; }
    	    	            		else { $my_src_ip='-s '.$muti_sourceip; }
    	    	            		if( grep(/-/, $muti_destip) ){ $my_dest_ip='-m iprange --dst-range '.$muti_destip; }
    	    	            		else { $my_dest_ip='-d '.$muti_destip; }
    	    		    		print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT $my_src_ip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    		    		print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT $my_src_ip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    		    		print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD $my_src_ip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    		    
    	    	            		if( grep(/-/, $muti_sourceip) ){ $my_src_ip='-m iprange --dst-range '.$muti_sourceip; }
    	    	            		else { $my_src_ip='-s '.$muti_sourceip;}
    	    	            		if( grep(/-/, $muti_destip) ){ $my_dest_ip='-m iprange --src-range '.$muti_destip; }
    	    	            		else { $my_dest_ip='-d '.$muti_destip; }
    	    		    		print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT $my_src_ip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    		    		print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT $my_src_ip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    		    		print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD $my_src_ip $my_dest_ip $protocol_parameter -j $action_allow \n";
    	    	        	    }
    	    	    		}
	    		    }
    	    		}
    	    		else
    	    		{
    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT -s $sourceip -d $destinationip $protocol_parameter -j $action_allow \n"; 
    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT -s $sourceip -d $destinationip $protocol_parameter -j $action_allow \n"; 
    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD -s $sourceip -d $destinationip $protocol_parameter -j $action_allow \n"; 
    	    	
    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A INPUT -d $sourceip -s $destinationip $protocol_parameter -j $action_allow \n"; 
    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A OUTPUT -d $sourceip -s $destinationip $protocol_parameter -j $action_allow \n"; 
    	    		    print IPTABLES_ACCESS qq "/sbin/iptables -A FORWARD -d $sourceip -s $destinationip $protocol_parameter -j $action_allow \n"; 
    	    		}
    		    }			    # foreach my $protocolandport  @portinfo 		End
	} 				    # foreach my $schedule  @$schedulelist   		End	schedule.xml
	
#####################################################################################################
      }
    }
    `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/access.xml`; 
    if ( !open(XMLLOCK, "> $gXMLLOCK") )
    {
        exit;
    }
    flock(XMLLOCK, 2);
    if ( !open(XMLFILE, "> /usr/local/apache/qbconf/access.xml") )
    {
        `/usr/local/apache/qb/setuid/run chmod 777 /usr/local/apache/qbconf/access.xml`; 
        exit;
    }
    my $result=XMLout($accessref);
    print XMLFILE $result;
    `/usr/local/apache/qb/setuid/run cp -a /usr/local/apache/qbconf/access.xml /usr/local/apache/active/access.xml`;
    close XMLFILE;
    flock(XMLLOCK, 8);
    close XMLLOCK;
   
#    print IPTABLES_ACCESS qq "\n \n";
    close(IPTABLES_ACCESS);
    chmod(0777, $iptables_access);
    
    &GetCookies('username');    my $username=$Cookies{username};
    my $local_time=localtime(time());
    
    if ( $status eq 'true' )
    {
    	`/usr/local/apache/qb/setuid/run /bin/cat /tmp/$target_name > /tmp/$tmp_target_name`;
    	`/usr/local/apache/qb/setuid/run /bin/cat /tmp/$tmp_target_name | sed 's/-A/-D/' > /tmp/$target_name`;
    	`/usr/local/apache/qb/setuid/run /bin/cat /tmp/$target_name | sed 's/\$/ >\\/dev\\/null 2>\\&1 /g' > /tmp/$tmp_target_name.1`;
    	`/usr/local/apache/qb/setuid/run /bin/cat /tmp/$tmp_target_name.1 > /tmp/$target_name`;
    	`/usr/local/apache/qb/setuid/run /bin/cat /tmp/$tmp_target_name >> /tmp/$target_name`;
    	
    	
    	`/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/$target_name`;
    	`/usr/local/apache/qb/setuid/run /tmp/$target_name`;
    	`/usr/local/apache/qb/setuid/run /bin/rm /tmp/$tmp_target_name /tmp/$target_name`;
    	
    	#############################
    	##
    	## Write in user.log
    	##
    	#############################
    	`/usr/local/apache/qb/setuid/run /bin/echo "$local_time $username Enabled $target_name" on Firewall page >> /tmp/user.log`;
    }
    elsif ( $status eq 'false' )
    {
    	`/usr/local/apache/qb/setuid/run /bin/cat /tmp/$target_name > /tmp/$tmp_target_name`;
    	`/usr/local/apache/qb/setuid/run /bin/cat /tmp/$tmp_target_name | sed 's/-A/-D/' > /tmp/$target_name`;
    	`/usr/local/apache/qb/setuid/run /bin/cat /tmp/$tmp_target_name | sed 's/-A/-D/' >> /tmp/$target_name`;
    	
    	`/usr/local/apache/qb/setuid/run /bin/cat /tmp/$target_name | sed 's/\$/ >\\/dev\\/null 2>\\&1 /g' > /tmp/$tmp_target_name`;
    	`/usr/local/apache/qb/setuid/run /bin/cat /tmp/$tmp_target_name > /tmp/$target_name`;
    	
    	`/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/$target_name`;
    	`/usr/local/apache/qb/setuid/run /tmp/$target_name`;
    	`/usr/local/apache/qb/setuid/run /bin/rm /tmp/$tmp_target_name /tmp/$target_name`;
    	
    	#############################
    	##
    	## Write in user.log
    	##
    	#############################
    	`/usr/local/apache/qb/setuid/run /bin/echo "$local_time $username Disabled $target_name" on Firewall page >> /tmp/user.log`;
    }
    
   
#
