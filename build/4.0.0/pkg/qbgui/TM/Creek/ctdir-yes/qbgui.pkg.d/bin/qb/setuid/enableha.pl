#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');


# ---------------------------------------------------------------
# unpack function.pkg to <dir>/conf/registry.
# ---------------------------------------------------------------
sub check_registry
{
    my $tmp_dir=$_[0];

    # ensure there's no more file in <dir>/conf/...041230

    my $cmd='/bin/tar zxfC /mnt/function.pkg '.$tmp_dir;
    `$cmd`;
    my $ENABLEHA=0;

    my $REGISTRY_FILE=$tmp_dir.'/conf/registry';
    if ( open(IN,"<$REGISTRY_FILE") ) {
        while (<IN>) {
            chomp;
            if ( $_=~m/^ENABLEHA\s+(\S+)\s*/ ) {$ENABLEHA=$1; last;}
        } 
        close(IN);
    }
    return $ENABLEHA;
}


# ---------------------------------------------------------------
# edit /mnt/syslinux.cfg for HA. 1st line: HA+EZIO, 2nd line: HA+qbcli
# ---------------------------------------------------------------
sub syslinux
{
    my $SYSLINUX_FILE="/mnt/syslinux.cfg";
    my $HA_SERIAL="SERIAL 0 19200";
    my $HA_SERIAL1="SERIAL 1 19200";
    my $BMONPORT_FILE="/mnt/conf/afsconf/bmonport";  #20080313 Brian for S400/S200 HW
    my $HA_TTY0="/dev/ttyS0";
    my $HA_TTY1="/dev/ttyS1";

    my $HA_EZIO='APPEND console=tty0 root=/dev/ram0 initrd=image.gz';
    my $HA_qbcli='APPEND console=tty0 console=ttyS0,19200n8 root=/dev/ram0 initrd=image.gz';
    my $HA_null='APPEND console=tty0 console=null,19200n8 root=/dev/ram0 initrd=image.gz';  #20080313 Brian for S400/S200 HW

    if ($gEZIOTYPE) {
        modifyfile($SYSLINUX_FILE,'^\s*#\s*'.$HA_EZIO,"\t".$HA_EZIO);
        modifyfile($SYSLINUX_FILE,'^\s*#*\s*'.$HA_qbcli,"\t# ".$HA_qbcli);
    } else {
            if ($gMANUFACTURER=~m/ARINFOTEK/ || $gHARDWARE=~m/NA-100/) {
        modifyfile($BMONPORT_FILE,'^\s*'.$HA_TTY1, $HA_TTY0);
        modifyfile($SYSLINUX_FILE,'^\s*'.$HA_SERIAL, $HA_SERIAL1);
        modifyfile($SYSLINUX_FILE,'^\s*\s*'.$HA_EZIO,"\t#".$HA_EZIO);
        modifyfile($SYSLINUX_FILE,'^\s*#*\s*'.$HA_qbcli,"\t ".$HA_null);
        }else {
        modifyfile($SYSLINUX_FILE,'^\s*#*\s*'.$HA_EZIO,"\t# ".$HA_EZIO);
        modifyfile($SYSLINUX_FILE,'^\s*#\s*'.$HA_qbcli,"\t".$HA_qbcli);
        }
    }
}

# ---------------------------------------------------------------
# MAIN:
#
# 1. unpack function.pkg to check ENABLEHA (create temp registry)
# ---------------------------------------------------------------
my $tmp_dir='/tmp';
my $ha = check_registry($tmp_dir);
if ( $ha ) { print "HA is already enable.\n\nPlease restart Q-Balancer to lanuch HA.\n"; exit; }

# ---------------------------------------------------------------
# 1a. change ENABLEHA => 1 in <dir>/conf/registry
# ---------------------------------------------------------------
print "Change registry ...\n";
my $REGISTRY_FILE=$tmp_dir.'/conf/registry';
my $enableha="ENABLEHA";
modifyfile($REGISTRY_FILE,$enableha.'\s+.+',$enableha.' 1');

# ---------------------------------------------------------------
# 1b. repack  function package
# ---------------------------------------------------------------
chdir $tmp_dir;
my $cmd='/bin/tar zcf /mnt/function.pkg ./conf/ ';
`$cmd`;
my $cmd='/bin/sync';
`$cmd`;


# ---------------------------------------------------------------
# 2. edit syslinux.cfg 
# ---------------------------------------------------------------
print "Change syslinux ...\n";
my $syslinux = syslinux();
if ( $syslinux ) { print "Finish HA enable.\nPlease restart Q-Balancer !\n"; }
else { print "Fail to enable HA.\nPlease try again !!\n"; }
qbSync(); #20130419 To prevent DOM/CF become readonly
