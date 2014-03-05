#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("./qblib/upgmanager.lib");


print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{number} = $form->param('number');
$action{upgid} = $form->param('upgid');

my @qbtoupgrade = $form->param('qbtoupgrade');
$action{qbtoupgrade} = \@qbtoupgrade;

my @reboot_time = $form->param('reboot_time');
$action{reboot_time} = \@reboot_time;


#print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);


if ( $action{action} ) { maintainUPG( %action ); }
elsif ( !$gENABLECMS ) { noneFunctionExit('UPG Managemnt is an Option');} #No PPTP server

#print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------
#print qq(<form name="upgform" method="post" action="upgmanager.cgi">);
#print qq (<table cellspacing="0" border="0">);
#print qq (<tr><td>);

#=============================================================================================
    my $ispref=XMLread($gACTIVEPATH.'basic.xml');
    my $isplist=$ispref->{isp};

    #remeber select upg 
    my $selectnum=runCommand(command=>'cat', params=>'/tmp/number');
    $selectnum=~s/\n//g; 

    my @SN=getallsn();
    my $lineCount=0;
    
    my $shownum=$selectnum;
    $shownum=~s/UPG//g;
    
    #upg version
    my $upgversion=runCommand(command=>'/usr/bin/find', params=>'/tmp/upg'.$shownum.' '.'-name \*\.upg');
    $upgversion=~s/\n//g;
    $upgversion=~s/\/tmp\/upg.*\///g;
    $upgversion=~s/\.upg//g;
    my @actionver=split('-', $upgversion);
    my $upgid=$actionver[0].'-'.$actionver[1];
    
    foreach my $sn ( @SN )
    {
        my $originalColor=$bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' ); 
        my $version;
        my $upgradestate;
        my $regist;
        my $warranty;
        my $uptime;
        my $time;
        @sninfo=split('\s', $sn);
        
        if ( $sninfo[0] eq '' ) { next; }
        
        $sninfo[1]=~s/VERSIONDETAIL://g;
        
        #my @actionver=split('-', $upgversion);
        my @showver=split('-', $sninfo[1]); 
        
        #if upg version different show bg color oringe
        if ( $selectnum ne 'None' && $selectnum ne 'Library'&& $selectnum ne 'Filesystem' )
        {
            if ( $actionver[0] ne $showver[0] || $actionver[1] ne $showver[1] ) { next; }
            if ( $upgversion ne $sninfo[1] ) { $originalColor=$bgcolor='#FF6600'; }
        }
        
        foreach my $isp ( @$isplist )
        {
            # if ( $isp->{qbsn} eq $sninfo[0] )
            # {
                $version = $isp->{info};
                $upgradestate = $isp->{upgradestate};
                $regist = $isp->{regist};
                $warranty = $isp->{warranty};
                $uptime=$isp->{uptime};
                $reboot_time = $isp->{reboot_time};
                #$image = $isp->{image};
                #$fs = $isp->{fs};
                #print qq ($isp->{ispname}); 
                #print qq (<br>);
                last;
            # }
        }
        $version=~s/VERSIONDETAIL://g;
        
        #if ( $upgradestate eq 'Success' ) { $originalColor=$bgcolor='#00FF00'; }
        #if ( grep(/Error/, $upgradestate) ) { $originalColor=$bgcolor='#CC0000'; } 
        my $mytime=runCommand(command=>'date', params=>'\+\%s');
        my $wtime=runCommand(command=>'date', params=>'-d'.' '.$warranty.' '.'\+\%s');
        
        #if ( $mytime > $wtime ) { $originalColor=$bgcolor='#999999'; $upgradestate='Warranty Expiried'; } 
        #elsif ( $upgradestate eq 'Success' ) { $originalColor=$bgcolor='#00FF00'; }
        #elsif ( grep(/Error/, $upgradestate) ) { $originalColor=$bgcolor='#CC0000'; } 
        
        foreach my $isp ( @$isplist )
        {
            # if ( $isp->{qbsn} eq $sninfo[0] )
            # {

##### Gary Get IP ###################################
                print qq ($isp->{remote},);

                my $state = ( $isp->{alive} ) ? "alive.png" : "dead.png";

                print qq ($state,);
#####################################################

            # }
        }
        
        $lineCount++;
    }


sub getallsn 
{
    my $ispref=XMLread($gACTIVEPATH.'basic.xml');
    my $isplist=$ispref->{isp};
	# foreach my $isp ( @$isplist ){
	# print $isp->{isptype};
	# }
	# print "GETALLSN_TEST";
    
         my @allsn;
         foreach my $isp ( @$isplist )
         {
             if ( $isp->{isptype} eq 'tunnel' || $isp->{isptype} eq 'dtunnel' )
             {
                 # push(@allsn, $isp->{qbsn}.' '.$isp->{info}); 
                 push(@allsn, "Luka".' '.$isp->{info}); 
                 
             }
         }
         #sort @allsn;
		 # print @allsn;
         return @allsn;

}
#print qq (</td></tr>);
#print qq (</table>);

