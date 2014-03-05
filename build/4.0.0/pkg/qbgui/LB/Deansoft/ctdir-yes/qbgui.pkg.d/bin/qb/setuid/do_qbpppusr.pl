#!/usr/bin/perl
use File::Copy;

require ('/usr/local/apache/qb/qbmod.cgi');

# --------------------------
#
# main program start routine
#
# --------------------------
my $QB_L2TPLOGIN_FILE="/usr/local/apache/active/l2login.xml";
my $QB_PPDLOGIN_FILE="/usr/local/apache/active/ppdlogin.xml";
my $chap_secrets_file = '/etc/ppp/chap-secrets';
my $pap_secrets_file = '/etc/ppp/pap-secrets';
my $l2tpuser=XMLread($QB_L2TPLOGIN_FILE);
my $ppduser=XMLread($QB_PPDLOGIN_FILE);

if(!$ppduser) { print "$QB_PPDLOGIN_FILE is NULL \n"; }#if the string is NULL
if(!$l2tpuser) { print "$QB_L2TPLOGIN_FILE is NULL \n"; }#if the string is NULL
#------------------------------------------------------------------
copy("$chap_secrets_file-bak","$chap_secrets_file");
copy("$pap_secrets_file-bak","$pap_secrets_file");

my $userList=$l2tpuser->{user};
foreach my $ppduser ( @$userList )
{
    if ( $ppduser->{username} eq 'system' ) { next; }
    if ( $ppduser->{username} )
    {
	print "$ppduser->{username} $ppduser->{password} $ppduser->{assignip} \n";
        runCommand(command=>'ppusradd', params=>' --create --username '.$ppduser->{username}.' --password '.$ppduser->{password}.' --assignip '.$ppduser->{assignip});
    }
}


my $userList=$ppduser->{user};
foreach my $ppduser ( @$userList )
{
    if ( $ppduser->{username} eq 'system' ) { next; }
    if ( $ppduser->{username} )
    {
	print "$ppduser->{username} $ppduser->{password} $ppduser->{assignip} \n";
        runCommand(command=>'ppusradd', params=>' --create --username '.$ppduser->{username}.' --password '.$ppduser->{password}.' --assignip '.$ppduser->{assignip});
    }
}
