#!/usr/bin/perl
use CGI;
use Data::Dumper;
require ("qbmod.cgi");

print "Content-type:text/html\n\n";

    my $interface=$ENV{'QUERY_STRING'};
    $interface=~s/interface=//;
    my @intname=split(/&/,$interface);
    my $action=$intname[2];
    $interface=$intname[0];
    $action=~s/action=//;
    
     
    my $Info_3G=XMLread($gACTIVEPATH."basic.xml");
    my $List_3G=$Info_3G->{isp};

    foreach $isp ( @$List_3G ) 
    {
       # if ( $isp->{alive} eq "0" && $isp->{flag_3g} eq "1" && $isp->{pppoeportdev} eq $interface ) 
       # {
       #     print qq (alive,);
       #     print qq ($interface,);
       #     my $imgsrc = ( $isp->{alive} ) ? ( 'alive.png' ) : ( 'dead.png' );
       #print qq ($imgsrc,);
       # }
        if ( $isp->{pppoeportdev} ne $interface || $isp->{flag_3g} ne "1" || $isp->{pppoeportdev} eq "" ) { next; }

#	runCommand(command=>'/usr/bin/killall ', params=>'-9 get3gsignal.sh');

        #=================================================================== 

	if ($action eq "signal")
	{
	    my $signal=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} signal));
            $signal=~s/\n//g;
            if ( $signal eq "99" ){ $signal="0"; }
            if ( $signal eq "100" ){ $signal=runCommand(command=>'cat', params=>qq(/tmp/Sierra_signal.$isp->{pppoeportdev})); }
            my $signalfree = 31 - $signal;
            my $usage_3g=int $signal/31*100;
            my $RSSI=113-($signal*2);
            
            print qq ($action,);
            print qq ($interface,);
	    print qq ($signal,);
	    print qq ($signalfree,);
	    print qq ($usage_3g,);
	    print qq ($RSSI,);
	}
	
        #===================================================================
         
	if ($action eq "isp")
	{
	    my $isp_3G=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} isp));
	    $isp_3G=~s/\n//g;
            if ( $isp_3G eq "100" ){ $isp_3G=runCommand(command=>'cat', params=>qq(/tmp/Sierra_isp.$isp->{pppoeportdev})); $isp_3G=~s/\n//g;}
            if($isp->{usbmodemtype} eq "H20"){
	      if ( $isp_3G eq "0" ){ $isp_3G="None"; }
              print qq ($action,);
              print qq ($interface,);
	      print qq ($isp_3G,);
	    }else{
	      %isphash = ("46601" =>"Far EasTone","46602" =>"Asia Pacific Telecom","46689" =>"Vibo Telecom","46692" =>"Chunghwa","46697" =>"TWN GSM" );
	      if ( $isp_3G eq "0" ){ $isp_3G="None"; }
	      if ( $isp_3G eq "2" ){ $isp_3G="None"; }
              print qq ($action,);
              print qq ($interface,);
	      print $isphash{$isp_3G}.',';
	    }
	}
	
        #===================================================================     
         
	if ($action eq "cell")
	{
	    my $cell_id=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} cell));
	    if ( $cell_id eq "" ){ $cell_id="None"; }
	    if($isp->{usbmodemtype} eq "H20"){
	    print qq ($action,);
	    print qq ($interface,);
	    print qq ($cell_id,);
		}else{
		@outact = split(',',$cell_id);
		print qq ($action,);
	    print qq ($interface,);
		$outact[3] =~s/ //g;
		$outact[3] =~s/\r\n//g;
	    print $outact[3].',';
		}
	}
	
        #===================================================================      

	if ($action eq "band")
	{
            my $band=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} band));
            if ( $band eq "" ){ $band="None"; }
			if($isp->{usbmodemtype} eq "H20"){
            print qq ($action,);
            print qq ($interface,);
			print qq ($band,);
			}else{
			@outact = split(',',$band);
			if ( $outact[1] eq "" ){ $outact[1]="None"; }
            print qq ($action,);
            print qq ($interface,);
			$outact[1] =~s/ //g;
			$outact[1] =~s/\r\n//g;
			if($outact[1] eq "5"){
			$outact[1] ="HSDPA";
			}elsif($outact[1] eq "4"){
			$outact[1] ="WCDMA";
			}elsif($outact[1] eq "3"){
			$outact[1] ="EDEG";
			}elsif($outact[1] eq "2"){
			$outact[1] ="GPRS";
			}
			print $outact[1].',';
			}
	}

        #===================================================================      

	if ($action eq "ecio" || $action eq "rscp")
	{
            my $eciorscp=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} eciorscp));
            my @tmp=split(' ',$eciorscp);
            my @tmp1=split(',',$tmp[0]);
            my $ecio=$tmp1[0];
            my $rscp=$tmp1[1];

            print qq ($action,);
            print qq ($interface,);
			if($isp->{usbmodemtype} eq "H20"){
			print qq (-$ecio dBm,);
			print qq (-$rscp dBm,);
			}else{
			print "N/A,N/A,";
			}
			
	}

        #===================================================================      

	if ($action eq "tx" || $action eq "rx")
	{
	    my $txrx=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} txrx));
	    my @temp=split(' ',$txrx);
	    my @temp1=split(',',$temp[0]);
		if($isp->{usbmodemtype} eq "H20"){
	     $tx=$temp1[0];
	     $rx=$temp1[1];
		}else{
		 $tx=hex($temp1[1]) / 1000;
	     $rx=hex($temp1[2]) / 1000;
		}
		

            print qq ($action,);
            print qq ($interface,);
	    print qq ($tx,);
	    print qq ($rx,);
	}
	
        #===================================================================      
#        my $tx=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} tx));

        #===================================================================      
#        my $rx=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} rx));

        #===================================================================      
        my $imgsrc = ( $isp->{alive} ) ? ( 'alive.png' ) : ( 'dead.png' );
	print qq ($imgsrc,);
	print qq ($action);

        
    }
