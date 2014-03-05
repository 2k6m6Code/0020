#!/usr/bin/perl
require ("qbmod.cgi");
print "Content-type:text/html\n\n";

use CGI;
use Data::Dumper;

    my  $form = new CGI;
    my $beip=$form->param('beip');
    my $limit_time=$form->param('limit_time');
    
    #my $USERLOCK_LIST='/usr/local/apache/active/userlock_list';
    my $lock_list=runCommand(command=>'/usr/local/apache/qb/setuid/getlocklist.sh', params=>$beip.' '.$limit_time);
=cut 
    my $ALL_USER_LOCK_LIST=runCommand(command=>'cat', params=>'/usr/local/apache/active/userlock_list' );
    my @ALL_LOCK_ARRAY=split('\n',$ALL_USER_LOCK_LIST);
    
    my $LOCKUSER_TABLE_CMD = "/usr/local/apache/active/userlock_cmd";
 
    if ( !open(LOCKUSER_TABLE, ">$LOCKUSER_TABLE_CMD") )
    {
     	print "open lock-user-table fail!!\n";
     	return;
    }
    print LOCKUSER_TABLE qq " # ************ Drop User list ************ \n";
    foreach my $lock_ip (@ALL_LOCK_ARRAY)
    {
    	foreach my $type ( 'FORWARD','INPUT','OUTPUT' )
    	{
    	  print LOCKUSER_TABLE qq "/sbin/iptables -D $type -s $lock_ip -j DROP & \n";
    	  print LOCKUSER_TABLE qq "/sbin/iptables -D $type -d $lock_ip -j DROP & \n";
    	  print LOCKUSER_TABLE qq "/sbin/iptables -$action $type -s $lock_ip -j DROP & \n";
    	  print LOCKUSER_TABLE qq "/sbin/iptables -$action $type -d $lock_ip -j DROP & \n";
    	}
    }
    close(LOCKUSER_TABLE);
    chmod(0777, $LOCKUSER_TABLE_CMD);
=cut    
#

