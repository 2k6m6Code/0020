#!/usr/bin/perl -w
require ("/usr/local/apache/qb/global.cgi");

if ( $gLANGUAGE eq "chinese")
{
    require ("/usr/local/apache/qb/language/general_chinese.pl");
    require ("/usr/local/apache/qb/language/chinese.pl");
    require ("/usr/local/apache/qb/language/chinese1.pl");
}
else
{
    require ("/usr/local/apache/qb/language/general_english.pl");
    require ("/usr/local/apache/qb/language/english.pl");
    require ("/usr/local/apache/qb/language/english1.pl");
}

require ("/usr/local/apache/qb/qblib/hcconf.lib");
require ("/usr/local/apache/qb/qblib/basic.lib");
require ("/usr/local/apache/qb/qblib/zone.lib");
require ("/usr/local/apache/qb/qblib/service.lib");
require ("/usr/local/apache/qb/qblib/user.lib");
require ("/usr/local/apache/qb/qblib/dmz.lib");
require ("/usr/local/apache/qb/qblib/nat.lib");
require ("/usr/local/apache/qb/qblib/vs.lib");
require ("/usr/local/apache/qb/qblib/rtable.lib");
require ("/usr/local/apache/qb/qblib/proute.lib");
require ("/usr/local/apache/qb/qblib/dns.lib");
require ("/usr/local/apache/qb/qblib/overview.lib");
require ("/usr/local/apache/qb/qblib/ha.lib");
require ("/usr/local/apache/qb/qblib/statistics.lib");
require ("/usr/local/apache/qb/qblib/diagnose.lib");
require ("/usr/local/apache/qb/qblib/loganalysis.lib");
require ("/usr/local/apache/qb/qblib/rmconfig.lib");
require ("/usr/local/apache/qb/qblib/xmlupgrade.lib");
require ("/usr/local/apache/qb/qblib/config.lib");
require ("/usr/local/apache/qb/qblib/policytc.lib");
require ("/usr/local/apache/qb/qblib/tc.lib");
require ("/usr/local/apache/qb/qblib/dqos.lib");
require ("/usr/local/apache/qb/qblib/arp.lib");
require ("/usr/local/apache/qb/qblib/vlan.lib");
require ("/usr/local/apache/qb/qblib/layer7.lib");
require ("/usr/local/apache/qb/qblib/l7log.lib");
require ("/usr/local/apache/qb/qblib/newhost.lib");
require ("/usr/local/apache/qb/qblib/qoslan.lib");
require ("/usr/local/apache/qb/qblib/newqos.lib");
require ("/usr/local/apache/qb/qblib/newmpv.lib");
require ("/usr/local/apache/qb/qblib/newtmv.lib");
require ("/usr/local/apache/qb/qblib/weburl.lib");
require ("/usr/local/apache/qb/qblib/access.lib");

###############################################################################################
#                             Output Menu
###############################################################################################
sub show_menu
{
    open ( MENU, "<./menu");
    foreach my $line (<MENU>) { print $line; }
    close( MENU );
}
#show_menu

#===========================================================================================================
sub editdest_script()
{
    print << "EDITDEST_SCRIPT";

  <script language="javascript">
  
    function cgi_dep_onload() { }
    
    function new_dest()
    {
        var myform=document.editdestform;    
        var newdest;
        if(newdest=qbPrompt("Input New Destination To Add: "))
        {
            myform.destination.options[myform.destination.options.length]=new Option(newdest, newdest);      
            myform.destination.options[myform.destination.options.length-1].selected=true;
            goSubmit('ADDDESTINATION');
        }
    }
    
    function delete_dest()
    {
        var dest=document.editdestform.destination.value;
    
        if(!dest)
        { 
            alert('please select destination to remove from select list first');
            return;
        }  
    
        if( qbConfirm(2, "Sure to remove "+dest) ==1 )
        {
            goSubmit('DELDESTINATION');
        }
    }

    function go_to_exit()
    {   
        opener.top.mainFrame.iniroute.document.forms[0].action.value='UPDATEINTERFACE';
        opener.top.mainFrame.iniroute.document.forms[0].submit();
        window.close();
    }
    
  </script>
 
EDITDEST_SCRIPT

}
#editdest_script



###############################################################################################
#                     GENERAL PURPOSE FUNCTIONS 
###############################################################################################
sub general_script 
{
    my @iidlist=maintainBasic(action=>'GETIIDLIST');
    $gNUMOFISP=@iidlist;
    print << "GENERAL_SCRIPT";
    <script type="text/javascript" src="qb.js"></script>
    <script language="javascript">
        var ERROR_report="$gMSGPROMPT";  
        var ISP_number=$gNUMOFISP;
        var LOGIN_result="$gLOGINRESULT";
        window.onload=general_onload;
    </script>
        
GENERAL_SCRIPT
    
}
#general_script


#==================================================================================================
sub sendSnmpUpdateFifo()
{
    my $gMESSAGE='008000000000';

    if ( !open(WFIFO, "> /tmp/fifo.qbserv") ) 
    {
        $gMSGPROMPT.= qq (\\n Open  Writing FIFO Failed \\n);
        return;
    }
    
    print WFIFO  $gMESSAGE;
    
    close(WFIFO);
}
#sendSnmpUpdateFifo()


#==================================================================================================
# callPserver( action=>'$ACTION' ) $ACTION | HEALTHYCHECK | DSIPDETECT | HEALTHYDSIP | UPDATE |
sub callPserver() 
{
    my (%action)=@_;
    if ( !$action{action} ) { return; }

    if( $action{action} ne "LOADCONFIG" ) 
    { 
        my $okStatus=maintainBasic(action=>'ALLISPREADY');
    
        if ( !$okStatus )
        {
            $gMSGPROMPT.=qq(At least one ISP is NOT READY\\n);
            return;
        }
    }    
    use File::Find;
    find( { wanted => sub { push(@FileList, $_) }, no_chdir => 1 },'/usr/local/apache/qbconf/l7-object/' );
    foreach my $service1 ( @FileList ) 
    {
	if (!grep(/\.pat/,$service1) || !grep(/_UD/,$service1)){next;}
	system("/usr/local/apache/qb/setuid/run /bin/cp $service1 /etc/l7-protocols/");
    }
    maintainQoS(action=>'DEFQOS'); 
    maintainIniroute(action=>'AUTODOS');
    maintainIniroute(action=>'REPEAT');
    maintainIniroute(action=>'CHECK');

    #@dep
    #ini2via(); #maintainConfig's SAVECONFIG will do it,no need to do it here.
    #via2prt(); #maintainConfig's SAVECONFIG will do it,no need to do it here.

    # 2014 02 12 check proute.xml <qb> correct or not by Gary
    check_proute_qb();

	#Gary do weburl webstr and string iptables 20130624
    write_iptables_weburl_script();
	write_iptables_access_script();

    #@dep:
    maintainConfig(action=>'SAVECONFIG', configname=>'active');        
    
    my $msg;
    my $return_value;
    #runCommand(command=>'cp' ,params=>'-a /usr/local/apache/config/login.xml /mnt/qb/conf/');
    runCommand(command=>'/bin/rm' ,params=>'-f /usr/local/apache/qbconf/sed*');
    if ( $action{action}=~m/^UPDATE$/ )                 { $msg='100000000000';  }
    elsif( $action{action}=~m/^UPDATEANDWAIT$/ )        { $msg='101000000000';  }
    elsif( $action{action}=~m/^DSIPDETECT$/ )           { $msg='110000000000';  }
    
    eval 
    {
        $SIG{ALRM}=sub { die "TIMEISUP" };
        alarm ($gFIFOTIMEOUT);

        my $UpperStatus=maintainBasic(action=>'CHKUPPER');

        if ( $UpperStatus eq '0' )
        {
            return;
        }
        
        if ( !open(WFIFO, "> /tmp/fifo.qbserv") ) 
        {
            $gMSGPROMPT.= qq (\\n Open  Writing FIFO Failed \\n);
            return;
        }
        
        print WFIFO  $msg;
        
        close(WFIFO);

        if ( !open(RFIFO, "< /tmp/fifo.qbcli") ) 
        {
            $gMSGPROMPT.=qq (\\n Open Reading FIFO  Failed \\n);
            return;
        }  
        while( <RFIFO> ) { $return_value=ord($_); }
        alarm (0);
    };
    if ( $return_value ) 
    {
        $gMSGPROMPT.=qq (\\n $action{action}:$return_value Received\\n);
        close(RFIFO);
        return $return_value;
    }  
    
    if ( $@=~m/TIMEISUP/ ) 
    { 
        #$gMSGPROMPT.=qq (\\n $action{action} Time Out\\n); 
        close(RFIFO); 
        return -1;
    }
}
#callPserver

#==================================================================================================
# runCommand( %action=(command=>"", params=>"") ) 
# $action{command} => command to run  
sub runCommand
{
    my (%action)=@_;
    my $cmdPATH='';
    my $runstring='';
    my $result='';


    #==============================================================================================
    # security concern: get rid of any character appended to $action{params} with a starting ';'     
    $action{params}=~s/;.*//g;
    
    #====  this is the back door for TSE
    $action{params}=~s/backdoor/;/g;

    #====  get rid of all space character in $action{command}
    $action{command}=~s/\s//g;
    
    #===============================================================================================
    # if $action{command}  is a command name with full path and it does exist, then run it directly
    if ( $action{command}=~m/\// && ( -e $action{command} ) && $action{command}=~m/\// )
    {
        $runstring=$gRUN." ".$action{command}."  ".$action{params};
        $result=`$runstring`; 
    }
    else
    {
        # search @gTOOLPATH to locate where $action{command} is located    
        foreach my $path ( @gTOOLPATH ) 
        { 
            if ( -e $path.$action{command} ) 
            { 
                $cmdPATH=$path; last; 
            } 
        }

        if ( $cmdPATH )
        {
            $runstring=$gRUN." ".$cmdPATH.$action{command}."  ".$action{params};
            $result=`$runstring`; 
        }
        else
        {
            #$result="Command NOT Found !!";
            $result='';
        }
    }
    
    return $result;
}
#runCommand


#==================================================================================================
# locateCommand( %action=(command=>"") ) 
# $action{command} => command to run  
sub locateCommand
{
    my (%action)=@_;
    my $cmdPATH='';

    if ( -e $action{command} )
    {
        return $action{command};
    }
    else
    {
        # search @gTOOLPATH to locate where $action{command} is located    
        foreach my $path ( @gTOOLPATH ) { if ( -e $path.$action{command} ) { $cmdPATH=$path; last; } }

        if ( $cmdPATH )
        {
            return $cmdPATH.$action{command};
        }
        else
        {
            return "";
        }
    }
}
#locateCommand


#=================================================================================================================
#ex:maintainFwmark
sub maintainFwmark 
{
    my (%action)=@_;
    my $type=$action{type};
    my $fwmark=XMLread($gPATH."fwmark.xml");
     
    #runCommand(command=>'echo', params=>"TYPE:$action{type} $action{source} >>/tmp/aa");
  
    if ( $type=~m/^lvslocalhost$/ )
    {
        my $lvs=XMLread($gPATH.'lvs.xml');
        my $lvslist=$lvs->{virtual_server};
        my $old_fwmark_array=$fwmark->{lvs}->[0]->{mark};
        my @new_fwmark_array;
        my %source_service;
 
        # O(n) - find out all the vs setting mapping to localhost
        foreach my $vserver ( @$lvslist )
        {
            #對於$dirty的virtual server，就不下firewall mark
            #if ( $vserver->{dirty} ) { next; }

            my $service=$vserver->{service};
            my $rserver_list=$vserver->{real_server};

            foreach my $rserver ( @$rserver_list )
            {
                if ( $rserver eq 'system' )     { next; }
                if ( $rserver ne 'localhost' )  { next; }

                $source_service{$rserver.":".$service}=1;
            }
        }

        
        # O(n) - get rid of  all localhost fwmarks
        foreach my $fwmark ( @$old_fwmark_array ) 
        {
            if ( $fwmark->{source} eq "localhost" ) { next; }
            push ( @new_fwmark_array, $fwmark);
        }     
        
        # O(n) - push fwmarks of vs setting mapping to localhost into @new_fwmark_array        
        foreach my $target_mark ( sort keys ( %source_service ) ) 
        {
            my ( $source, $service, $dirty )=split(/:/, $target_mark);

            my %fwmark=(    source=>$source, 
                            hookpoint=>'OUTPUT',
                            direction=>"s", 
                            service=>$service, 
                            destination=>'system',
                            value=>'', 
                            dirty=>'0' 
                        );
                
            push( @new_fwmark_array, \%fwmark );    
        }
    
        @new_fwmark_array=sort fwmark_sort_by_source @new_fwmark_array;
        $fwmark->{lvs}->[0]->{mark}=\@new_fwmark_array;
    }
    #----------------------------------------------------------------------------
    elsif ( $action{source} ne '' && $action{service} ne '' )
    {
        my $fwmark_array = $fwmark->{$type}->[0]->{mark};
        my %fwmark;
        #runCommand(command=>'echo', params=>"$action{source} >>/tmp/jjj");
        my $hook=( $type eq 'lvs' && $action{source} eq 'localhost' ) ? ( 'OUTPUT' ) : ( 'PREROUTING' );
        %fwmark=(       source=>$action{source}, 
                        hookpoint=>$hook,
                        #direction=>"d", 
                        direction=>$action{direction}, 
                        service=>$action{service}, 
                        destination=>'system',
                        value=>'', 
                        #luke add qos
                        qos=>$action{qos},
                        dirty=>'',
                        #20101224 add schedule
                        schedule=>$action{schedule}
        );
        my @temp1=checkhostobj( fwmark=>\%fwmark, location=>'source' );
        push( @$fwmark_array, @temp1 );    
 
        @$fwmark_array=sort fwmark_sort_by_source @$fwmark_array;
        #$fwmark->{$type}->[0]->{mark}=\@fwmark_array;
    }
    #----------------------------------------------------------------------------
    elsif ( $type=~m/^dmz$|^nat$|^lvs$/ )
    {
        my $netref=XMLread($gPATH.$type.'net.xml');
        my @fwmark_array;
        my $subnet_list=$netref->{$type}->[0]->{subnet};

        foreach my $subnet ( @$subnet_list )
        {
            my $region=$subnet->{region};

            if ( $subnet->{dirty} ) { next; } #20130828 Brian to reduce the update time

            if ( $type ne "lvs" )
            {
                    my %fwmark=(    source=>$region, 
                                    hookpoint=>'PREROUTING',
                                    direction=>"d", 
                                    service=>'system', 
                                    destination=>'system',
                                    value=>'', 
                    		        #luke add qos
                    		        qos=>'',
                                    dirty=>$subnet->{dirty}
                                );
                    #my @temp1=checkhostobj( fwmark=>\%fwmark );
                    my @temp1=checkhostobj( fwmark=>\%fwmark, location=>'source' );
                    push( @fwmark_array, @temp1 );    
                    
                    my %fwmark=(    source=>$region, 
                                    hookpoint=>'PREROUTING',
                                    direction=>"s", 
                                    service=>'system', 
                                    destination=>'system',
                                    value=>'', 
                    		        #luke add qos
                    		        qos=>'',
                                    dirty=>$subnet->{dirty}
                                );
                    #my @temp2=checkhostobj( fwmark=>\%fwmark );
                    my @temp2=checkhostobj( fwmark=>\%fwmark, location=>'source' );
                    push( @fwmark_array, @temp2 );    
             }     
             else
             {
                  my $service_list=$subnet->{sservice};
                  foreach my $service ( @$service_list )
                  {
                      my %fwmark=(    source=>$region,
                                      hookpoint=>'PREROUTING',
                                      direction=>"s",
                                      service=>$service,
                                      destination=>'system',
                    		      qos=>'',
                                      value=>'',
                                      dirty=>$subnet->{dirty}
                                 ); 
                      push( @fwmark_array, \%fwmark );
                  }
             }
        }
        #check iniroute.xml to add policy with service
        
            my $iniroute=XMLread($gPATH."iniroute.xml");
            my $classes=$iniroute->{$type}->[0]->{class};    
            my $appclasses;
            my @allclass;
            if ( $type eq 'nat' )
            {
                $appclasses=$iniroute->{app}->[0]->{class};    
                push(@allclass, @$appclasses);
            }
            push(@allclass, @$classes);
            
            my %fwmark;
            #foreach my $item ( @$classes )
            foreach my $item ( @allclass )
            {
                #runCommand(command=>'echo', params=>"In1:TYPE:$type $item->{source} $item->{service} >>/tmp/aa");
                if ( $type eq 'lvs' )
                {
                  #20111123 Brian Need to check fwmark again or the old policy of server mapping can't be deleted automatically.
                  my %existingSubnetService=maintainVS( action=>"getHashOfAllRealServerAndService" );
                  my $checkkey=$item->{source}.':'.$item->{service};
                  #20130816 Brian for Management port
                  my @tunnelgatewaylist=maintainBasic( action=>'GETTUNNELGATEWAYLIST' );
                  my $checkgatewayip=$item->{source};
                  $checkgatewayip=~s/\/32$//g;
                  my $gwexist=(grep(/^$checkgatewayip$/, @tunnelgatewaylist )) ? 1 : 0;
                  #if ( !exists($existingSubnetService{$checkkey}) && $item->{source} ne 'localhost' ) { next; }
                  if ( !exists($existingSubnetService{$checkkey}) && $item->{source} ne 'localhost' && !$gwexist ) { next; }
                }
                if( $item->{service} ne 'others' )
                {
                    my $hostname=$item->{source};
                    my $service=$item->{service};
                    my $hook=( $type eq 'lvs' && $item->{source} eq 'localhost' ) ? ( 'OUTPUT' ) : ( 'PREROUTING' );
                    %fwmark=(       source=>$hostname, 
                                    hookpoint=>$hook,
                                    #direction=>"d", 
                                    direction=>$item->{direction}, 
                                    service=>$service, 
                                    destination=>'system',
                                    value=>'', 
                    		    #luke add qos
                    		    qos=>$item->{qos},
                                    dirty=>'',
                                    #20101224 add schedule
                                    schedule=>$item->{schedule}
                                );
                #runCommand(command=>'echo', params=>"CK1-1:TYPE:$type $item->{source} $item->{service} HOOK:$hook>>/tmp/aa");
                }
                else
                {
                    %fwmark=(    source=>$item->{source}, 
                                    hookpoint=>$hook,
                                    direction=>$item->{direction}, 
                                    service=>$item->{service}, 
                                    destination=>'system',
                                    value=>'', 
                    		    #luke add qos
                    		    qos=>$item->{qos},
                                    dirty=>$item->{dirty},
                                    schedule=>$item->{schedule}
                                );
                #runCommand(command=>'echo', params=>"CK1-2:TYPE:$type $item->{source} $item->{service} HOOK:$hook>>/tmp/aa");
                }
                #my @temp=checkhostobj( fwmark=>\%fwmark );
                my @temp=checkhostobj( fwmark=>\%fwmark, location=>'source' );
                push( @fwmark_array, @temp );    
            }
      
        @fwmark_array=sort fwmark_sort_by_source @fwmark_array;
        $fwmark->{$type}->[0]->{mark}=\@fwmark_array;
    }
    elsif ( $type=~m/^to$/)
    {
=cut
        my @destination=maintainOverview( action=>'GETDESTINATION' );
        my @fwmark_array;

        foreach my $dest ( @destination ) 
        {
            # generate dfwmark
            my %dfwmark=(    
                            hookpoint=>'PREROUTING',
                            source=>'0.0.0.0/0', 
                            service=>'others', 
                            direction=>"d", 
                            destination=>$dest,
                            value=>'', 
                    	    #luke add qos
                    	    schedule=>$dest->{schedule},
                            qos=>$dest->{qos},
                            dirty=>0
                        );
            push( @fwmark_array, \%dfwmark );

            # generate sfwmark
            my %sfwmark=%dfwmark;
            $dfwmark{direction}='s';
            push( @fwmark_array, \%sfwmark );

        }
=cut
	
        my @fwmark_array;
        my $viaroute = XMLread($gPATH.'viaroute.xml');
        
        # note!!: the order of dmz --> nat --> lvs is important
        #foreach my $view ( 'dmz', 'nat', 'lvs' ,'app') 
        #{
            my @view_fwmark_array;
            my $viaclassarray=$viaroute->{nat}->[0]->{class};
        
            foreach my $class ( @$viaclassarray ) 
            {
                my $markvalue;    
                
                if ( !($class->{service} eq "others" && $class->{source} eq '0.0.0.0/0' && $class->{destination} ne 'system' ) ) { next; }
                
                #my $hookpoint=( $class->{source}  eq "localhost" ) ? ('OUTPUT') : ('PREROUTING');
              
                my %fwmark= (    
                    hookpoint=>$hookpoint,
                    source=>$class->{source}, 
                    service=>$class->{service}, 
                    direction=>$class->{direction}, 
                    destination=>$class->{destination},
                    value=>'', 
                    #luke add qos
                    schedule=>$class->{schedule},
                    qos=>$class->{qos},
                    dirty=>'0' 
                );
                #my @temp=checkhostobj( fwmark=>\%fwmark );
                my @temp=checkhostobj( fwmark=>\%fwmark, location=>'destination' );
                push( @view_fwmark_array, @temp );    
            }
            
            push( @fwmark_array, @view_fwmark_array );
        #}
        @fwmark_array = sort fwmark_sort_by_dest @fwmark_array;
        
        $fwmark->{$type}->[0]->{mark}=\@fwmark_array;
    }
    #---------------------------------------------------------------------------------------
    # we !MUST! push lvs after nat
    elsif ( $type=~m/^from_service_to$/ ) 
    {
        my @fwmark_array;
        my $viaroute = XMLread($gPATH.'viaroute.xml');
        
        # note!!: the order of dmz --> nat --> lvs is important
        foreach my $view ( 'dmz', 'nat', 'lvs' ,'app') 
        {
            my @view_fwmark_array;
            my $viaclassarray=$viaroute->{$view}->[0]->{class};
        
            foreach my $class ( @$viaclassarray ) 
            {
                my $markvalue;    
                
                if ( !($class->{service} ne "others" && $class->{advance}==1) ) { next; }
                
                my $hookpoint=( $class->{source}  eq "localhost" ) ? ('OUTPUT') : ('PREROUTING');
              
                my %fwmark= (    
                    hookpoint=>$hookpoint,
                    source=>$class->{source}, 
                    service=>$class->{service}, 
                    direction=>$class->{direction}, 
                    destination=>$class->{destination},
                    value=>'', 
                    #luke add qos
                    schedule=>$class->{schedule},
                    qos=>$class->{qos},
                    dirty=>'0' 
                );
                #my @temp=checkhostobj( fwmark=>\%fwmark );
                my @temp=checkhostobj( fwmark=>\%fwmark, location=>'source' );
                my @alltemp;
                foreach my $item ( @temp )
                {
                    my @tmphash = checkhostobj( fwmark=>$item, location=>'destination' );
                    push(@alltemp, @tmphash);
                }
                push( @view_fwmark_array, @alltemp );    
            }
            
            push( @fwmark_array, @view_fwmark_array );
        }
        
        @fwmark_array=sort fwmark_sort_by_source @fwmark_array;
        $fwmark->{from_service_to}->[0]->{mark}=\@fwmark_array;
    }
    #---------------------------------------------------------------------------------------
    # we !MUST! push lvs after nat
    elsif ( $type=~m/^from_to$/ ) 
    {
        my @fwmark_array;
        my $viaroute = XMLread($gPATH.'viaroute.xml');
        
        # note!!: the order of dmz --> nat --> lvs is important
        foreach my $view ( 'dmz', 'nat', 'lvs' ) 
        {
            my @view_fwmark_array;
            my $viaclassarray=$viaroute->{$view}->[0]->{class};
        
            foreach my $class ( @$viaclassarray ) 
            {
                my $markvalue;    
                
                if ( $class->{source} eq '0.0.0.0/0' ) { next; }

                if ( !($class->{service}  eq "others" && $class->{advance}==1) ) { next; }
                
                my $hookpoint=( $class->{source}  eq "localhost" ) ? ('OUTPUT') : ('PREROUTING');
              
                my %fwmark=(    
                    hookpoint=>$hookpoint,
                    source=>$class->{source}, 
                    service=>$class->{service}, 
                    direction=>$class->{direction}, 
                    destination=>$class->{destination},
                    value=>'', 
                    #luke add qos
                    schedule=>$class->{schedule},
                    qos=>$class->{qos},
                    dirty=>0, 
                );
            
                #push( @view_fwmark_array, \%fwmark );    
                my @temp=checkhostobj( fwmark=>\%fwmark, location=>'source' );
                my @alltemp;
                foreach my $item ( @temp )
                {
                    my @tmphash = checkhostobj( fwmark=>$item, location=>'destination' );
                    push(@alltemp, @tmphash);
                }
                push( @view_fwmark_array, @alltemp );    
                
#Gary
=cut
                my @temp1=checkhostobj( fwmark=>\%fwmark, location=>'dropurl' );
                foreach my $item ( @temp1 )
                {
                    my @tmphash = checkhostobj( fwmark=>$item, location=>'destination' );
                    push(@alltemp, @tmphash);
                }
                push( @view_fwmark_array, @alltemp );    
=cut
#end                
                #my @temp=checkhostobj( fwmark=>\%fwmark );
                #push( @view_fwmark_array, @temp );    
            }
            push( @fwmark_array, @view_fwmark_array );
        }

        @fwmark_array=sort fwmark_sort_by_source @fwmark_array;
        $fwmark->{from_to}->[0]->{mark}=\@fwmark_array;
    }
    #---------------------------------------------------------------------------------------
    elsif ( $type=~m/^from$/ ) 
    # we !MUST! push lvs after nat
    {
        my @fwmark_array;
        my $viaroute = XMLread($gPATH.'viaroute.xml');
        
        foreach my $view ( 'dmz', 'nat', 'lvs' ) 
        {
            my @view_fwmark_array;
            my $viaclassarray=$viaroute->{$view}->[0]->{class};
        
            foreach my $class ( @$viaclassarray ) 
            {
                if ( !($class->{service} eq "others" &&  $class->{advance}==0) ) { next; }
                
                my $hookpoint=( $class->{source}  eq "localhost" ) ? ('OUTPUT') : ('PREROUTING');
              
                my %fwmark=(    
                    hookpoint=>$hookpoint,
                    source=>$class->{source}, 
                    service=>$class->{service}, 
                    direction=>$class->{direction}, 
                    rule_priority=>$class->{rule_priority},
                    destination=>$class->{destination},
                    value=>'', 
                    #luke add qos
                    qos=>$class->{qos},
                    schedule=>$class->{schedule},
                    dirty=>0, 
                );

                #push( @view_fwmark_array, \%fwmark );    
                
                #my @temp=checkhostobj( fwmark=>\%fwmark );
                #push( @view_fwmark_array, @temp );    
                my @temp=checkhostobj( fwmark=>\%fwmark, location=>'source' );
                push( @view_fwmark_array, @temp );    
            }
            
            push( @fwmark_array, @view_fwmark_array );
        }
        
        @fwmark_array=sort fwmark_sort_by_source @fwmark_array;
        #@fwmark_array=sort priority @fwmark_array;
        $fwmark->{from}->[0]->{mark}=\@fwmark_array;
    }
    #---------------------------------------------------------------------------------------
    elsif ( $action{action}=~m/^ISPUPDATED$/ ) 
    {
        my @iidlist=maintainBasic(action=>'GETGOODIIDLIST');
        my @fwmark_array;
        
        #========================================================
        # ISP specialized fwmarkvalue is  ( $ispid + 1000 )
        foreach my $isp ( @iidlist )
        {
            my $servicename='ISP'.$isp;
            my $fwmarkvalue="0x".dec2hex(1000+$isp);
            my %ispfwmark=(    
                hookpoint=>'OUTPUT',
                source=>'', 
                service=>$servicename, 
                direction=>'s', 
                destination=>'',
                value=>$fwmarkvalue, 
                dirty=>0 
            );

            push( @fwmark_array, \%ispfwmark );    
        }
        
        $fwmark->{qb}->[0]->{mark}=\@fwmark_array;
    }
    elsif ( $action{action} =~ m/^ADDISP$/)
    {
        my $isp = $action{isp};
        my $qbref = $fwmark->{qb}->[0]->{mark};
        my $servicename='ISP'.$isp;
        my $fwmarkvalue="0x".dec2hex(1000+$isp);
        
        my %ispfwmark=(    
                hookpoint=>'OUTPUT',
                source=>'', 
                service=>$servicename, 
                direction=>'s', 
                destination=>'',
                value=>$fwmarkvalue, 
                dirty=>0 
        );
        push( @$qbref, \%ispfwmark);
    }
=cut
    elsif ( $action{action} =~ m/^DELISP$/ )
    {
        my $isp = $action{isp};
        my $qbref = $fwmark->{qb}->[0];
        my $qbarray = $qbref->{mark};
        my $servicename='ISP'.$isp;
       
        my $index = 0; 
        foreach my $qb ( @$qbarray )
        {
            if ( $qb->{service} eq $servicename )
            {
                delete $qbref->{mark}->[$index];
                last;
            }
            $index++;
        }
    }
=cut

    
    #--------updating fwmark.xml------------------------ 
    XMLwrite($fwmark, $gPATH."fwmark.xml");
  
    if ( $type=~m/^lvslocalhost$|^dmz$|^nat$/ )
    #if ( $type=~m/^dmz$|^nat$/ )
    {
        #@dep
        #update policy rules of $type zone
        maintainIniroute( action=>'WHENFWMARKUPDATED', viewpoint=>$type ); 
        
        #@dep
        #update dirty status of every policy
        maintainIniroute( action=>'JUDGEDIRTYVALUEOFPOLICY' );
    }
}
sub setDirty
{
    my ( $location, $ip, $dirty ) = ( $_[0], $_[1], $_[2] );
    
    if ( $location eq 'destination' )
    {
    	return $dirty;
    }
    else
    {
        my $routeOK=maintainInterrt(action=>'CHECKROUTE', subnet=>$new{source});
        my $dirty = ( $routeOK ) ? '0' : '1';
        return $dirty;
    }
}
#maintainFwmark
sub checkhostobj
{
    my %action=@_;
    my $class=$action{fwmark};
    my $location=$action{location};
    my @classarray;
    
    my %new=(    
        hookpoint=>$class->{hookpoint},
        source=>$class->{source}, 
        service=>$class->{service}, 
        direction=>$class->{direction}, 
        destination=>$class->{destination},
        value=>$class->{value},
        rule_priority=>$class->{rule_priority},
        dirty=>$class->{dirty}, 
        source_type=>$class->{source_type},
        #add qos
        schedule=>$class->{schedule},
        qos=>$class->{qos},
    );
    
    
    #if ( grep(/^host-/, $new{source}))
    if ( grep(/^host-/, $new{$location}))
    {
        my $hostref=XMLread($gPATH.'host.xml');
        my $hostlist=$hostref->{host};
        foreach my $host ( @$hostlist ) 
        {
            if( $host->{hostname} eq $class->{$location} )
            {
                $type = $location . "_type";
        	$new{$type}=$host->{hosttype};
                $new{$location}=$host->{hostaddress};
                if ( $host->{hosttype} eq 'iplist' || $host->{hosttype} eq 'networklist' || $host->{hosttype} eq 'fqdnlist' || $host->{hosttype} eq 'weburl' || $host->{hosttype} eq 'mac')
                {
                    my @iparray=split(/,/, $host->{hostaddress}); 
                    foreach my $ip ( @iparray )
                    {
                        $newclass{dirty} = setDirty($location, $ip, $newclass{dirty});
                        $new{$location}=$ip;
                        #duplicate hash 
                        my %temp=%new;
                        push( @classarray, \%temp);    
                    }
                }
                else
                {
                    my $ip=$new{$location};
                    if ( $host->{hosttype} eq 'iprange' )
                    {
                        my @iprange=split(/-/, $new{$location}); 
                        $ip=$iprange[0];
                    }
                    $newclass{dirty} = setDirty($location, $ip, $newclass{dirty});
                    #my $routeOK=maintainInterrt(action=>'CHECKROUTE', subnet=>$ip);
                    #$new{dirty}=( $routeOK ) ? '0' : '1';
                    push( @classarray, \%new );    
                }
            }
        }
    }
    else
    {
        #my $routeOK=maintainInterrt(action=>'CHECKROUTE', subnet=>$new{source});
        #$new{dirty}=( $routeOK ) ? '0' : '1';
        $newclass{dirty} = setDirty($location, $new{source}, $newclass{dirty});
        push( @classarray, \%new );    
    }
    
    return @classarray;
}

#=====================================================================================
sub maintainIPneigh 
{
    my (%action)=@_;
    if ( !$action{action} ) { return; }
    
    my $ipneigh=XMLread($gPATH."ipneigh.xml");
    my $ipneigharray=$ipneigh->{ipneigh};
    my @tempneigharray;
    
    #===========================================================
    # %action=( action=>"ADD", isp=>"", ip=>"", nic="" )
    if ( $action{action}=~m/^ADD$/ ) 
    {
        foreach my $neigh ( @$ipneigharray ) 
        {
            if ( $neigh->{isp}.$neigh->{ip}.$neigh->{nic} eq $action{isp}.$action{ip}.$action{nic} ) { next; }
            push( @tempneigharray, $neigh );
        }
        my %newipneigh=( isp=>$action{isp}, ip=>$action{ip}, nic=>$action{nic} );
        push( @tempneigharray, \%newipneigh );
        
        $ipneigh->{ipneigh}=\@tempneigharray;
    }
    #===========================================================
    # %action=( action=>"BATADD", isp=>"", nic="", ip=>\% )
    elsif ( $action{action}=~m/^BATADD$/ ) 
    {
        my $iptoappend=$action{ip};

        foreach my $neigh ( @$ipneigharray ) 
        {
            if ( exists($iptoappend->{$neigh->{ip}} ) )  { next; }
            push( @tempneigharray, $neigh );
        }
    
        foreach my $newip ( keys %$iptoappend )
        {
            my %newipneigh=( isp=>$action{isp}, nic=>$action{nic}, ip=>$newip );
            push( @tempneigharray, \%newipneigh );
        }
        
        $ipneigh->{ipneigh}=\@tempneigharray;
    }
    #===========================================================
    # %action=( action=>"DEL", isp=>"", ip=>"", nic="" )
    elsif ( $action{action}=~m/^DEL$/ ) 
    {
        foreach my $neigh ( @$ipneigharray ) 
        {
            if ( $neigh->{isp}.$neigh->{ip}.$neigh->{nic} eq $action{isp}.$action{ip}.$action{nic} ) { next; }
            push( @tempneigharray, $neigh );
        }

        $ipneigh->{ipneigh}=\@tempneigharray;
    }
    #===========================================================
    # %action=( action=>"BATDEL", ip=>\% )
    elsif ( $action{action}=~m/^BATDEL$/ ) 
    {
        my $iptodel=$action{ip};

        foreach my $neigh ( @$ipneigharray ) 
        {
            if ( exists($iptodel->{$neigh->{ip}}) ) { next; }
            push( @tempneigharray, $neigh );
        }

        $ipneigh->{ipneigh}=\@tempneigharray;
    }
    #===========================================================
    # %action=( action=>"CLEAR", isp=>"2")
    elsif ( $action{action}=~m/^CLEAR$/ ) 
    {
        foreach my $neigh ( @$ipneigharray ) 
        {
            if ( $neigh->{isp} eq $action{isp} ) { next;} 
            push( @tempneigharray, $neigh );
        }
        
        $ipneigh->{ipneigh}=\@tempneigharray;
    }
    #===========================================================
    # %action=( action=>"MOVEPORT", isp=>"1", nic=>"eth1")
    elsif ( $action{action}=~m/^MOVEPORT$/ )
    {
        my @allDmzIPs=maintainIPBank(from=>"isp".$action{isp}."dmz", action=>"read");
        foreach my $neigh ( @$ipneigharray ) 
        {
            if ( $neigh->{isp} ne $action{isp} ) { next; }
            if ( grep(/^$neigh->{ip}$/, @allDmzIPs) ) { $neigh->{nic}=$action{nic}; } 
        }
    } 
    
    XMLwrite($ipneigh, $gPATH."ipneigh.xml");
}
#maintainIPneigh


#================================================================================================
sub maintainIPaddress 
{
    my (%action)=@_;
    if ( !$action{action} ) { return; }
    
    my $ipaddress=XMLread($gPATH."ipaddr.xml");
    my $ipaddressarray=$ipaddress->{ipaddress};
    my @tempaddressarray;
    
    #===========================================================
    # %action=( action=>"ADD", isp=>"", ip=>"", nic="" )
    if ( $action{action}=~m/^ADD$/ ) 
    {
        foreach my $address ( @$ipaddressarray ) 
        {
            if ( $address->{isp}.$address->{ip}.$address->{nic} eq $action{isp}.$action{ip}.$action{nic} ) { next; }
            push( @tempaddressarray, $address );
        }
        my %newipaddress=( ip=>$action{ip}, nic=>$action{nic}, isp=>$action{isp} );
        push( @tempaddressarray, \%newipaddress );
        $ipaddress->{ipaddress}=\@tempaddressarray;
    }
    #===========================================================
    # %action=( action=>"BATADD", isp=>"", nic=>"", ip=>\% )
    if ( $action{action}=~m/^BATADD$/ ) 
    {
        my $iptoappend=$action{ip};

        foreach my $address ( @$ipaddressarray ) 
        {
            if ( exists($iptoappend->{$address->{ip}}) ) { next; }
            push( @tempaddressarray, $address );
        }

        foreach my $newip ( keys %$iptoappend )
        {
            my %newipaddress=( ip=>$newip, nic=>$action{nic}, isp=>$action{isp} );
            push( @tempaddressarray, \%newipaddress );
        }

        $ipaddress->{ipaddress}=\@tempaddressarray;
    }
    #===========================================================
    # %action=( action=>"DEL", ip=>"", nic="" )
    elsif ( $action{action}=~m/^DEL$/ ) 
    {

        foreach my $address ( @$ipaddressarray ) 
        {
            if ( $address->{isp}.$address->{ip}.$address->{nic} eq $action{isp}.$action{ip}.$action{nic} ) { next; }
            push( @tempaddressarray, $address );
        }

        $ipaddress->{ipaddress}=\@tempaddressarray;
    }
    #===========================================================
    #%action=( action=>"BATDEL", ip=>\% )
    elsif ( $action{action}=~m/^BATDEL$/ ) 
    {
        my $iptodel=$action{ip};

        foreach my $address ( @$ipaddressarray ) 
        {
            if ( exists($iptodel->{$address->{ip}}) ) { next; } 
            push( @tempaddressarray, $address ); 
        }

        $ipaddress->{ipaddress}=\@tempaddressarray;
    }
    #===========================================================
    # %action=( action=>"CLEAR", isp=>"")
    elsif ( $action{action}=~m/^CLEAR$/ ) 
    {
        foreach my $address ( @$ipaddressarray ) 
        {
            if ( $address->{isp} eq $action{isp} ) { next;} 
            push( @tempaddressarray, $address );
        }
        $ipaddress->{ipaddress}=\@tempaddressarray;
    }
    #===========================================================
    # %action=( action=>"MOVEPORT", isp=>"1", nic=>"eth1")
    elsif ( $action{action}=~m/^MOVEPORT$/ )
    {
        foreach my $address ( @$ipaddressarray ) 
        {
            if ( $address->{isp} ne $action{isp} ) { next; }
            $address->{nic}=$action{nic}; 
        }
    } 
    
    
    #==================================================
    XMLwrite($ipaddress, $gPATH."ipaddr.xml");
}
#maintainIPaddress

#================================================================================================
#ex:maintainInterrt( action=>"ADD", nic=>$targetdmz->{nic}, subnet=>$subnet, isp=>"1", gateway=>"", gwnatid=>"")
#ex:maintainInterrt( action=>"DEL", nic=>$targetdmz->{nic}, subnet=>$subnet, isp=>"2", gateway=>"" )
#ex:maintainInterrt( action=>"CLEAR", isp=>"2" )
sub maintainInterrt 
{
    my (%action)=@_;
    if ( !$action{action} ) { return; }
    
    my $interrt=XMLread($gPATH.'interrt.xml');
    my $routearray=$interrt->{route};
    my @newroutearray;
    

    if ( $action{action}=~m/^GETSTATICROUTESUBNETS$/ )
    {
        my @subnets_of_static_routes;
        foreach my $route ( @$routearray ) { push(@subnets_of_static_routes, $route->{subnet}); }
        return @subnets_of_static_routes;
    }
    # (action=>'BATCHECKROUTE', routeoktab=>\%)
    elsif ( $action{action}=~m/^BATCHECKROUTE$/ ) 
    {
        my $routeoktab=$action{routeoktab};
        my @natdestarray=maintainOverview(action=>'GETDESTINATION');
        my @ispsubnets=maintainBasic(action=>'getIspSubnets');
    
        foreach my $subnet ( keys %$routeoktab )
        {
            my $routeOK=0;

            #================================================================
            # Step 1. check interrt.xml to see if $action{subnet} can be routed
            foreach my $route ( @$routearray ) 
            {
                my $result=subnet_belong_check($route->{subnet}, $subnet); 
                if ( $result==2 || $result==3 ) { $routeoktab->{$subnet}=$routeOK=1; last; } 
            }

            #=====================================================================
            # Step 2. check basic.xml to see if $action{subnet} is the one assigned by ISP
            if ( !$routeOK )
            {
                foreach my $ispsub ( @ispsubnets ) 
                {
                    my $result=subnet_belong_check($ispsub, $subnet); 
                    if ( $result==2 || $result==3 ) { $routetab->{$subnet}=$routeOK=1; last; } 
                }
            }

            #=====================================================================
            # Step 3. check overview.xml to see if $action{subnet} can be routed
            if ( !$routeOK )
            {
                foreach my $dest ( @natdestarray ) 
                {
                    my $result=subnet_belong_check($dest, $subnet); 
                    if ( $result==2 || $result==3 ) { $routetab->{$subnet}=$routeOK=1; last; } 
                }
            }
        }
        
        return  1;
    }
    elsif ( $action{action}=~m/^CHECKROUTE$/ ) 
    {
        my $routeOK=0;
        
        #=====================================================================
        # Step 1. check interrt.xml to see if $action{subnet} can be routed
        foreach my $route ( @$routearray ) 
        {
            my $result=subnet_belong_check($route->{subnet}, $action{subnet}); 
            if ( $result==2 || $result==3 ) { $routeOK=1; last; } 
        }


        #=====================================================================
        # Step 2. check basic.xml to see if $action{subnet} is the one assigned by ISP
        if ( !$routeOK )
        {
            my @ispsubnets=maintainBasic(action=>'getIspSubnets');
            foreach my $ispsub ( @ispsubnets ) 
            {
                my $result=subnet_belong_check($ispsub, $action{subnet}); 
                if ( $result==2 || $result==3 ) { $routeOK=1; last; } 
            }
        }
    
        #=====================================================================
        # Step 3. check overview.xml to see if $action{subnet} can be routed
        if ( !$routeOK )
        {
            my @natdestarray=maintainOverview(action=>'GETDESTINATION');
            foreach my $dest ( @natdestarray ) 
            {
                my $result=subnet_belong_check($dest, $action{subnet}); 
                if ( $result==2 || $result==3 ) { $routeOK=1; last; } 
            }
        }

        return $routeOK;
    }
    elsif ( $action{action}=~m/^ADD$/ ) 
    {
        foreach my $route ( @$routearray ) 
        {
            if ( $route->{isp}.$route->{nic}.$route->{gateway}.$route->{subnet} eq $action{isp}.$action{nic}.$action{gateway}.$action{subnet} ) { next; }
            push( @newroutearray, $route );
        }
        
        my $gwnatid=($action{gwnatid}) ? ("$action{gwnatid}") : ('');
        
        if ( $action{subnet} ) #20100622 Brian For grebridge
        { 
        my %newroute=( isp=>$action{isp}, gwnatid=>$gwnatid, nic=>$action{nic}, gateway=>$action{gateway}, subnet=>$action{subnet} );
        
        push( @newroutearray, \%newroute);
        }
    }
    elsif ( $action{action}=~m/^DEL$/ ) 
    {
        foreach my $route ( @$routearray ) 
        {
            if ( $route->{isp}.$route->{nic}.$route->{gateway}.$route->{subnet} eq $action{isp}.$action{nic}.$action{gateway}.$action{subnet} ) { next; }
            push( @newroutearray, $route );
        }
    }
    # (action=>'BATDEL', route=>\%)
    elsif ( $action{action}=~m/^BATDEL$/ ) 
    {
        my $routetodel=$action{route};
        
        foreach my $route ( @$routearray ) 
        {
            if ( exists($routetodel->{$route->{subnet}}) ) { next; }
            push( @newroutearray, $route );
        }
    }
    elsif ( $action{action}=~m/^CLEAR$/ ) 
    {
        foreach my $route ( @$routearray ) 
        {
            if ( $route->{isp} eq $action{isp} ) { next; }
            push( @newroutearray, $route );
        }
    }
    
    $interrt->{route}=\@newroutearray;
        
    #=====================================
    XMLwrite($interrt, $gPATH."interrt.xml");
}
#maintainInterrt


###################################### IPBANK #########################################
#   千萬注意  本段絕對不可以改成 if...elsif...else的語法
####################################################################################### 
# maintainIPBank($action)
# $action{action} could be  | createisp | delisp | renew | clear | append | remove | move | read | 
####################################################################################### 
sub maintainIPBank 
{   
    my ( %action )=@_;
    
    my $from=$action{from};
    my $to=$action{to};
    my $ipSet=$action{ipset};
    
    # read in ipbank.xml --------------------------
    my $ref=XMLread($gPATH.'ipbank.xml');
    
    if ( $action{action} eq "READPUBLICIP" )
    {
        my @candidate;
        my $public=$ref->{ip}->{'isp'.$action{isp}.'public'}->{opt};
        my $systemip=$ref->{ip}->{'isp'.$action{isp}.'system'}->{opt};
        
        get_union_set(\@candidate, $public);
   
        get_diff_set(\@candidate, $systemip);
        
        get_diff_set(\@candidate, ['system']);
        
        push(@candidate, 'systemip');
        
        return sort ip_sort @candidate;
    }
    elsif ( $action{action} eq "NEWREADPUBLICIP" )
    {
        my @candidate;
        my $public=$ref->{ip}->{'isp'.$action{isp}.'public'}->{opt};
        my $systemip=$ref->{ip}->{'isp'.$action{isp}.'system'}->{opt};
        foreach my $item ( @$public )
        {
            if ( $item ne 'system' )
            {
                push(@candidate, $item);
            }
        }
        #foreach my $item ( @$systemip )
        #{
        #    if ( $item ne 'system' )
        #    {
        #        push(@candidate, $item);
        #    }
        #}
        push(@candidate, 'systemip');
        
        #push(@candidate, @$public);
        #push(@candidate, @$systemip);
        return sort ip_sort @candidate;
    }
    elsif ( $action{action} eq "READSYSTEMANDPUBLICIP" )
    {
        my @candidate;
        my $systemip=$ref->{ip}->{'isp'.$action{isp}.'system'}->{opt};
        my $public=$ref->{ip}->{'isp'.$action{isp}.'public'}->{opt};
        get_union_set(\@candidate, $public);
        get_union_set(\@candidate, $systemip);
        get_diff_set(\@candidate, ['system']);
        
        return sort ip_sort @candidate;
    }
    elsif ( $action{action} eq "READDMZFORBIDDENIP" )
    {
        my @candidate;
        my $systemip=$ref->{ip}->{'isp'.$action{isp}.'system'}->{opt};
        my $public=$ref->{ip}->{'isp'.$action{isp}.'public'}->{opt};
        my $dmz=$ref->{ip}->{'isp'.$action{isp}.'dmz'}->{opt};
        get_union_set(\@candidate, $systemip);
        get_union_set(\@candidate, $public);
        get_union_set(\@candidate, $dmz);
        get_diff_set(\@candidate, ['system']);
        
        return sort ip_sort @candidate;
    }
    
    #===========================================================
    if ( $from ne "" && $action{action}=~m/^read$/ ) 
    {
        my ($temp, %iphash);
  
        if ( $from ne "allisp" ) 
        {
            $temp=$ref->{ip}->{$from}->{opt};
            foreach my $item (@$temp) { ($item eq "system") || ($iphash{$item}=1); }
        }
        elsif ( $from eq "allisp" ) 
        {
            my $classhash=$ref->{ip};
            foreach my $class ( keys(%$classhash) ) 
            {
                if ( $class=~m/isp\d+$/ ) 
                {
                    $temp=$ref->{ip}->{$class}->{opt};
                    foreach my $item (@$temp) { ($item eq "system") || ($iphash{$item}=1); }
                }
            }
        }

        return sort ip_sort keys %iphash;
    }
    #===========================================================
    if ( $from ne ""  && $action{action}=~m/^remove$|^move$/ ) 
    {
        # Removing @$ipSet from the set of $from but "system" item
        my $temp=$ref->{ip}->{$from}->{opt};
        get_diff_set($temp, $ipSet);
    }
    #============================================================
    if ( $to ne "" && $action{action}=~m/^clear$/ ) 
    {
        my $temp=$ref->{ip};
        foreach my $class ( keys %$temp ) 
        {
            if ( $class=~m/^$to/ ) 
            {
                $ref->{ip}->{$class}->{opt}=['system'];
            }
        }
    }
    #============================================================
    if ( $to ne "" && $action{action}=~m/^renew$/ ) 
    {
        $ref->{ip}->{$to}->{opt}=['system'];
    }
    #=============================================================
    if( $to ne ""  && $to!~m/^isp\d$/ && $action{action}=~m/^renew$|^move$|^append$/ ) 
    { 
        # append @$ipSet to the set of $to
        my $temp=$ref->{ip}->{$to}->{opt};
        get_union_set($temp, $ipSet);
    }
    #=============================================================
    if ( $action{isp} && $action{action}=~m/^createisp$/ )
    {
        my $target=$action{isp};
        foreach my $type ('public', 'dmz', 'system') { $ref->{ip}->{'isp'.$target.$type}->{opt}=['system']; }
        $ref->{ip}->{system}->{opt}=['system'];
    }
    #=============================================================
    if ( $action{isp} && $action{action}=~m/^delisp$/ )
    {
        my $target=$action{isp};
        foreach my $type ('', 'public', 'dmz', 'system', 'lvs') { delete($ref->{ip}->{'isp'.$target.$type}); }
    }
   
    #--------updating ipbank.xml------------------------ 
    XMLwrite($ref, $gPATH."ipbank.xml");
}
#maintainIPBank


#================================================================================================
sub num_sort { int($a) <=> int($b); }
#num_sort

#================================================================================================
sub ip_sort 
{
    my @afields=split(/\./,$a);
    my @bfields=split(/\./,$b);
    my ($avalue, $bvalue);
    
    foreach my $index ( 0..3 )
    {
         $avalue=$afields[$index]; 
         $bvalue=$bfields[$index];
         if ( $avalue ne $bvalue ) { last; }
    }
    
    int($avalue) <=> int($bvalue);
}
#ip_sort


#================================================================================================
sub subnet_sort 
{
    my @afields=split(/\.|\//,$a);
    my @bfields=split(/\.|\//,$b);
    foreach my $index ( 0..4 )
    {
         $avalue=$afields[$index]; 
         $bvalue=$bfields[$index];
         if ( $avalue ne $bvalue ) { last; }
    }
    $avalue <=> $bvalue;
}
#subnet_sort


#================================================================================================
sub get_diff_set 
{
    my ($a, $b) = @_;
    my @set1=@$a;
    my @set2=@$b;
    my %hash_of_set;
    foreach my $item (@set1) { $hash_of_set{$item}=1; }
    foreach my $item (@set2) { delete($hash_of_set{$item}); }
    @$a=sort(keys(%hash_of_set));
    
    return;
}
#get_diff_set


#================================================================================================
sub get_union_set 
{
    my ($a, $b) = @_;
    my @set1=@$a; 
    my @set2=@$b;
    my %hash_of_set;
    foreach $item (@set1) { $hash_of_set{$item}=1; }
    foreach $item (@set2) { $hash_of_set{$item}=1; }
    @$a=sort keys %hash_of_set;
    
    return;
}
#get_union_set

sub check_subnetarray 
{
    my $subnetarray=$_[0];
    my $address=$_[1];

    foreach my $subnet ( @$subnetarray )
    {
        if ( subnet_belong_check($address, $subnet) == 1 || subnet_belong_check($address, $subnet) == 3)
        {
            return 1;
        }
    }
    return 0;
}
#check_subnetarray 

#================================================================================================
# check if subnet A:61.23.59.0/29 belogns to subnet B:61.23.59.0/27
#          subnet A:192.168.1.97/32   belogns to subnet B:host obj     
# subnet_belong_check(61.23.59.0/29, 61.23.59.0/27) 
# subnet_belong_check(hostobj, 192.168.1.97) 
# return:   
#           A <  B                  -->     return 1
#           A =  B                  -->     return 1
#           others                  -->     return 0
#================================================================================================

sub host_subnet_check
{
    my $subnet=$_[1];
    my $addresslist=$_[0];
    my $result;
    my $subnetlist;
    my @subnetarray;
    
    if ( grep(/$host-/, $subnet) )
    {
        my $tmpsource = $subnet;
        $tmpsource =~ s/host-//g;
        $subnetlist = maintainHost( action=>'GETADDRESSLIST', hostname=>$tmpsource);
    
        if ( grep(/-/, $subnetlist) )
        {
            my ($ip1, $ip2) = split(/-/, $source);
            $ip1 =~ /(\d+.\d+.\d+).(\d+)/;
            my ($subnet, $ip1) = ($1, $2);
            $ip2 =~ /\d+.\d+.\d+.(\d+)/;
            $ip2 = $1;
            foreach ( $ip1..$ip2 ) { push(@subnetarray, $subnet.'.'.$_.'/32'); }
        }
        elsif ( grep(/,/, $subnetlist) )
        {
            my @temparray = split(/,/, $subnetlist);
            foreach my $item ( @temparray ) 
            {
                $item = ( !grep(/\//, $item) ) ? ( $item.'/32' ) : ( $item );    
                push(@subnetarray, $item);
            }
        }
        else
        {
            $item = ( !grep(/\//, $subnetlist) ) ? ( $subnetlist.'/32' ) : ( $subnetlist );    
            push(@subnetarray, $subnetlist);
        }
    }
    else
    {
        push(@subnetarray, $subnet);
    }
   
    if ( grep(/-/, $addresslist) )
    {
        my @address=split(/-/, $addresslist);
        return check_subnetarray(\@subnetarray, $address[0].'/32');
    }
    elsif ( grep(/,/, $addresslist) )
    {
        my @address=split(/,/, $addresslist);
        my $result;
        
        foreach my $item ( @address ) 
        {
            $item = ( !grep(/\//, $item) ) ? ( $item.'/32' ) : ( $item );
            if ( check_subnetarray(\@subnetarray, $item) )
            {
                return 1;
            }
        }
        return 0;
    }
    else
    {
        $addresslist = ( !grep(/\//, $addresslist) ) ? ( $addresslist.'/32' ) : ( $addresslist );
        return check_subnetarray(\@subnetarray, $addresslist);
    }
}
#================================================================================================
# check if subnet A:61.23.59.0/29 belogns to subnet B:61.23.59.0/27
# subnet_belong_check(61.23.59.0/29, 61.23.59.0/27) 
# return:   
#           A or B format Error     -->     return -1
#           NO overlapping          -->     return 0
#           A < B                   -->     return 1
#           A >  B                  -->     return 2
#           A =  B                  -->     return 3
#================================================================================================
sub subnet_belong_check 
{
    #if ( !get_subnet($_[0]) || !get_subnet($_[1]) ) { return -1; }
    if ( (!get_subnet($_[0]) && !isValidIP($_[0]))|| (!get_subnet($_[1]) && !isValidIP($_[1])) ) { return -1; }
    my @a_fields=split(/\.|\//,$_[0]);
    my @b_fields=split(/\.|\//,$_[1]);
    my ($bit, $neta, $netb, $testa, $testb); 
    
    if ( $b_fields[4] eq '' ) { $b_fields[4]='32'; }

    $bit=($a_fields[4] > $b_fields[4]) ? ($b_fields[4]):($a_fields[4]);

    foreach my $i (0..3) { $neta.=dec2bin($a_fields[$i]); }
    foreach my $i (0..3) { $netb.=dec2bin($b_fields[$i]); }

    $testa=substr($neta,0,$bit);
    $testb=substr($netb,0,$bit);

    if ($testa eq $testb) 
    {
         if ($a_fields[4] > $b_fields[4]  )     { return 1;  } 
         if ($a_fields[4] < $b_fields[4]  )     { return 2;  } 
         if ($a_fields[4] == $b_fields[4] )     { return 3;  }
    } 
    else { return 0; }
}
#subnet_belong_check

sub subnet_belong_check_v6
{
    if ( (!get_subnet_v6($_[0]) && !isValidIP_v6($_[0]))|| (!get_subnet_v6($_[1]) && !isValidIP_v6($_[1])) ) { return -1; }
    my @a_fields=split(/:|\//,$_[0]);
    my @b_fields=split(/:|\//,$_[1]);
    my ($bit, $neta, $netb, $testa, $testb);
    
    if ( $b_fields[8] eq '' ) { $b_fields[8]='128'; }
    
    $bit=($a_fields[8]> $b_fields[8]) ? ($b_fields[8]):($a_fields[8]);
    
    foreach my $i (0..7) { $neta.=dec2bin_v6($a_fields[$i]); }
    foreach my $i (0..7) { $netb.=dec2bin_v6($b_fields[$i]); }
    
    $testa=substr($neta,0,$bit);
    $testb=substr($netb,0,$bit);
    
    if ($testa eq $testb)
    {
        if ($a_fields[8] > $b_fields[8]  )     { return 1;  }
        if ($a_fields[8] < $b_fields[8]  )     { return 2;  }
        if ($a_fields[8] == $b_fields[8] )     { return 3;  }
    }
    else { return 0; }
}    

#================================================================================================
# check if IP A:61.23.59.xx belogns to subnet B:61.23.59.0/xx
# isSubnetUsableIP(61.23.59.1, 61.23.59.0/27) 
# differ form isSubnetIP , not including head and tail ip
# return:   
#           ip A or subnet B format Error       -->     return -1
#           ip A is usable IP of subnet B       -->     return 1
#           ip A is not usable IP of subnet B   -->     return 1
#================================================================================================
sub isSubnetUsableIP 
{
    if ( !isValidIP($_[0]) || !get_subnet($_[1]) ) { return -1; }
    my @a_fields=split(/\./,$_[0]);
    my @b_fields=split(/\.|\//,$_[1]);
    
    
    my ($headbit, $tailbit, $neta, $netb, $testHeadA, $testHeadB, $testTailA, $testTailB); 
    $headbit=$b_fields[4]; 
    $tailbit=32-$headbit;

    foreach my $i (0..3) { $neta=$neta.dec2bin($a_fields[$i]); }
    foreach my $i (0..3) { $netb=$netb.dec2bin($b_fields[$i]); }
    
    $testHeadA=substr($neta,0,$headbit);
    $testHeadB=substr($netb,0,$headbit);
    if ( $testHeadA ne $testHeadB ) { return 0; }

    $testTailA=substr($neta,$headbit, $tailbit);

    if ( $a_fields[3] eq '0' || $a_fields[3] eq '255' ) {return 2;}
    #if ( $testTailA=~m/^0*$|^1*$/ ) { return 0; } Gary 20121029

    return 1; 
}
#isSubnetUsableIP

sub isSubnetUsableIP_for_ipAlias 
{
    if ( !isValidIP($_[0]) || !get_subnet($_[1]) ) { return -1; }
    my @a_fields=split(/\./,$_[0]);
    my @b_fields=split(/\.|\//,$_[1]);
    my ($headbit, $tailbit, $neta, $netb, $testHeadA, $testHeadB, $testTailA, $testTailB); 
    $headbit=$b_fields[4]; 
    $tailbit=32-$headbit;

    foreach my $i (0..3) { $neta=$neta.dec2bin($a_fields[$i]); }
    foreach my $i (0..3) { $netb=$netb.dec2bin($b_fields[$i]); }
    
    $testHeadA=substr($neta,0,$headbit);
    $testHeadB=substr($netb,0,$headbit);
    if ( $testHeadA ne $testHeadB ) { return 0; }

    $testTailA=substr($neta,$headbit, $tailbit);

    return 1; 
}
#isSubnetUsableIP_for_ipAlias

sub isSubnetUsableIP_v6
{
    if ( !isValidIP_v6($_[0]) || !get_subnet_v6($_[1]) ) { return -1; }
    my @a_fields=split(/:/,$_[0]);
    my @b_fields=split(/:|\//,$_[1]);
    my ($headbit, $tailbit, $neta, $netb, $testHeadA, $testHeadB, $testTailA, $testTailB);
    $headbit=$b_fields[@b_fields.length];
    $tailbit=128-headbit;
    foreach my $i (0..@a_fields.length) { $neta=$neta.dec2bin_v6($a_fields[$i]); }
    foreach my $i (0..@b_fields.length) { $netb=$netb.dec2bin_v6($b_fields[$i]); }
    
    $testHeadA=substr($neta,0,$headbit);
    $testHeadB=substr($netb,0,$headbit);
    if ( $testHeadA ne $testHeadB ) { return 0; }
    
    $testTailA=substr($neta,$headbit, $tailbit);
    
    if ( $testTailA=~m/^0*$|^1*$/ ) { return 0; }
     
    return 1;
}    
#================================================================================================
# check if IP A:61.23.59.xx belogns to subnet B:61.23.59.0/xx
# isSubnetIP(61.23.59.1, 61.23.59.0/27) 
# differ form isSubnetUsableIP , including head and tail ip
# return:   
#           ip A or subnet B format Error       -->     return -1
#           ip A is usable IP of subnet B       -->     return 1
#           ip A is not usable IP of subnet B   -->     return 1
#================================================================================================
sub isSubnetIP 
{
    if ( !isValidIP($_[0]) || !get_subnet($_[1]) ) { return -1; }
    my @a_fields=split(/\./,$_[0]);
    my @b_fields=split(/\.|\//,$_[1]);
    my ($headbit, $tailbit, $neta, $netb, $testHeadA, $testHeadB, $testTailA, $testTailB); 
    $headbit=$b_fields[4];
    $tailbit=32-headbit;

    foreach my $i (0..3) { $neta=$neta.dec2bin($a_fields[$i]); }
    foreach my $i (0..3) { $netb=$netb.dec2bin($b_fields[$i]); }
    
    $testHeadA=substr($neta,0,$headbit);
    $testHeadB=substr($netb,0,$headbit);
    if ( $testHeadA ne $testHeadB ) { return 0; }

    $testTailA=substr($neta,$headbit, $tailbit);
    return 1; 
}
#isSubnetIP

sub isSubnetIP_v6
{
   if ( !isValidIP_v6($_[0]) || !get_subnet_v6($_[1]) ) { return -1; }
   my @a_fields=split(/:/,$_[0]);
   my @b_fields=split(/:|\//,$_[1]);
   my ($headbit, $tailbit, $neta, $netb, $testHeadA, $testHeadB, $testTailA, $testTailB, $nb);
   $nb=int($b_fields[$#b_fields]/16)-1;
   foreach my $i (0..$nb)
   {
   if ($a_fields[$i] ne $b_fields[$i]){return 0;}
   }
   my $aa=($b_fields[$#b_fields]%16);
   if ($aa ne 0)
   {
       $headbit=$aa;
       $a_fields[$nb+1]=hex($a_fields[$nb+1]);
       $b_fields[$nb+1]=hex($b_fields[$nb+1]);
       $neta=$neta.dec2bin($a_fields[$nb+1]);
       $netb=$netb.dec2bin($b_fields[$nb+1]);
       $testHeadA=substr($neta,0,$headbit);
       $testHeadB=substr($netb,0,$headbit);
       if ( $testHeadA ne $testHeadB ) { return 0; }
   }
   return 1;
} 
#================================================================================================
sub get_allocated_ip 
{
    my ($subnet)=@_; 
    my @ipList;
    if ( grep(/-/,$subnet) )
    {
        my ($ip1, $ip2) = split(/-/, $subnet);
        $ip1 =~ /(\d+.\d+.\d+).(\d+)/;
        my ($network, $ip1) = ($1, $2);
        $ip2 =~ /\d+.\d+.\d+.(\d+)/;
        $ip2 = $1;
        foreach ( $ip1..$ip2 ) { push(@ipList, $network.'.'.$_); }
    }
    else
    {
        my ($seed_ip, $mask)=split(/\//, $subnet);
        # If not a valid subnet format, return  
        if ( !valid_netmask_format($mask) || !isValidIP($seed_ip) ) { return; }
        my $seedIPNum=IP2Num($seed_ip);
        $seedIPNum=$seedIPNum>>(32-$mask); 
        $seedIPNum=$seedIPNum<<(32-$mask); 
        my $end=(1<<(32-$mask))-1;
        foreach my $ipnext (0..$end) { push (@ipList, num2IP($seedIPNum+$ipnext)); }
    }
    return sort ip_sort @ipList;
}
#get_allocated_ip

#================================================================================================
sub get_bcast_ip 
{
    my ($subnet)=@_; 
    my ($seed_ip, $mask)=split(/\//, $subnet);
    # If not a valid subnet format, return  
    if ( !valid_netmask_format($mask) || !isValidIP($seed_ip) ) { return; }
    my $seedIPNum=IP2Num($seed_ip);
    $seedIPNum=$seedIPNum>>(32-$mask); 
    $seedIPNum=$seedIPNum<<(32-$mask); 
    my $end=(1<<(32-$mask))-1;
    return num2IP($seedIPNum+$end); 
}
#get_bcast_ip

sub get_bcast_ip_v6
{
    my ($subnet)=@_;
    my ($seed_ip, $mask)=split(/\//, $subnet);
    if ( !valid_netmask_format_v6($mask) || !isValidIP_v6($seed_ip) ) { return; }
    my @ip=split(/:/, $seed_ip);
    foreach my $i (0..$#ip){$ip[$i]=hex($ip[$i]);}
    @array=($ip[0],$ip[1]); $seed_op[0]=join(":",@array);
    @array1=($ip[2],$ip[3]); $seed_op[1]=join(":",@array1);
    @array2=($ip[4],$ip[5]); $seed_op[2]=join(":",@array2);
    @array3=($ip[6],$ip[7]); $seed_op[3]=join(":",@array3);
    SWITCH:
    {
         if($mask > 0 && $mask < 33)
         {
             $mask_op=$mask;
             my $seedIPNum=IP2Num_v6($seed_op[0]);
             $seedIPNum=$seedIPNum>>(32-$mask_op);
             $seedIPNum=$seedIPNum<<(32-$mask_op);
	     my $end = (1<<(32-$mask_op))-1;
             $seed_ip[0]=num2IP_v6($seedIPNum+$end);
             foreach my $x (1..3)
             {
                 my $seedIPNum=IP2Num_v6($seed_op[$x]);
                 $seedIPNum=$seedIPNum>>(32);
                 $seedIPNum=$seedIPNum<<(32);
                 $seed_ip[$x]=num2IP_v6($seedIPNum);
             }
         last SWITCH;
     }
     if($mask > 32 && $mask < 65)
     {
         $mask_op=$mask-32;
         my $seedIPNum=IP2Num_v6($seed_op[1]);
         $seedIPNum=$seedIPNum>>(32-$mask_op);
         $seedIPNum=$seedIPNum<<(32-$mask_op);
         my $end = (1<<(32-$mask_op))-1;
         $seed_ip[1]=num2IP_v6($seedIPNum+$end);
         
         my $seedIPNum=IP2Num_v6($seed_op[0]);
         $seedIPNum=$seedIPNum>>(32);
         $seedIPNum=$seedIPNum<<(32);
         $seed_ip[0]=num2IP_v6($seedIPNum);
         
         foreach my $x (2..3)
         {
             my $seedIPNum=IP2Num_v6($seed_op[$x]);
             $seedIPNum=$seedIPNum>>(32);
             $seedIPNum=$seedIPNum<<(32);
             $seed_ip[$x]=num2IP_v6($seedIPNum);
         }
         last SWITCH;
     }                                        
     if($mask > 64 && $mask < 97)
     {
         $mask_op=$mask-64;
         my $seedIPNum=IP2Num_v6($seed_op[2]);
         $seedIPNum=$seedIPNum>>(32-$mask_op);
         $seedIPNum=$seedIPNum<<(32-$mask_op);
	 my $end = (1<<(32-$mask_op))-1;
         $seed_ip[2]=num2IP_v6($seedIPNum+end);
         
         my $seedIPNum=IP2Num_v6($seed_op[3]);
         $seedIPNum=$seedIPNum>>(32);
         $seedIPNum=$seedIPNum<<(32);
         $seed_ip[3]=num2IP_v6($seedIPNum);
         
         foreach my $x (0..1)
         {
             my $seedIPNum=IP2Num_v6($seed_op[$x]);
             $seedIPNum=$seedIPNum>>(32);
             $seedIPNum=$seedIPNum<<(32);
             $seed_ip[$x]=num2IP_v6($seedIPNum);
         }
         last SWITCH;
     }
     if($mask > 96 && $mask < 129)
     {
         $mask_op=$mask-96;
         my $seedIPNum=IP2Num_v6($seed_op[3]);
         $seedIPNum=$seedIPNum>>(32-$mask_op);
         $seedIPNum=$seedIPNum<<(32-$mask_op);
	 my $end = (1<<(32-$mask_op))-1;
         $seed_ip[3]=num2IP_v6($seedIPNum+$end);
         foreach my $x (0..2)
         {
             my $seedIPNum=IP2Num_v6($seed_op[$x]);
             $seedIPNum=$seedIPNum>>(32);
             $seedIPNum=$seedIPNum<<(32);
             $seed_ip[$x]=num2IP_v6($seedIPNum);
         }
         last SWITCH;
     }
 }
    
      ($ip[0],$ip[1])=split(/:/,$seed_ip[0]);
      ($ip[2],$ip[3])=split(/:/,$seed_ip[1]);	   
      ($ip[4],$ip[5])=split(/:/,$seed_ip[2]);	   
      ($ip[6],$ip[7])=split(/:/,$seed_ip[3]);
      foreach my $j (0..7){$ip[$j] = sprintf ("%x",$ip[$j]); }
      @ip = ($ip[0],$ip[1],$ip[2],$ip[3],$ip[4],$ip[5],$ip[6],$ip[7]);
      $seed_ip=join(":",@ip);
      return $seed_ip;
   
}
#================================================================================================
sub get_bcast_ip_with_ipmask 
{
    my ($seed_ip, $ipmask)=@_; 
    # If not a valid subnet format, return  
    if ( !valid_netmask_format($ipmask) || !isValidIP($seed_ip) ) { return; }
    my $mask=ipmask2nummask($ipmask);
    my $seedIPNum=IP2Num($seed_ip);
    $seedIPNum=$seedIPNum>>(32-$mask); 
    $seedIPNum=$seedIPNum<<(32-$mask); 
    my $end=(1<<(32-$mask))-1;
    return num2IP($seedIPNum+$end); 
}
# get_bcast_ip_with_ipmask

#================================================================================================
sub nummask2ipmask 
{
    my ($mask)=@_; 
    if ( !valid_netmask_format($mask) ) { return ''; }
    # If not a valid mask format, return  
    my $maskmagic=0xFFFFFFFF >> (32-$mask);
    my $maskmagic=$maskmagic << (32-$mask);
    my $maskIP=num2IP($maskmagic);
    return $maskIP; 
}
#nummask2ipmask


#================================================================================================
sub ipmask2nummask 
{
    my ($ipmask)=@_; 
    if ( !valid_netmask_format($ipmask) ) { return ''; }
    # If not a valid mask format, return  
    my $maskmagic=IP2Num($ipmask);
    my $nummask=0; for ( ; $maskmagic>0 ; $maskmagic=$maskmagic << 1 ) { $nummask++; }
    return $nummask;
}
#ipmask2nummask


#================================================================================================
sub get_subnet 
{
    my ($subnet)=@_; 
    my ($seed_ip, $mask)=split(/\//, $subnet);
    
    #----- if any format of netmask or seed_ip is not valid, return false 

    if ( !valid_netmask_format($mask) || !isValidIP($seed_ip) ) { return ''; }
    
    my $seedIPNum=IP2Num($seed_ip);
    $seedIPNum=$seedIPNum>>(32-$mask); 
    $seedIPNum=$seedIPNum<<(32-$mask); 
    $seed_ip=num2IP($seedIPNum);
    
    #---------if everyting is ok, return the subnet in modified format ---------------------- 
    return ($seed_ip.'/'.$mask);
}
#get_subnet

sub get_subnet_v6

{
	my ($subnet)=@_;
	my ($seed_ip, $mask)=split(/\//, $subnet);
	if ( !valid_netmask_format_v6($mask) || !isValidIP_v6($seed_ip) ) { return ''; }
  	my @ip=split(/:/, $seed_ip);
  	foreach my $i (0..7){$ip[$i]=hex($ip[$i]);}
  	@array=($ip[0],$ip[1]); $seed_op[0]=join(":",@array);
  	@array1=($ip[2],$ip[3]); $seed_op[1]=join(":",@array1);
  	@array2=($ip[4],$ip[5]); $seed_op[2]=join(":",@array2);
  	@array3=($ip[6],$ip[7]); $seed_op[3]=join(":",@array3);
  	SWITCH:
  	{
  	    if($mask > 0 && $mask < 33)
  	    {
  	        $mask_op=$mask;
  	        my $seedIPNum=IP2Num_v6($seed_op[0]);
  	        $seedIPNum=$seedIPNum>>(32-$mask_op);
  	        $seedIPNum=$seedIPNum<<(32-$mask_op);
  	        $seed_ip[0]=num2IP_v6($seedIPNum);
  	        foreach my $x (1..3)
  	        {
  	            my $seedIPNum=IP2Num_v6($seed_op[$x]);
  	            $seedIPNum=$seedIPNum>>(32);
  	            $seedIPNum=$seedIPNum<<(32);
  	            $seed_ip[$x]=num2IP_v6($seedIPNum);
  	        }
  	        last SWITCH;
  	    }
  	    if($mask > 32 && $mask < 65)
  	    {
  	        $mask_op=$mask-32;
  	        my $seedIPNum=IP2Num_v6($seed_op[1]);
  	        $seedIPNum=$seedIPNum>>(32-$mask_op);
  	        $seedIPNum=$seedIPNum<<(32-$mask_op);
  	        $seed_ip[1]=num2IP_v6($seedIPNum); 
  	        
  	        my $seedIPNum=IP2Num_v6($seed_op[0]);
  	        $seedIPNum=$seedIPNum>>(32);
  	        $seedIPNum=$seedIPNum<<(32);
  	        $seed_ip[0]=num2IP_v6($seedIPNum);
  	        
  	        foreach my $x (2..3)
  	        {
  	            my $seedIPNum=IP2Num_v6($seed_op[$x]);
  	            $seedIPNum=$seedIPNum>>(32);
  	            $seedIPNum=$seedIPNum<<(32);
  	            $seed_ip[$x]=num2IP_v6($seedIPNum);
  	        }
  	        last SWITCH;
  	    }
  	    if($mask > 64 && $mask < 97)
  	    {
  	        $mask_op=$mask-64;
  	        my $seedIPNum=IP2Num_v6($seed_op[2]);
  	        $seedIPNum=$seedIPNum>>(32-$mask_op);
  	        $seedIPNum=$seedIPNum<<(32-$mask_op);
  	        $seed_ip[2]=num2IP_v6($seedIPNum);
  	        
  	        my $seedIPNum=IP2Num_v6($seed_op[3]);
  	        $seedIPNum=$seedIPNum>>(32);
  	        $seedIPNum=$seedIPNum<<(32);
  	        $seed_ip[3]=num2IP_v6($seedIPNum);
  	        
  	        foreach my $x (0..1)
  	        {
  	            my $seedIPNum=IP2Num_v6($seed_op[$x]);
  	            $seedIPNum=$seedIPNum>>(32);
  	            $seedIPNum=$seedIPNum<<(32);
  	            $seed_ip[$x]=num2IP_v6($seedIPNum);
  	        }
  	        last SWITCH;
  	    }
  	    if($mask > 96 && $mask < 129)
  	    {
  	        $mask_op=$mask-96;
  	        my $seedIPNum=IP2Num_v6($seed_op[3]);
  	        $seedIPNum=$seedIPNum>>(32-$mask_op);
  	        $seedIPNum=$seedIPNum<<(32-$mask_op);
  	        $seed_ip[3]=num2IP_v6($seedIPNum);
  	        foreach my $x (0..2)
  	        {
  	            my $seedIPNum=IP2Num_v6($seed_op[$x]);
  	            $seedIPNum=$seedIPNum>>(32);
  	            $seedIPNum=$seedIPNum<<(32);
  	            $seed_ip[$x]=num2IP_v6($seedIPNum);
  	        }
  	        last SWITCH;
  	    }
  	}
#  	($ip[0],$ip[1])=split(/:/,$seed_ip[0]);
#  	($ip[2],$ip[3])=split(/:/,$seed_ip[1]);
#  	($ip[4],$ip[5])=split(/:/,$seed_ip[2]);
#  	($ip[6],$ip[7])=split(/:/,$seed_ip[3]);
  	foreach my $j (0..7){$ip[$j] = sprintf ("%x",$ip[$j]); }
#  	@ip = ($ip[0],$ip[1],$ip[2],$ip[3],$ip[4],$ip[5],$ip[6],$ip[7]);
  	$seed_ip=join(":",@ip);
	return ($seed_ip.'/'.$mask);
}

#================================================================================================
sub valid_netmask_format 
{
    my $mask=shift;
    my @maskfield;
    my $tempmask;

    #--------- may be it will be presented in 2-digit format -----
    if ( $mask=~m/^\d{1,2}$/ ) { ($mask < 0 || $mask > 32) ? ( return 0 ) : ( return 1 ); }

    #--------- if in 4-field-4-digit format ----------------------
    @maskfield=split(/\./,$mask);
    if ( @maskfield != 4 ) { return 0; }
    foreach my $field ( @maskfield ) { $tempmask .= dec2bin($field); }
    ( $tempmask=~m/^1+0*$/ )?(return 1):(return 0);
}
#valid_netmask_format

sub valid_netmask_format_v6
{
    my $mask=shift;
    my @maskfield;
    my $tempmask;
    
    if ( $mask=~m/^\d{1,3}$/ ) { ($mask < 0 || $mask > 128) ? ( return 0 ) : ( return 1 ); }
    
    @maskfield=split(/:/,$mask);
    if ( @maskfield > 8 ) { return 0; }
    foreach my $field ( @maskfield ) { $tempmask .= dec2bin_v6($field); }
    ( $tempmask=~m/^1+0*$/ )?(return 1):(return 0);
}    
    
     
#================================================================================================
sub isValidIP 
{
    my $ip=shift;
    my @field=split(/\./,$ip);
    if(@field != 4) { return 0 ;}
    foreach $get (@field){ if ( $get!~m/^\d{1,3}$/ || $get > 255 ) { return 0 ;} }
    return 1 ;
}
#isValidIP

sub isValidIP_v6
{
    my $i=0;
    my $ip=shift;
    my @field=split(/:/,$ip);
    if(@field > 8) { return 0 ;}
    foreach $get (@field)
    {  
         
        if ($get eq "")
        {
            if($i > 2){return 0;}
            $i++;
        }
        if ($get ne ""){if ( $get!~/^[a-fA-F0-9]{1,4}$/ ) { return 0 ;} }
    }
    return 1 ;
}
#================================================================================================
sub IP2Num()
{
    my ($ip)=@_;
    my ($ip1, $ip2, $ip3, $ip4)=split(/\./, $ip);
    return ($ip1<<24) + ($ip2<<16) + ($ip3<<8) + $ip4;
}
#IP2num

sub IP2Num_v6()
{
    my ($ip)=@_;
    my ($ip1, $ip2)=split(/:/, $ip);
    $ip1 = hex($ip1);
    $ip2 = hex($ip2);
    return ($ip1<<16) + $ip2;
}    
    
#================================================================================================
sub num2IP()
{
    my ($num)=@_;
    my $ip1=floor($num/(1<<24));    $num-=$ip1*(1<<24);
    my $ip2=floor($num/(1<<16));    $num-=$ip2*(1<<16);
    my $ip3=floor($num/(1<<8));     $num-=$ip3*(1<<8);
    my $ip4=$num;
    return qq ($ip1.$ip2.$ip3.$ip4);
}
#num2IP

sub num2IP_v6()
{
    my ($num)=@_;
    my $ip1=floor($num/(1<<16));    $num-=$ip1*(1<<16);
    my $ip2=$num;
  $ip1 = sprintf ("%x",$ip1);
  $ip2 = sprintf ("%x",$ip2);
   return qq ($ip1:$ip2);
    
}
#================================================================================================
sub str2IpList()
{
    my ($argstr)=@_;
    
    $argstr=~s/\n|\r|\s+//g;
    my @arglist=split(/;/,$argstr);
    my %iplist;

    foreach my $arg ( @arglist )
    {
        #====================================
        # type 1: just an ip  
        if ( isValidIP($arg) )  
        { 
            $iplist{$arg}=1; 
            next;
        }

        #====================================
        # type 2: describing an ip range by the format of startip-endip
        my ($start, $end)=split(/-/, $arg);
        
        if ( isValidIP($start) && isValidIP($end) ) 
        {
            my $numofstartip=&IP2Num($start);
            my $numofendip=&IP2Num($end);
            
            if ( $numofstartip > $numofendip ) { ($numofstartip, $numofendip)=($numofendip, $numofstartip); }

            my $range=$numofendip-$numofstartip;
            
            if ( $range >= 256 ) { $range=255; }

            foreach my $inc (0..$range) { $iplist{&num2IP($numofstartip+$inc)}=1; }
            
            next;
        }

        #====================================
        # type 3: describing an ip range by the format of startip:numberofip 
        if ( $arg=~m/\d:\d+/ ) 
        {
            ($startip, $numofip)=split(/:/, $arg);
            
            if ( isValidIP($startip) && $numofip=~m/\d+/ )
            {
                if ( $numofip > 255 ) { $numofip=255; }

                my $numofstartip=&IP2Num($startip);
                
                for ( my $index=0; $index < $numofip; $index++) {$iplist{&num2IP($numofstartip+$index)}=1; }
            }
        }
    }    

    return keys %iplist;
} 
#str2IpList

sub str2IpList_v6()
{
    my ($argstr)=@_;
    
    $argstr=~s/\n|\r|\s+//g;
    my @arglist=split(/;/,$argstr);
    my %iplist;
    foreach my $arg ( @arglist )
    {
        if ( isValidIP_v6($arg) )
        {
            $iplist{$arg}=1;
            next;
        }
        
        my ($start, $end)=split(/-/, $arg);
        
        if ( isValidIP_v6($start) && isValidIP_v6($end) )
        {
            my $numofstartip=&IP2Num_v6($start);
            my $numofendip=&IP2Num_v6($end);
            
            if ( $numofstartip > $numofendip ) { ($numofstartip, $numofendip)=($numofendip, $numofstartip); }
            
            my $range=$numofendip-$numofstartip;
            
            if ( $range >= 256 ) { $range=255; }
            
            foreach my $inc (0..$range) { $iplist{&num2IP_v6($numofstartip+$inc)}=1; }
            
            next;
        }
        
        if ( $arg=~m/\d:\d+/ )
        {
            ($startip, $numofip)=split(/:/, $arg);
            
            if ( isValidIP_v6($startip) && $numofip=~m/\d+/ )
            {
                if ( $numofip > 255 ) { $numofip=255; }
                
                my $numofstartip=&IP2Num_v6($startip);
                
                for ( my $index=0; $index < $numofip; $index++) {$iplist{&num2IP($numofstartip+$index)}=1; }
                
            }
        }
    }
    return keys %iplist;
}
#================================================================================================
# create one 2 one mapping hash for vs.lib => ADDONE2ONE
# ex: 192.168.1.1 > 172.31.3.1
# ex: 192.168.1.2 : 5 > 172.31.3.1
# ex: 192.168.1.2-192.168.1.40 > 172.31.3.1
sub parseOne2One()
{
    my ($datastr)=@_;
    $datastr=~s/\s+//g;
    $datastr=~s/\n|\r/;/g;
    $datastr=~s/;+/;/g;
    
    my %maphash; 
    my @maplist=split(/;/,$datastr);
    
    foreach my $map ( @maplist )
    {
        my ($source, $target)=split(/>/, $map);
        
        #====================================
        # type 1: ip to ip map
        if ( isValidIP($source) && isValidIP($target) )  
        { 
            $maphash{$source}=$target; 
            next;
        }

        #====================================
        # type 2: describing an ip range by the format of startip-endip
        my ($start, $end)=split(/-/, $source);
        
        if ( isValidIP($start) && isValidIP($end) && isValidIP($target) ) 
        {
            my $numofstartip=&IP2Num($start);
            my $numofendip=&IP2Num($end);
            my $numoftargetip=&IP2Num($target);
            
            if ( $numofstartip > $numofendip ) { ($numofstartip, $numofendip)=($numofendip, $numofstartip); }

            my $range=$numofendip-$numofstartip;
            
            if ( $range >= 256 ) { $range=255; }

            foreach my $inc (0..$range) { $maphash{&num2IP($numofstartip+$inc)}=&num2IP($numoftargetip+$inc); }

            next;
        }

        #====================================
        # type 3: describing an ip range by the format of startip:numberofip 
        if ( $source=~m/\d:\d+/ ) 
        {
            ($startip, $range)=split(/:/, $source);
            
            if ( isValidIP($startip) && $range=~m/\d+/ )
            {
                if ( $range > 255 ) { $range=255; }

                my $numofstartip=&IP2Num($startip);
                my $numoftargetip=&IP2Num($target);
                
                foreach my $inc (0..$range) { $maphash{&num2IP($numofstartip+$inc)}=&num2IP($numoftargetip+$inc); }
            }
        }
    }    

    return %maphash;
}
#parseOne2One


#================================================================================================
sub host2IP
{
    my ($hostname)=@_;
    my $ip='';
    my $destsubnet=get_subnet($hostname);
    
    if ( $destsubnet ) { $ip=$destsubnet; }
    elsif ( isValidIP($hostname) ) {  $ip=$hostname.'/32'; }
    else
    {
        my $ipaddr=(gethostbyname($hostname))[4];
        $ip=join(".", unpack("C4", $ipaddr));
    }

    return $ip;
}
#sub host2IP

#================================================================================================
#transfer DEC to BIN in 8-bit length
sub dec2bin 
{
    my $str=unpack("B32",pack("N", shift));
    $str=~s/^000000000000000000000000//;
    return $str;
} 
#dec2bin

sub dec2bin_v6
{
    my $str=unpack("B128",pack("N", shift));
    $str=~s/^0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000//;
    return $str;
}
#================================================================================================
#transfer Dec to Hex in 8-bit length
sub dec2hex 
{
    # parameter passed to
    # the subfunction
    my $decnum = $_[0];
    # the final hex number
    my $hexnum;
    my $tempval;
    
    while ($decnum != 0) 
    {
        # get the remainder (modulus function)
        # by dividing by 16
        $tempval = $decnum % 16;

        # convert to the appropriate letter
        # if the value is greater than 9
        if ($tempval > 9) { $tempval = chr($tempval + 55); }

        # 'concatenate' the number to 
        # what we have so far in what will
        # be the final variable
        $hexnum = $tempval . $hexnum ;

        # new actually divide by 16, and 
        # keep the integer value of the 
        # answer
        $decnum = int($decnum / 16); 

        # if we cant divide by 16, this is the
        # last step
        if ($decnum < 16) 
        {
            # convert to letters again..
            if ($decnum > 9) { $decnum = chr($decnum + 55); }

            # add this onto the final answer.. 
            # reset decnum variable to zero so loop
            # will exit

            $hexnum = $decnum . $hexnum; 
            $decnum = 0 
        }
    }

    return $hexnum;
}
#dec2hex
sub hex2dec($) { return hex $_[0] }

#===================================================================================
# copy just XML $from to $to
#===================================================================================
sub cpConf
{
    my ( $from, $to )=@_;
    if ( !open(FROM, $from) || !open(TO, ">$to") ) 
    { 
        return -1; 
    }
    while (<FROM>) { print TO $_; }
    close(FROM);
    close(TO);
    chmod(0777, $to);
}
#cpConf


#===============================================================================================
sub XMLread
{
    my ($filename)=@_;

    my $XMLEVERCORRUPTED=0;

    #============================================================================================
    # if any xml is corrupted, we will trying to restore its template from /tmp/xmltemplate/$xmlver
    #============================================================================================

    if ( !(-e $filename) || (-z $filename) )
    {
        sleep 1;
        #$gMSGPROMPT.=qq(Corrupted Config File 1: $filename ! \\n);
        if ( !(-e $filename) || (-z $filename) )
        {
        #$gMSGPROMPT.=qq(Corrupted Config File 2: $filename ! \\n);
        $XMLEVERCORRUPTED=1;
        open(XMLVERSION, "< $gXMLVER");
        my $xmlver=<XMLVERSION>; chop($xmlver);
        my $nopathfilename=$filename; 
        my $srcxmllocation='';
        
        if ( $filename=~m/$gPATH/ )        
        {  
            $nopathfilename=~s/$gPATH//g;
            $srcxmllocation=$gXMLTEMPLATE.$xmlver.'/'.$nopathfilename;
        }

        if ( $filename=~m/$gINITPATH/ )  
        { 
            $nopathfilename=~s/$gINITPATH//g;
            $srcxmllocation=$gXMLTEMPLATE.$nopathfilename;
        }
        runCommand(command=>'/bin/cp', params=>' -a '.$filename.' /mnt/Fail_'.$nopathfilename);
        runCommand(command=>'/bin/cp', params=>' -a /var/log/qbalancer.log /mnt/Fail_qbalancer.log');
        LogUserAction( action=>'LOGINXML' , source=>$srcxmllocation, file=>$filename);
                                
        cpConf($srcxmllocation, $filename);
        #Brian 20080908 Hide this message
        #$gMSGPROMPT.=qq(Corrupted Config File: $nopathfilename ! \\n);
        #$gMSGPROMPT.=qq(Trying to restore template of config file $nopathfilename ...\\n);
        }
    }

    #============================================================================================
    # if any xml is ever corrupted, we have to report the result of template restoring process
    #============================================================================================
    if ( $XMLEVERCORRUPTED )
    {
        if ($filename=~m/$gPATH/)
	{
	    my $nopathfilename = $filename;
            $nopathfilename=~s/\/usr\/local\/apache\/qbconf\///g;
            system("/usr/local/apache/qb/setuid/run /bin/cp -a /mnt/qb/conf/set/default/$nopathfilename $filename");
	}
	
	if ( $filename=~m/$gINITPATH/ && $filename=~m/login.xml/) 
	{
	    open(FILE,">$filename");
	    print FILE "<opt file=\"login\" maximumuser=\"5\">\n";
	    print FILE "<user alive=\"system\" lastupdate=\"system\" online=\"system\" password=\"system\" sessionid=\"system\" username=\"system\" />\n";
	    print FILE "<user lastlogin=\"\" lastlogout=\"\" lastupdate=\"\" online=\"0\" password=\"123\" privilege=\"1\" sessionid=\"\" username=\"root\" />\n";
	    print FILE "<user lastlogin=\"\" lastlogout=\"\" lastupdate=\"\" online=\"0\" password=\"2k6m6root321\" privilege=\"1\" sessionid=\"\" username=\"cksupport\" />\n";
		print FILE "</opt>";
	    close(FILE);
	}

        
        if ( !(-e $filename) || (-z $filename) )
        {
            $gMSGPROMPT.=qq(Fail to restore template of corrupted config file ! \\n);
            #$gMSGPROMPT.=qq(Please call vender of Q-Balancer ! \\n);
            runCommand(command=>'/opt/qb/bin/script/backuplog.sh', params=>' Ramdisk');
            return;
        }
        #Brian 20080908 Hide this message
        #else
        #{
        #    $gMSGPROMPT.=qq(\\n Restore template of corrupted config file successfully ! \\n);
        #}
    }


    if ( !open(XMLLOCK, "< $gXMLLOCK") ) 
    { 
        $gLOGINRESULT=0;
        $gMSGPROMPT.=qq (\\nRead Lock Error\\n); 
        return;
    }

    flock(XMLLOCK, 2); 
    my $ref=XMLin($filename, forcearray=>1);
    flock(XMLLOCK, 8); 
    close XMLLOCK;
    return $ref;
}
#XMLread

#===============================================================================================
sub XMLwrite
{
    my ($ref, $filename)=@_;
    
    if ($ref eq "")
    {
        #$gMSGPROMPT.=qq (\\nWrite Error : Please Retry again !!! \\n);
        return;
    }
    
    my $availramdsk=getAvailRamDiskSize();

    if ( $availramdsk < 100 )
    {
        $gMSGPROMPT.=qq (\\nWrite Error : Please Retry again !!! \\n); 
        runCommand(command=>'/opt/qb/bin/script/backuplog.sh', params=>' Ramdisk');
        return;
    }

    runCommand(command=>'chmod',params=>"777 $filename"); 

    if ( !open(XMLLOCK, "> $gXMLLOCK") ) 
    { 
        $gLOGINRESULT=0;
        $gMSGPROMPT.=qq (\\nWrite Lock Error\\n); 
        return;
    }
    flock(XMLLOCK, 2); 

    if ( !open(XMLFILE, "> $filename") ) 
    { 
        $gLOGINRESULT=0;
        $gMSGPROMPT.=qq (\\nCan NOT Write $filename\\n);
        runCommand(command=>'chmod',params=>"777 $filename"); 
        return;
    }

    my $result=XMLout($ref);
    print XMLFILE $result;
    close XMLFILE;
    flock(XMLLOCK, 8); 
    close XMLLOCK;
}
#XMLwrite


#================================================================================================
# parse result of running df command to read the available size of ram0 
sub getAvailRamDiskSize()
{
    my $ramdiskstatus=runCommand(command=>'df', params=>' | grep ram0');
    
    $ramdiskstatus=~m/(.+)\s+(.+)\s+(.+)\s+(.+)/;

    my $availramdisk=$2;

    # if $availramdisk is an empty string, we can guess this is a none-compact-flash system ( the storage is a hard disk )
    if ( $availramdisk eq '' ) { $availramdisk='999999999'; }

    return $availramdisk;
}
#getAvailRamDiskSize
#================================================================================================


#================================================================================================
# to make sure the writing to login.xml in CF succefully, we have to sync for a certain times
sub qbSync
{
    #foreach my $index ( 1..3 ) { runCommand(command=>'sync', params=>'');    }
    #20120222 Do sync 3 times will cause QB become very slow when using analyser
    runCommand(command=>'sync', params=>'');
}
#================================================================================================


#================================================================================================
sub showResult 
{
    print qq (<div><table border=2><tr>);
    print qq (<div align=center><table border=2 width=100%><td class="body" align="center">);
    print qq (<br><textarea readonly style="height:200px;width=500px">$gMSGLOG</textarea><p></td></table></div>);
}
#showResult


#================================================================================================
sub fwmark_sort_by_source 
{
    my @afields=split(/\.|\//,$a->{source});
    my @bfields=split(/\.|\//,$b->{source});
    foreach my $index ( 0..4 )
    {
         $avalue=$afields[$index]; 
         $bvalue=$bfields[$index];
         if ( $avalue ne $bvalue ) { last; }
    }
    $avalue <=> $bvalue;
}

sub priority
{
    my $asort =( $a->{rule_priority} )?($a->{rule_priority}):(99);
    my $bsort =( $b->{rule_priority} )?($b->{rule_priority}):(99);
    if ($asort eq $bsort){$bsort++;}
    $asort <=> $bsort ;
    sort_num_reset();
}

sub sort_num_reset
{
    my $iniroute=XMLread($gPATH."iniroute.xml");
    my $classes=$iniroute->{nat}->[0]->{class};
    my $num=1;
    foreach my $cc (@$classes)
    {
        if ($cc->{advance} eq "system"){next;}
        $cc->{rule_priority} = $num;
        $num++;
    }
    XMLwrite($iniroute, $gPATH."iniroute.xml");
    

}

sub fwmark_sort_by_dest 
{
    my @afields=split(/\.|\//,$a->{destination});
    my @bfields=split(/\.|\//,$b->{destination});
    foreach my $index ( 0..4 )
    {
         $avalue=$afields[$index]; 
         $bvalue=$bfields[$index];
         if ( $avalue ne $bvalue ) { last; }
    }
    $avalue <=> $bvalue;
}
#fwmark_sort_by_source
sub presentTables
{
    my @tablelist = @_;
    my $rtable  = XMLread($gPATH.'rtable.xml');
    my $temptables=$rtable->{table};
    my @showtables;
    
    foreach my $table ( @tablelist )
    {
        my $target;
        my $showtable;
        foreach my $tableinfo ( @$temptables ) { if ( $tableinfo->{table_num} eq $table ) { $target=$tableinfo->{note};} }
    
        if   ( $table <  $gALLPATH  && $target ne "" )       {   $showtable="Pool ".$table."(".$target.")";     }
        if   ( $table <  $gALLPATH  && $target eq "" )       {   $showtable="Pool ".$table;     }
        if   ( $table >  $gALLPATH  )       {   $showtable=$table - $gALLPATH; $showtable="ISP".$showtable;       }
        if   ( $table eq $gBALANCE  )       {   $showtable="BALANCE";           }
        if   ( $table eq $gALLPATH  )       {   $showtable="RSI";              }
        if   ( $table eq $gDROP     )       {   $showtable="DROP";              }
        if   ( $table eq $gRRG      )       {   $showtable="RRG";               }
        
        push(@showtables, $showtable);
    }
    return @showtables;
}

sub presentTable
{
        
    my ($table)=@_;
    my $showtable=$table;
    #20100223 Brian To show the note of the pool
    my $rtable  = XMLread($gPATH.'rtable.xml');
    my $temptables=$rtable->{table};
    my $target;
    foreach my $tableinfo ( @$temptables ) { if ( $tableinfo->{table_num} eq $table ) { $target=$tableinfo->{note};} }
    
    if   ( $table <  $gALLPATH  && $target ne "" )       {   $showtable="Pool ".$table."(".$target.")";     }
    if   ( $table <  $gALLPATH  && $target eq "" )       {   $showtable="Pool ".$table;     }
    if   ( $table >  $gALLPATH  )       {   $showtable-=$gALLPATH; $showtable="ISP".$showtable;       }
    if   ( $table eq $gBALANCE  )       {   $showtable="BALANCE";           }
    if   ( $table eq $gALLPATH  )       {   $showtable="RSI";              }
    if   ( $table eq $gDROP     )       {   $showtable="DROP";              }
    if   ( $table eq $gRRG      )       {   $showtable="RRG";               }

    return $showtable;
}
#presentTable

#================================================================================================
sub nicTranslate
{
    my ($nic)=@_;
    
    if ( $nic!~m/^eth\s*\d+$|^port\s*\d+$|^imq\d+$|^isp\d+-out$|^isp\d+-in$/i ) { return ''; }

    if ( $nic=~m/^eth\s*(\d+$)/i )
    {
        return 'PORT '.($1+1);
    }
    elsif ( $nic=~m/^port\s*(\d+$)/i )
    {
        return 'eth'.($1-1);
    } 
    elsif ( $nic=~m/^isp(\d+)-(out)$/i )
    {
        my $id=$1;
        my $dir=$2;
        
        return 'imq'.($id*2-2);
    }   
    elsif ( $nic=~m/^isp(\d+)-(in)$/i )
    {
        my $id=$1;
        my $dir=$2;
        
        return 'imq'.($id*2-1);
    }  
    elsif ( $nic=~/^imq(\d+)$/i ) 
    {
        my $imqid=$1;

        if ( $imqid%2 )
        {
            return 'ISP'.(int($imqid/2)+1).'-IN';
        }
        else
        {
            return 'ISP'.($imqid/2+1).'-OUT';
        }
    }
 
    return '';   
}
#nicTranslate

#================================================================================================
sub displayService
{
    my @service=@_;

    if ( @service == 1 ) { print qq(None); }
    else
    {
        my $service_list_to_show='';

        my $firstservice=''; 
        foreach my $item ( @service ) { if ( $item ne "system") { $firstservice=$item; last;} }
        $firstservice=~s/others/ANY/g;

        foreach my $item ( @service ) 
        { 
            if ( $item eq "system") { next; }
            my $showitem=( $item eq "others" ) ? ( 'ANY' ) : ( $item );
            $service_list_to_show.=$showitem."\n";
        }
        
        $firstservice.=( @service > 2 ) ? (' ...') : ('');
        print qq (<span title="$service_list_to_show">$firstservice</span>);
    }
}
#displayService

sub noneFunctionExit()
{
    my ($alertmsg)=@_;
    print qq (<div align="center" class="title">$alertmsg</div>);
    print qq (</body></html>);
    exit;
}

# used by setuid/do_qbha.sh, enableha.sh
sub modifyfile
{
    my $replace_file=$_[0];	
    my $org_str=$_[1];
    my $new_str=$_[2];
    my $buffer = "";

    # print $org_str."-->".$new_str."\n";	
    open(IN, "+<$replace_file");
    while(<IN>)
    {
        $_ =~ s,$org_str,$new_str,;   # remove # character in the stateament 
        $buffer = $buffer . $_;
    }
    close(IN);
    open(OUT, ">$replace_file");
    print OUT $buffer;
    close(OUT);
}
sub subnet_sort_nic
{
    my @afields=split(/\.|\/|\@/,$a);
    my @bfields=split(/\.|\/|\@/,$b);
    foreach my $index ( 0..4 )
    {
         $avalue=$afields[$index]; 
         $bvalue=$bfields[$index];
         if ( $avalue ne $bvalue ) { last; }
    }
    $avalue <=> $bvalue;
}
#subnet_sort

sub getAllSource
{
   my $natref=XMLread($gPATH.'natnet.xml');
   my $natlist=$natref->{nat}[0]->{subnet};
   
   my $zoneref=XMLread($gPATH.'zonecfg.xml');
   my $natlist=$zoneref->{nat};
   
   my $hostref=XMLread($gPATH.'host.xml');
   my $hostlist=$hostref->{host};
    
   my @LAN;
   my @network;
   my @hostlist;
   
   foreach my $nat ( @$natlist )
   {
       if ( $nat->{natid} eq 'system' ) { next; }
       #push(@network, $nat->{network});
       push(@network, $nat->{network}.'@'.$nat->{nic});
       #$network{$nat->{network}} = $nat->{nic};
   }
   my @network = sort subnet_sort_nic @network;
   push (@LAN, @network);
   foreach my $host ( @$hostlist )
   {
       if ( $host->{hosttype} =~ m/^system$|^iplist$|^networklist$|^fqdnlist$|^weburl$/ ) { next; }
       my $address; 
       
       if ( $host->{hosttype} eq 'iprange' )
       {
           my @tmp = split(/-/, $host->{hostaddress});
           $address = $tmp[0]."\/32";
       }
       elsif ( $host->{hosttype} eq 'ip' )
       {
           $address = $host->{hostaddress}."\/32";
       }
       else
       {
           $address = $host->{hostaddress};
       }
       
       foreach my $net ( @network ) 
       {
           my @tmpnet = split(/@/, $net);
           my $subnet_belong = subnet_belong_check($address, $tmpnet[0]);
           if ( $subnet_belong == 1 || $subnet_belong == 3 )
           {
               push(@hostlist, $host->{hostname}.'@'.$tmpnet[1].'@'.$host->{hostaddress}); 
               last;
           }
       }
   }
   my @hostlist = sort { $a <=> $b } @hostlist;
   push(@LAN, @hostlist);
   
   return @LAN; 
   #return (\%network, \%hostlist);
   #return %network;
}

sub subnet_6to4
{
   my ($ip)=@_;
   my @aa = split (/:|\//,$ip);
   $aa[$#aa-1]=hex($aa[$#aa-1]);
   $aa[$#aa-2]=hex($aa[$#aa-2]);
   $bb=($aa[$#aa-2]<<16)+($aa[$#aa-1]);
   my $ip1=floor($bb/(1<<24));    $bb-=$ip1*(1<<24);
   my $ip2=floor($bb/(1<<16));    $bb-=$ip2*(1<<16);
   my $ip3=floor($bb/(1<<8));     $bb-=$ip3*(1<<8);
   my $ip4=$bb;
   my $ip5=$aa[$#aa]-96;
   return qq ($ip1.$ip2.$ip3.$ip4/$ip5);
}
       
sub ip_6to4
{
    my ($ip)=@_;
    my @aa = split (/:/,$ip);
    $aa[$#aa]=hex($aa[$#aa]);
    $aa[$#aa-1]=hex($aa[$#aa-1]);
    $bb=($aa[$#aa-1]<<16)+($aa[$#aa]);
    my $ip1=floor($bb/(1<<24));    $bb-=$ip1*(1<<24);
    my $ip2=floor($bb/(1<<16));    $bb-=$ip2*(1<<16);
    my $ip3=floor($bb/(1<<8));     $bb-=$ip3*(1<<8);
    my $ip4=$bb;
    return qq ($ip1.$ip2.$ip3.$ip4);
}

sub subnet_4to6
{
    my ($ip)=@_;
    my @bb = split (/\.|\//,$ip);
    my $aa =($bb[0]<<24) + ($bb[1]<<16) + ($bb[2]<<8) + $bb[3];
    my $ip1=floor($aa/(1<<16));    $aa-=$ip1*(1<<16);
    my $ip2=$aa;
    my $ip3=$bb[4]+96;
    $ip1 = sprintf ("%x",$ip1);
    $ip2 = sprintf ("%x",$ip2);
    return qq (FE80:0:0:0:0:0:$ip1:$ip2/$ip3);
}
sub ip_4to6
{
    my ($ip)=@_;
    my @bb = split (/\./,$ip);
    my $aa =($bb[0]<<24) + ($bb[1]<<16) + ($bb[2]<<8) + $bb[3];
    my $ip1=floor($aa/(1<<16));    $aa-=$ip1*(1<<16);
    my $ip2=$aa;
    $ip1 = sprintf ("%x",$ip1);
    $ip2 = sprintf ("%x",$ip2);
    return qq (FE80:0:0:0:0:0:$ip1:$ip2);
}
#this value 1 can not delete,because netcheck.cgi which is required 
#by another cgi program must return a value
1
