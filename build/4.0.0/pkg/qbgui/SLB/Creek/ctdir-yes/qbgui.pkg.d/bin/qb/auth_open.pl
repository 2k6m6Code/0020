#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }
require ("/usr/local/apache/qb/qbmod.cgi");

use CGI;

my $cgi=new CGI;
my $action=$cgi->param('action');
my $auth_server = XMLread($gPATH.'auth.xml');
my $auth_zone = XMLread($gPATH.'zonecfg.xml');
my $zone = $auth_zone->{nat};
my $server = $auth_server->{server};
my $user = $auth_server->{user};
my $do='0';
system("/sbin/iptables -t nat -F AUTH_CHAIN");
system("/sbin/iptables -t nat -X AUTH");
system("/sbin/iptables -t nat -N AUTH");
system("/sbin/iptables -t nat -F AUTH");       
 
if ($action)
{
    Reset();
}
foreach my $list (@$server)
{
    if ($list->{schname} eq 'system'){next;}
    if ($list->{enabled} eq '1' )
    {
        $do = '1';
    }
}
if ($do eq '1')
{
    foreach my $list (@$zone)
    {
        if ($list->{natid} eq 'system'){next;}
        if ($list->{ip} ne '' && $list->{network} ne '')
        {
            my $rand=time();
	    system("/sbin/iptables -t nat -D AUTH_CHAIN -s $list->{network} -j AUTH");
            system("/sbin/iptables -t nat -A AUTH_CHAIN -s $list->{network} -j AUTH");
    	    system("/sbin/iptables -t nat -A AUTH -p tcp -s $list->{network} --dport 443 -j DNAT --to-destination $list->{ip}:443");
    	    system("/sbin/iptables -t nat -A AUTH -p tcp -s $list->{network} --dport 1:65535 -j DNAT --to-destination $list->{ip}:8000?time=$time");
	    system("/sbin/iptables -t nat -I AUTH -s $list->{ip} -j RETURN");
	    system("/sbin/iptables -t nat -I AUTH -d $list->{ip} -j RETURN"); 
        }
    
    }

    my $timer;
    foreach my $user_list (@$user)
    {
        if ($user_list->{schname} eq 'system')
        {
            $timer = $user_list->{login_time};
            next;
        }
        if ($timer eq ''){$timer = 43200;}
        my $ref  = $user_list->{member};
        my $def = '0';
        my $now_data = time()+(8*60*60);
        if ($action ne '')
        {
            $timer = 0;
        }
        if ($user_list->{description} eq 'None'){$def='1';}
        foreach my $pass (@$ref) 
        {
            if (($def eq '1' || ($now_data - $pass->{time}) < $timer ) && ($now_data - $pass->{time}) > 0)
            {
                if ($pass->{ip} ne '')
                {
                    system("/sbin/iptables -t nat -I AUTH -s $pass->{ip} -j RETURN");
                }else
                {
                    system("/sbin/iptables -t nat -I AUTH -s $pass->{iip} -j RETURN");
                }
            }
        }
        system("/sbin/iptables -t nat -I AUTH -s 172.31.3.0/24 -j RETURN");
        
    }
}
system("/sbin/iptables -t nat -A AUTH_CHAIN -j RETURN");
sub Reset
{
    my $auth_server = XMLread($gPATH.'auth.xml');
    my $user = $auth_server->{user};
    foreach my $user_list (@$user)
    {
        if ($user_list->{schname} eq 'system'){next;}
        my $ref  = $user_list->{member};
        foreach my $pass (@$ref)
        {
            if ($pass->{time} eq ''){next;}
            $pass->{old_time}=$pass->{time};
            $pass->{time}='';
        }
    }
    XMLwrite($auth_server, $gPATH."auth.xml");
}


