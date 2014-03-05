#!/usr/bin/perl

use CGI;
use XML::Simple;
use File::Find;

require ("/usr/local/apache/qb/global.cgi");
my $form=new CGI;
my $id = $form->param("id");
my $pkginfo = `cat /mnt/conf/pkginfo|grep \"VERSION DETAIL\"`;
$pkginfo =~ s/VERSION DETAIL : //g;

print "Content-type:text/html\n\n";

print qq(<table bgcolor="#332211" width="100%" border="0">);
if ($id eq 'dashboard_1')
{
	print qq(<tr bgcolor="#556677" originalColor="#556677" onclick="location.href='/status/system_sel.cgi?id=../sys_status_history.cgi'">);
}
else
{
	print qq(<tr bgcolor="#556677" originalColor="#556677">);
}
if ($id eq 'dashboard_0')
{
    p_td('System Time :');
    my @time=`date`.&p_link('time.cgi');
    p_td(@time);
    
    p_tr('#334455');
    p_td('System Uptime :');
    my @sys_time=`/opt/qb/bin/script/getuptime`;
    p_td(@sys_time);
    
    p_tr('#556677');
    p_td('Firmware Version :');
    $pkginfo .=&p_link('rmconfig.cgi?viewpoint=firmware');
    p_td($pkginfo);
    
    p_tr('#334455');
    p_td('Fsimage Version :');
    my $fsinfo = `cat /mnt/conf/fsimage.ifo|grep \"version\"`;
    $fsinfo =~ s/version = //g;
    p_td($fsinfo);
    
    p_tr('#556677');
    p_td('Libimage Version :');
    my $libinfo = `cat /mnt/conf/libimage.ifo|grep \"version\"`;
    $libinfo =~ s/version= //g;
    p_td($libinfo);

}elsif ($id eq 'dashboard_1')
{
    p_td('CPU Usage(%):');
    p_td('<span id=\'cpu\'></span>');
    
    p_tr('#334455');
    p_td('Memory Usage(M):');
    p_td('<span id="mem"></span>');
        
    #p_tr('#556677');
    #p_td('Cache Usage(M):');
    #p_td('<span id="cache"></span>');
 
    #p_tr('#334455');
    #p_td('Ramdisk Usage(M):');
    #p_td('<span id="ram"></span>');
    
    p_tr('#556677');
    p_td('Active Sessions:');
    p_td('<span id="session"></span>');
 
}elsif ($id eq 'dashboard_2')
{
    p_td('Host Name:');
    my $overview=XMLin('/usr/local/apache/qbconf/overview.xml');
    p_td($overview->{hostname});
    
    p_tr('#334455');
    p_td('Model Name:');
    my @pkginfo = split(/-/, $pkginfo);
    my $modelname = $pkginfo[0].' '.$pkginfo[3].$pkginfo[1];
    p_td($modelname);
    
    p_tr('#556677');
    p_td('MAC Address Range:');
    my $macrange = `/opt/qb/bin/script/getmacrange`;
    p_td($macrange);
}elsif ($id eq 'dashboard_3')
{
    p_td('Attack Type');
    p_td('Traffic Dropped');
    
    my @file=`/bin/cat /mnt/log/alert.log`;
    my $syn_f=0,$tcp_c=0,$port=0;
    foreach my $o (@file)
    {
        if (grep(/syn_flood/,$o) || grep(/icmp_flood/,$o) || grep(/udp_flood/,$o))
        {
            $syn_f++;
        }elsif (grep(/t_connect/,$o) || grep(/u_connect/,$o))
        {
            $tcp_c++;
        }elsif (grep(/port_scan/,$o))
        {
            $port++;
        }
    }     
    p_tr('#334455');
    p_td('SYN/ICMP/UDP Flood');
    p_td($syn_f);

    p_tr('#556677');
    p_td('TCP/UDP Connection Limit');
    p_td($tcp_c);
    
    p_tr('#334455');
    p_td('Port Scan');
    p_td($port);
    
}elsif ($id eq 'dashboard_4')
{
    p_td('IP');
    p_td('Flows(%)');
    
    my $index=1;
    my $check=0;
    my $now_data=`date "+%Y%m%d%H%M" -d'-2 min'`;
    my $now_data_Y=`date "+%Y"`;
    my $now_data_m=`date "+%m"`;
    my $now_data_d=`date "+%d"`;
    $now_data_Y=~ s/\s+//;
    $now_data_m=~ s/\s+//;
    $now_data_d=~ s/\s+//;
    my $data = "/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -s srcip/flows -n 10 -r /mnt/tclog/nfcapd/$now_data_Y/$now_data_m/$now_data_d/nfcapd.$now_data";
    my $path= "-e /mnt/tclog/nfcapd/$now_data_Y/$now_data_m/$now_data_d/nfcapd.$now_data";
    if($path)
    {
    while($index eq '1')
    {
        my @yy = `$data`;
    	foreach my $a (@yy)
    	{
            if (!grep(/(\d+)\.(\d+)\.(\d+)\.(\d+)/,$a) || grep(/172.31.3/,$a) || grep(/8.8./,$a)){next;}
	    if ($index > 3){last;}
            my $bgcolor=($index % 2) ? ( '#334455' ) : ( '#556677' );
            p_tr($bgcolor);
    	    $a=~s/\s+/ /g;
    	    $a=~s/\(\s/\(/g;
    	    my @ffile = split(/\s/,$a);
    	    p_td($ffile[4]);
    	    p_td($ffile[5]);
    	    $index++;
       }
       if ($index eq 1 && $check > 0 )
       {
           break;
       }
       $check++;
   }
   }
}elsif ($id eq 'dashboard_5')
{
    p_td('Soure:Port');
    p_td('Direction');
    p_td('Destination:Port');
    p_td('Protocol');
    
    my $now_data=`date "+%Y%m%d%H%M" -d'-1 min'`;
    my $now_data_Y=`date "+%Y"`;
    my $now_data_m=`date "+%m"`;
    my $now_data_d=`date "+%d"`;
    $now_data_Y=~ s/\s+//;
    $now_data_m=~ s/\s+//;
    $now_data_d=~ s/\s+//;
    my $data = "/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -o line -c 20 -r /mnt/tclog/nfcapd/$now_data_Y/$now_data_m/$now_data_d/nfcapd.$now_data";
    my $index=1;
    my $check=0;
    my $path="-e /mnt/tclog/nfcapd/$now_data_Y/$now_data_m/$now_data_d/nfcapd.$now_data";
    if($path)
    {
    while($index eq '1')
    {
    	my @yy = `$data`;
    	foreach my $a (@yy)
    	{
            if (!grep(/(\d+)\.(\d+)\.(\d+)\.(\d+)/,$a) || grep(/172.31.3/,$a) ||grep(/127.0.0.1/,$a) || grep(/8.8./,$a)){next;}
            if ($index > 3){next;}
            my $bgcolor=($index % 2) ? ( '#334455' ) : ( '#556677' );
            p_tr($bgcolor);
            $a=~s/\s+/ /g;
            $a=~s/\(\s/\(/g;
            my @ffile = split(/\s/,$a);
            p_td($ffile[4]);
            p_td($ffile[5]);
            p_td($ffile[6]);
            p_td($ffile[3]);
	    $index++;
    	}
       if ($index eq 1 && $check > 0 )
       {
           break;
       }
       $check++;
    }
    }
}elsif ($id eq 'dashboard_6')
{
    my $qbsn = `cat /mnt/conf/qbsn`;
    my $registered_date = '';
    my $needregister = 1;
    my $registered_date_sec;
    if (open(INSDATE, "/mnt/conf/insdate"))
    {
        $registered_date_sec=`/usr/local/apache/qb/setuid/run /bin/cat /mnt/conf/dtstamp.dc`;
	if ( $registered_date_sec ne '' )
	{
	    $registered_date=`date -d \"1970-01-01 UTC $registered_date_sec seconds\"`;
	}
    }else
    {
        $needregister = 0;
    }
    close(INSDATE);
    
    my $Warranty_time=`/usr/local/apache/qb/setuid/run /bin/cat /tmp/init|grep Warranty|tail -n 1|awk '{print $2}'`;
    my $Reg_Warranty_time;
    $Warranty_time=~s/\n//g;
    $Warranty_time=~s/Warranty //g;
    if ( $registered_date_sec ne '' )
    {
        $Reg_Warranty_time=365 * 86400 + $registered_date_sec;
    }
    if ( $Warranty_time ne '' )
    {
        @Warranty_time_date=`/bin/date -d \"1970-01-01 UTC $Warranty_time seconds\"`;
        
        if ( $Reg_Warranty_time >= $Warranty_time )
        {
            $Warranty_time_date=`/bin/date -d \"1970-01-01 UTC $Reg_Warranty_time seconds\"`;
        }else
        {
            $Warranty_time_date=`/bin/date -d \"1970-01-01 UTC $Warranty_time seconds\"`;
        }
    }
    p_tr('#334455');
    p_td('Serial Number:');
    p_td($qbsn);
    
    p_tr('#556677');
    p_td('Registered Date:');
    if ( $registered_date_sec eq '' && $needregister )
    {
        p_td('<font color="red">Not registered</font>');
        if ( !$gENABLEVM )
        {
       	    p_tr('#556677');
            p_td('Register Within:');
            p_td(`/usr/local/apache/qb/setuid/run /opt/qb/bin/script/trialtime`);
        }
    }else
    {
        p_td($registered_date);
    }
    
    p_tr('#334455');
    if ( $gENABLEVM )
    {
    	p_td('License Expiry:');
        p_td(`/usr/local/apache/qb/setuid/run /opt/qb/bin/script/licensetime`);
    }else
    {
    	p_td('Warranty Expiry:');
        p_td($Warranty_time_date);
    }
    
}elsif ($id eq 'dashboard_7')
{
    my $ispref=XMLin('/usr/local/apache/active/basic.xml');
    my $isplist=$ispref->{isp};
    
    p_td('&#32 ISP');
    p_td('&#32 System IP');
    p_td('&#32 Status');
    my $index=0;
    foreach my $isp ( @$isplist )
    {
        if ( $index > 2){p_tr($bgcolor);p_td('&#32:');p_td('&#32:');p_td('&#32:');last;}
        if ( $isp->{iid} eq 'system' ) { next; }
        if ( $isp->{isptype} ne 'tunnel' &&  $isp->{isptype} ne 'ipsec' && $isp->{isptype} ne 'dtunnel' )
        {
            my $bgcolor=($index % 2) ? ( '#556677' ) : ( '#334455' );
            p_tr($bgcolor);
       	    p_td('&#32ISP'.$isp->{iid}.' - '.$isp->{ispname});
       	    p_td('&#32 '.$isp->{systemip}); 
       	    my $imgsrc = ( $isp->{alive} ) ? ( 'alive.png' ) : ( 'dead.png' );
       	    p_td('<img src="image/'.$imgsrc.'" width="14" height="14" border="0" />');
    	    $index++;
    	}
    }
}elsif ($id eq 'dashboard_8')
{
    my $zoneref=XMLin('/usr/local/apache/active/zonecfg.xml');
    my $zonelist=$zoneref->{nat};
    p_td('&#32 Interface');
    p_td('&#32 Network');
    p_td('&#32 IP / Gateway');
    my $index=0;
    foreach my $zone ( @$zonelist )
    {
        if ( $zone->{natid} eq 'system' ) { next; }
        my $bgcolor=($index % 2) ? ( '#556677' ) : ( '#334455' );
        p_tr($bgcolor);
        p_td('&#32 '.$zone->{nic});
        p_td('&#32 '.$zone->{network});
        p_td('&#32 '.$zone->{ip});
        $index++;
    }
    
}elsif ($id eq 'dashboard_9')
{
    find( { wanted => sub { push(@FileList, $_) }, no_chdir => 1 },'/proc/net/ipt_account/' );
    print qq (<table bgcolor="#332211" width="100%" border="0" id="tables">);
    print qq (<thead><tr><th style="width: 300px;">IP</th>);
    print qq (<th style="width: 300px;">Download</th>);
    print qq (<th style="width: 300px;">Upload</th></tr></thead>);
    foreach my $id (@FileList)
    {
	$id  =~ s/\/proc\/net\/ipt_account\///g;
	if (grep(/\/proc\/net\/ipt_account/,$id)){next;}
	my @tttt = `/usr/local/apache/qb/setuid/run /bin/sh /usr/local/apache/qb/setuid/reset.sh $id`;
	sleep 1;
	my @data = `/usr/local/apache/qb/setuid/run /bin/cat /proc/net/ipt_account/$id`;
	my $index = 0;
	my $tmpip = '';
	foreach my $line (@data)
	{
	    my @record = split(/ /, $line);
	    my $ip = $record[2];
	    if ( $tmpip ne $ip )
	    {
	        my @total_data = split(/ /, $line);
	        my @number = split(/\./, $ip);
	        my $nb = $number[3];
	        my $download = sprintf ("%.2f",(($total_data[19]/1024)*8));
	        my $upload = sprintf ("%.2f",(($total_data[5]/1024)*8));
	        if ($nb ne "0")
	        {
        	    p_tr('#556677');
        	    p_td($ip);
        	    p_td($download." Kbps");
        	    p_td($upload." Kbps");
	        }
	        $tmpip = $ip;
	        $index++;
	    }
	}
    }
}elsif ($id eq 'dashboard_10')
{
    my $dmzref=XMLin('/usr/local/apache/active/dmzreg.xml');
    my $dmzlist=$dmzref->{host};
    p_td('&#32 ISP');
    p_td('&#32 Pass Through IP ');
    my $index=0;
    @$dmzlist = sort fwmark_sort_by_dest @$dmzlist;
    foreach my $dmz ( @$dmzlist )
    {
        if ( $dmz eq 'system' ) { next; }
        my $bgcolor=($index % 2) ? ( '#556677' ) : ( '#334455' );
        p_tr($bgcolor);
        p_td('&#32 ISP'.$dmz->{isp});
        p_td('&#32 '.$dmz->{ip});
        $index++;
    }
}

print qq(</tr></table>);
sub p_link
{
    my @link = @_;
    return "<a href=\'@link\' style='text-decoration:none' ><img src='image/link.gif' width='12' height='12' border='0' /></a>";
}

sub p_td
{
    my @data = @_;
	if ($id eq 'dashboard_1')
	{
		if (-e "/usr/local/apache/qb/status/cpu.status")
		{
		my $cpuusage = `cat /usr/local/apache/qb/status/cpu.status`;
		}
		#my $cpuusage = system("/usr/local/apache/qb/status/getsysstatus.cgi");
		#my $cpuusage = runCommand(command=>'/usr/local/apache/qb/status/getsysstatus.cgi', params=>'');
		if (-e "/usr/local/apache/qb/status/memory.status")
		{
		my $memusage = `cat /usr/local/apache/qb/status/memory.status`; 
		$memusage =~ s/,.*//g;
		}
		if (-e "/usr/local/apache/qb/status/cache.status")
		{
		my $cacheusage = `cat /usr/local/apache/qb/status/cache.status`;
		$cacheusage =~ s/,.*//g;		
		}
		if (-e "/usr/local/apache/qb/status/ramdisk.status")
		{
		my $ramdiskusage = `cat /usr/local/apache/qb/status/ramdisk.status`;
		$ramdiskusage =~ s/,.*//g; 		
		}
		if (-e "/usr/local/apache/qb/status/session.status")
		{
		my $session = `cat /usr/local/apache/qb/status/session.status`;
		my @session = split(/,/, $session);
		}
		my $sessionusage = $session[0];
		my $showsession = $session[3].'/'.$session[1];
		$showsession =~ s/\s//g;
		my $use='';
		if(grep(/^CPU/, @data)){$use=$cpuusage;}
		if(grep(/^Memory/, @data)){$use=$memusage."M";}
		if(grep(/^Cache/, @data)){$use=$cacheusage."M";}
		if(grep(/^Ramdisk/, @data)){$use=$ramdiskusage."M";}
		if(grep(/^Active/, @data)){$use=$showsession;}
		print qq(<td class="body" height="20" align="center" title="$use">@data</td>);
	}
	else
	{
		print qq(<td class="body" height="20" align="center" >@data</td>);
	}
}

sub p_tr
{
    my @data = @_;
	if ($id eq 'dashboard_1')
	{
		print qq(</tr><tr bgcolor="@data" originalColor="@data" onclick="location.href='sys_status_history.cgi'">);
	}
	else
	{
		print qq(</tr><tr bgcolor="@data" originalColor="@data">);
	}
}

sub fwmark_sort_by_dest
{
    my @afields=split(/\.|\//,$a->{ip});
    my @bfields=split(/\.|\//,$b->{ip});
    foreach my $index ( 0..4 )
    {
        $avalue=$afields[$index];
        $bvalue=$bfields[$index];
        if ( $avalue ne $bvalue ) { last; }
    }
    $avalue <=> $bvalue;
}


