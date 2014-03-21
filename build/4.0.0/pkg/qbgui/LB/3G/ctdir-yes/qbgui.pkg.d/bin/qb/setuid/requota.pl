#!/usr/bin/perl

use CGI;
require ("/usr/local/apache/qb/qbmod.cgi");

my $cgi=new CGI;
my $action=$cgi->param("action");


my $quotaref = XMLread($gPATH.'quota.xml');
my $quotalist = $quotaref->{quota};
my @quota;
my $i=0;
my @quotaUP;
my $ii=0;
foreach my $countquota (@$quotalist)
{
	if ($countquota->{gateway} eq "system"){next;}
	if ($countquota->{enabled} eq "0"){next;}
	if ($countquota->{name} eq ""){next;}
	if($countquota->{bs} eq "1")
	{
		system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -L $countquota->{name}.total --line-numbers -vn|awk '/quota/' >/tmp/quota");
		system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/quota");
		system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -L $countquota->{name}.total --line-numbers -vn|awk '/quota/' >/tmp/quota2");
		system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/quota2");
	}
	else
	{
		system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -L $countquota->{name}.down --line-numbers -vn|awk '/quota/' >/tmp/quota");
		system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/quota");
		system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -L $countquota->{name}.up --line-numbers -vn|awk '/quota/' >/tmp/quota2");
		system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/quota2");
	}	
	system('echo gettime:`date +"%s"` >> /usr/local/apache/qb/Log_file/quota_log');
	open(FILE,'</tmp/quota');
	open(FILEUP,'</tmp/quota2');
	foreach my $line (<FILE>)
	{
		if (grep(/IMQ/,$line) || grep(/PREROUTING/,$line) || grep(/source/,$line) || grep(/CTDIRMARK/,$line) || grep(/MARK/,$line)){next;}
		my @quotaref=split(/\s+/,$line);
		#if (!grep(/ACCEPT/,$line)){next;}
		#if($quotaref[9] eq '0.0.0.0/0'){$quota[$i]=join(",",$quotaref[0],$quota->{name},$quotaref[11]);}
		#if($quotaref[6] eq '*'){$quota[$i]=join(",",$quotaref[0],$quota->{name},$quotaref[11]);}
		$quota[$i]=join(",",$quotaref[0],$countquota->{name},$quotaref[11]);
		my $source='0';
		my $dest='0';
		#print "$source $dest \n [$quotaref[11]] \n";
		#print "$countquota->{mail} \n [$quotaref[11]] \n $countquota->{qn} \n";
		if ((!$countquota->{mail}||$countquota->{mail} eq '0')&&$quotaref[11] eq '0'&&$countquota->{qn} ne '0')
		{
			if($countquota->{source} ne '' && $countquota->{dest} ne '')
			{
				$source = $countquota->{source}; $dest = $countquota->{dest}; $source =~s/host-//g; $dest =~s/host-//g;
			}
			system("/usr/local/apache/qb/setuid/run /bin/sh /usr/local/apache/qb/setuid/mailquota.sh $countquota->{name} $quotaref[11] $countquota->{type} $source $dest $countquota->{qn}"); $countquota->{mail}='1';
			#print "/usr/local/apache/qb/setuid/run /bin/sh /usr/local/apache/qb/setuid/mailquota.sh $countquota->{name} $quotaref[11] $countquota->{type} $source $dest $countquota->{qn}";
		}
		if ($action eq "")
		{
			system("echo Line: $quota[$i] >> /usr/local/apache/qb/Log_file/quota_log");
		}
		$i++;
	}
	close(FILE);

	foreach my $lineUP (<FILEUP>)
	{
		if (grep(/IMQ/,$lineUP) || grep(/POSTROUTING/,$lineUP) || grep(/source/,$lineUP) || grep(/CTDIRMARK/,$lineUP) || grep(/MARK/,$lineUP)){next;}
		my @quotarefUP=split(/\s+/,$lineUP);
		#if (!grep(/ACCEPT/,$lineUP)){next;}
		#if($quotarefUP[8] eq '0.0.0.0/0'){$quotaUP[$ii]=join(",",$quotarefUP[0],$quota->{name},$quotarefUP[11]);}
		#if($quotarefUP[7] eq '*'){$quotaUP[$ii]=join(",",$quotarefUP[0],$quota->{name},$quotarefUP[11]);}
		$quotaUP[$ii]=join(",",$quotarefUP[0],$countquota->{name},$quotarefUP[11]);
		$source = '0';
		$dest = '0';
		
		if ((!$countquota->{mail}||$countquota->{mail} eq '0')&&$quotarefUP[11] eq '0'&&$countquota->{qn} ne '0')
		{
			if($countquota->{source} ne '' && $countquota->{dest} ne '')
			{
				$source = $countquota->{source}; $dest = $countquota->{dest}; $source =~s/host-//g; $dest =~s/host-//g;
			}
			system("/usr/local/apache/qb/setuid/run /bin/sh /usr/local/apache/qb/setuid/mailquota.sh $countquota->{name} $quotarefUP[11] $countquota->{type} $source $dest $countquota->{qn}"); $countquota->{mail}='1';
			#print "/usr/local/apache/qb/setuid/run /bin/sh /usr/local/apache/qb/setuid/mailquota.sh $countquota->{name} $quotarefUP[11] $countquota->{type} $source $dest $countquota->{qn}";
		}
		if ($action eq "")
		{
	#        system("echo Line: $quotaUP[$ii] >> /usr/local/apache/qb/Log_file/quota_log");
		}
		$ii++;
	}
	close(FILEUP);
}
XMLwrite($quotaref, $gPATH."quota.xml");

	if ($i ne '0')
	{
		system("cat /dev/null > /usr/local/apache/qb/Log_file/quota_Dynamic");

		for (my $z = 0 ; $z < $i; $z++)
		{
			system("echo $quota[$z] >> /usr/local/apache/qb/Log_file/quota_Dynamic");
		}
	}

	if ($ii ne '0')
	{
		system("cat /dev/null > /usr/local/apache/qb/Log_file/quota_Dynamic2");

		for (my $z = 0 ; $z < $ii; $z++)
		{
			system("echo $quotaUP[$z] >> /usr/local/apache/qb/Log_file/quota_Dynamic2");
		}
	}
	system("/bin/cp -a /usr/local/apache/qb/Log_file/quota_Dynamic /mnt/log/Log_file/");
	system("/bin/cp -a /usr/local/apache/qb/Log_file/quota_Dynamic2 /mnt/log/Log_file/");



	if ($action eq "")
	{
		my $quotaref = XMLread($gPATH.'quota.xml');
		my $quotalist = $quotaref->{quota};
		my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday) = localtime(time);
		foreach my $quota (@$quotalist)
		{
			if ($quota->{gateway} eq "system"){next;}
			#if ($quota->{name} eq ""){next;}
			my ($hr,$time)=split(/:/,$quota->{date});
			my ($cycle)=$quota->{cycle};
			system("cat /etc/crontab|grep quotawork.pl|grep $quota->{name}|grep $hr|grep $time|grep '#$cycle' > /tmp/quota_date");
			my $file = -z "/tmp/quota_date";
			my $info="";
			if ($quota->{enabled} eq '0' || $file)
			{
				my @buff;
				my @newbuff;
				open(FILEI,"/etc/crontab"); 
				foreach my $data (<FILEI>)
				{
				if(grep(/$quota->{name}/,$data)){next;}
				push(@buff,$data);
				}
				close(FILEI);
				open(FILEII,">/etc/crontab");
				print FILEII @buff;
				close(FILEII);
			}
			if ($file)
			{
				my ($aa,$bb)=split(/:/,$quota->{date});
				# if($quota->{type} eq 'port')
				# {
					if ($quota->{cycle} eq "0")
					{    
						$info="$bb  $aa * * *  root      /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=non-cyclic LINK=$quota->{name} #0\n";
					}
					elsif ($quota->{cycle} eq "1")
					{    
						$info="$bb  $aa * * *  root      /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=CREAT LINK=$quota->{name} #1\n";
					}
					elsif ($quota->{cycle} eq "7")
					{
						$info="$bb  $aa * * $quota->{chose}  root      /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=CREAT LINK=$quota->{name} #7\n";
					}
					elsif ($quota->{cycle} eq "30")
					{
						$info="$bb  $aa $quota->{chose} * * root      /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=CREAT LINK=$quota->{name} #30\n";
					}
				# }
				# if($quota->{type} eq 'ip')
				# {
					# if ($quota->{cycle} eq "0")
					# {    
						# $info="$bb  $aa * * *  root      /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=non-cyclic LINK==$quota->{name} #0\n";
					# }
					# elsif ($quota->{cycle} eq "1")
					# {    
						# $info="$bb  $aa * * *  root      /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=CREAT LINK=$quota->{name} #1\n";
					# }
					# elsif ($quota->{cycle} eq "7")
					# {
						# $info="$bb  $aa * * $quota->{chose}  root      /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=CREAT LINK=$quota->{name} #7\n";
					# }
					# elsif ($quota->{cycle} eq "30")
					# {
						# $info="$bb  $aa $quota->{chose} * * root      /usr/bin/perl /usr/local/apache/qb/quotawork.pl action=CREAT LINK=$quota->{name} #30\n";
					# }
				# }
				#print "$info\n";
				open(FILE2,">>/etc/crontab");
				print FILE2 $info; 
				close(FILE);
			}
			# for (my $z = 0 ; $z < $i; $z++)
			# {
				# my ($num,$dev,$size)=split(/,/,$quota[$z]);
				# if ($dev eq $quota->{port}){if ($num ne $quota->{num}){$quota->{num} = $num;}}
				# elsif($dev eq $quota->{ip}){if ($num ne $quota->{num}){$quota->{num} = $num;}}
				# else{next;}            
			# }
			# for (my $zz = 0 ; $zz < $ii; $zz++)
			# {
				# my ($num,$dev,$size)=split(/,/,$quotaUP[$zz]);
				# if ($dev eq $quota->{port}){if ($num ne $quota->{num2}){$quota->{num2} = $num;}}
				# elsif($dev eq $quota->{ip}){if ($num ne $quota->{num2}){$quota->{num2} = $num;}}
				# else{next;}
			# }
		}
	}
	system("sync");
	system("sync");
	system("sync");

#$file = -z "/usr/local/apache/qb/Log_file/quota_Dynamic";
#if (!$file && $action eq "")
#{
    #system("/usr/local/apache/qb/setuid/run /usr/bin/perl /usr/local/apache/qb/setuid/quota.pl action=date");
#}
