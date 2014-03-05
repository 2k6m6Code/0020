#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

require ("/usr/local/apache/qb/qbmod.cgi");

require ("/usr/local/apache/qb/auth/quotalogin.lib");
use CGI;
use JSON;
use QB_LOG;
use QB_Action;

my $form=new CGI;
my $json = new JSON;
my $log = QB_LOG->new();
my $action = QB_Action->new();
my $data = $form->param('POSTDATA') ;
my $reflist = XMLread($gPATH.'auth.xml');
my $quota = XMLread($gPATH.'quota.xml');
my $quotalist = $quota->{quota};
my $ip = '';
my $success = '0';
my $obj = $json->decode($data);
my $username=$obj->{'data'}->{'user'};
my $password=$obj->{'data'}->{'pwd'};
#$username='TOM';
#$password='123';
my $check='0';
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

if ($ENV{'HTTP_VIA'} && $ENV{'HTTP_X_FORWARDED_FOR'})
{
   ($fromip,$USE_DNS)=split(/\,/,$ENV{'HTTP_X_FORWARDED_FOR'});
   $ip=$ENV{'REMOTE_ADDR'};
}else 
{
   $ip = $ENV{'REMOTE_ADDR'};
}
   $username =~s/\s+//g;
   $password =~s/\s+//g;
   my $list = $reflist->{user};
   my $type;
   my $name_check = 0;
   my $badname ='';
   foreach my $server (@$list)
   {
       if ($server->{description} eq 'None'){next;}
       my $userlist = $server->{member};
       foreach my $user (@$userlist)
       {
           if ($user->{idd} eq $username && ($ip eq $user->{ip} || $user->{ip} eq ''))
           {
               $type = $user->{type};
               $name_check = 1;
           }
       }
   }
   my $ser=$reflist->{server};
   foreach my $name (@$ser)
   {
       if ($name->{enabled} eq '0' && $name->{schname} eq $type ){$type ='';}
   }
   if ($type eq 'LDAP')
   {
       #LDAP
       my $status = system("/mnt/ldapwhoami -H ldap://123.51.217.232:389 -x -D \"uid=$username,ou=rd,dc=creek,dc=com\" -w $password");
       if ($status =~m /Success/)
       {
           print qq($status);
       }
   }elsif ($type eq 'Radius')
   {
       #RADIUS
       my $list_r = $reflist->{server};
       my $ip,$group,$port;
       foreach my $ss  (@$list_r)
       {
           if ($ss->{schname} eq 'system' || $ss->{schname} eq 'LD'){next;}   
           $ip=$ss->{ip};
           $group=$ss->{group};
           $port=$ss->{port};
       } 
       #my $status = system("/usr/local/apache/qb/setuid/run /usr/local/bin/radtest $username $password 123.51.217.239 0 testing123 ");
       my @status = `/usr/local/apache/qb/setuid/run /usr/local/bin/radtest $username $password $ip $port $group`;
       #my @status = `/usr/local/apache/qb/setuid/run /tmp/radtest $username $password $ip $port $group`;
       foreach my $aa (@status)
       {
           if (!grep(/rad_recv:/,$aa)){next;}
           if (grep(/Accept/,$aa)){$success = '1';}
       }
   }elsif ($type eq 'AD')
   {
       #AD
       
   }elsif ($type eq 'LD')
   {
       foreach my $server (@$list)
       {
           if ($server->{description} eq 'None' || $server->{description} ne 'LD'){next;}
           my $userlist = $server->{member};
           my $ttime=time()+(8*60*60);
           foreach my $user (@$userlist)
           {
               if (($user->{idd} eq $username && ($ip eq $user->{ip} || $user->{ip} eq '') && ($user->{time} eq '' || ($ttime - $user->{time}) > 0)))
               {
                   $user->{time} = $ttime;
                   if ($user->{iip} ne '')
                   {
        		system("/usr/local/apache/qb/setuid/run /sbin/iptables -t nat -D AUTH -s $user->{iip} -j RETURN");
                   }
                   $user->{iip} = $ip;
                   $success = '1';
					foreach my $myquota (@$quotalist)
					{
						if($myquota->{name} eq $user->{idd})
						{
							system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D PREROUTING -d $myquota->{ip} -j $myquota->{name}.down");
							system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -D POSTROUTING -s $myquota->{ip} -j $myquota->{name}.up");
							$myquota->{ip}=$user->{iip}
						}
					}
               }
           }
           if ($success)
           {
				XMLwrite($quota,$gPATH.'quota.xml');
               XMLwrite($reflist,$gPATH.'auth.xml');
			   foreach $new_ip (@$quotalist)
			   {
					#print "$new_ip->{name}";
					if($new_ip->{name} eq $username){quotawork(quotaaction=>'CREAT', LINK=>$new_ip->{name});}
			   }
           }
       }
    }
    if ($name_check eq 0)
    {
        $badname = $username;
        $username='suspicious';
    }
    my @dd = split(/\//,$action->getdate());
    my $log_string = ($success)?("Success"):("Fail");
    $log->Save_Log("/mnt/tclog/auth/$username/$dd[0]/$dd[1]/",$dd[2],"$ip $log_string $badname");
    #system("/usr/local/apache/qb/setuid/run /bin/cp -a /tmp/tclog/auth/$username /mnt/tclog/auth/");
    system(sync);
    system(sync);
    system(sync);
    if ($success eq '1')
    {
        #system("/usr/local/apache/qb/setuid/run /sbin/iptables -t nat -I PREROUTING -s $ip -j ACCEPT");
        system("/usr/local/apache/qb/setuid/run /sbin/iptables -t nat -I AUTH -s $ip -j RETURN");
        #system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -I AUTH -d $ip -j ACCEPT");
        #system("/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -I AUTH -s $ip -j ACCEPT");
        print  "$ip,$success"
    }else
    {
        print  "$ip"
    }
