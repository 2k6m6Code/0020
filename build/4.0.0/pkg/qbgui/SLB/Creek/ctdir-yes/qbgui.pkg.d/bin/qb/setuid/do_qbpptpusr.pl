#!/usr/bin/perl
use File::Copy;

require ('/usr/local/apache/qb/qbmod.cgi');

# --------------------------
#
# main program start routine
#
# --------------------------
my $QB_PPDLOGIN_FILE="/usr/local/apache/active/ppdlogin.xml";
my $chap_secrets_file = '/etc/ppp/chap-secrets';
my $pap_secrets_file = '/etc/ppp/pap-secrets';
my $ppduser=XMLread($QB_PPDLOGIN_FILE);
my $userList=$ppduser->{user};
if(!$ppduser) { print "$QB_PPDLOGIN_FILE is NULL \n"; }#if the string is NULL
#------------------------------------------------------------------
copy("$chap_secrets_file-bak","$chap_secrets_file");
copy("$pap_secrets_file-bak","$pap_secrets_file");
foreach my $ppduser ( @$userList )
{
    if ( $ppduser->{username} eq 'system' ) { next; }
    if ( $ppduser->{username} )
    {
        print "$ppduser->{username} $ppduser->{password} $ppduser->{assignip} \n";
        runCommand(command=>'ppusradd', params=>' --create --username '.$ppduser->{username}.' --password '.$ppduser->{password}.' --assignip '.$ppduser->{assignip});
    }
}
