#!/usr/bin/perl

use CGI;

require ("/usr/local/apache/qb/qbmod.cgi");

print "Content-type: text/html\n\n";

my $cgi=new CGI;
my $data=$cgi->param('data');
my $action=$cgi->param('action');
my $action1=$cgi->param('action1');
my $creat = '0';
if ($action eq 'LOGO')
{
    open(FILE,">/usr/local/apache/qb/auth/message.htm");
    print FILE $data;
    close(FILE);
    syatem("/usr/local/apache/qb/setuid/run /bin/cp -a /usr/local/apache/qb/auth/message.htm /mnt/qb/conf/auth/image/");
    system("/bin/sync");
    system("/bin/sync");
    system("/bin/sync");
}
elsif ($action eq 'MAIL')
{
    system("/usr/local/apache/qb/setuid/run /bin/rm -rf /mnt/qb/conf/auth/*");
    system("/bin/sync");
    system("/bin/sync");
    system("/bin/sync");
    my @tmp=split(/,/,$data);
    my $name = $tmp[0].".message";
    open(FILE1,">/usr/local/apache/qb/auth/$name");
    print FILE1 $tmp[1];
    close(FILE1);
    
    system("/usr/local/apache/qb/setuid/run /bin/cp -a /usr/local/apache/qb/auth/$name /mnt/qb/conf/auth/");
    system("/bin/sync");
    system("/bin/sync");
    system("/bin/sync");
}
elsif ($action eq 'Timer')
{
    my $filelist=XMLread("/usr/local/apache/qbconf/auth.xml");
    my $list=$filelist->{user};
    ($login_time,$idle_time,$time_hr,$time_sec)=split(/,/,$data);
    foreach my $user (@$list)
    {
        if ($user->{schname} eq 'system')
        {
           $user->{login_time} = ($login_time)?($login_time):('43200');
           $user->{idle_time} = ($idle_time)?($login_time):('43200');
           if ($user->{time_hr} ne $time_hr || $user->{time_sec} ne $time_sec){$creat = '1';}
           $user->{time_hr} = ($time_hr)?($time_hr):('23');
           $user->{time_sec} = ($time_sec)?($time_sec):('59');
        }
    }    
    XMLwrite($filelist, "/usr/local/apache/qbconf/auth.xml");
    if ($action1 ne '')
    {
        $creat = '1';
    }
    if ($creat eq '1')
    {
	my @tmp_data;
	my $checkaa=0;
	open (FILE ,"</etc/crontab"); 
	foreach my $data (<FILE>)
	{
	    if (grep(/auth_open.pl/,$data))
	    {
	        next;
	    }
	    push(@tmp_data,$data);   
	} 
    	close(FILE);
      	
        foreach my $user (@$list)
        {
            if ($user->{schname} eq 'system')
            {
	        my $data1 = "$user->{time_hr}  $user->{time_sec} * * *  root      /usr/local/apache/qb/auth_open.pl action=OPEN\n";
    		push(@tmp_data,$data1);
   	    }
   	}
    	open (FILE1 ,">/tmp/crontab");
    	foreach my $data (@tmp_data)
    	{
    	    print FILE1 $data;
    	}
    	close(FIEL1);
    	system("/usr/local/apache/qb/setuid/run /bin/chmod 644 /tmp/crontab");
    	system("/usr/local/apache/qb/setuid/run /bin/cp -af /tmp/crontab /etc/");
    }
}

