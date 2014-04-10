#!/usr/bin/perl

use CGI;

print "Content-type:text/html\n\n";
require ("/usr/local/apache/qb/qbmod.cgi");
my $cgi = new CGI;

my $action = $cgi->param("action");
my $file = $cgi->param("file");
my $data = $cgi->param("data");
my $enable = $cgi->param("enable");

my $check_ajax = '1';

if ($file ne '')
{
my $fileref=XMLread($gPATH.$file);
}
my $list=$fileref->{"num"};

my $ip,$mac,$status;

if ( $action eq "SAVE")
{
    my @xx = &cutting($data);
    foreach my $num (@$list)
    {
        if ($num->{ip} eq $xx[0] && $num->{mac} eq $xx[1])
        {
            $check_ajax = '0';
        }
    }
    
    if ($check_ajax)
    {
        my %savedata=(
            ip		=> $xx[0],
            mac		=> $xx[1],
            status	=> '1'
        );
        
        push(@$list,\%savedata);
        XMLwrite($fileref,$gPATH.$file);
        screen();
        makesh();
    }

}elsif ( $action eq "DEL")
{
    $check_ajax = '0';
    my @xx = &cutting($data);
    foreach my $num (@$list)
    {
        if ($num->{ip} eq $xx[0] && $num->{mac} eq $xx[1]){$check_ajax = '1';next;}
        push(@list,$num);
    }
    if ($check_ajax)
    {
        $fileref->{"num"}=\@list;
        XMLwrite($fileref,$gPATH.$file);
        screen();
        makesh();
    }
    
    
}elsif ( $action eq "CHE")
{
    $check_ajax = '0';
    my ($old_data,$new_data)=split(/-/,$data);
    my @old=&cutting($old_data);
    my @new=&cutting($new_data);
    foreach my $num (@$list)
    {
        if ($num->{ip} eq $old[0] && $num->{mac} eq $old[1])
        {
            $num->{ip}=$new[0];
            $num->{mac}=$new[1];
            $check_ajax = '1';
        }
    }
    if ($check_ajax)
    {
        XMLwrite($fileref,$gPATH.$file);
        screen();
        makesh();
    }
    
}elsif ( $action eq "SEARCH")
{
    foreach my $num (@$list)
    {
        if ($num->{ip} eq 'system' && $num->{mac} eq 'system')
        {
            $num->{status}=$enable;
        }
    }
if ($file ne '')
{
    XMLwrite($fileref,$gPATH.$file);
}    
    print $check_ajax;
    makesh();    
}

sub makesh
{
    if($file ne '')
    {
    my $fileref=XMLread($gPATH.$file);
    }
    my $list=$fileref->{"num"};
    my @buff,$tmp;;
    open(FILE,">/usr/local/apache/qbconf/ipmac.sh");
    open(FILE1,">/tmp/ipmac.sh");
    system("/usr/local/apache/qb/setuid/run /mnt/qb/conf/set/boot/ipmac.sh");
    foreach my $num (@$list)
    {
        if ($num->{ip} eq 'system' && $num->{mac} eq 'system')
        {
            if ($num->{status} eq '0' || $num->{status} eq '')
            {
                return;
            }
            else{next;}
        }
        print FILE "/sbin/iptables -t mangle -A PREROUTING -s $num->{ip} -m mac --mac-source $num->{mac} -j ACCEPT\n";
        print FILE1 "/sbin/iptables -t mangle -D PREROUTING -s $num->{ip} -m mac --mac-source $num->{mac} -j ACCEPT\n";
        $tmp= "/sbin/iptables -t mangle -A PREROUTING -m mac --mac-source $num->{mac} -j DROP\n";
        push(@buff,$tmp);
        print FILE1 "/sbin/iptables -t mangle -D PREROUTING -m mac --mac-source $num->{mac} -j DROP\n";
    }
    print FILE @buff;
    close(FILE);
    close(FILE1);
    system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/ipmac.sh /usr/local/apache/qbconf/ipmac.sh");
    system("/usr/local/apache/qb/setuid/run /usr/local/apache/qbconf/ipmac.sh");
    system("/usr/local/apache/qb/setuid/run /bin/rm /mnt/qb/conf/set/boot/ipmac.sh");
    system("/usr/local/apache/qb/setuid/run /bin/cp /tmp/ipmac.sh /mnt/qb/conf/set/boot/");
    system("sync"); 
}

sub cutting
{
    ($data)=@_;
    $data=~s/[{}]//g;
    @ref = split(/,/,$data);
    foreach my $tmp (@ref)
    {
        if ($tmp =~ /ip:/)
        {
            $tmp =~ s/ip://;
            $ip = $tmp;
        }elsif ($tmp =~ /mac:/)
        {
            $tmp =~ s/mac://;
            $mac = $tmp;
        }elsif ($tmp =~ /status:/)
        {
            $tmp =~ s/status://;
            $status = $tmp;
        }
    }
    return ($ip,$mac,$status);
}    

sub screen
{
    if($file ne '')
    {
    my $fileref=XMLread($gPATH.$file);
    }
    my $list=$fileref->{"num"};
    
    my $line=0;
    foreach my $num (@$list)
    {
        if ($num->{ip} eq "system" || $num->{ip} eq "" || $num->{mac} eq "system" || $num->{mac} eq ""){next;}
        print qq(<tr onMouseOver='over(this)' onMouseOut='out(this)'>);
        print qq(<td onClick='alter(this)'>$num->{ip}</td>);
        print qq(<td onClick='alter(this)'>$num->{mac}</td>);
        $status1 = ($num->{status} eq '1')?("ACCEPT"):("DROP");
        print qq(<td onClick='alter(this)'>$status1</td>);
        print qq(<td onClick='del(this)'><a><img src='image/del.gif' title='Delete' border='0'></a><input type='hidden' value="$line"/></td></tr>);
        $line++;
    }
}

