#!/usr/bin/perl
require ('/usr/local/apache/qb/qbmod.cgi');
my $showmode = $ARGV[0];
=cut
my $ispref=XMLread($gACTIVEPATH.'basic.xml');
my $isplist=$ispref->{isp};
runCommand(command=>'cat', params=>'/proc/net/ip_conntrack >/tmp/conntrack.log');
foreach my $isp ( @$isplist )
{
	if ( $isp->{iid} eq 'system' ) { next; }
	if ( $isp->{isptype} ne 'tunnel' &&  $isp->{isptype} ne 'ipsec' )
	{
	       #my $sessions = `cat /proc/net/ip_conntrack |awk '{print $12}'|grep -c $isp->{systemip}`;
	       my $sessions = `/opt/qb/bin/script/ispsession $isp->{iid}`;
	       print "$isp->{ispname} $sessions";
	}
}
runCommand(command=>'rm', params=>'-f /tmp/conntrack.log');
=cut
if ( $showmode eq "src" )
{
   my $session=runCommand(command=>'/opt/qb/bin/script/ispsession', params=>'src');
   my @sessionrecord=split(/\n/, $session);
        
   foreach my $record ( @sessionrecord )
   {
      my @sessioninfo=split(/\s+/, $record);
      print "$sessioninfo[0] $sessioninfo[1]\n";
   }
}else{
   my $session=runCommand(command=>'/opt/qb/bin/script/ispsession', params=>'nat');
   my @sessionrecord=split(/\n/, $session);
        
   foreach my $record ( @sessionrecord )
   {
      my @sessioninfo=split(/\s+/, $record);
      print "$sessioninfo[0] $sessioninfo[1]\n";
   }
} 
