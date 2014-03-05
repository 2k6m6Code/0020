#!/usr/bin/perl -w
require ("../qbmod.cgi");
use CGI;
my $form= new CGI;
my $tool=$form->param('tool');
my $action=$form->param('action');

#==============================================
#for ping
my $ping_count=$form->param('ping_count');
my $pingoptions=$form->param('pingoptions');
my $pingpath=$form->param('pingpath');

#==============================================
#Brian 2005-0907
#for ethtool
my $ethtool_duplex=$form->param('ethtool_duplex');
my $ethtool_speed=$form->param('ethtool_speed');
my $ethtool_nic=$form->param('ethtool_nic');
my $ethtool_nego=$form->param('ethtool_nego');

#==============================================
#Brian 2005-0929
#for modify arp cache 
my $arpcache_nic=$form->param('arpcache_nic');
my $arpcache_sip=$form->param('arpcache_sip');
my $arpcache_tip=$form->param('arpcache_tip');
my $arpcache_mac=$form->param('arpcache_mac');
my $packet_num=$form->param('packet_num');

#==============================================
#Brian 2005-1123
#Bind Mac Address 
my $bindmac_nic=$form->param('bindmac_nic');
my $bindmac_tip=$form->param('bindmac_tip');
my $bindmac_mac=$form->param('bindmac_mac');
my $bindmac_save=$form->param('bindmac_save');

#==============================================
#Brian 2010-1019
#Open Port Check
my $telnet_dstip=$form->param('telnet_dstip');
my $telnet_dstport=$form->param('telnet_dstport');

#==============================================
#Brian 2006-0912
#Measure ISP Download Speed 
my $isp_iid=$form->param('isp_iid');
my $local_ip=maintainBasic(action=>'GETIPBYIID', iid=>$isp_iid);
#my $local_ip=$form->param('local_ip');
my $remote_file=$form->param('remote_file');
my $login_user=$form->param('login_user');
my $login_password=$form->param('login_password');

#==============================================
#Brian 2006-0915
#Measure Tunnel Speed 
my $tunnel_iid=$form->param('tunnel_iid');
my $tunnel_src=maintainBasic(action=>'GETIPBYIID', iid=>$tunnel_iid);
my $tunnel_dst=maintainBasic(action=>'GETGWBYIID', iid=>$tunnel_iid);
        
#my $tunnel_src=$form->param('tunnel_src');
#my $tunnel_dst=$form->param('tunnel_dst');

#==============================================
#Brian 2009-1117
#Measure Tunnel Speed by Pool
my $tunnel_pool=$form->param('tunnel_pool');
my $ispinfo = XMLread($gPATH.'basic.xml' );
my $allisp=$ispinfo->{isp};
my $rtable  = XMLread($gPATH.'rtable.xml');
my $temptables=$rtable->{table};
my $target;
foreach my $table ( @$temptables ) { if ( $table->{table_num} eq $tunnel_pool ) { $target=$table; last; } }

#==============================================
#Brian 2011-0412 Measure Speed and Latency 
my $speedtest_iid=$form->param('speed_latency_link');
my $max_latency=$form->param('max_latency');
my $target_latency;
if ($speedtest_iid =~m/pool/)
{
  my $pool_iid=$speedtest_iid;
  $pool_iid=~s/pool//;
  foreach my $table ( @$temptables ) { if ( $table->{table_num} eq $pool_iid ) { $target_latency=$table; last; } }
}                  
#==============================================
#Brian 
#Measure Packet loss
my $tunnel_iid_pl=$form->param('tunnel_iid_pl');
my $tunnel_src_pl=maintainBasic(action=>'GETIPBYIID', iid=>$tunnel_iid_pl);
my $tunnel_dst_pl=maintainBasic(action=>'GETGWBYIID', iid=>$tunnel_iid_pl);

#my $tunnel_src_pl=$form->param('tunnel_src_pl');
#my $tunnel_dst_pl=$form->param('tunnel_dst_pl');

#==============================================
#20100330 Brian Reboot time
#Measure Packet loss
my $reboot_time=$form->param('reboot_time');

#==============================================
#for traceroute
my $tracerouteoptions=$form->param('tracerouteoptions');
my $traceroutepath=$form->param('traceroutepath');

#==============================================
#for arping
my $arping_sip=$form->param('arping_sip');
my $arping_count=$form->param('arping_count');
my $arping_dev=$form->param('arping_dev');
my $arping_dip=$form->param('arping_dip');
my $tcobj=$form->param('tcobj');
my @tcdev=$form->param('tcdev');

#==============================================
#for tcpdump
my $tcpdumpoptions=$form->param('tcpdumpoptions');

#==============================================
#for arp ...nancy 041130
# file : /proc/qbalancer/qbreport
# ln1:Iface gateway ip       MAC                T in        T out       A in    A out   conns  KA  rtt dead
# ln2:eth0       210.64.6.238  00:30:DA:13:28:9B  2706489636  1480969569  0       0       11310310  0  0
# ln3:mpv0       172.16.29.235  00:00:00:00:00:00  14551960    43682620    0       0       0    0  0  1
# ln4:eth2       61.222.199.1  00:D0:59:A5:AA:6E  3399982480  590923645   0       0       9966750  0  0
# ln5:mpv1       172.16.29.2  00:00:00:00:00:00  14597304    43724744    0       0       0    0  0  1
# ln6:eth3       192.168.2.1  00:E0:4C:59:04:44  893508001   205213553   0       0       1493710  0  0
# ln7:...
sub get_qbreport_mac()
{
    my $count=0;
    my $info=runCommand(command=>'cat', params=>'/proc/qbalancer/qbreport');
    my @infolist=split(/\n/,$info);

    print "<br>===================================================";
    if (!@infolist) {print "<br>No Run-time Gateway Mac.<br>";}

    foreach (@infolist) {
        chomp; $count++; 
        if ($count==1) {
            print "<br>Run-time Gateway Mac:<p>";
            next;
        }
        my @repinfo=split(/\s+/, $_);
        my ($interface, $gwip, $mac) = ($repinfo[0], $repinfo[1], $repinfo[2]);

        my $count1=0;
        foreach ( split(/:/,$mac) ) {
            if ($_ eq "00") {$count1++;}
            else {last;}
        }
        print "on $interface ($gwip) ";
        ($count1<6) ? print "at $mac<br>" : print "<br>";
    }
}

my $runstring=$gRUN;

print "Content-type:text/html \n\n";
print qq (<html><head><link rel="stylesheet" href="../gui.css" type="text/css"></head><body class='message'>);

if ( $action eq "stop" && $tool eq "ping" )
{
    $runstring.=qq ( killall -2 $tool);
}
elsif ( $action eq "stop" )
{
    $runstring.=qq ( killall -9 $tool);
}
elsif ( $action eq "start" )
{
    if ( $tool eq "ping" )       
    {
        my $ispfwmark=( $pingpath ) ? ('0x'.dec2hex(1000+($pingpath))) : ( 'TOLAN' ) ;
        my $result;
        my $systemip=maintainBasic(action=>'GETIPBYIID', iid=>$pingpath);
        if ( $ping_count ne "0" )        { $pingoptions.=" -c ".$ping_count; }
        if ( $pingpath ne "" )
        {
          #$result=runCommand(command=>'ping', params=>qq( -I $systemip  -n $pingoptions ) );
          #$runstring.=qq(ping -I $systemip  -n $pingoptions ); #busybox version doesn't support it
          $runstring.=qq(ping -I $systemip  $pingoptions ); 
          #if ( $result eq "" )
          #{
            #print qq ( Fail to ping destination address from ISP$pingpath $systemip... )
          #}        
        }
        else
        {
          if ( $ping_count eq "0" )        { $pingoptions.=" -c 20"; }
          $result=runCommand(command=>'pingviaisp.sh', params=>qq($ispfwmark  ISP$pingpath  \" $pingoptions \") );
          if ( $ping_count eq "0" )        { print qq ( Sent 20 PING packets from LAN ...); }
          else { print qq ( Sent $ping_count PING packets from LAN ...); }
          print "<br>";
          $result=~s/\n/<br>/g;
          print qq ( $result );
          exit(0);
        }
	#$result=~s/\n/<br>/g;
        #print qq ( $result );
        #exit(0);
    }

#Brian 2005-0909
    elsif ( $tool eq "ethtool")
    {   
        my $params='';
        if ( $ethtool_nic && $ethtool_speed ne "Query" && $ethtool_duplex ne "Query" ) { $params.=" -s ".$ethtool_nic;}
        if ( $ethtool_speed ne "Query")          { $params.=" speed ".$ethtool_speed;}
        if ( $ethtool_duplex ne "Query" )        { $params.=" duplex ".$ethtool_duplex;}
        if ( $ethtool_speed ne "Query" && $ethtool_duplex ne "Query" && $ethtool_nego eq "Off") {$params.=" autoneg off ";}
        if ( $ethtool_speed ne "Query" && $ethtool_duplex ne "Query" && $ethtool_nego eq "On")  {$params.=" autoneg on ";}
	
        my $result=runCommand(command=>'/opt/qb/bin/script/ethtool', params=>qq($params));
	$result=~s/\n/<br>/g;
	my $ethinfo=runCommand(command=>'/opt/qb/bin/script/ethtool', params=>qq($ethtool_nic));
	$ethinfo=~s/\n/<br>/g;

        if ( $ethtool_speed ne "Query" && $ethtool_duplex ne "Query") 
       {
           # add and write ethtool set
            open(ETHSET, ">> /usr/local/apache/active/ethset");
            print ETHSET "/opt/qb/bin/script/ethtool "; 
            print ETHSET qq($params)."\n";
            close (ETHSET);
            
           # show change result
            print "Changing NIC ( $ethtool_nic ) Speed and Duplex....";
            print qq ( $result );
            print qq ( $ethinfo );
            
           #save config
            $params=" /usr/local/apache/active/ethset /mnt/qb/conf/ethset ";
	    my $cfginfo=runCommand(command=>'cp', params=>qq($params));
	    $cfginfo=~s/\n/<br>/g;
            print qq ( $cfginfo );
       }
        else
       {
           # show query result
             print qq ( $ethinfo );
       }
 
        exit(0);
    }

#Brian 2010-1019
    elsif ( $tool eq "telnet")
    {   
        my $params='';
        if ( $telnet_dstip )        { $params.=" ".$telnet_dstip;}
        if ( $telnet_dstport )      { $params.=" ".$telnet_dstport;}
	
        my $result=runCommand(command=>'/usr/bin/telnet', params=>qq($params < /dev/null 2>&1 | grep Connected ));
	$result=~s/\n/<br>/g;
        # show check result
        print "<br>Port Check Result:<p> ";
        if ( $result eq ""){print qq ( Can't connect to $telnet_dstip 's port $telnet_dstport.");}
        else
        { 
         print qq ( $params );
         print qq ( $result );
         print qq ( Port $telnet_dstport tested OK!!!");
        }
        exit(0);
    }

#Brian 2006-0912
    elsif ( $tool eq "wget")
    {   
        my $params='';
        if ( $remote_file )        { $params.=" ".$remote_file;}
        if ( $local_ip )           { $params.=" --bind-address=".$local_ip;}
        if ( $login_user )         { $params.=" --user=".$login_user;}
        if ( $login_password )     { $params.=" --password=".$login_password;}
	
        runCommand(command=>'/sbin/wget', params=>qq($params -T 10 -t 1 -o /tmp/wgetresult -O /tmp/measure_file));
        runCommand(command=>'/bin/rm', params=>qq( -f /tmp/measure_file));
        #my $result=runCommand(command=>'/bin/grep', params=>qq( \/s /tmp/wgetresult));
        my $result=runCommand(command=>'/bin/grep', params=>qq( -v 4000 /tmp/wgetresult));
        runCommand(command=>'/bin/rm', params=>qq( -f /tmp/wgetresult));
	$result=~s/\n/<br>/g;
	$result=~s/tmp//g;
       
        # show measure result
        print "<br>Measure Result:<p> ";
        if ( $result eq ""){print qq ( Please Check your "Options of Measure Info.");}
        print qq ( $result );
        exit(0);
    }

#Brian 2006-0915
    elsif ( $tool eq "tunnel_speed")
    {   
        
        my $params='';
        if ( $tunnel_dst )        { $params.=" http://".$tunnel_dst.":4000/clean/testfile";}
        if ( $tunnel_src )         { $params.=" --bind-address=".$tunnel_src;}
	
        runCommand(command=>'/sbin/wget', params=>qq($params -T 10 -t 1 -o /tmp/wgetresult.$tunnel_dst -O /tmp/measure_file.$tunnel_dst));
        runCommand(command=>'/bin/rm', params=>qq( -f /tmp/measure_file.$tunnel_dst));
        my $result=runCommand(command=>'cat', params=>qq( /tmp/wgetresult.$tunnel_dst));
        #my $result=runCommand(command=>'/bin/grep', params=>qq( \/s /tmp/wgetresult.$tunnel_dst));
        #my $result=runCommand(command=>'/bin/grep', params=>qq( -v 4000 /tmp/wgetresult.$tunnel_dst));
        runCommand(command=>'/bin/rm', params=>qq( -f /tmp/wgetresult.$tunnel_dst));
	$result=~s/:4000//g;
	$result=~s/http.*//g;
	$result=~s/tmp//g;
	$result=~s/Saving.*//g;
	$result=~s/HTTP/Download/g;
	$result=~s/\n/<br>/g;
        print "<br><p> ";

        # show measure result
        print "<br>Measure Result:<p> ";
        print "<br>Download a file from remote IP:$tunnel_dst<p> ";
        if ( $result eq ""){print qq ( "Measure Error.");}
        print qq ( $result );
        my $delparams=" -rf /tmp/measure_file*";
        runCommand(command=>'rm ', params=>qq($delparams));
        exit(0);
    }

#Brian 2009-1117
    elsif ( $tool eq "tunnel_speed_pool")
    { 
      my $params='';
      my $allpath=$target->{path};

print<<'_EOF_';
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
_EOF_
      foreach my $isp ( @$allisp )
      {
         if ( $isp->{iid} eq 'system' ) { next; }
         foreach my $item ( @$allpath )
         { 
           if ( $item->{isp} == $isp->{iid} )
           { 
              $tunnel_dst=$isp->{gateway};
              $tunnel_src=$isp->{systemip};
              if ( $tunnel_dst )        { $params.="/sbin/wget http://".$tunnel_dst.":4000/clean/testfile";}
              if ( $tunnel_src )         { $params.=" --bind-address=".$tunnel_src."  -T 10 -t 1 -o /tmp/wgetresult.$tunnel_dst -O /tmp/measure_file.$tunnel_dst\|";}
              print "<br>Download a file from remote IP:$tunnel_dst ";
		
           }
         }
      } 
        $params.="cat wgetresult* \>/tmp/wget_total";
        # write wget command.
        open(WGETCMD, ">/tmp/wgetcmd");
        print WGETCMD qq($params)."\n";
        print WGETCMD qq(cat /tmp/wgetresult* \>/tmp/wget_total)."\n";
        close (WGETCMD);
        chmod(0755, "/tmp/wgetcmd");     
        runCommand(command=>'/tmp/wgetcmd', params=>qq());
        #my $result=runCommand(command=>'/bin/grep', params=>qq( -v 4000 /tmp/wget_total));
        my $result=runCommand(command=>'cat', params=>qq( /tmp/wget_total));
	$result=~s/:4000//g;
	$result=~s/http.*//g;
	$result=~s/tmp//g;
	$result=~s/Saving.*//g;
	$result=~s/Giving.*/Please try "Measure Tunnel Speed by Link"/g;
	$result=~s/HTTP/Download/g;
	$result=~s/\n/<br>/g;
        print "<br><p> ";
        print "<br>Measure Result:<p> ";
        if ( $result eq ""){print qq ( "Measure Error.");}
        print qq ( $result );
        my $delparams=" -rf /tmp/measure_file*";
        #runCommand(command=>'rm ', params=>qq($delparams));
        my $delparams_01=" -rf /tmp/wget*";
        #runCommand(command=>'rm ', params=>qq($delparams_01));
        exit(0);
    }

#Brian 2011-0412 Measure Speed and Latency
    elsif ( $tool eq "latency_speed")
    { 
      my $params='';
      #if ($target_latency)
      if ($speedtest_iid =~m/pool/)
      {
       my $allpath=$target_latency->{path};
       foreach my $isp ( @$allisp )
       {
        foreach my $item ( @$allpath )
        { 
          if ( $item->{isp} == $isp->{iid} )
          { 
             $runstring.=qq(/sbin/latency.tst $item->{isp} $max_latency);
             print "<br>Testing Speed on ISP$item->{isp}: From $isp->{systemip} to $isp->{target}";
          }
        }
       }
      }else{
       foreach my $isp ( @$allisp )
       {
          if ( $speedtest_iid == $isp->{iid} )
          { 
             $runstring.=qq(/sbin/latency.tst $speedtest_iid $max_latency);
             print "<br>Testing Speed on ISP$speedtest_iid: From $isp->{systemip} to $isp->{target}";
          }
       }
      }
       
        # write wget command.
        print "<br><p> ";
        print "<br>Measure Result:<p> ";
        if ( $runstring eq ""){print qq ( "Measure Error.");}
    }

#Brian 2006-0920
    elsif ( $tool eq "packet_lost")
    {   
        
        my $params='';
        if ( $tunnel_src_pl )        { $params.=" -I ".$tunnel_src_pl." -s 1500 -c 50 ";}
        if ( $tunnel_dst_pl )        { $params.=$tunnel_dst_pl;}
	
        $runstring.=qq(ping $params);

        # show measure result
        print "<br>Measure Result:<p> ";
        if ( $runstring eq ""){print qq ( "Measure Error.");}
    }

#Brian 2005-0929
    elsif ( $tool eq "arpcache")
    {   
        my $params='';
        if ( $arpcache_nic ) { $params.=$arpcache_nic;}
        my $result=runCommand(command=>'/sbin/ifconfig', params=>qq($params));
        if($result=~/HWaddr *([a-z0-9\:]+)/i)
        { 
          $mac=$1;
        }
        if($result=~/addr: *([a-z0-9\.]+)/i)
        {
          $sip=$1;
        }
        my $modifyparams='';
        if ( $arpcache_nic ) { $modifyparams.=" -i ".$arpcache_nic;}
        if ( $arpcache_tip ) { $modifyparams.=" -d ".$arpcache_tip;}
        if ( $arpcache_sip ) { $modifyparams.=" -s ".$arpcache_sip;}
        #if ( $sip ) { $modifyparams.=" -s ".$sip;}
        if ( $arpcache_mac ) { $modifyparams.=" -t ".$arpcache_mac;}
        if ( $mac ) { $modifyparams.=" -r ".$mac;}
        if ( $packet_num ) { $modifyparams.=" -n ".$packet_num;}
        print "<br>Sender hardware address: $mac \n\n ";
        #print "<br>Sender protocol address: $sip \n\n";
        print "<br>Sender protocol address: $arpcache_sip \n\n";
        print "<br>Target hardware address: $arpcache_tip \n\n";
        print "<br>Target protocol address: $arpcache_mac \n\n";
        print "<br>Sending New ARP Packets from ( $arpcache_nic ) to ($arpcache_tip )....<p>";
        my $modifyresult=runCommand(command=>'/opt/qb/bin/script/arpoison', params=>qq($modifyparams)); 
	$modifyresult=~s/\n/<br>/g;
      # Usage: -i <device> -d <dest IP> -s <src IP> -t <target MAC> -r <src MAC> [-a] [-w time between packets] [-n number to send]
        print "<br>Result:<p> ";
        print qq($modifyresult);
        exit(0);
    }

#Brian 2005-1123
    elsif ( $bindmac_save eq "clear")
    {
        #delete config file
         my $delparams=" -rf /usr/local/apache/qbconf/macset";
         runCommand(command=>'rm ', params=>qq($delparams));
         my $delparams=" -rf /mnt/qb/conf/set/boot/macset";
         runCommand(command=>'rm ', params=>qq($delparams));
         qbSync();
        print "<br>If you want to clear all binded mac,please reboot QB! <p>";
    }
    elsif ( $tool eq "bindmac" && macbind_save ne "clear")
    {   
        my $params='';
        if ( $bindmac_nic ) { $params.=" -i ".$bindmac_nic;}
        if ( $bindmac_tip ) { $params.=" -s ".$bindmac_tip;}
        if ( $bindmac_mac ) { $params.=" ".$bindmac_mac;}
        print "<br>Target hardware NIC: $bindmac_nic \n\n";
        print "<br>Target hardware address: $bindmac_tip \n\n";
        print "<br>Target Mac address: $bindmac_mac \n\n";
        print "<br>Params: $params <p>";
        my $result1=runCommand(command=>'arp ', params=>qq($params)); 
	$result1=~s/\n/<br>/g;
        my $result=runCommand(command=>'arp', params=>'-a -n');
	$result=~s/\n/<br>/g;
	print $result;
     
        if ( $bindmac_save eq "yes")
       {
           # write config
            open(MACSET, ">>/usr/local/apache/qbconf/macset");
            #open(MACSET, ">> /mnt/qb/conf/macset");
            print MACSET "arp "; 
            print MACSET qq($params)."\n";
            close (MACSET);
            
           #save config on boot
            $cpparams=" -f /usr/local/apache/qbconf/macset /mnt/qb/conf/set/boot ";
	    my $cfginfo=runCommand(command=>'cp ', params=>qq($cpparams));
	    $cfginfo=~s/\n/<br>/g;
            print qq ( $cfginfo );
            qbSync();
            print "<br>Mac configurations are all saved on boot!<p>";
       
       }
        
        exit(0);
    }

    elsif ( $tool eq "traceroute" )       
    {
        my $ispfwmark=( $traceroutepath ) ? ('0x'.dec2hex(1000+($traceroutepath))) : ( 'TOLAN' ) ;
        my $systemip=maintainBasic(action=>'GETIPBYIID', iid=>$traceroutepath);
        my $result;

        if ( $traceroutepath ne "" )
        {
          print qq ( Sent traceroute packets from ISP$traceroutepath ... );
          print "<br>";
          $runstring.=qq( traceroute -s $systemip $tracerouteoptions );
          if ( $runstring eq "" )
          {
            print qq ( Fail to traceroute $tracerouteoptions from ISP$traceroutepath $systemip... )
          }        
        }
        else
        {
          #$result=runCommand(command=>'tracerouteviaisp.sh', params=>qq($ispfwmark  ISP$traceroutepath  \"$tracerouteoptions \") );
          $runstring.=qq( /usr/local/apache/qb/setuid/tracerouteviaisp.sh $ispfwmark ISP $tracerouteoptions );
          print qq ( Sent traceroute packets from LAN ... );
          print "<br>";
        }

	#$result=~s/\n/<br>/g;
        #print qq ( $result );
        #exit(0);
    }
    elsif ( $tool eq "arping")
    {   
        my $params='';
        if ( $arping_sip )          { $params.=" -s ".$arping_sip;   }
        if ( $arping_count )        { $params.=" -c ".$arping_count; }
        if ( $arping_dev )          { $params.=" -I ".$arping_dev;   }
        if ( $arping_dip )          { $params.=' '.$arping_dip;      }
        
	runCommand(command=>'sysctl', params=>qq(-w net.ipv4.ip_nonlocal_bind=1)); # 20080513 Brian Support alter remote arp table
	my $result=runCommand(command=>'arping', params=>qq($params));
	$result=~s/\n/<br>/g;
        print qq ( $result );
	runCommand(command=>'sysctl', params=>qq(-w net.ipv4.ip_nonlocal_bind=0));
        exit(0);
    }
    elsif ( $tool eq "tcpdump" )    
    { 
        my $cmd=locateCommand(command=>'tcpdump');

        # "-l" is an option for tcpdump to make stdout line buffered. Modified  since 2003.04.02 15:38  2.1.5.0007
        $tcpdumpoptions=~s/\|/<br>/g;#Fix a security hole
        $runstring.=qq($cmd -l -n $tcpdumpoptions); 
    }
    elsif ( $tool eq "arp" )
    {
        my $result=runCommand(command=>'arp', params=>'-a -n');
	$result=~s/\n/<br>/g;
	print $result;
        
	get_qbreport_mac(); # nancy 041130
        
	exit (0);
    }
    elsif ( $tool eq "tc" )
    {
        foreach my $dev ( @tcdev )
        {
            my $params='';

            if ( $tcobj eq 'filter' )     { $params.=qq( -s $tcobj show parent 1: ); }
            else                          { $params.=qq( -s $tcobj show ); }
                
            $params.=qq( dev $dev); 
            
            my $cmd=locateCommand(command=>'tc');

            $runstring.=qq ($cmd $params <<and>>);
        }
    }
    elsif ( $tool eq "restartqbserv" )
    {
        print qq ( Restart QB Engine ...OK !! );
        my $cmd=locateCommand(command=>'killall');
        #$runstring.=qq ($cmd -9 qbserv );
        $runstring.=qq ($cmd -9 qbserv | sleep 20 | /opt/qb/bin/script/qbserv.chk & );
    }
#Brian 2005-0913    
    elsif ( $tool eq "rebootqb" )
    {
        if ( $reboot_time eq '24')          
        { 
         print "<br>Rebooting QB now....Please wait a moment.....<p>";
         runCommand(command=>'/opt/qb/bin/script/rebootqb', params=>'');
	 exit (0);
	}
        else
        {
         #Permission Denied
         #my $CRON_FILE="/etc/crontab";
         #open( FILE, ">>$CRON_FILE" ) || die "$!\n";
         #print FILE "\n# added to reboot QB\n00   $reboot_time  * * *  root      /opt/qb/bin/script/rebootqb\n";
         #close(FILE);
         print "<br>Setuping QB to reboot.....<p>";
         runCommand(command=>'/opt/qb/bin/script/rebootqb', params=>qq($reboot_time));
         print "Done.";
        }
    }
}

# For Debug Mode
print qq(<pre>);

$runstring=~s/;.*|<<and>>$//g;

$runstring=~s/<<and>>/;$gRUN/g;

#print qq ($runstring);

exec($runstring);
