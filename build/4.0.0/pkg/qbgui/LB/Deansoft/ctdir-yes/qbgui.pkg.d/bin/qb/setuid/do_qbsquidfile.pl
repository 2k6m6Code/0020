#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start
# --------------------------------------------------------------
my $QB_SQUID="/usr/local/squid/etc/";
my $QB_SQUID_CONF="/etc/squid/squid.conf";
my $QB_SQUID_XMLCONF="/usr/local/apache/qbconf/squidfil.xml";
my $QB_SQUID_BLKFILE=$QB_SQUID."blockfile.txt";

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/squidgen.xml
#------------------------------------------------------------------
my $squid=XMLread($QB_SQUID_XMLCONF);

if ( !$squid ) #if the string is NULL
{
    print "$QB_SQUID_FILE_XMLCONF is NULL \n";
}

if ( !open(BLKFILE,">$QB_SQUID_BLKFILE") )
{
   print qq (Fail to Open BLKFILE Config file !!);
}

if ( $squid->{mp3} eq '1' ) { print BLKFILE qq "\\\.mp3\$\n"; }
if ( $squid->{mp4} eq '1' ) { print BLKFILE qq "\\\.mp4\$\n"; }
if ( $squid->{wma} eq '1' ) { print BLKFILE qq "\\\.wma\$\n"; }
if ( $squid->{wmv} eq '1' ) { print BLKFILE qq "\\\.wmv\$\n"; }
if ( $squid->{mpg} eq '1' ) { print BLKFILE qq "\\\.mpg\$\n"; }
if ( $squid->{mpeg} eq '1' ) { print BLKFILE qq "\\\.mpeg\$\n"; }
if ( $squid->{rm} eq '1' ) { print BLKFILE qq "\\\.rm\$\n"; }
if ( $squid->{rmvb} eq '1' ) { print BLKFILE qq "\\\.rmvb\$\n"; }
if ( $squid->{avi} eq '1' ) { print BLKFILE qq "\\\.avi\$\n"; }
if ( $squid->{mov} eq '1' ) { print BLKFILE qq "\\\.mov\$\n"; }
if ( $squid->{zip} eq '1' ) { print BLKFILE qq "\\\.zip\$\n"; }
if ( $squid->{rar} eq '1' ) { print BLKFILE qq "\\\.rar\$\n"; }
if ( $squid->{tgz} eq '1' ) { print BLKFILE qq "\\\.tgz\$\n"; }
if ( $squid->{gz} eq '1' ) { print BLKFILE qq "\\\.gz\$\n"; }
if ( $squid->{z7z} eq '1' ) { print BLKFILE qq "\\\.7z\$\n"; }
if ( $squid->{exe} eq '1' ) { print BLKFILE qq "\\\.exe\$\n"; }
if ( $squid->{bin} eq '1' ) { print BLKFILE qq "\\\.bin\$\n"; }
if ( $squid->{dll} eq '1' ) { print BLKFILE qq "\\\.dll\$\n"; }
if ( $squid->{msi} eq '1' ) { print BLKFILE qq "\\\.msi\$\n"; }
if ( $squid->{bat} eq '1' ) { print BLKFILE qq "\\\.bat\$\n"; }
if ( $squid->{iso} eq '1' ) { print BLKFILE qq "\\\.iso\$\n"; }
if ( $squid->{doc} eq '1' ) { print BLKFILE qq "\\\.doc\$\n"; }
if ( $squid->{pdf} eq '1' ) { print BLKFILE qq "\\\.pdf\$\n"; }
if ( $squid->{ppt} eq '1' ) { print BLKFILE qq "\\\.ppt\$\n"; }
if ( $squid->{reg} eq '1' ) { print BLKFILE qq "\\\.reg\$\n"; }
if ( $squid->{pif} eq '1' ) { print BLKFILE qq "\\\.pif\$\n"; }
if ( $squid->{chm} eq '1' ) { print BLKFILE qq "\\\.chm\$\n"; }
if ( $squid->{vbs} eq '1' ) { print BLKFILE qq "\\\.vbs\$\n"; }
if ( $squid->{scr} eq '1' ) { print BLKFILE qq "\\\.scr\$\n"; }
if ( $squid->{hta} eq '1' ) { print BLKFILE qq "\\\.hta\$\n"; }

#------------------------------------------------------------------
# Enable/Disable Prohibit multi-thread download
#------------------------------------------------------------------
$statement="http_reply_access deny partial maxcon";
if ( $squid->{prohibitmulti} eq '1' )
{
    modifyfile($QB_SQUID_CONF,"^#*".$statement,$statement); # remove # character in the stateament
}
elsif ( $squid->{prohibitmulti} eq '0' )
{
    modifyfile($QB_SQUID_CONF,$statement,"#".$statement); # Add # character in the stateament
}
else
{
    print "ERROR: INVALID PARAMETER \n";
    exit;
}



