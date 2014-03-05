#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# --------------------------
#
# main program start routine
#
# --------------------------
my $QB_ARP_CFG="/usr/local/apache/active/arp.xml";
my $ARP_SCRIPT="/tmp/arp.sh";
my $ARP_SCRIPT_DEL="/tmp/arpdel.sh";
my $arptable=XMLread($QB_ARP_CFG);
my $arpList=$arptable->{arp};

if(!$arptable) { print "$QB_ARP_CFG is NULL \n"; }#if the string is NULL

runCommand(command=>$ARP_SCRIPT_DEL, params=>'');

#========================================================
# To write arp-table
if (!open(FOUT, ">$ARP_SCRIPT"))
{
  print qq (ARP Script Write Permission Error !!);
  return;
}
    
print FOUT qq(#!/bin/bash \n);
print FOUT qq(# User defined arp-table list from arp.xml \n);
foreach my $arpentry ( @$arpList )
{
    if ( $arpentry->{ip} eq 'system' ) { next; }
    print FOUT qq(/sbin/arp -s $arpentry->{ip} $arpentry->{mac} \n);
}
close(FOUT);
chmod 0755, $ARP_SCRIPT;
#========================================================
# To delete arp-table
if (!open(FOUT, ">$ARP_SCRIPT_DEL"))
{
  print qq (ARP Script Write Permission Error !!);
  return;
}
print FOUT qq(#!/bin/bash \n);
print FOUT qq(# User defined arp-table list from arp.xml \n);
foreach my $arpentry ( @$arpList )
{
    if ( $arpentry->{ip} eq 'system' ) { next; }
    print FOUT qq(/sbin/arp -d $arpentry->{ip} \n);
}
close(FOUT);
chmod 0755, $ARP_SCRIPT_DEL;
                                    
runCommand(command=>$ARP_SCRIPT, params=>'');
