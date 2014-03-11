#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# --------------------------
# main program start routine
# --------------------------

#----------------------------
# Level-Facility to file hash

my %FILE_OR_SERVER=(
                'local2.warn'               =>  '/mnt/log/runway.log',
                'local4.info'               =>  '/var/log/diagnose.log',
                'daemon.*'                  =>  '/var/log/daemon.log'
);

my %FILE_ANALY=(
                'local5.info'               =>  '/mnt/tclog/squidaccess.log',
                'kern.info;kern.!notice'    =>  '/mnt/tclog/traffic.log',
                'kern.notice;kern.!warning' =>  '/mnt/tclog/service.log'
);

my %SYSLOGFTP=(
                'kern.info;kern.!notice'    =>  '/mnt/tclog/traffic0.log',
                'kern.notice;kern.!warning' =>  '/mnt/tclog/service0.log'
);

my %ONLY2SERVER=(
#                'kern.notice'   =>  '1',
#                'kern.info'     =>  '1', 
                 'kern.warn'     =>  '1' 
);

my %MUST2FILE=(
                'kern.emerg'      =>  '/mnt/log/panic.log',
                'kern.alert'      =>  '/mnt/log/alert.log',
                'local3.*'        =>  '/var/log/qbalancer.log'
);



my $QB_SYSLOG_FILE="/usr/local/apache/config/syslog.xml";
my $QB_SYSLOG_CONF="/etc/syslog.conf";
my $QB_SQUID_CONF="/etc/squid/squid.conf";
my $QB_CRONTAB="/etc/crontab";
my $accesslog= "access_log syslog:local5.info squid";
#=======================================================
# parsing syslog.xml into $syslog

my $syslog=XMLread($QB_SYSLOG_FILE);

#=========================================================
# store the ip of remote syslog server in $SYSLOGSERVER
my $SYSLOGSERVER=$syslog->{syslogserverip};

if(!$syslog) #if the string is NULL
{
    print "$QBHA_SYSLOG_FILE is NULL \n";
}


#------------------------------------------------------------------
if ( !open(SYSLOG,">$QB_SYSLOG_CONF") )
{
    print qq (Fail to Open SYSLOG Config file !!);
}

my $checktclog=runCommand(command=>'df', params=>qq(-h \|grep tclog) );

foreach my $type ( keys  %FILE_OR_SERVER )
{
    if ( !$syslog->{serverlog} && $type eq 'local4.info' )  {  next; } #Brian 20080918 let user can enable or disable serverlog.
    if ( $syslog->{syslogserver} )  {   print SYSLOG qq($type       \@$SYSLOGSERVER\n); }
    if ( $syslog->{locallog} )      {   print SYSLOG qq($type       $FILE_OR_SERVER{$type}\n); }
}

foreach my $type ( keys  %FILE_ANALY )
{
    #Check for Server first
    if ( !$syslog->{squidlog} && $type eq 'local5.info' )  {  next; }
    if ( !$syslog->{kernellog} && $type eq 'kern.info;kern.!notice' )  {  next; }
    if ( !$syslog->{kernellog} && $type eq 'kern.notice;kern.!warning' )  {  next; }
    if ( $syslog->{syslogserver} )  {   print SYSLOG qq($type       \@$SYSLOGSERVER\n); }
    #Check for tclog later
    #if ( !$checktclog )  {  next; }
    #if ( $syslog->{locallog} && $gENABLEANALYSER )      {   print SYSLOG qq($type       $FILE_ANALY{$type}\n); } #Brian 20120731 To prevent traffic log is saved in the CF.
}

if ( $syslog->{kernellog} ) #20080424 Brian Let QB's Traffic log can be disabled
{
      foreach my $type ( keys  %ONLY2SERVER )
      {
          if ( $syslog->{syslogserver} ) { print SYSLOG qq($type         \@$SYSLOGSERVER\n);       }
      }
}

if ( $syslog->{kernellog} && $checktclog ) #20090720 Brian to separate syslog for syslogftp function
{
      foreach my $type ( keys  %SYSLOGFTP )
      {
          if ( $syslog->{syslogdev} ) { print SYSLOG qq($type         $SYSLOGFTP{$type}\n);       }
      }
}

foreach my $type ( keys  %MUST2FILE )
{
    print SYSLOG qq($type         $MUST2FILE{$type}\n);
}

close(SYSLOG);
qbSync(); #20080424 To prevent DOM/CF become readonly
if ( $syslog->{ftpserverip} && $syslog->{ftpserver})
{
    if ( $syslog->{ftpfrequency}=~m/day/)
    {
      $syslog->{ftpfrequency}=~s/\.day//g;
      modifyfile($QB_CRONTAB,"syslogftp.*","syslogftp ".$syslog->{ftpserverip}." ".$syslog->{ftpusername}." ". $syslog->{ftppassword}." ".$syslog->{ftpdir}); # refresh https proxy port No.
      modifyfile($QB_CRONTAB,"^#.*syslogftp","0 0 */$syslog->{ftpfrequency} * *  root       /opt/qb/bin/script/syslogftp"); # remove # character in the stateament
      modifyfile($QB_CRONTAB,"^*.*syslogftp","0 0 */$syslog->{ftpfrequency} * *  root       /opt/qb/bin/script/syslogftp"); # remove # character in the stateament
    }
    if ( $syslog->{ftpfrequency}=~m/hour/)
    {
      $syslog->{ftpfrequency}=~s/\.hour//g;
      modifyfile($QB_CRONTAB,"syslogftp.*","syslogftp ".$syslog->{ftpserverip}." ".$syslog->{ftpusername}." ". $syslog->{ftppassword}." ".$syslog->{ftpdir}); # refresh https proxy port No.
      modifyfile($QB_CRONTAB,"^#.*syslogftp","0 */$syslog->{ftpfrequency} * * *  root       /opt/qb/bin/script/syslogftp"); # remove # character in the stateament
      modifyfile($QB_CRONTAB,"^*.*syslogftp","0 */$syslog->{ftpfrequency} * * *  root       /opt/qb/bin/script/syslogftp"); # remove # character in the stateament
    }
    if ( $syslog->{ftpfrequency}=~m/everyd/)
    {
      $syslog->{ftpfrequency}=~s/\.everyd//g;
      modifyfile($QB_CRONTAB,"syslogftp.*","syslogftp ".$syslog->{ftpserverip}." ".$syslog->{ftpusername}." ". $syslog->{ftppassword}." ".$syslog->{ftpdir}); # refresh https proxy port No.
      modifyfile($QB_CRONTAB,"^#.*syslogftp","0 $syslog->{ftpfrequency} * * *  root       /opt/qb/bin/script/syslogftp"); # remove # character in the stateament
      modifyfile($QB_CRONTAB,"^*.*syslogftp","0 $syslog->{ftpfrequency} * * *  root       /opt/qb/bin/script/syslogftp"); # remove # character in the stateament
    }
}
else
{
    modifyfile($QB_CRONTAB,"^#*"."syslogftp","#"."syslogftp"); # Disable https proxy function
}
                    
