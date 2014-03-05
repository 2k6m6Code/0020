#!/usr/bin/perl -w
require ('../qbmod.cgi');
use CGI;
my $form= new CGI;
my $type=$form->param('type');
my $action=$form->param('action');

print "Content-type:text/html \n\n";
print qq (<html><head><script type="text/javascript" language="javascript" src="../qbjs/jquery.js"></script>
<script type="text/javascript" language="javascript" src="../qbjs/jquery.dataTables.min.js"></script>
<link rel="stylesheet" href="../gui.css" type="text/css"></head><body class='message'>);
print qq(<style>table {
	border-width: 1px;
	border-spacing: 0px;
	border-style: solid;
	border-color: black;
	border-collapse: collapse;
	background-color: white;
	font-size: 12px;
	width:98%;
}
table th {
    background-color: white;
    border-color: black;
    border-style: solid;
    border-width: 1px;
    padding: 1px;
}
table td {
    background-color: white;
    border-color: black;
    border-style: solid;
    border-width: 1px;
    padding: 3px;
}
body{
background-color:#C2D1E1;

}
.dataTables_filter {

margin-bottom: 5px;
}
</style>);
my $info='';

if ( $type eq "qbengine")    
{ 
    $head.="Show Q-Balancer Engine...";
    $str = runCommand(command=>'cat', params=>$gDIAGNOSELOG);
    $info .="<table id=\"example\" style=\"font-size: 12px;\"><thead><tr><th>Time</th><th>Action</th></tr></thead><tbody>";
    @sstr = split(/\n/,$str);
	# $info .= $sstr[3];
    for($ii = 0; $ii<= $#sstr;$ii++){
	$sstr[$ii] =~ s/  / 0/;
	@colstring = split(/ /,$sstr[$ii]);
	# $info .= $colstring[3];
	if(grep(/00/, $colstring[5])){
		$info .='<tr><td>';
		
		$info .=$colstring[2]." ";
		$info .=$colstring[1]." ";
		$info .=$colstring[4]." ";
		$info .=$colstring[3]." ";
		$info .="</td><td>";
		for($k = 6;$k<$#colstring+1;$k++){
		$info.=$colstring[$k]." ";
		}
		$info .="</td>";
		next;
	}
	if($colstring[6] eq 'Config.'){
		$info .='<tr><td>';
		
		$info .=$colstring[1]." ";
		$colstring[2]= sprintf("%02d",$colstring[2]);
		$info .=$colstring[2]." ";
		$info .=$colstring[3]." ";
		$info .=$colstring[5]." ";
		$info .="</td><td>";
		for($k = 6;$k<$#colstring+1;$k++){
		$info.=$colstring[$k]." ";
		}
		$info .="</td>";
	}else{
		$info .='<tr>';
		
		
		$info .="<td>";
		for($k = 0;$k<3;$k++){
		$info .=$colstring[$k]." ";
		}
		$info .="</td>";
		
		
		$info .= "<td>";
		for($k = 3;$k<$#colstring+1;$k++){
		$info .=$colstring[$k]." ";
		}
		$info .="</td>";
		}
		$info .="</tr>";
	
	}
	    $info .= "</tbody></table>";
    
    
     if ( !$info ) { $info.="Wait a moment for Information Collection ...<br>"; }
}
elsif ( $type eq "qbalertlog" ) 
{
    $head.="Show Q-Balancer Alert Logs ...";
    $infos=runCommand(command=>'cat', params=>$gALERTLOG);
    if ( !$infos ) 
    { 
        $info="!! Empty Log !!<br>"; 
    }
    my @infot=split(/\n/,$infos);
    # my $newinfo;
	$ttable= "";
    for($ff= 0;$ff<=$#infot;$ff++)
    {
		$linelog = $infot[$ff];
        if ( grep(/dead4ead/, $linelog) ){next;}
        elsif ( grep(/spinlock/, $linelog) ){next;}
        elsif ( grep(/register_vlan_device/, $linelog) ){next;}
        else
        {
		$linelog =~ s/  / 0/;
		@colstring=split(/ /,$linelog);
		
		$ttable .="<tr>";
		
		
		$ttable .="<td>";
		for($k = 0;$k<3;$k++){
		$ttable .=$colstring[$k]." ";
		}
		 ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) =localtime(time);
		$ttable .=($year+1900)." ";
		$ttable .="</td>";
		
		
		$ttable .="<td style=\'width: 415px;\'>";
		for($k = 3;$k<=$#colstring;$k++){
		$ttable .=$colstring[$k]." ";
		# $ttable .="$ff";
		}
		$ttable .="</td>";
		$ttable .="</tr>";
        $newinfo.=$ttable;
		$ttable = "";
		
		
		
        }
		
    }
	$info='<table id="example" style="width: 565px;" ><thead><tr><th>Time</th><th>Action</th></tr></thead><tbody>';
	
    $info.=$newinfo;
	$info.="</tbody></table>";
}   
elsif ( $type eq "clearalertlog" ) 
{
    $head.="Clear Q-Balancer Alert Logs ...";

    if ( -z $gALERTLOG )
    {
        $info="!! Empty Log !!<br>";
    }
    else
    {
        #runCommand(command=>'cp', params=>qq(/dev/null $gALERTLOG) );
        #20080414 Brian cp or cat can't work,so use rm to replace it.
        runCommand(command=>'rm', params=>qq( -f $gALERTLOG) );
        #================================================================================================
        # to make sure the writing to CF succefully, we have to sync for a certain times
        # sync the writing to CF
        qbSync();
        #20080414 Brian kill syslog will cause high cpu usage.
        runCommand(command=>'service', params=>'syslog restart');
        # kill klogd and syslogd
        #runCommand(command=>'killall', params=>'-9 klogd');
        #runCommand(command=>'killall', params=>'-9 syslogd');

        # restart klogd and syslogd
        #runCommand(command=>'klogd', params=>'');
        #runCommand(command=>'syslogd', params=>'');
        $info="!! Log is empty now !!<br>";
    }
}   
elsif ( $type eq "daemonlog" ) 
{
    $head.="Show Q-Balancer Daemon Logs ...";
    $info=runCommand(command=>'cat', params=>$gDAEMONLOG);
    if ( !$info ) 
    { 
        $info="!! Empty Log !!<br>"; 
    }
    my @info=split(/\n/,$info);
    my $newinfo;
    foreach my $linelog ( @info )
    {
        if ( grep(/Internet/, $linelog) ){next;}
        elsif ( grep(/All right/, $linelog) ){next;}
        elsif ( grep(/Copyright/, $linelog) ){next;}
        elsif ( grep(/For info/, $linelog) ){next;}
        elsif ( grep(/Please/, $linelog) ){next;}
        elsif ( grep(/Cannot determine ethernet/, $linelog) ){next;}
        elsif ( grep(/ppp/, $linelog) ){next;}
        else
        {
          $newinfo.=$linelog."<br>";
        }
    }
    $info=$newinfo;
}   
elsif ( $type eq "pppoelog" ) 
{
    $head.="Show Q-Balancer PPPoE Dial Logs ...";
    $info=runCommand(command=>'cat', params=>$gDAEMONLOG);
    if ( !$info ) 
    { 
        $info="!! Empty Log !!<br>"; 
    }
    my @info=split(/\n/,$info);
    my $newinfo;
    foreach my $linelog ( @info )
    {
        if ( grep(/Internet/, $linelog) ){next;}
        elsif ( grep(/All right/, $linelog) ){next;}
        elsif ( grep(/Copyright/, $linelog) ){next;}
        elsif ( grep(/For info/, $linelog) ){next;}
        elsif ( grep(/Please/, $linelog) ){next;}
        elsif ( grep(/Bad TCP checksum/, $linelog) ){next;}
        elsif ( grep(/Cannot determine ethernet/, $linelog) ){next;}
        elsif ( ! grep(/ppp/, $linelog) ){next;}
        elsif ( grep(/named/, $linelog) ){next;}
        else
        {
		$linelog =~ s/  / 0/;
          $linelog=~s/2.4.5/daemon/g;
          $linelog=~s/pppd/pppoe/g;
		  @colstring = split(/ /,$linelog);
		  	$ttable = "";
		  $ttable .='<tr>';
		
		
		$ttable .="<td>";
		for($k = 0;$k<3;$k++){
		$ttable .=$colstring[$k]." ";
		}
		 ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) =localtime(time);
		$ttable .=($year+1900)." ";
		$ttable .="</td>";
		
		$ttable .="<td>";
		$ttable .=$colstring[3]." ";
		$ttable .=$colstring[4]." ";
		$ttable .="</td>";
		
		$ttable .="<td>";
		for($k = 5;$k<=$#colstring;$k++){
		$ttable .=$colstring[$k]." ";
		}
		$ttable .="</td>";
		$ttable .='</tr>';
          $newinfo.=$ttable;
        }
    }
	$info = '<table id="example" ><thead><tr><th>Time</th><th>Name</th><th>Action</th></tr></thead><tbody>';
    $info.=$newinfo;
	$info .= "</tbody></table>";
}   
elsif ( $type eq "ipseclog" ) 
{
    $head.="Show Q-Balancer IPSEC Logs ...";
    $info=runCommand(command=>'cat', params=>$gDAEMONLOG);
    if ( !$info ) 
    { 
        $info="!! Empty Log !!<br>"; 
    }
    my @info=split(/\n/,$info);
    my $newinfo;
    foreach my $linelog ( @info )
    {
        if ( grep(/Internet/, $linelog) ){next;}
        elsif ( grep(/All right/, $linelog) ){next;}
        elsif ( grep(/Copyright/, $linelog) ){next;}
        elsif ( grep(/For info/, $linelog) ){next;}
        elsif ( grep(/Please/, $linelog) ){next;}
        elsif ( grep(/Cannot determine ethernet/, $linelog) ){next;}
        elsif ( ! grep(/racoon/, $linelog) ){next;}
        elsif ( grep(/http:/, $linelog) ){next;}
        elsif ( grep(/Reading configuration from/, $linelog) ){next;}
        else
        {
		$linelog =~ s/  / 0/;
          $linelog=~s/racoon/ipsec/g;
		  @colstring = split(/ /,$linelog);
		  $ttable = '';
		  $ttable .='<tr>';
		
		
		$ttable .="<td>";
		for($k = 0;$k<3;$k++){
		$ttable .=$colstring[$k]." ";
		}
		($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) =localtime(time);
		$ttable .=($year+1900)." ";
		$ttable .="</td>";
		
		$ttable .="<td>";
		$ttable .=$colstring[3]." ";
		$ttable .=$colstring[4]." ";
		$ttable .="</td>";
		
		$ttable .="<td>";
		for($k = 5;$k<$#colstring;$k++){
		$ttable .=$colstring[$k]." ";
		}
		$ttable .="</td>";
		$ttable .='</tr>';
          $newinfo.=$ttable;
        }
    }
	$info  = '<table id="example" ><thead><tr><th>Time</th><th>Name</th><th>Action</th></tr></thead><tbody>';
    $info .= $newinfo;
	$info .="</tbody></table>";
}  
elsif ( $type eq "pptplog" ) 
{
    $head.="Show Q-Balancer PPTP Logs ...";
    $info=runCommand(command=>'cat', params=>$gDAEMONLOG);
    if ( !$info ) 
    { 
        $info="!! Empty Log !!<br>"; 
    }
    my @info=split(/\n/,$info);
    my $newinfo;
    foreach my $linelog ( @info )
    {
        if ( ! grep(/pptp/, $linelog) ){next;}
        else
        {
		$linelog =~ s/  / 0/;
          $linelog=~s/pptpd/pptp/g;
         @colstring = split(/ /,$linelog);
		  $ttable = '';
		  $ttable .='<tr>';
		
		
		$ttable .="<td>";
		for($k = 0;$k<3;$k++){
		$ttable .=$colstring[$k]." ";
		}
		($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) =localtime(time);
		$ttable .=($year+1900)." ";
		$ttable .="</td>";
		
		$ttable .="<td>";
		$ttable .=$colstring[3]." ";
		$ttable .=$colstring[4]." ";
		$ttable .="</td>";
		
		$ttable .="<td>";
		for($k = 5;$k<$#colstring;$k++){
		$ttable .=$colstring[$k]." ";
		}
		$ttable .="</td>";
		$ttable .='</tr>';
          $newinfo.=$ttable;
        }
    }
	$info  = '<table id="example" ><thead><tr><th>Time</th><th>Name</th><th>Action</th></tr></thead><tbody>';
    $info .= $newinfo;
	$info .="</tbody></table>";
}   
elsif ( $type eq "pppoestatus" ) 
{
    $head.="Show PPPoE Status Logs ...";
    $info=runCommand(command=>'cat', params=>'/tmp/pppoestatus');
    if ( !$info ) 
    { 
        $info="!! Empty Log !!<br>"; 
    }
    my @info=split(/\n/,$info);
    my $newinfo;
    foreach my $linelog ( @info )
    {
		
		if(length($linelog) <2){next;}
        if ( grep(/Internet/, $linelog) ){next;}
        elsif ( grep(/error/, $linelog) ){next;}
        elsif ( grep(/collisions/, $linelog) ){next;}
        else
        {
		    # $linelog =~s/\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\./<hr>/g;
			$ttable = "";
			# $ttable .="<tr><td style='border: 1px inset;padding :5px;'>";
			$ttable .=$linelog." ";
			# $ttable .="</td></tr>";
			
			$newinfo.=$ttable;
        }
    }
	@colstring = split(/\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\./,$newinfo);
	$info = '<table id="example" ><thead><tr><th>Time</th><th>Status</th><th>device</th><th>Info</th></tr></thead><tbody>';
	for($k= 0;$k<=$#colstring; $k++){
	if(length($colstring[$k]) <5){next;}
	if(!grep(/Time/,$colstring[$k])){next;}
	$colstring[$k] =~s/  / 0/;
		if(grep(/PPPoE Status/,$colstring[$k]) ){
		@onecol = split(' ',$colstring[$k]);
		$info .="<tr><td style='border: 1px inset;padding :5px;' noWrap>";
		for($f= 4;$f<=6;$f++){
		$info .= $onecol[$f]." ";
		}
		$info .= $onecol[8]." ";
		$info .="</td><td>";
		$info .= $onecol[1];
		$info .="</td><td>";
		$info .= $onecol[11]."</td>";
		$info .="</td><td>";
		for($g = 12;$g<=$#onecol;$g++){
		if($onecol[$g] eq "inet" || $onecol[$g] eq "UP" || $onecol[$g] eq "RX"){
		$info .= "<br />";
		}
		$info .= $onecol[$g]." ";
		}
				
		$info .= "</td></tr>";
		}else{
		# @onecol = split(' ',$colstring[$k]);
		# $info .="<tr><td style='border: 1px inset;padding :5px;' noWrap>";
		# for($f= 3;$f<=8;$f++){
		# $info .= $onecol[$f]." ";
		# }
		@onecol = split(' ',$colstring[$k]);
		$info .="<tr><td style='border: 1px inset;padding :5px;' noWrap>";
		for($f= 5;$f<=7;$f++){
		# $onecol[$f] =~s 'Time:'';
		$info .= $onecol[$f]." ";
		}
		$info .= $onecol[9]." ";
		$info .="</td><td>";
		$info .= $onecol[3];
		$info .="</td><td>";
		$onecol[2] =~s 'Device:'';
		$info .= $onecol[2]."</td>";
		$info .="</td><td>";
		for($g = 12;$g<=$#onecol;$g++){
		
		$info .= $onecol[$g]." ";
		}
				
		$info .= "</td></tr>";
		
		
		}
	}
	
	
	$info .="</tbody></table>";
}   
elsif ( $type eq "ipchangelog" ) 
{
    $head.="Show Q-Balancer IP Change Logs for DDNS MPV...";
    $info=runCommand(command=>'cat', params=>$gIPCHANGELOG);
	my $newinfo;
    if ( !$info ) 
    { 
        $info="!! Empty Log !!<br>"; 
		
    }else{
		  @rowstring = split(/\n/,$info);
		  foreach $sstring(@rowstring){
		  @colstring = split(/ /,$sstring);
		  $ttable  = "";
		  $ttable .= '<tr><td noWrap>';
		  # for($k = 0;$k<=5;$k++){
			# $ttable .=$colstring[$k]."[$k]";
		  # }
		  $ttable .=$colstring[2]." ";
		  $ttable .=$colstring[1]." ";
		  $ttable .=$colstring[4]." ";
		  $ttable .=$colstring[3]." ";
		 
		  $ttable .="</td><td>";
		  for($k = 6;$k<=$#colstring;$k++){
			$ttable .=$colstring[$k]." ";
		  }
		  $ttable .= "</td></tr>";
			
          $newinfo.=$ttable;
		  }
		  $info  = '<table id="example" ><thead><tr><th>Time</th><th>Action</th></tr></thead><tbody>';
    $info .= $newinfo;
	$info .="</tbody></table>";
	
	}
	
}   
elsif ( $type eq "tunnellog" ) 
{
    $head.="Show Q-Balancer MPV Tunnel Bandwidth Measure Logs ...";
    $info=runCommand(command=>'cat', params=>$gTUNNELLOG);
    if ( !$info ) 
    { 
        $info="!! Empty Log !!<br>"; 
    }
}   
elsif ( $type eq "bottleneck" )    
{ 
    $head.="Bottle Neck Monitoring...";
    $info=runCommand(command=>'cat', params=>$gBTKAVGLOG);
    if ( !$info ) 
    { 
        $info="Bottle Neck Monitoring is Processing ...<br>"; 
        $info.="Wait a moment for Bottle Neck Detection ...<br>"; 
    }
}
elsif ( $type eq "versioninfo")  
{
    $info.="<br>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br>";
    $info.="Version information of Packge for each component";
    $info.="<br>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br>";
    $info.=runCommand(command=>'cat', params=>$gPKGINFO);
} 
elsif ( $type eq "systemstatus")  
{
    $info.="<br>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br>";
    $info.="System status information of Q-Balancer";
    $info.="<br>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br>";
    runCommand(command=>'perl', params=>'/usr/local/apache/qb/status/getsysstatus.cgi');
    #runCommand(command=>'/usr/local/apache/qb/status/getsysstatus.cgi', params=>'');
    $info.="<br>Uptime:<br>";
    $info.=runCommand(command=>'uptime', params=>'');
    $info.="<br>==============================================================<br>";
    $info.="<br>CPU Usage:<br>";
    $info.="<br>Percentage(%)<br>";
    $info.=runCommand(command=>'cat', params=>'./cpu.status');
    $info.="<br>==============================================================<br>";
    $info.="<br>Memory Usage:<br>";
    $info.="<br>Percentage(%)Total          Available<br>";
    $info.=runCommand(command=>'cat', params=>'./memory.status');
    $info.="<br>==============================================================<br>";
    $info.="<br>Ramdisk Usage:<br>";
    $info.="<br>Percentage(%)Total          Available<br>";
    $info.=runCommand(command=>'cat', params=>'./ramdisk.status');
    $info.="<br>==============================================================<br>";
    $info.="<br>Current Sessions:<br>";
    $info.="<br>Percentage(%)Max Concurrent<br>";
    $info.=runCommand(command=>'cat', params=>'./session.status');
    $info.="<br>==============================================================<br>";
} 
elsif ( $type eq "systeminfo")  
{
    $info.="<br>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br>";
    $info.="hardware information of Q-Balancer";
    $info.="<br>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br>";
    $info.=runCommand(command=>'cat', params=>'/proc/cpuinfo');
    $info.="<br>==============================================================<br>";
    $info.=runCommand(command=>'cat', params=>'/proc/meminfo');
} 
elsif ( $type eq "category" )
{
    $info=runCommand(command=>'cat', params=>'/usr/local/squidGuard/log/blockaccesses');
	my $newinfo;
    if ( !$info ) 
    { 
        $info="!! Empty Log !!<br>"; 
		 
    }else{
		my @info=split(/\n/,$info);
		 
		 foreach $linelog ( @info ){
			 @colstring = split(' ',$linelog);
			 $ttable = "";
			 $ttable .="<tr><td noWrap>";
			 
			 $ttable .=$colstring[0]." ";
			 $ttable .=$colstring[1]."</td><td>";
			 $colstring[3] =~s /Request\(//;
			 $colstring[3] =~s /\/-\)//;
			 $ttable .=$colstring[3].'</td><td style="word-break: break-all;">';
			 $ttable .=$colstring[4];
			 # $ttable .=$colstring[5];
			 $ttable .="</td></tr>";
			 $newinfo .=$ttable;
		 }
	
	
	}
	$info  = '<table id="example" ><thead><tr><th>Time</th><th>Request</th><th>GET REDIRECT</th></tr></thead><tbody>';
    $info .= $newinfo;
	$info .="</tbody></table>";
}
elsif ( $type eq "webproxy" )
{
    $info=runCommand(command=>'cat', params=>'/mnt/tclog/squid/log/access.log');
    if ( !$info ) 
    { 
        $info="!! Empty Log !!<br>"; 
    }
    my @info=split(/\n/,$info);
    my $newinfo;
    foreach my $linelog ( @info )
    {
        if ( ! grep(/HIT/, $linelog) ){next;}
        else
        {
		  
          $linelog=~s/:NONE//g;
		  @colstring = split(/ /,$linelog);
		  $ttable  = "";
		  $ttable .= '<tr><td noWrap>';
		  $ttable .= $colstring[0].'</td>';
		  $ttable .='<td noWrap>';
		  $ttable .= $colstring[3].' ';
		  $ttable .= $colstring[4].'</td>';
		  $ttable .="<td>";
		  for($k = 5;$k<=$#colstring;$k++){
			$ttable .=$colstring[$k]." ";
		  }
		  $ttable .= "</td></tr>";
			
          $newinfo.=$ttable;
        }
    }
    $info  = '<table id="example" ><thead><tr><th>IP</th><th>Time</th><th>Action</th></tr></thead><tbody>';
    $info .= $newinfo;
	$info .="</tbody></table>";
}
elsif ( $type eq "userlog" )
{
    &GetCookies('username');    my $username=$Cookies{username};
    $info=runCommand(command=>'cat', params=>$gUSERACTIONLOG_Read);
    if ( !$info ) 
    { 
        $info="!! Empty Log !!<br>"; 
    }
    my @info=split(/\n/,$info);
    my $newinfo;
    if ( $username eq "cksupport" )
    {
      foreach my $linelog ( @info )
      {
          @colstring = split(/ /,$linelog);
		  $colstring[2]= sprintf("%02d",$colstring[2]);
			$ttable  = "";
			$ttable .='<tr><td noWrap>';
		

			for($k = 1;$k<5;$k++){
			$ttable .=$colstring[$k]." ";
			}
			$ttable .="</td>";
		
			$ttable .="<td>".$colstring[5]."</td>";
			$ttable .="<td>";
			for($k = 6;$k<=$#colstring;$k++){
			$ttable .=$colstring[$k]." ";
			}
			$ttable .="</td></tr>";
	
			$newinfo.=$ttable;
      }
    }
    elsif ( $username eq "root" )
    {
      foreach my $linelog ( @info )
      {
        if ( grep(/cksupport/, $linelog) ){next;}
        else
        {
			@colstring = split(/ /,$linelog);
			$colstring[2]= sprintf("%02d",$colstring[2]);
			$ttable  = "";
			$ttable .='<tr><td noWrap>';
		

			for($k = 1;$k<5;$k++){
			$ttable .=$colstring[$k]." ";
			}
			$ttable .="</td>";
		
			$ttable .="<td>".$colstring[5]."</td>";
			$ttable .="<td>";
			for($k = 6;$k<=$#colstring;$k++){
			$ttable .=$colstring[$k]." ";
			}
			$ttable .="</td></tr>";
	
			$newinfo.=$ttable;
        }
      }
    }
    else
    {
      foreach my $linelog ( @info )
      {
        if ( !grep(/$username/, $linelog) ){next;}
        else
        {
          @colstring = split(/ /,$linelog);
		  $colstring[2]= sprintf("%02d",$colstring[2]);
			$ttable  = "";
			$ttable .='<tr><td noWrap>';
		

			for($k = 1;$k<5;$k++){
			$ttable .=$colstring[$k]." ";
			}
			$ttable .="</td>";
		
			$ttable .="<td>".$colstring[5]."</td>";
			$ttable .="<td>";
			for($k = 6;$k<=$#colstring;$k++){
			$ttable .=$colstring[$k]." ";
			}
			$ttable .="</td></tr>";
	
			$newinfo.=$ttable;
        }
      }
    }
    $info  = '<table id="example" ><thead><tr><th>Time</th><th>Name</th><th>Action</th></tr></thead><tbody>';
    $info .= $newinfo;
	$info .="</tbody></table>";
}
elsif ( $type eq "dhcplog" )
{
    $head.="Show Q-Balancer DHCP Logs ...";
    $info=runCommand(command=>'cat', params=>'/var/lib/dhcp/dhcpd.leases');
    if ( !$info )
    {
    	$info="!! Empty Log !!<br>";
    }
    my @info=split(/\n/,$info);
    my $newinfo;
	
    foreach my $linelog ( @info )
    {
    	if (length($linelog)<2){next;}
		if ( grep(/#/, $linelog) ){next;}
    	else
    	{
			
			if(grep(/{/,$linelog)){
			$ttable ="";
			$ttable .="<tr><td style='width: 200px;'>";
			$linelog =~ s' {'';
			$ttable .=$linelog.'</td><td>';
			$newinfo.=$ttable;
			next;
			}
			$linelog =~ s';'';
    		$newinfo.=$linelog.'<br />';
    	}
    }
	$info= '<table id="example" ><thead><tr><th>lease IP</th><th>Action</th></tr></thead><tbody>';

    $info.=$newinfo;
	$info.="</tbody></table>";
}

print $head."<br>"; 

$info='<pre>'.$info.'</pre>';

print $info; 
$scriptData = '<script type="text/javascript">
$("#example").dataTable({
		
		"iDisplayLength": 50,
		"bPaginate": false,
		"bInfo": false
		
		

	});


</script> ';
print qq ($scriptData</body></html>);
