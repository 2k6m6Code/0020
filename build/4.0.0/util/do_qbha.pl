#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
my $QB_CONF_DIR="/mnt/qb/conf/set";
my $QBHA_CONF_DIR="/mnt/qb/conf/ha";
my $AFSBOOT_FLAG_FILE="/mnt/qb/conf/ha/AFSBOOT";
my $AFS_WORK_DIR="/usr/afs";
my $AFS_CONF_DIR="/usr/afs/conf";
my $AFS_MONPORT_FILE="/usr/afs/conf/monport";
my $QBHA_XML_FILE="/usr/local/apache/config/ha.xml";
my $SYSINIT_FILE="/opt/qb/bin/script/sysinit";
my $SPROG_FILE=$AFS_CONF_DIR."/sprog";
my $SNET_FILE=$AFS_CONF_DIR."/snet";
my $new_str;
my $statement;
my $statement1;

my $cmd='mkdir /tmp/doqbha';
`$cmd`;
my $cmd='/bin/tar zxfC /mnt/script.pkg /tmp/doqbha/';
`$cmd`;

#------------------------------------------------------------------
# read the option from the file  /mnt/qb/conf/ha/basic
#------------------------------------------------------------------
my $haopt=XMLread($QBHA_XML_FILE);

if( !$haopt ) #if the string is NULL
{
    print "$QBHA_XML_FILE is NULL \n";
}


#------------------------------------------------------------------
# set monport of ha heart beat 
#------------------------------------------------------------------
my $monport=( $gEZIOTYPE  && $gENABLEHA ) ? '/dev/ttyS0' : '/dev/ttyS1';
if ($gMANUFACTURER=~m/ARINFOTEK/ || $gHARDWARE=~m/NA-100/ || $gHARDWARE=~m/NA320R/) { #20080318 Brian For S400 HW.
$monport="/dev/ttyS0";
}
open(MONPORT, ">$AFS_MONPORT_FILE");
print MONPORT $monport."\n";
close(MONPORT);


#------------------------------------------------------------------
# set network failover option according to the config of the file  
#------------------------------------------------------------------
if( !exists($haopt->{nicfail}) ) # if the string is NULL 
{
    print "$QBHA_XML_FILE => nicfail=NULL \n";
}

$statement= "A:init:-:/usr/afs/NDEV A:/usr/afs/stopp NDEV A";

if ( $haopt->{nicfail} eq '1' ) 
{
    modifyfile($SPROG_FILE,"^#*".$statement,$statement); # remove # character in the stateament 
} 
elsif ( $haopt->{nicfail} eq '0' ) 
{
    modifyfile($SPROG_FILE,"^#*".$statement,"#".$statement); # add # character in the statement
}
else
{
    print "ERROR: INVALID PARAMETER \n"; 
    exit;
}


#------------------------------------------------------------------
# set afs start on booting flag file  according to the config of the file  
#------------------------------------------------------------------
if( !exists($haopt->{afs}) ) # if the string is NULL 
{
    print "$QBHA_XML_FILE => afs=NULL \n";
}

if ( $haopt->{afs} eq '1' )
{
    runCommand(command=>"touch", params=> qq($AFSBOOT_FLAG_FILE) );
}
elsif ( $haopt->{afs} eq '0' ) 
{ 
    runCommand(command=>"rm", params=> qq(-rf $AFSBOOT_FLAG_FILE) );
}
else
{
    print "ERROR: INVALID PARAMETER \n"; 
    exit;
}


#------------------------------------------------------------------
# modify SNET_FILE option according to the config of the file
#------------------------------------------------------------------
my $SNET_TEMP_FILE=$SNET_FILE.".tmp";
my @iparray;
my $maskaddr;
my $bcastaddr;

my $hatargets=$haopt->{hatarget};
foreach my $target ( @$hatargets ) { if ( $target->{value} ne 'system' ) { push(@iparray, $target->{value}); } }

open(IN, $SNET_FILE);
open(OUT, ">$SNET_TEMP_FILE");

while (<IN>)
{
    if($_=~/^#/)   # don't care the comment line
    {
        print OUT $_;
        next;
     }    

    if ( $_=~/NDEV/ )
    {
        next;
    }
    elsif ($_=~ /HAN1/)  #  catch the lines "HAN1", modify it 
    {
        $maskaddr=nummask2ipmask($haopt->{prisipmask});
        $bcastaddr=get_bcast_ip_with_ipmask($haopt->{primarysip},$maskaddr);
        print OUT "HAN1 $haopt->{primaryport} $haopt->{primarysip} $maskaddr $bcastaddr hostA \n"; 
    }
    elsif ($_ =~ /HBN1/)   #  catch the lines "HBN1", modify it 
    {
        $maskaddr=nummask2ipmask($haopt->{slvsipmask});
        $bcastaddr=get_bcast_ip_with_ipmask($haopt->{slavesip},$maskaddr);
        print OUT "HBN1 $haopt->{slaveport} $haopt->{slavesip} $maskaddr $bcastaddr hostB \n";
    }
    elsif ($_=~ /HASVCA/)   
    {
        $maskaddr=nummask2ipmask($haopt->{pripipmask});
        $bcastaddr=get_bcast_ip_with_ipmask($haopt->{primarypip},$maskaddr);
        print OUT "HASVCA $haopt->{floatingport} $haopt->{primarypip} $maskaddr $bcastaddr apserverA \n"; 
    }
    elsif ($_ =~  /HBSVCA/)    
    {
        $maskaddr=nummask2ipmask($haopt->{slvpipmask});
        $bcastaddr=get_bcast_ip_with_ipmask($haopt->{slavepip},$maskaddr);
       #  print OUT "HBSVCA $haopt->{slaveport} $haopt->{slavepip} $maskaddr $bcastaddr apserverB \n";  # 050107 equal with A.
        print OUT "HBSVCA $haopt->{floatingport} $haopt->{slavepip} $maskaddr $bcastaddr apserverB \n"; 
    }
    else
    {
        print OUT $_;
    }
}

# configure NDEV entries
foreach $item (@iparray)  { print OUT "NDEV $item\n"; }

close(IN);
close(OUT);

unlink($SNET_FILE);
rename($SNET_TEMP_FILE,$SNET_FILE);


# -----------------------------------------------
# build qbha.sh 
# -----------------------------------------------
my $QBHA_FILE="/tmp/doqbha/script/qbha.sh";
my $QB_ACTIVE_DIR="/usr/local/apache/active";
my $QB_QBCONF_DIR="/usr/local/apache/qbconf";
my $QBSERVER_DONE_TO_INFORM_AFS="/var/run/qbserver_is_done";

open(OUT,">$QBHA_FILE");
print OUT "#! /bin/sh \n";
print OUT "rm -rf $QBSERVER_DONE_TO_INFORM_AFS \n";

print OUT "case \"\$1\" in  \n";

print OUT "boot)   \n";
print OUT "cp -rf $QB_CONF_DIR/$haopt->{slaveconfigid}/* $QB_ACTIVE_DIR \n";
print OUT "cp -rf $QB_CONF_DIR/$haopt->{slaveconfigid}/* $QB_QBCONF_DIR \n";
print OUT "chmod 777 $QB_ACTIVE_DIR/* \n";
print OUT "chmod 777 $QB_QBCONF_DIR/* \n";
print OUT "sync \n";
print OUT "echo 101 > /tmp/fifo.qbserv  \n";
print OUT ";;      \n";

print OUT "start)  \n";
print OUT "cp -rf $QB_CONF_DIR/$haopt->{primaryconfigid}/* $QB_ACTIVE_DIR \n";
print OUT "cp -rf $QB_CONF_DIR/$haopt->{primaryconfigid}/* $QB_QBCONF_DIR \n";
print OUT "chmod 777 $QB_ACTIVE_DIR/* \n";
print OUT "chmod 777 $QB_QBCONF_DIR/* \n";
print OUT "sync \n";

# config virtual mac on selected interfaces
my @vmacarray=split(/:/, $haopt->{vmacnic});
foreach my $nic ( sort @vmacarray )
{
    print $nic;
    my $mac_tail=$nic; $mac_tail=~s/eth/0/g; 
    print OUT qq(ifconfig $nic down \n);
    print OUT qq(ifconfig $nic hw ether 00:90:fb:fe:fe:$mac_tail \n);
    print OUT qq(ifconfig $nic up \n);
}

#00:90:fb:fe:fe:01
#00:90:fb:fe:fe:02

#20090406 Brian For vlan device
print OUT "/usr/local/apache/qb/setuid/do_qbvlan.pl \n";

print OUT "echo 101 > /tmp/fifo.qbserv  \n";
#20090406 Brian For PPPoE & DHCP client
print OUT "sleep 60 \n";  #Wait sysinit's change level.
print OUT "/sbin/dhcpstart \n";
print OUT "/mnt/pppoe/pppstart \n";
print OUT "/opt/qb/bin/script/enable_analyser &\n";
print OUT ";;      \n";

print OUT "stop)   \n";
print OUT "(sleep 3; /sbin/reboot) & \n";
print OUT ";;     \n";

print OUT "esac    \n";
print OUT "exit 0  \n";


close(OUT);

chmod(0755,$QBHA_FILE);

# repack  script package in /mnt/script.pkg
chdir '/tmp/doqbha';
my $cmd='/bin/tar zcf /mnt/script.pkg script/ ';
`$cmd`;
my $cmd='/bin/sync';
`$cmd`;

# cp ha.xml from /usr/local/apache/config/ha.xml  to  /mnt/qb/conf/ha.xml
open(HAXMLSOURCE, '< /usr/local/apache/config/ha.xml' );
open(HAXMLTARGET, '> /mnt/qb/conf/ha.xml' );
while (<HAXMLSOURCE>) { print HAXMLTARGET $_; }
close(HAXMLTARGET);
close(HAXMLSOURCE);
qbSync(); #20130419 To prevent DOM/CF become readonly
