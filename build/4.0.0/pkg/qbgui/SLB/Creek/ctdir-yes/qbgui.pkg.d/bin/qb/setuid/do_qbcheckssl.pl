#!/usr/bin/perl
#this script for when user login check username and password
#if math exit 0 
require ('/usr/local/apache/qb/qbmod.cgi');

my $QB_SSL = "/usr/local/apache/qbconf/ssllogin.xml";

my $sslinfo = XMLread($QB_SSL);
my $userlist = $sslinfo->{user};
#-----------------------------------------------------------------
if ( $sslinfo ) #if the string is NULL
{
    print "$QB_SSL_FILE is NULL \n";
}
#------------------------------------------------------------------    
       
foreach my $user ( @$userlist )
{
    if ( $user->{username} eq $ENV{username} && $user->{password} eq $ENV{password} )
    {
    	runCommand(command=>"echo", params=>'ok'.' '.'>/tmp/ssl');
    	exit 0;
    }
}

runCommand(command=>"echo", params=>$ENV{username}.' '.'>/tmp/ssl');
exit 1;
