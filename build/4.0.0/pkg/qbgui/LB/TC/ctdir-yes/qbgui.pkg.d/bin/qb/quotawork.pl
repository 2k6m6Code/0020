#!/usr/bin/perl

use CGI;
my $cgi = new CGI;
my $action = $cgi->param("action");
my $link = $cgi->param("LINK");
my $check1 = $cgi->param("CHECK");
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type:text/html\n\n";
my $quota = XMLread($gPATH.'quota.xml');
my $data1 = $cgi->param("DATA");
my @filestr;

if ($action eq "ENABLED")
{
    my $zonelist = $quota->{quota};
    my $name=$check1;
    foreach my $ref (@$zonelist)
    {
        if($ref->{gateway} eq "system" || $ref->{name} ne $name){next;}
        $ref->{enabled}=$link;
		$ref->{mail}='0';
        if ($link eq '0')
        {
			if($ref->{type} eq 'group')
			{
				if($ref->{bs} eq '1')
				{
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.total");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -A $ref->{name}.total -j ACCEPT");
				}
				else
				{
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.down");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.up");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -A $ref->{name}.down -j ACCEPT");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -A $ref->{name}.up -j ACCEPT");
				}
			}
			if($ref->{type} eq 'port')
			{
				if($ref->{bs} eq '1')
				{
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -o $ref->{port} -j $ref->{name}.total");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -i $ref->{port} -j $ref->{name}.total");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.total");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.total");
				}
				else
				{
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -o $ref->{port} -j $ref->{name}.up");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -i $ref->{port} -j $ref->{name}.down");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.down");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.down");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.up");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.up");
				}
			}
			if($ref->{type} eq 'ip')
			{
				if($ref->{bs} eq '1')
				{
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{ip} -j $ref->{name}.total");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -d $ref->{ip} -j $ref->{name}.total");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.total");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.total");
				}
				else
				{
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{ip} -j $ref->{name}.up");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -d $ref->{ip} -j $ref->{name}.down");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.down");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.down");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.up");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.up");
				}
			}
			if($ref->{type} eq 'policy')
			{
				my $hostref=XMLread($gPATH."host.xml");
				my $hostlist=$hostref->{host};
				my ($shost,$sip) = split(/-/,$ref->{source});
				my ($dhost,$dip) = split(/-/,$ref->{dest});
				if($shost eq 'host' && $dhost ne 'host')
				{
					foreach my $host (@$hostlist)
					{
						if ( $host->{hostname} eq "system" ) { next; }
						if ( $host->{hostname} eq $ref->{source})
						{
							my @splithost=split(',', $host->{hostaddress});
							foreach my $splitlist ( @splithost )
							{
								if($ref->{bs} eq '1')
								{
									system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $ref->{dest} -j $ref->{name}.total"); #UP
									system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $splitlist -j $ref->{name}.total"); #DOWN
								}
								else
								{
									system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $ref->{dest} -j $ref->{name}.up"); #UP
									system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $splitlist -j $ref->{name}.down"); #DOWN
								}
							}
						}
					}
				}
				elsif($shost ne 'host' && $dhost eq 'host')
				{
					foreach my $host (@$hostlist)
					{
						if ( $host->{hostname} eq "system" ) { next; }
						if ( $host->{hostname} eq $ref->{dest})
						{
							my @splithost=split(',', $host->{hostaddress});
							foreach my $splitlist ( @splithost )
							{
								if($ref->{bs} eq '1')
								{
									system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $splitlist -j $ref->{name}.total");
									system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $splitlist -d $ref->{source} -j $ref->{name}.total");
								}
								else
								{
									system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $splitlist -j $ref->{name}.up");
									system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $splitlist -d $ref->{source} -j $ref->{name}.down");
								}
							}
						}
					}
				}
				elsif($shost eq 'host' && $dhost eq 'host')
				{
					foreach my $host (@$hostlist)
					{
						if ( $host->{hostname} eq "system" ) { next; }
						if ( $host->{hostname} eq $ref->{source})
						{
							foreach my $host2 (@$hostlist)
							{
								if ( $host2->{hostname} eq "system" ) { next; }
								if ( $host2->{hostname} eq $ref->{dest})
								{
									my @splithost=split(',', $host->{hostaddress});
									foreach my $splitlist ( @splithost )
									{
										my @splithost2=split(',', $host2->{hostaddress});
										foreach my $splitlist2 ( @splithost2 )
										{
											if($ref->{bs} eq '1')
											{
												system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $splitlist2 -j $ref->{name}.total");
												system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $splitlist2 -d $splitlist -j $ref->{name}.total");
											}
											else
											{
												system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $splitlist2 -j $ref->{name}.up");
												system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $splitlist2 -d $splitlist -j $ref->{name}.down");
											}
										}
									}
								}
							}
						}
					}
				}
				else
				{
					if($ref->{bs} eq '1')
					{
						system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $ref->{dest} -j $ref->{name}.total");
						system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $ref->{source} -j $ref->{name}.total");
					}
					else
					{
						system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $ref->{dest} -j $ref->{name}.up");
						system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $ref->{source} -j $ref->{name}.down");
					}
				}
				if($ref->{bs} eq '1')
				{
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.total");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.total");			
				}
				else
				{
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.down");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.down");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.up");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.up");
				}
			}
            #print qq("0");
        }
        if ($link eq '1')
        {
            $action = "CREAT";
            $link = $name;
            #print qq("1");
        }
    }
    XMLwrite($quota, $gPATH."quota.xml");
	system("/usr/local/apache/qb/setuid/run /usr/bin/perl /usr/local/apache/qb/setuid/requota.pl");
}

if ($action eq "SAVE")
{
    my @newquota;	
    my $zonelist = $quota->{quota};
    my ($ip,$type,$gateway,$port,$down,$up,$date,$cycle,$alert,$gateway_16,$chose,$enabled,$name,$source,$dest,$group_name,$qn,$bs,$ql,$lmit)=split(/,/,$data1);
    if($name eq ''){return;}
    foreach my $ref (@$zonelist)
    {
		#if($ref->{name} eq ''){next;}
		if ($ref->{gateway} ne "system" && $ref->{name} eq $name && $ref->{type} eq 'group')
		{
			if($ref->{bs} eq '1')
			{
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.total");
			}
			else
			{
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.down");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.up");
			}
			next;
		}
        if ($ref->{gateway} ne "system" && $ref->{name} eq $name && $ref->{type} eq 'port')
		{
			if($ref->{bs} eq '1')
			{
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -o $ref->{port} -j $ref->{name}.total");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -i $ref->{port} -j $ref->{name}.total");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.total");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.total");
			}
			else
			{
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -o $ref->{port} -j $ref->{name}.up");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -i $ref->{port} -j $ref->{name}.down");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.down");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.down");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.up");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.up");
			}
			next;
		}
		if ($ref->{gateway} ne "system" && $ref->{name} eq $name && $ref->{type} eq 'ip')
		{
			if($ref->{bs} eq '1')
			{
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{ip} -j $ref->{name}.total");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -d $ref->{ip} -j $ref->{name}.total");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.total");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.total");
			}
			else
			{
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{ip} -j $ref->{name}.up");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -d $ref->{ip} -j $ref->{name}.down");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.down");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.down");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.up");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.up");
			}
			next;
		}
		if ($ref->{gateway} ne "system" && $ref->{name} eq $name && $ref->{type} eq 'policy')
        	{
			my $hostref=XMLread($gPATH."host.xml");
			my $hostlist=$hostref->{host};
			my ($shost,$sip) = split(/-/,$ref->{source});
			my ($dhost,$dip) = split(/-/,$ref->{dest});
			if($shost eq 'host' && $dhost ne 'host')
			{
				foreach my $host (@$hostlist)
				{
					if ( $host->{hostname} eq "system" ) { next; }
					if ( $host->{hostname} eq $ref->{source})
					{
						my @splithost=split(',', $host->{hostaddress});
						foreach my $splitlist ( @splithost )
						{
							if($ref->{bs} eq '1')
							{
								system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $ref->{dest} -j $ref->{name}.total"); #UP
								system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $splitlist -j $ref->{name}.total"); #DOWN
							}
							else
							{
								system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $ref->{dest} -j $ref->{name}.up"); #UP
								system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $splitlist -j $ref->{name}.down"); #DOWN
							}
						}
					}
				}
			}
			elsif($shost ne 'host' && $dhost eq 'host')
			{
				foreach my $host (@$hostlist)
				{
					if ( $host->{hostname} eq "system" ) { next; }
					if ( $host->{hostname} eq $ref->{dest})
					{
						my @splithost=split(',', $host->{hostaddress});
						foreach my $splitlist ( @splithost )
						{
							if($ref->{bs} eq '1')
							{
								system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $splitlist -j $ref->{name}.total");
								system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $splitlist -d $ref->{source} -j $ref->{name}.total");
							}
							else
							{
								system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $splitlist -j $ref->{name}.up");
								system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $splitlist -d $ref->{source} -j $ref->{name}.down");
							}
						}
					}
				}
			}
			elsif($shost eq 'host' && $dhost eq 'host')
			{
				foreach my $host (@$hostlist)
				{
					if ( $host->{hostname} eq "system" ) { next; }
					if ( $host->{hostname} eq $ref->{source})
					{
						foreach my $host2 (@$hostlist)
						{
							if ( $host2->{hostname} eq "system" ) { next; }
							if ( $host2->{hostname} eq $ref->{dest})
							{
								my @splithost=split(',', $host->{hostaddress});
								foreach my $splitlist ( @splithost )
								{
									my @splithost2=split(',', $host2->{hostaddress});
									foreach my $splitlist2 ( @splithost2 )
									{
										if($ref->{bs} eq '1')
										{
											system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $splitlist2 -j $ref->{name}.total");
											system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $splitlist2 -d $splitlist -j $ref->{name}.total");
										}
										else
										{
											system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $splitlist2 -j $ref->{name}.up");
											system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $splitlist2 -d $splitlist -j $ref->{name}.down");
										}
									}
								}
							}
						}
					}
				}
			}
			else
			{
				if($ref->{bs} eq '1')
				{
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $ref->{dest} -j $ref->{name}.total");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $ref->{source} -j $ref->{name}.total");
				}
				else
				{
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $ref->{dest} -j $ref->{name}.up");
					system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $ref->{source} -j $ref->{name}.down");
				}
			}
			if($ref->{bs} eq '1')
			{
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.total");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.total");
			}
			else
			{
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.down");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.down");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -F $ref->{name}.up");
				system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -X $ref->{name}.up");
			}
			next;
        	}
        	push(@newquota,$ref);
    }
    
    $quota->{quota}=\@newquota;
    my $zonelistref = $quota->{quota}; 
    
    my %write = (
		ip			=> $ip,
		type		=> $type,
    	gateway		=> $gateway,
    	port		=> $port,
    	down		=> $down,
    	up			=> $up,
    	date		=> $date,
    	cycle		=> $cycle,
    	alert		=> $alert,
    	chose		=> $chose,
    	num			=> "",
		num2		=> "",
    	enabled		=> $enabled,
    	gateway_16	=> $gateway_16,
		name	=> $name,
		source	=> $source,
		dest	=> $dest,
		mail	=> "0",
		group_name	=> $group_name,
		qn		=>	$qn,
		bs		=>	$bs,
		ql		=>	$ql,
		lmit	=>	$lmit
    );
    push(@$zonelistref,\%write);
    
    XMLwrite($quota, $gPATH."quota.xml");
    
    my @buff;
    open(FILEI,"/etc/crontab");
    foreach my $data (<FILEI>)
    {
        if(grep(/$name/,$data)){next;}
        push(@buff,$data);
    }
    close(FILEI);
    open(FILEII,">/etc/crontab");
    print FILEII @buff;
    close(FILEII);

	$link = $name;
	$action = "CREAT";
}
if ($action eq "CREAT")
{
    my $point = '0';
    my $check = '0';
    my $zonelist = $quota->{quota};
    open(FILE,">/usr/local/apache/qb/setuid/quota.sh");
    print FILE "\#!/bin/bash\n";
    
    foreach my $ref (@$zonelist) 
    {
        if ($ref->{gateway} eq "system" ){next;}
        if ($ref->{enabled} eq "0" ){next;}
        if ($check1 eq "repeat")
        {
            open(FILE1,"/usr/local/apache/qb/Log_file/quota_Dynamic");
            foreach my $line (<FILE1>)
            {
                ($num,$dev,$size)=split(/,/,$line);
            
                if ($check1 eq "repeat" && $ref->{name} eq $dev)
                {     
                    $link = $ref->{name};
                    $down=$size;
                    $down=~s/\n//;
                    $check='1';
                }
            }
			open(FILE11,"/usr/local/apache/qb/Log_file/quota_Dynamic2");
            foreach my $line (<FILE11>)
            {
                ($num,$dev,$size)=split(/,/,$line);
            
                if ($check1 eq "repeat" && $ref->{name} eq $dev)
                {     
                    $link = $ref->{name};
                    $up=$size;
                    $up=~s/\n//;
                    $check='1';
                }
            }
		}
        if ($ref->{name} eq $link && $ref->{enabled} eq '1')
		{##################################
			$ref->{mail}='0';
			if ($check eq '0')
			{
				$point = '1';
				my ($dnum,$doo)=split(":",$ref->{down});
				my ($unum,$uoo)=split(":",$ref->{up});
				$down = $dnum*$doo;
				$up = $unum*$uoo;
			}
			if($ref->{type} eq 'group')
			{
				print FILE "/sbin/iptables -t mangle -N $ref->{name}.total\n";
				print FILE "/sbin/iptables -t mangle -F $ref->{name}.total\n";
				
				$tmp = "/sbin/iptables -t mangle -A $ref->{name}.total -j DROP\n";
				#$tmp1 = "/sbin/iptables -t mangle -A $ref->{name}.down -j DROP\n";
				
				#print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -m quota --quota $up -j ACCEPT\n";
				print FILE "/sbin/iptables -t mangle -A $ref->{name}.total -m quota --quota $down -j ACCEPT\n";
				
				#print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
				#print FILE "/sbin/iptables -t mangle -A $ref->{name}.down -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
				
				push(@filestr,$tmp);
				#push(@filestr,$tmp1);
				close(FILE1);
			}
			if($ref->{type} eq 'port')
			{
				#$tmp = "/sbin/iptables -t mangle -A $ref->{name}.up -j DROP\n";
				#$tmp1 = "/sbin/iptables -t mangle -A $ref->{name}.down -j DROP\n";
				if($ref->{bs} eq '1')
				{
					print FILE "/sbin/iptables -t mangle -D POSTROUTING -o $ref->{port} -j $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -D PREROUTING -i $ref->{port} -j $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -F $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -X $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{name}.total\n";
					
					print FILE "/sbin/iptables -t mangle -A POSTROUTING -o $ref->{port} -j $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -A PREROUTING -i $ref->{port} -j $ref->{name}.total\n";
					
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.total -m quota --quota $down -j ACCEPT\n";
					if($ref->{ql} eq '1')
					{
						print FILE "/sbin/iptables -t mangle -A $ref->{name}.total -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
					}
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.total -j DROP\n";
				}
				else
				{
					print FILE "/sbin/iptables -t mangle -D POSTROUTING -o $ref->{port} -j $ref->{name}.up\n";
					print FILE "/sbin/iptables -t mangle -D PREROUTING -i $ref->{port} -j $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -F $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -X $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -F $ref->{name}.up\n";
					print FILE "/sbin/iptables -t mangle -X $ref->{name}.up\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{name}.up\n";
					
					print FILE "/sbin/iptables -t mangle -A POSTROUTING -o $ref->{port} -j $ref->{name}.up\n";
					print FILE "/sbin/iptables -t mangle -A PREROUTING -i $ref->{port} -j $ref->{name}.down\n";
					
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -m quota --quota $up -j ACCEPT\n";
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.down -m quota --quota $down -j ACCEPT\n";
					
					if($ref->{ql} eq '1')
					{
						print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
						print FILE "/sbin/iptables -t mangle -A $ref->{name}.down -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
					}
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -j DROP\n";
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.down -j DROP\n";
				}				
				#push(@filestr,$tmp);
				#push(@filestr,$tmp1);
				close(FILE1);
			}
			if($ref->{type} eq 'ip')
			{
				if($ref->{bs} eq '1')
				{
					print FILE "/sbin/iptables -t mangle -D POSTROUTING -s $ref->{ip} -j $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -D PREROUTING -d $ref->{ip} -j $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{group_name}.total\n";
					print FILE "/sbin/iptables -t mangle -A $ref->{group_name}.total -j ACCEPT\n";
					print FILE "/sbin/iptables -t mangle -F $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -X $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -A POSTROUTING -s $ref->{ip} -j $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -A PREROUTING -d $ref->{ip} -j $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.total -m quota --quota $down -j $ref->{group_name}.total\n"; #DOWN
					
					if($ref->{ql} eq '1')
					{

						print FILE "/sbin/iptables -t mangle -A $ref->{name}.total -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
					}
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.total -j DROP\n";
				}
				else


				{
					print FILE "/sbin/iptables -t mangle -D POSTROUTING -s $ref->{ip} -j $ref->{name}.up\n";
					print FILE "/sbin/iptables -t mangle -D PREROUTING -d $ref->{ip} -j $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{group_name}.total\n";
					print FILE "/sbin/iptables -t mangle -A $ref->{group_name}.total -j ACCEPT\n";
					print FILE "/sbin/iptables -t mangle -F $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -X $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -F $ref->{name}.up\n";
					print FILE "/sbin/iptables -t mangle -X $ref->{name}.up\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{name}.up\n";
					
					print FILE "/sbin/iptables -t mangle -A POSTROUTING -s $ref->{ip} -j $ref->{name}.up\n";
					print FILE "/sbin/iptables -t mangle -A PREROUTING -d $ref->{ip} -j $ref->{name}.down\n";
					
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -m quota --quota $up -j $ref->{group_name}.total\n"; #UP
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.down -m quota --quota $down -j $ref->{group_name}.total\n"; #DOWN
					
					if($ref->{ql} eq '1')
					{
						print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
						print FILE "/sbin/iptables -t mangle -A $ref->{name}.down -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
					}
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -j DROP\n";
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.down -j DROP\n";
				}
				close(FILE1);
			}
			if($ref->{type} eq 'policy')
			{
				my $hostref=XMLread($gPATH."host.xml");
				my $hostlist=$hostref->{host};
				my ($shost,$sip) = split(/-/,$ref->{source});
				my ($dhost,$dip) = split(/-/,$ref->{dest});
				if($ref->{bs} eq '1')
				{
					print FILE "/sbin/iptables -t mangle -F $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -X $ref->{name}.total\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{name}.total\n";
				}
				else
				{
					print FILE "/sbin/iptables -t mangle -F $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -X $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{name}.down\n";
					print FILE "/sbin/iptables -t mangle -F $ref->{name}.up\n";
					print FILE "/sbin/iptables -t mangle -X $ref->{name}.up\n";
					print FILE "/sbin/iptables -t mangle -N $ref->{name}.up\n";
				}				
				#$tmp = "/sbin/iptables -t mangle -A $ref->{name}.up -j DROP\n";
				#$tmp1 = "/sbin/iptables -t mangle -A $ref->{name}.down -j DROP\n";
				if($shost eq 'host' && $dhost ne 'host')
				{
					foreach my $host (@$hostlist)
					{
						if ( $host->{hostname} eq "system" ) { next; }
						if ( $host->{hostname} eq $ref->{source})
						{
							my @splithost=split(',', $host->{hostaddress});
							foreach my $splitlist ( @splithost )
							{
								if($ref->{bs} eq '1')
								{
									print FILE "/sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $ref->{dest} -j $ref->{name}.total\n"; #UP
									print FILE "/sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $splitlist -j $ref->{name}.total\n"; #DOWN
									print FILE "/sbin/iptables -t mangle -A POSTROUTING -s $splitlist -d $ref->{dest} -j $ref->{name}.total\n"; #UP
									print FILE "/sbin/iptables -t mangle -A PREROUTING -s $ref->{dest} -d $splitlist -j $ref->{name}.total\n"; #DOWN
								}
								else
								{
									print FILE "/sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $ref->{dest} -j $ref->{name}.up\n"; #UP
									print FILE "/sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $splitlist -j $ref->{name}.down\n"; #DOWN
									print FILE "/sbin/iptables -t mangle -A POSTROUTING -s $splitlist -d $ref->{dest} -j $ref->{name}.up\n"; #UP
									print FILE "/sbin/iptables -t mangle -A PREROUTING -s $ref->{dest} -d $splitlist -j $ref->{name}.down\n"; #DOWN
								}
							}
						}
					}
				}
				elsif($shost ne 'host' && $dhost eq 'host')
				{
					foreach my $host (@$hostlist)
					{
						if ( $host->{hostname} eq "system" ) { next; }
						if ( $host->{hostname} eq $ref->{dest})
						{
							my @splithost=split(',', $host->{hostaddress});
							foreach my $splitlist ( @splithost )
							{
								if($ref->{bs} eq '1')
								{
									print FILE "/sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $splitlist -j $ref->{name}.total\n";
									print FILE "/sbin/iptables -t mangle -D PREROUTING -s $splitlist -d $ref->{source} -j $ref->{name}.total\n";
									print FILE "/sbin/iptables -t mangle -A POSTROUTING -s $ref->{source} -d $splitlist -j $ref->{name}.total\n";
									print FILE "/sbin/iptables -t mangle -A PREROUTING -s $splitlist -d $ref->{source} -j $ref->{name}.total\n";
								}
								else
								{
									print FILE "/sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $splitlist -j $ref->{name}.up\n";
									print FILE "/sbin/iptables -t mangle -D PREROUTING -s $splitlist -d $ref->{source} -j $ref->{name}.down\n";
									print FILE "/sbin/iptables -t mangle -A POSTROUTING -s $ref->{source} -d $splitlist -j $ref->{name}.up\n";
									print FILE "/sbin/iptables -t mangle -A PREROUTING -s $splitlist -d $ref->{source} -j $ref->{name}.down\n";
								}
								
							}
						}
					}
				}
				elsif($shost eq 'host' && $dhost eq 'host')
				{
					foreach my $host (@$hostlist)
					{
						if ( $host->{hostname} eq "system" ) { next; }
						if ( $host->{hostname} eq $ref->{source})
						{
							foreach my $host2 (@$hostlist)
							{
								if ( $host2->{hostname} eq "system" ) { next; }
								if ( $host2->{hostname} eq $ref->{dest})
								{
									my @splithost=split(',', $host->{hostaddress});
									foreach my $splitlist ( @splithost )
									{
										my @splithost2=split(',', $host2->{hostaddress});
										foreach my $splitlist2 ( @splithost2 )
										{
											if($ref->{bs} eq '1')
											{
												print FILE "/sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $splitlist2 -j $ref->{name}.total\n";
												print FILE "/sbin/iptables -t mangle -D PREROUTING -s $splitlist2 -d $splitlist -j $ref->{name}.total\n";
												print FILE "/sbin/iptables -t mangle -A POSTROUTING -s $splitlist -d $splitlist2 -j $ref->{name}.total\n";
												print FILE "/sbin/iptables -t mangle -A PREROUTING -s $splitlist2 -d $splitlist -j $ref->{name}.total\n";
											}
											else
											{
												print FILE "/sbin/iptables -t mangle -D POSTROUTING -s $splitlist -d $splitlist2 -j $ref->{name}.up\n";
												print FILE "/sbin/iptables -t mangle -D PREROUTING -s $splitlist2 -d $splitlist -j $ref->{name}.down\n";
												print FILE "/sbin/iptables -t mangle -A POSTROUTING -s $splitlist -d $splitlist2 -j $ref->{name}.up\n";
												print FILE "/sbin/iptables -t mangle -A PREROUTING -s $splitlist2 -d $splitlist -j $ref->{name}.down\n";
											}
											
										}
									}
								}
							}
						}
					}
				}
				else
				{
					if($ref->{bs} eq '1')
					{
						print FILE "/sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $ref->{dest} -j $ref->{name}.total\n";
						print FILE "/sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $ref->{source} -j $ref->{name}.total\n";
						print FILE "/sbin/iptables -t mangle -A POSTROUTING -s $ref->{source} -d $ref->{dest} -j $ref->{name}.total\n";
						print FILE "/sbin/iptables -t mangle -A PREROUTING -s $ref->{dest} -d $ref->{source} -j $ref->{name}.total\n";
					}
					else
					{
						print FILE "/sbin/iptables -t mangle -D POSTROUTING -s $ref->{source} -d $ref->{dest} -j $ref->{name}.up\n";
						print FILE "/sbin/iptables -t mangle -D PREROUTING -s $ref->{dest} -d $ref->{source} -j $ref->{name}.down\n";
						print FILE "/sbin/iptables -t mangle -A POSTROUTING -s $ref->{source} -d $ref->{dest} -j $ref->{name}.up\n";
						print FILE "/sbin/iptables -t mangle -A PREROUTING -s $ref->{dest} -d $ref->{source} -j $ref->{name}.down\n";
					}
				}
				if($ref->{bs} eq '1')
				{
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.total -m quota --quota $down -j ACCEPT\n";
					if($ref->{ql} eq '1')
					{
						print FILE "/sbin/iptables -t mangle -A $ref->{name}.total -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
					}
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.total -j DROP\n";
				}
				else
				{
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -m quota --quota $up -j ACCEPT\n"; #UP
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.down -m quota --quota $down -j ACCEPT\n"; #DOWN
					if($ref->{ql} eq '1')
					{
						print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
						print FILE "/sbin/iptables -t mangle -A $ref->{name}.down -m limit --limit $ref->{lmit}/s --limit burst 50 -j ACCEPT\n";
					}
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.up -j DROP\n";
					print FILE "/sbin/iptables -t mangle -A $ref->{name}.down -j DROP\n";
				}
				#push(@filestr,$tmp);
				#push(@filestr,$tmp1);
				close(FILE1);
			}
		}
		else{next;}
    }
    print FILE @filestr;
    close(FILE);
    system("/usr/local/apache/qb/setuid/run /bin/sh /usr/local/apache/qb/setuid/quota.sh");
    system("/usr/local/apache/qb/setuid/run /usr/bin/perl /usr/local/apache/qb/setuid/requota.pl");
    #print qq ($point);
    open(QUOTA,"/usr/local/apache/qb/Log_file/quota_Dynamic");
    foreach my $data (<QUOTA>)
    {
       my @tmpnum=split(/,/,$data);
	   foreach my $ref (@$zonelist)
       {
           if($ref->{gateway} eq "system"){next;}
           if ($ref->{port} ne '' && $ref->{port} ne $tmpnum[1]){next;}
           #$ref->{num}=$tmpnum[0];
       }
       foreach my $ref (@$zonelist)
       {
           if($ref->{gateway} eq "system"){next;}
           if ($ref->{ip} ne $tmpnum[1]){next;}
           #$ref->{num}=$tmpnum[0];
       }
    }
    close(QUOTA);
	open(QUOTA2,"/usr/local/apache/qb/Log_file/quota_Dynamic2");
    foreach my $data (<QUOTA2>)
    {
       my @tmpnum=split(/,/,$data);
	   foreach my $ref (@$zonelist)
       {
           if($ref->{gateway} eq "system"){next;}
           if ($ref->{port} ne $tmpnum[1]){next;}
           #$ref->{num2}=$tmpnum[0];
       }
       foreach my $ref (@$zonelist)
       {
           if($ref->{gateway} eq "system"){next;}
           if ($ref->{ip} ne $tmpnum[1]){next;}
           #$ref->{num2}=$tmpnum[0];
       }
    }
    close(QUOTA2);
    XMLwrite($quota, $gPATH."quota.xml"); 
}
