#!/usr/bin/perl
#print "Content-type:text/html\n\n";
$status_dir="/usr/local/apache/qb/status/";

my @file_path=('/mnt/log/Cpu_User.log','/mnt/log/Mem_User.log','/mnt/log/Cache_User.log','/mnt/log/Session_User.log','/mnt/log/Ram_User.log');
foreach my $name (@file_path)
{
   my $file_date=`cat $name`;
   if (!grep(/:/,$file_date))
   {
       system("/usr/local/apache/qb/setuid/run /bin/rm -f $name");
       system(sync);
       system(sync);
       system(sync);
   }
}

get_Mem_Status();
get_Cache_Status();
get_Session_Status();
get_Ramdisk_Status();

my $cpuusage=&get_CPU_Usage(1); print $cpuusage;


sub get_CPU_Usage()
{
    my $interval=$_[0];
    my @cpu_start=get_CPU_Status();
    sleep $interval;
    my @cpu_end=get_CPU_Status();

    my $cpu_used=$cpu_end[1] + $cpu_end[2] + $cpu_end[3] - $cpu_start[1] - $cpu_start[2] - $cpu_start[3];
    my $cpu_total=$cpu_used + $cpu_end[4] - $cpu_start[4];
    my $cpu_usage=int(100*$cpu_used/$cpu_total);
    open(CPUSTATUS, "> cpu.status");
    print CPUSTATUS qq($cpu_usage %);
    close CPUSTATUS;
    my $date='';	
    if (!open(FILE,"/mnt/log/Cpu_User.log"))
    {
        my ($sec, $min, $hour, $day, $mon, $year) = localtime(time);
        $data=$hour.":".$min."--";
    }
    
    open(CPUSTATUS1, ">> /mnt/log/Cpu_User.log");
    print CPUSTATUS1 qq($data$cpu_usage %);
    close CPUSTATUS1;
    return $cpu_usage;
}

sub get_CPU_Status()
{
#/proc/stat
    my $cpuload;
    open(CPU, "< /proc/stat");
    while($cpuload=<CPU>) { if ($cpuload=~m/cpu/) { last; } }
    close(CPU);
    my @cpu=split(/\s+/, $cpuload);
    return @cpu;
}


sub get_Mem_Status()
{
# my @meminfo=readpipe 'cat /proc/meminfo';
# ln1:        total:    used:    free:  shared: buffers:  cached:
# ln2:Mem:  63668224 52686848 10981376        0  2318336 33447936
# ln3:Swap: 271392768  9093120 262299648
# ln4:MemTotal:        62176 kB
# ln5:MemFree:         10724 kB

    my $memtotal;
    open(MEM, "< /proc/meminfo");
    while($memtotal=<MEM>) { if ($memtotal=~m/MemTotal:/) { last; } }
    close(MEM);
    
    my $memfree;
    open(MEM, "< /proc/meminfo");
    while($memfree=<MEM>) { if ($memfree=~m/MemFree:/) { last; } }
    close(MEM);

    my $cached;
    open(MEM, "< /proc/meminfo");
    while($cached=<MEM>) { if ($cached=~m/Cached:/) { last; } }
    close(MEM);

    my @memtotal=split(/\s+/, $memtotal);
    my @memfree=split(/\s+/, $memfree);
    my @cached=split(/\s+/, $cached);
    my $usedmem=$memtotal[1]-$memfree[1]-$cached[1];
    my $mem_usage=int(100*$usedmem/$memtotal[1]); # the same as (ln4-ln5)*100/ln4
    my $availmem=$memfree[1];
	
	my $save_usedmem = sprintf("%.2f",$usedmem/1024);
	
    open(MEMSTATUS, "> ${status_dir}memory.status"); 
    #print MEMSTATUS qq($mem_usage,    $usedmem KBytes,,    $availmem KBytes); 
	print MEMSTATUS qq($save_usedmem,    $usedmem KBytes,,    $availmem KBytes); 
    close MEMSTATUS;
    my $cachefree=$memtotal[1]-$cached[1];
    my $cache_usage=int(100*$cached[1]/$memtotal[1]);
    my $availcache=$cachefree;
    open(CACHESTATUS, "> ${status_dir}cache.status");
    print CACHESTATUS qq($cache_usage,    $cached[1] KBytes,,    $availcache KBytes);
    close CACHESTATUS;
    
    my $data='';	
    if (!open(FILE,"/mnt/log/Mem_User.log"))
    {
        my ($sec, $min, $hour, $day, $mon, $year) = localtime(time);
        $data=$hour.":".$min."--";
    }
    open(CACHESTATUS1, ">> /mnt/log/Mem_User.log");
    #print CACHESTATUS1 qq($cache_usage %);
	print CACHESTATUS1 qq($data$save_usedmem %);
    close CACHESTATUS1;
}

sub get_Cache_Status()
{
    my $memtotal;
    open(MEM, "< /proc/meminfo");
    while($memtotal=<MEM>) { if ($memtotal=~m/MemTotal:/) { last; } }
    close(MEM);
    
    my $cached;
    open(MEM, "< /proc/meminfo");
    while($cached=<MEM>) { if ($cached=~m/Cached:/) { last; } }
    close(MEM);
    
    my @memtotal=split(/\s+/, $memtotal);
    my @cached=split(/\s+/, $cached);
    my $cachefree=$memtotal[1]-$cached[1];
    my $cache_usage=int(100*$cached[1]/$memtotal[1]);
    my $availcache=$cachefree;
	
    my $save_cached = sprintf("%.2f",$cached[1]/1024);	
	
    open(CACHESTATUS, "> ${status_dir}cache.status");
    #print CACHESTATUS qq($cache_usage,    $cached[1] KBytes,,    $availcache KBytes); 
	print CACHESTATUS qq($save_cached,    $cached[1] KBytes,,    $availcache KBytes); 
    close CACHESTATUS;
    my $data='';	
    if (!open(FILE,"/mnt/log/Cache_User.log"))
    {
        my ($sec, $min, $hour, $day, $mon, $year) = localtime(time);
        $data=$hour.":".$min."--";
    }
    open(CACHESTATUSi, ">> /mnt/log/Cache_User.log");
    #print CACHESTATUSi qq($cache_usage %); 
	print CACHESTATUSi qq($data$save_cached %); 
    close CACHESTATUSi;
}

sub get_Session_Status()
{
    #my $conn_count=0;
    open(CONN, "< /proc/sys/net/ipv4/netfilter/ip_conntrack_count");
    my $conn_count=<CONN>;
    #while (<CONN>) {$conn_count++;}
    close(CONN);

    if ( !open(CONN, "< /proc/sys/net/ipv4/ip_conntrack_max") )
    {
       open(CONN, "< /proc/sys/net/ipv4/netfilter/ip_conntrack_max"); #For QB V4.0.0
    }
    #open(CONN, "< /proc/sys/net/ipv4/ip_conntrack_max");
    my $max_conn=<CONN>;
    close(CONN);

    chomp($max_conn);
    my $session=int($conn_count*100/$max_conn);
    open(SESSIONSTATUS, "> ${status_dir}session.status"); 
    print SESSIONSTATUS qq($session,    $max_conn,,    $conn_count); 
    close SESSIONSTATUS;
    
    my $data='';	
    if (!open(FILE,"/mnt/log/Session_User.log"))
    {
        my ($sec, $min, $hour, $day, $mon, $year) = localtime(time);
        $data=$hour.":".$min."--";
    }
    open(SESSIONSTATUS1, ">> /mnt/log/Session_User.log"); 
    #print SESSIONSTATUS1 qq($session %); 
	print SESSIONSTATUS1 qq($data$conn_count %); 
    close SESSIONSTATUS1;
}

sub get_Ramdisk_Status()
{
    my @diskusage=readpipe 'df';
    my $ramdisk;
    foreach my $data ( @diskusage ) { if ( $data=~m/ram/ ) { $ramdisk=$data;last;} }
    my ($used, $avail, $usage)=($ramdisk=~m/(\d+)\s+(\d+)\s+(\d+)\%/);
    my $total=$used+$avail;
	
	my $save_ram = sprintf("%.2f",$used/1024);

    open(RAMDISKSTATUS, "> ${status_dir}ramdisk.status"); 
    #print RAMDISKSTATUS qq($usage,    $total KBytes,,    $avail KBytes); 
	print RAMDISKSTATUS qq($save_ram,    $total KBytes,,    $avail KBytes); 
    close RAMDISKSTATUS;
    my $data='';	
    if (!open(FILE,"/mnt/log/Ram_User.log"))
    {
        my ($sec, $min, $hour, $day, $mon, $year) = localtime(time);
        $data=$hour.":".$min."--";
    }
    open(RAMDISKSTATUSi, ">> /mnt/log/Ram_User.log");
    #print RAMDISKSTATUSi qq($usage %); 
    print RAMDISKSTATUSi qq($data$save_ram %); 
    close RAMDISKSTATUSi;
}

system("sync");
system("sync");
system("sync");
system("sync");
