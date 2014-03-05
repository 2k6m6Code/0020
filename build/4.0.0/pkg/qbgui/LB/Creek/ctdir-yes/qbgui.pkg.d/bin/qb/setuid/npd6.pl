#!/usr/bin/perl
require ("/usr/local/apache/qb/qbmod.cgi");
my $ispref=XMLread('/usr/local/apache/qbconf/zonecfg.xml');
my $dmzref=XMLread('/usr/local/apache/qbconf/dmzreg.xml'); 
#my $basref=XMLread('/usr/local/apache/qbconf/basic.xml');
#my $baslist=$basref->{isp};
my $isplist=$ispref->{nat};
my $dmzlist=$dmzref->{host};
$entry="";
runCommand (command=>'rm' , params=>"-f /tmp/npd6.conf*");
$x="0";
foreach my $nat (@$isplist)
{
    if( !$nat->{network} || !$nat->{nic} ){next;}
    if ($nat->{network} !~ /:/ ||  $nat->{nic} !~ /eth/){next;}
    $file="/tmp/npd6.conf$x";
    @tmp = split(/:/,$nat->{network},5);
    $subnet = join(":",$tmp[0],$tmp[1],$tmp[2],$tmp[3],$entry);
    $npd="prefix = $subnet
    interface = $nat->{nic}
    listtype = none
    collectTargets = 100
    linkOption = false
    ignoreLocal = true
    routerNA = true
    maxHops = 255";
    
    open(FILE, ">$file");
    print FILE "$npd";
    close(FILE);
    
    runCommand (command=>'chmod' , params=>"664 $file");
    runCommand (command=>'/opt/qb/apps/npd6' , params=>"-c $file");
$x++;
}
$x="10";
my $isplist=$ispref->{dmz};
foreach my $dmz (@$dmzlist)
{
    if( !$dmz->{ip} || !$dmz->{isp} ){next;}
    if ($dmz->{ip} !~ /:/){next;}
    foreach my $isp (@$isplist)
    {
        if(!$isp->{isp} || !$isp->{nic} || $isp->{mode} ne "ARPPROXY"){next;}
        if($isp->{isp} ne $dmz->{isp} ){next;}
        $interface = $isp->{nic};
    }
    $file="/tmp/npd6.conf$x";
    @tmp = split(/:/,$dmz->{ip},5);
    $subnet = join(":",$tmp[0],$tmp[1],$tmp[2],$tmp[3],$entry);
    
    $npd="prefix=$subnet
interface = $interface
listtype = none
collectTargets = 100
linkOption = false
ignoreLocal = true
routerNA = true
maxHops = 255";
                                                 
    open(FILE, ">$file");
    print FILE "$npd";
    close(FILE);
                                                             
    runCommand (command=>'chmod' , params=>"664 $file");
    runCommand (command=>'/opt/qb/apps/npd6' , params=>"-c $file");
    $x++;
}                                                                     
#
1
