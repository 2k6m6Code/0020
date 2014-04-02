#!/usr/bin/perl

use CGI;
require ("/usr/local/apache/qb/qbmod.cgi");

my $cgi=new CGI;
#require ("./qblib/neweditdos.lib");
#require ("./qblib/neweditflood.lib");
#require ("./qblib/neweditportscan.lib");
makeshell();
sub makeshell
{
  my $DQOSSHELL="/usr/local/apache/qbconf/dqos.sh";
    my $IPTCMD="/usr/local/sbin/iptables -t mangle";
    my $SHELLHEAD="#!/bin/sh ";
    my $LOGLEVEL="--log-level alert ";
    my $LIMITBURST=5;

    open(DQOS, ">$DQOSSHELL");
                
    my $dqos=XMLread('/usr/local/apache/qbconf/dqos.xml');
	
	my $newflood=XMLread('/usr/local/apache/qbconf/newflood.xml');
	my $newdos=XMLread('/usr/local/apache/qbconf/newdos.xml');
	my $newportscan=XMLread('/usr/local/apache/qbconf/newportscan.xml');
	
	my $doslistFLOOD=$newflood->{newflood};
	my $doslistCOD=$newdos->{newdos};
	my $doslistPSD=$newportscan->{newportscan};
	
	my $host=XMLread('/usr/local/apache/qbconf/host.xml');
	my $hostlist=$host->{host};
	
    print DQOS qq ($SHELLHEAD \n\n);

    my $dosref=$dqos->{dos};
    #print DQOS qq ($IPTCMD -X DEF \n);
    #print DQOS qq ($IPTCMD -N DEF \n);
    
    #print DQOS qq ($IPTCMD -X COD \n);
    #print DQOS qq ($IPTCMD -N COD \n);                
    
    #print DQOS qq ($IPTCMD -X PSD \n);
    #print DQOS qq ($IPTCMD -N PSD \n);
        
    #print DQOS qq ($IPTCMD -X ICMP \n);
    #print DQOS qq ($IPTCMD -N ICMP \n);
	
	print DQOS qq ($IPTCMD -X PORTSCAN \n);
	
	#my $CMDFLOOD=$IPTCMD." -A ICMP";
	#my $CMDCOD=$IPTCMD." -A COD";
	my $CMDFLOOD=$IPTCMD." -A PREROUTING";
	my $CMDCOD=$IPTCMD." -A PREROUTING";
	my $CMDPSD=$IPTCMD." -A PREROUTING";
#===================================================
#	COD
#===================================================
	foreach my $ip (@$doslistCOD)
	{
		if($ip->{type} eq 'ip')
		{
			#if logset=true write
			
			if($ip->{enable} eq 'true')
			{
				if ($ip->{cls} eq 'tcp')
				{
					print DQOS qq($CMDCOD -p tcp -s $ip->{dosip} --syn -m connlimit --connlimit-above $ip->{ipnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix t_connect: \n); 
				print DQOS qq($CMDCOD -p tcp -s $ip->{dosip} --syn --dport $ip->{port} -m connlimit --connlimit-above $ip->{portnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix t_connect: \n);
				print DQOS qq($CMDCOD -p tcp -d $ip->{dosip} --syn -m connlimit --connlimit-above $ip->{ipnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix t_connect: \n); 
				print DQOS qq($CMDCOD -p tcp -d $ip->{dosip} --syn --dport $ip->{port} -m connlimit --connlimit-above $ip->{portnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix t_connect: \n);

				    print DQOS qq($CMDCOD -p tcp -s $ip->{dosip} --syn -m connlimit --connlimit-above $ip->{ipnum} -j DROP \n);
				    print DQOS qq($CMDCOD -p tcp -s $ip->{dosip} --dport $ip->{port} --syn -m connlimit --connlimit-above $ip->{portnum} -j DROP \n);
				    print DQOS qq($CMDCOD -p tcp -d $ip->{dosip} --syn -m connlimit --connlimit-above $ip->{ipnum} -j DROP \n);
				    print DQOS qq($CMDCOD -p tcp -d $ip->{dosip} --dport $ip->{port} --syn -m connlimit --connlimit-above $ip->{portnum} -j DROP \n);
				}
				
				if ($ip->{cls} eq 'udp')
				{
				print DQOS qq($CMDCOD -p udp -s $ip->{dosip} -m connlimit --connlimit-above $ip->{ipnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix u_connect: \n); 
				print DQOS qq($CMDCOD -p udp -s $ip->{dosip} --dport $ip->{port} -m connlimit --connlimit-above $ip->{portnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix u_connect: \n);
				print DQOS qq($CMDCOD -p udp -d $ip->{dosip} -m connlimit --connlimit-above $ip->{ipnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix u_connect: \n); 
				print DQOS qq($CMDCOD -p udp -d $ip->{dosip} --dport $ip->{port} -m connlimit --connlimit-above $ip->{portnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix u_connect: \n);
				
				print DQOS qq($CMDCOD -p udp -s $ip->{dosip} -m connlimit --connlimit-above $ip->{ipnum} -j DROP \n);
				print DQOS qq($CMDCOD -p udp -s $ip->{dosip} --dport $ip->{port} -m connlimit --connlimit-above $ip->{portnum} -j DROP \n);
				print DQOS qq($CMDCOD -p udp -d $ip->{dosip} -m connlimit --connlimit-above $ip->{ipnum} -j DROP \n);
				print DQOS qq($CMDCOD -p udp -d $ip->{dosip} --dport $ip->{port} -m connlimit --connlimit-above $ip->{portnum} -j DROP \n);
				}
			}
		}
		if($ip->{type} eq 'host')
		{
			#if logset=true write
			#if ( $ip->{logset} eq 'true' ) 
			#{ 
				foreach my $hostip(@$hostlist)
				{
					if ( $hostip->{hostname} eq "system" ) { next; }
					if ( $hostip->{hostname} eq $ip->{dosip})
					{
						my @splithost=split(',', $hostip->{hostaddress});
						foreach my $splitlist ( @splithost )
						{
							if ($ip->{cls} eq 'tcp')
							{
							print DQOS qq($CMDCOD -p tcp -s $splitlist --syn -m connlimit --connlimit-above $ip->{ipnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix t_connect: \n); 
							print DQOS qq($CMDCOD -p tcp -s $splitlist --syn --dport $ip->{port} -m connlimit --connlimit-above $ip->{portnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix t_connect: \n);
							print DQOS qq($CMDCOD -p tcp -d $splitlist --syn -m connlimit --connlimit-above $ip->{ipnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix t_connect: \n); 
							print DQOS qq($CMDCOD -p tcp -d $splitlist --syn --dport $ip->{port} -m connlimit --connlimit-above $ip->{portnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix t_connect: \n);
							}
							if ($ip->{cls} eq 'udp')
							{
							print DQOS qq($CMDCOD -p udp -s $splitlist -m connlimit --connlimit-above $ip->{ipnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix u_connect: \n); 
							print DQOS qq($CMDCOD -p udp -s $splitlist --dport $ip->{port} -m connlimit --connlimit-above $ip->{portnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix u_connect: \n);
							print DQOS qq($CMDCOD -p udp -d $splitlist -m connlimit --connlimit-above $ip->{ipnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix u_connect: \n); 
							print DQOS qq($CMDCOD -p udp -d $splitlist --dport $ip->{port} -m connlimit --connlimit-above $ip->{portnum} -m limit --limit 1/m -j LOG --log-level alert --log-prefix u_connect: \n);
							}
						}
					}
				}
			#}
			if($ip->{enable} eq 'true')
			{
				foreach my $hostip(@$hostlist)
				{
					if ( $hostip->{hostname} eq "system" ) { next; }
					if ( $hostip->{hostname} eq $ip->{dosip})
					{
						my @splithost=split(',', $hostip->{hostaddress});
						foreach my $splitlist ( @splithost )
						{
						
							if ($ip->{cls} eq 'tcp')
							{
							print DQOS qq($CMDCOD -p tcp -s $splitlist --syn -m connlimit --connlimit-above $ip->{ipnum} -j DROP \n);
							print DQOS qq($CMDCOD -p tcp -s $splitlist --dport $ip->{port} --syn -m connlimit --connlimit-above $ip->{portnum} -j DROP \n);
							print DQOS qq($CMDCOD -p tcp -d $splitlist --syn -m connlimit --connlimit-above $ip->{ipnum} -j DROP \n);
							print DQOS qq($CMDCOD -p tcp -d $splitlist --dport $ip->{port} --syn -m connlimit --connlimit-above $ip->{portnum} -j DROP \n);
							}
							if ($ip->{cls} eq 'udp')
							{
							print DQOS qq($CMDCOD -p udp -s $splitlist -m connlimit --connlimit-above $ip->{ipnum} -j DROP \n);
							print DQOS qq($CMDCOD -p udp -s $splitlist --dport $ip->{port} --syn -m connlimit --connlimit-above $ip->{portnum} -j DROP \n);
							print DQOS qq($CMDCOD -p udp -d $splitlist -m connlimit --connlimit-above $ip->{ipnum} -j DROP \n);
							print DQOS qq($CMDCOD -p udp -d $splitlist --dport $ip->{port} --syn -m connlimit --connlimit-above $ip->{portnum} -j DROP \n);
							}
						}
					}
				}
			}
		}
	}
	#default
	#print DQOS qq($CMDCOD -p tcp --syn -m connlimit --connlimit-above 50 -m limit --limit 50/s --limit-burst 50 -j ACCEPT\n);
   	#print DQOS qq($CMDCOD -p tcp --syn -m connlimit --connlimit-above 50 -m limit --limit 1/m -j LOG $LOGLEVEL --log-prefix t_connect: \n);
	#print DQOS qq($CMDCOD -p udp -m connlimit --connlimit-above 50 -m limit --limit 50/s --limit-burst 50 -j ACCEPT\n);
	#print DQOS qq($CMDCOD -p udp -m connlimit --connlimit-above 50 -m limit --limit 1/m -j LOG $LOGLEVEL --log-prefix u_connect: \n);
	#print DQOS qq($CMDCOD -j ICMP \n\n);
#===================================================

#===================================================
#	PSD
#===================================================
	print DQOS qq($IPTCMD -N PORTSCAN \n);
	
	foreach my $ip (@$doslistPSD)
	{
		if($ip->{type} eq 'ip')
		{
			#if enable=true write
			if($ip->{enable} eq 'true')
			{
				if($ip->{enable_AN} eq 'true')
				{
					print DQOS qq($CMDPSD -d $ip->{dosip} -p tcp --tcp-flags ALL FIN,URG,PSH -m recent --set -j PORTSCAN \n);
				}
				if($ip->{enable_SR} eq 'true')
				{
					print DQOS qq($CMDPSD -d $ip->{dosip} -p tcp --tcp-flags SYN,RST SYN,RST -m recent --set -j PORTSCAN \n);
				}
				if($ip->{enable_SF} eq 'true')
				{
					print DQOS qq($CMDPSD -d $ip->{dosip} -p tcp --tcp-flags SYN,FIN SYN,FIN -m recent --set -j PORTSCAN \n);
				}
				if($ip->{enable_NF} eq 'true')
				{
					print DQOS qq($CMDPSD -d $ip->{dosip} -p tcp --tcp-flags ALL FIN -m recent --set -j PORTSCAN \n);
				}
				if($ip->{enable_AA} eq 'true')
				{
					print DQOS qq($CMDPSD -d $ip->{dosip} -p tcp --tcp-flags ALL ALL -m recent --set -j PORTSCAN \n);
				}
				if($ip->{enable_NN} eq 'true')
				{
					print DQOS qq($CMDPSD -d $ip->{dosip} -p tcp --tcp-flags ALL NONE -m recent --set -j PORTSCAN \n);
				}
				if($ip->{enable_XM} eq 'true')
				{
					print DQOS qq($CMDPSD -d $ip->{dosip} -p tcp --tcp-flags ALL URG,ACK,PSH,RST,SYN,FIN -m recent --set -j PORTSCAN \n);
				}
			}
		}
		if($ip->{type} eq 'host')
		{
			if($ip->{enable} eq 'true')
			{
				foreach my $hostip(@$hostlist)
				{
					if ( $hostip->{hostname} eq "system" ) { next; }
					if ( $hostip->{hostname} eq $ip->{dosip})
					{
						my @splithost=split(',', $hostip->{hostaddress});
						foreach my $splitlist ( @splithost )
						{
							if($ip->{enable_AN} eq 'true')
							{
								print DQOS qq($CMDPSD -d $splitlist -p tcp --tcp-flags ALL FIN,URG,PSH -m recent --set -j PORTSCAN \n);
							}
							if($ip->{enable_SR} eq 'true')
							{
								print DQOS qq($CMDPSD -d $splitlist -p tcp --tcp-flags SYN,RST SYN,RST -m recent --set -j PORTSCAN \n);
							}
							if($ip->{enable_SF} eq 'true')
							{
								print DQOS qq($CMDPSD -d $splitlist -p tcp --tcp-flags SYN,FIN SYN,FIN -m recent --set -j PORTSCAN \n);
							}
							if($ip->{enable_NF} eq 'true')
							{
								print DQOS qq($CMDPSD -d $splitlist -p tcp --tcp-flags ALL FIN -m recent --set -j PORTSCAN \n);
							}
							if($ip->{enable_AA} eq 'true')
							{
								print DQOS qq($CMDPSD -d $splitlist -p tcp --tcp-flags ALL ALL -m recent --set -j PORTSCAN \n);
							}
							if($ip->{enable_NN} eq 'true')
							{
								print DQOS qq($CMDPSD -d $splitlist -p tcp --tcp-flags ALL NONE -m recent --set -j PORTSCAN \n);
							}
							if($ip->{enable_XM} eq 'true')
							{
								print DQOS qq($CMDPSD -d $splitlist -p tcp --tcp-flags ALL URG,ACK,PSH,RST,SYN,FIN -m recent --set -j PORTSCAN \n);
							}
						}
					}
				}
			}
		}
	}
	print DQOS qq($IPTCMD -A PORTSCAN -m limit --limit 1/m -j LOG --log-level alert --log-prefix port_scan: \n);
	print DQOS qq($IPTCMD -A PORTSCAN -j DROP \n);
	#print DQOS qq($CMDPSD -m psd --psd-weight-threshold 21 --psd-delay-threshold 5 --psd-lo-ports-weight 3 --psd-hi-ports-weight 1 -m limit --limit 1/m --limit-burst $LIMITBURST -j ACCEPT \n); 
	#print DQOS qq($CMDPSD -m psd --psd-weight-threshold 21 --psd-delay-threshold 5 --psd-lo-ports-weight 3 --psd-hi-ports-weight 1 -j LOG --log-level alert --log-prefix psd: \n); 
	#print DQOS qq($CMDPSD -j COD \n\n);
#===================================================

#===================================================
#	ICMP
#===================================================
	foreach my $ip (@$doslistFLOOD)
	{
		if($ip->{type} eq 'ip')
		{
			if($ip->{enable} eq 'true')
			{
				if ($ip->{cls} eq 'ICMP')
				{
				print DQOS qq($CMDFLOOD -p icmp -d $ip->{dosip} --icmp-type echo-request -m limit --limit $ip->{icmp_num}/s --limit-burst $LIMITBURST -j ACCEPT\n);
				print DQOS qq($CMDFLOOD -p icmp -d $ip->{dosip} --icmp-type echo-request -m limit --limit 1/m -j LOG --log-level alert --log-prefix icmp_flood:\n);
				print DQOS qq($CMDFLOOD -p icmp -d $ip->{dosip} --icmp-type echo-request -j DROP \n);
				}
				if ($ip->{cls} eq 'SYN')
				{
				print DQOS qq($CMDFLOOD -p tcp -d $ip->{dosip} -m state --state ESTABLISHED,RELATED -j ACCEPT \n);
				print DQOS qq($CMDFLOOD -p tcp -d $ip->{dosip} --syn -m limit --limit $ip->{syn_num}/s --limit-burst $LIMITBURST -j ACCEPT\n);
				print DQOS qq($CMDFLOOD -p tcp -d $ip->{dosip} --syn -m limit --limit 1/m -j LOG --log-level alert --log-prefix syn_flood:\n);
				print DQOS qq($CMDFLOOD -p tcp -d $ip->{dosip} --syn -j DROP\n);
				}
				if ($ip->{cls} eq 'UDP')
				{
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -j ACCEPT \n);
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -m limit --limit $ip->{udp_num}/s --limit-burst $LIMITBURST -j ACCEPT\n);
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -m limit --limit 1/m -j LOG --log-level alert --log-prefix udp_flood:\n);
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -j DROP\n);
				}
				
			}
		}
		if($ip->{type} eq 'host')
		{
			if($ip->{enable} eq 'true')
			{
				if ( $ip->{logset} eq 'true' ) 
				{
					foreach my $hostip(@$hostlist)
					{
						if ( $hostip->{hostname} eq "system" ) { next; }
						if ( $hostip->{hostname} eq $ip->{dosip})
						{
							my @splithost=split(',', $hostip->{hostaddress});
							foreach my $splitlist ( @splithost )
							{
								if ($ip->{cls} eq 'ICMP')
								{
								print DQOS qq($CMDFLOOD -p icmp -d $splitlist --icmp-type echo-request -m limit --limit $ip->{icmp_num}/s --limit-burst $LIMITBURST -j ACCEPT\n);
								print DQOS qq($CMDFLOOD -p icmp -d $splitlist --icmp-type echo-request -m limit --limit 1/m -j LOG --log-level alert --log-prefix icmp_flood:\n);
								print DQOS qq($CMDFLOOD -p icmp -d $splitlist --icmp-type echo-request -j DROP \n);
								}
								if ($ip->{cls} eq 'SYN')
								{
								print DQOS qq($CMDFLOOD -p tcp -d $splitlist -m state --state ESTABLISHED,RELATED -j ACCEPT \n);
								print DQOS qq($CMDFLOOD -p tcp -d $splitlist --syn -m limit --limit $ip->{syn_num}/s --limit-burst $LIMITBURST -j ACCEPT\n);
								print DQOS qq($CMDFLOOD -p tcp -d $splitlist -m limit --limit 1/m --syn -j LOG --log-level alert --log-prefix syn_flood:\n);
								print DQOS qq($CMDFLOOD -p tcp -d $splitlist -j DROP\n);
								}
				if ($ip->{cls} eq 'UDP')
				{
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -j ACCEPT \n);
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -m limit --limit $ip->{syn_num}/s --limit-burst $LIMITBURST -j ACCEPT\n);
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -m limit --limit 1/m -j LOG --log-level alert --log-prefix udp_flood:\n);
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -j DROP\n);
				}
							}
						}
					}
				}
				else
				{
					foreach my $hostip(@$hostlist)
					{
						if ( $hostip->{hostname} eq "system" ) { next; }
						if ( $hostip->{hostname} eq $ip->{dosip})
						{
							my @splithost=split(',', $hostip->{hostaddress});
							foreach my $splitlist ( @splithost )
							{
								if ($ip->{cls} eq 'ICMP')
								{
								print DQOS qq($CMDFLOOD -p icmp -d $splitlist --icmp-type echo-request -m limit --limit $ip->{icmp_num}/s --limit-burst $LIMITBURST -j ACCEPT\n);
								print DQOS qq($CMDFLOOD -p icmp -d $splitlist --icmp-type echo-request -m limit --limit 1/m -j LOG --log-level alert --log-prefix icmp_flood:\n);
								print DQOS qq($CMDFLOOD -p icmp -d $splitlist --icmp-type echo-request -j DROP \n);
								}
								if ($ip->{cls} eq 'SYN')
								{
								print DQOS qq($CMDFLOOD -p tcp -d $splitlist -m state --state ESTABLISHED,RELATED -j ACCEPT \n);
								print DQOS qq($CMDFLOOD -p tcp -d $splitlist --syn -m limit --limit $ip->{syn_num}/s --limit-burst $LIMITBURST -j ACCEPT\n);
								print DQOS qq($CMDFLOOD -p tcp -d $splitlist --syn -m limit --limit 1/m -j LOG --log-level alert --log-prefix syn_flood:\n);
								print DQOS qq($CMDFLOOD -p tcp -d $splitlist -j DROP\n);
								
								}
				if ($ip->{cls} eq 'UDP')
				{
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -m limit --limit $ip->{syn_num}/s --limit-burst $LIMITBURST -j ACCEPT\n);
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -m limit --limit 1/m -j LOG --log-level alert --log-prefix udp_flood:\n);
				print DQOS qq($CMDFLOOD -p udp -d $ip->{dosip} -j DROP\n);
				}
							}
						}
					}
				}
			}
		}
	}
	#print DQOS qq($CMDFLOOD -p icmp --icmp-type echo-request -m limit --limit 50/s --limit-burst 50 -j ACCEPT\n);
	#print DQOS qq($CMDFLOOD -p icmp --icmp-type echo-request -m limit --limit 1/m -j LOG --log-level alert --log-prefix icmp_flood:\n);
	#print DQOS qq($CMDFLOOD -j DEF \n); 
	#print DQOS qq($CMDFLOOD -j DROP \n\n);
#===================================================
    
    #print DQOS qq ($IPTCMD -A DEF -j ACCEPT \n\n);
    
    #print DQOS qq ($IPTCMD -A INPUT -p icmp -j ICMP \n\n);
    
    #print DQOS qq ($IPTCMD -t mangle -A PREROUTING -j COD \n\n);

}

#
1
