#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
my $QB_BASIC_XML="/usr/local/apache/qbconf/basic.xml";
my $XL2TP_CONF="/etc/xl2tpd/xl2tpd.conf";

my $QB_PSK = "/etc/racoon/psk.txt";

my $ispref=XMLread($QB_BASIC_XML);
my $isplist=$ispref->{isp};
my $ispname = $ARGV[0];
my $pptpserver = $ARGV[1];
my $pppoename = $ARGV[2];

open(L2TPD, "> $XL2TP_CONF" );
   if ( $ispname ) 
   { 
     print L2TPD qq(\[lac $ispname\] \n);
     print L2TPD qq(lns = $pptpserver \n);
     print L2TPD qq(redial = yes \n);
     print L2TPD qq(autodial = yes \n);
     print L2TPD qq(require chap = yes \n);
     print L2TPD qq(name = $pppoename \n);
     print L2TPD qq(length bit = yes \n);
     print L2TPD qq(ppp debug = no \n);
     print L2TPD qq(pppoptfile = /etc/ppp/options.xl2tpd.$ispname \n);
     print L2TPD qq(\n);
   }
foreach my $isp ( @$isplist ) 
{  
   if ( $isp->{isptype} eq "l2tp" && $isp->{pptpserver} ne "" ) 
   { 
     print L2TPD qq(\[lac $isp->{ispname}\] \n);
     print L2TPD qq(lns = $isp->{pptpserver} \n);
     print L2TPD qq(redial = yes \n);
     print L2TPD qq(autodial = yes \n);
     print L2TPD qq(require chap = yes \n);
     print L2TPD qq(name = $isp->{pppoename} \n);
     print L2TPD qq(length bit = yes \n);
     print L2TPD qq(ppp debug = no \n);
     print L2TPD qq(pppoptfile = /etc/ppp/options.xl2tpd.$isp->{ispname} \n);
     print L2TPD qq(\n);
     #---------------------------------------------------------------
     # L2TP/ IPsec PSK /etc/racoon/psk.txt
     #---------------------------------------------------------------
     open(PSK, ">>$QB_PSK" );
     print PSK qq ($isp->{pptpserver} $isp->{psk}\n);
     print qq ($isp->{pptpserver} $isp->{psk}\n);
     close(PSK);
   } 
}
close(L2TPD);
close(PSK);

 my $myfile = -f "/etc/racoon/delipsecrule";
 runCommand(command=>'/sbin/setkey', params=>'-f /etc/racoon/flush');
 runCommand(command=>'killall', params=>'-9 racoon');
 runCommand(command=>'rm', params=>'-f /etc/racoon/*.conf');
 runCommand(command=>'/usr/local/apache/qb/setuid/do_qbipsec.pl', params=>'');
 runCommand(command=>'/usr/local/apache/qb/setuid/do_qbipsec_route.pl', params=>'');
 runCommand(command=>'/usr/local/apache/qb/setuid/do_qbracoon.pl', params=>'');
 runCommand(command=>'sleep', params=>'5');
 if (grep(/sainfo address/,'/etc/racoon/racoon.conf') eq 0)
 {
    runCommand(command=>'/sbin/setkey', params=>'-f /etc/racoon/ipsec.conf');
    runCommand(command=>'/etc/racoon/ipsecroute', params=>'');
    runCommand(command=>'/usr/sbin/racoon', params=>'');
 }
 if($myfile)
 {
    runCommand(command=>'/etc/racoon/delipsecrule', params=>'');
 }
 runCommand(command=>'/etc/racoon/ipsecrule', params=>'');
