#!/usr/bin/perl
#print "Content-type:text/html\n\n";
$status_dir="/usr/local/apache/qb/status/";

get_Mem_Status();
#get_Cache_Status();
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
    open(MEMSTATUS, "> ${status_dir}memory.status"); 
    print MEMSTATUS qq($mem_usage,    $usedmem KBytes,,    $availmem KBytes); 
    close MEMSTATUS;
    my $cachefree=$memtotal[1]-$cached[1];
    my $cache_usage=int(100*$cached[1]/$memtotal[1]);
    my $availcache=$cachefree;
    open(CACHESTATUS, "> ${status_dir}cache.status");
    print CACHESTATUS qq($cache_usage,    $cached[1] KBytes,,    $availcache KBytes);
    close CACHESTATUS;
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
    open(CACHESTATUS, "> ${status_dir}cache.status");
    print CACHESTATUS qq($cache_usage,    $cached[1] KBytes,,    $availcache KBytes); 
    close CACHESTATUS;
}

sub get_Session_Status()
{
    #my $conn_count=0;
    open(CONN, "< /proc/sys/net/ipv4/netfilter/ip_conntrack_count");
    my $conn_count=<CONN>;
    #while (<CONN>) {$conn_count++;}
    close(CONN);

    open(CONN, "< /proc/sys/net/ipv4/ip_conntrack_max");
    my $max_conn=<CONN>;
    close(CONN);

    chomp($max_conn);
    my $session=int($conn_count*100/$max_conn);
    open(SESSIONSTATUS, "> ${status_dir}session.status"); 
    print SESSIONSTATUS qq($session,    $max_conn,,    $conn_count); 
    close SESSIONSTATUS;
}

sub get_Ramdisk_Status()
{
    my @diskusage=readpipe 'df';
    my $ramdisk;
    foreach my $data ( @diskusage ) { if ( $data=~m/ram/ ) { $ramdisk=$data;last;} }
    my ($used, $avail, $usage)=($ramdisk=~m/(\d+)\s+(\d+)\s+(\d+)\%/);
    my $total=$used+$avail;

    open(RAMDISKSTATUS, "> ${status_dir}ramdisk.status"); 
    print RAMDISKSTATUS qq($usage,    $total KBytes,,    $avail KBytes); 
    close RAMDISKSTATUS;
}
