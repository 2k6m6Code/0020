#!/usr/bin/perl
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );
print "Content-type:text/html\n\n";

use CGI;

#---------------- read-in form information ------------------------------
my $form=new CGI;
my %action;

#========================================================================
#GENERAL
$action{action}=$form->param('action');
$action{afs}=$form->param('afs');

$action{role}=$form->param('role');
$action{autofailover}=$form->param('autofailover');
$action{autoswitchback}=$form->param('autoswitchback');
$action{hosttimeout}=$form->param('hosttimeout');
$action{nicfail}=$form->param('nicfail');
$action{networktimeout}=$form->param('networktimeout');

$action{floatingip}=$form->param('floatingip');
$action{floatingipmask}=$form->param('floatingipmask');
$action{floatingport}=$form->param('floatingport');

$action{primaryconfigid}=$form->param('primaryconfigid');
$action{primarypip}=$action{floatingip};
$action{pripipmask}=$action{floatingipmask};
$action{pripipport}=$action{floatingport};

$action{primarysip}=$form->param('primarysip');
$action{prisipmask}=$form->param('prisipmask');
$action{primaryport}=$form->param('primaryport');

$action{slaveconfigid}=$form->param('slaveconfigid');
$action{slavepip}=$action{floatingip};
$action{slvpipmask}=$action{floatingipmask};

$action{slavesip}=$form->param('slavesip');
$action{slvsipmask}=$form->param('slvsipmask');
$action{slaveport}=$form->param('slaveport');

#========================================================
# collect virtual mac interface
my @vmacnicarray=$form->param('vmacnic');
my $vmacnic='';
foreach my $eth ( @vmacnicarray ) { $vmacnic.= $eth.':'; }
$vmacnic=~s/:$//g;
$action{vmacnic}=$vmacnic;

#=========================================================
my @hatargetlist;
for my $count (1..4)
{
    my $target=$form->param('target'.$count);
    if ( !$target ) { $target='system'; }
    my %targethash=(value=>$target);
    push( @hatargetlist, \%targethash );
}

$action{hatarget}=\@hatargetlist;


print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);

if ( $action{action} )
{
    print qq (<body class='hamessage'>);
    maintainHA( %action );
}
else
{
    print qq(<body bgcolor="#336699">);

    #------- start to draw every form object to interact with users ------------------------------------
    print qq (<div align="center">);
    print qq (<form name="consoleform" method="post" action="ha.cgi" target="result">);

    haScript();
    #if ( $gMODEL =~ m/^S400/) { # no HA on S400, S400Lite.
    #    noneFunctionExit('High Availability is an Option');
    #} elsif ( $gMODEL =~ m/^S200/) { # no HA on S200, S200Lite.
    #    noneFunctionExit('High Availability is an Option');
    #} elsif ( !$gENABLEHA ) {
    if ( $gENABLEVM ) { # no HA on S400, S400Lite.
        noneFunctionExit('High Availability is not supported for vmware version.');
    }
    if ( !$gENABLEHA ) {
        showHA0( %action );
    } else {
        showHA( %action ); 
    }
    print qq (<input type="hidden" name="action" value="">);
    print qq (</form>);
    print qq (</div>);

    general_script();
}

print qq(</body></html>);

