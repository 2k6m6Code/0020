#!/usr/bin/perl
 
require ('/usr/local/apache/qb/qbmod.cgi');

my $QB_BASIC = "/usr/local/apache/active/basic.xml";
my $QB_CLIENT = "/usr/local/apache/qbconf/client.xml";
my $ispinfo = XMLread($QB_BASIC);
my $isplist = $ispinfo->{isp};
my $client = XMLread($QB_CLIENT);
my $isplist = $ispinfo->{isp};
#-----------------------------------------------------------------
if ( !$ispinfo ) #if the string is NULL
{
    print "$QB_BASIC_FILE is NULL \n";
}
#------------------------------------------------------------------    
my $logfile = "/mnt/qb/conf/cms";
if (-e $logfile)
{
}else{
runCommand(command=>'mkdir' ,params=>"$logfile");
runCommand(command=>'sync' ,params=>""); #20130419 To prevent DOM/CF become readonly
}

foreach my $isp ( @$isplist )
{
    if ( $isp->{isptype} eq 'tunnel' || $isp->{isptype} eq 'dtunnel' )
    {
        if ( $isp->{alive} eq '1' )
        {
        
            my $info=runCommand(command=>'/usr/local/apache/qb/setuid/catclient.sh', params=>$isp->{gateway});
           print "$info\n";
           @allinfo=split('\;', $info);
        
           $isp->{qbsn}=$allinfo[0];
           $isp->{qbsn}=~s/[\s\n]//g;
           $isp->{info}=$allinfo[1];
           $isp->{info}=~s/[\s\n]//g;
           $isp->{upgradestate}='None';
           $isp->{image}=$allinfo[2];
           $isp->{image}=~s/[\n]//g;
           $isp->{fs}=$allinfo[3];
           $isp->{fs}=~s/[\n]//g;
           $isp->{regist}=$allinfo[4];
           $isp->{regist}=~s/\sRegister_date\s//g;
           $isp->{warranty}=$allinfo[5];
           $isp->{warranty}=~s/\sWarranty_date_00\s//g;
           $isp->{upgradestate}=$allinfo[6];
           $isp->{upgradestate}=~s/[\s]//;
           $allinfo[7]=~s/\:/\ Hour\ /g;
           $allinfo[7]=~s/days/\ Day\ /g;
           $allinfo[7]=~s/day/\ Day\ /g;
          $isp->{uptime}=$allinfo[7].' Min';
#           $isp->{uptime}=~s/[\s]//;
           $isp->{reboot_time}=$allinfo[8];
           $isp->{reboot_time}=~s/[\s]//;
        }
        else
        {
           $isp->{qbsn}='';
        }
        
    }
}

XMLwrite($ispinfo, $gACTIVEPATH."basic.xml");
