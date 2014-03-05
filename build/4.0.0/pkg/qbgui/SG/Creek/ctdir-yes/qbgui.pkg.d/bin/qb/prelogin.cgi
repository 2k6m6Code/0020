#!/usr/bin/perl
require "qbmod.cgi";

print "Content-type:text/html\n\n";

my $model=$gMODEL;
my $type=$gTYPE;

my $qbservver=runCommand(command=>'qbserv', params=>'-v'); chop($qbservver); if ( !$qbservver ) { $qbservver='unknown'; }
my $qbuiver=runCommand(command=>'cat', params=>$gUIVER);   chop($qbuiver);   if ( !$qbuiver )   { $qbuiver='unknown'; }
my $qbver=runCommand(command=>'grep', params=>'DETAIL '.$gPKGINFO);   chop($qbver);   if ( !$qbver )   { $qbver='unknown'; }
my $qbsn=runCommand(command=>'cat', params=>'/mnt/conf/qbsn');   chop($qbsn);   if ( !$qbsn )   { $qbsn='unknown'; }
my $qblibimg=runCommand(command=>'cat', params=>'/mnt/conf/libimage.ifo|grep version|tail -n 1');   chop($qblibimg);   if ( !$qblibimg) { $qblibimg='unknown'; }
my $qbfs=runCommand(command=>'cat', params=>'/mnt/conf/fsimage.ifo|grep version|tail -n 1');   chop($qbfs);   if ( !$qbfs ) { $qbfs='unknown'; }

print qq(<html><head><link rel="stylesheet" type="text/css"></head><body bgcolor="#445588" text="#ffffff" link="#000040" vlink="#400040">);

    print << "CHANGEIMAGE";

    <script for='window' event='onload'>
        if((url = parent.location + ''))
            if(parent.location.href != window.location.href)
                parent.reportVersion('$qbuiver','$qbservver', '$gMODEL' ,'$qbver' ,'$gTYPE' ,'$qbsn' ,'$qblibimg' ,'$qbfs');
    </script>

CHANGEIMAGE

print qq (</body>);
print qq (</html>);
