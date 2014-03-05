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
    my ($gateway,$port)=split(/,/,$check1);
    foreach my $ref (@$zonelist)
    {
        if($ref->{gateway} eq "system" || $ref->{gateway} ne $gateway || $ref->{port} ne $port){next;}
        $ref->{enabled}=$link;
        if ($link eq '0')
        {
            system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING $ref->{num}");
            system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -i $ref->{port} -m gw --gw $ref->{gateway} -j DROP");
            print qq("0");
        }
        if ($link eq '1')
        {
            $action = "CREAT";
            $link = $ref->{gateway};
            print qq("1");
        }
    }
    XMLwrite($quota, $gPATH."quota.xml");
}

if ($action eq "SAVE")
{
    my $zonelist = $quota->{quota};
    my ($gateway,$port,$down,$up,$date,$cycle,$alert,$gateway_16,$chose,$enabled)=split(/,/,$data1);
    
    foreach my $ref (@$zonelist)
    {
        if ($ref->{gateway} ne "system" && $ref->{gateway} eq $gateway && $ref->{port} eq $port )
        {
            system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING $ref->{num}");
            system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -i $ref->{port} -m gw --gw $ref->{gateway} -j DROP");
            next;
        }
        push(@zonelist,$ref);
    }
    $quota->{quota}=\@zonelist;
    my $zonelistref = $quota->{quota}; 
    
    my %write = (
    	gateway    => $gateway,
    	port 	   => $port,
    	down	   => $down,
    	up	   => $up,
    	date	   => $date,
    	cycle	   => $cycle,
    	alert      => $alert,
    	chose	   => $chose,
    	num	   => "",
    	enabled	   => $enabled,
    	gateway_16 => $gateway_16
    );
    push(@$zonelistref,\%write);
    
    XMLwrite($quota, $gPATH."quota.xml");
    
    my @buff;
    open(FILEI,"/etc/crontab");
    foreach my $data (<FILEI>)
    {
        if(grep(/$gateway/,$data)){next;}
        push(@buff,$data);
    }
    close(FILEI);
    open(FILEII,">/etc/crontab");
    print FILEII @buff;
    close(FILEII);
                                                                                     
    $action = "CREAT";
    $link = $gateway;
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
            
                if ($check1 eq "repeat" && $ref->{port} eq $dev)
                {     
                    $link = $ref->{gateway};
                    $down=$size;
                    $down=~s/\n//;
                    $check='1';
                }
            }
	}
        if ($ref->{gateway} ne $link ){next;}
        if ($check eq '0')
        {
            $point = '1';
            my ($dnum,$doo)=split(":",$ref->{down});
            #my ($unum,$uoo)=split(":",$ref->{up});
            $down = $dnum*$doo;
            #my $up = $unum*$uoo;
        }
        #my $tmp = "/sbin/iptables -t mangle -A POSTROUTING -o $ref->{port} -m gw --gw $ref->{gateway} -j DROP\n";
        #my $tmp1 = "/sbin/iptables -t mangle -A PREROUTING -i $ref->{port} -m gw --gw $ref->{gateway} -j DROP\n";
        my $tmp1 = "/sbin/iptables -t mangle -A PREROUTING -i $ref->{port} -j DROP\n";
        #print FILE "/sbin/iptables -t mangle -D POSTROUTING $ref->{num}\n";
        print FILE "/sbin/iptables -t mangle -D PREROUTING $ref->{num}\n";
        #print FILE "/sbin/iptables -t mangle -D POSTROUTING -o $ref->{port} -m gw --gw $ref->{gateway} -j DROP\n";
        
        print FILE "/sbin/iptables -t mangle -D PREROUTING -i $ref->{port} -j DROP\n";
        
        #print FILE "/sbin/iptables -t mangle -D PREROUTING -i $ref->{port} -m gw --gw $ref->{gateway} -j DROP\n";
        #print FILE "/sbin/iptables -t mangle -A POSTROUTING -o $ref->{port} -m gw --gw $ref->{gateway} -m quota --quota $up -j ACCEPT\n";
        
        print FILE "/sbin/iptables -t mangle -A PREROUTING -i $ref->{port} -m quota --quota $down -j ACCEPT\n";
        
        #print FILE "/sbin/iptables -t mangle -A PREROUTING -i $ref->{port} -m gw --gw $ref->{gateway} -m quota --quota $down -j ACCEPT\n";
        #push(@filestr,$tmp);
        push(@filestr,$tmp1);
        close(FILE1);
    }
    print FILE @filestr;
    close(FILE);
    system("/usr/local/apache/qb/setuid/run /bin/sh /usr/local/apache/qb/setuid/quota.sh");
    system("/usr/local/apache/qb/setuid/run /usr/bin/perl /usr/local/apache/qb/setuid/requota.pl");
    print qq ($point);
    open(QUOTA,'</usr/local/apache/qb/Log_file/quota_Dynamic');
    foreach my $data (<QUOTA>)
    {
       my @tmp=split(/,/,$data);
       foreach my $ref (@$zonelist)
       {
           if($ref->{gateway} eq "system"){next;}
           if ($ref->{port} ne $tmp[1] && $ref->{gateway_16} ne $tmp[2] ){next;}
#           if ($ref->{gateway} eq $link && $ref->{num} ne "")
#           {
               #system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING $ref->{num}");
               #system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING $ref->{num}");
#           }
           $ref->{num}=$tmp[0];
       }
    }
    close(QUOTA);
    XMLwrite($quota, $gPATH."quota.xml"); 
}
