#!/usr/bin/perl
use CGI;
use Data::Dumper;

print "Content-type:text/html\n\n";

    my $MC8090_nic=$ENV{'QUERY_STRING'};
    $MC8090_nic=~s/MC8090_nic=//;
    my @intname=split(/&/,$MC8090_nic);
    $interface=$intname[0];
    
    my $txrx=`cat /proc/qbalancer/qbreport | grep $interface | awk \'\{print \$7 \",\" \$8\}\'`;
    my $status=`grep $interface /usr/local/apache/active/basic.xml |sed -e \"s/  <isp.*alive=\\"//"|sed -e \"s/\\".*//\"`;
    my $pppoeportdev=`grep $interface /usr/local/apache/active/basic.xml |sed -e \"s/  <isp.*pppoeportdev=\\"//"|sed -e \"s/\\".*//\"`;
    my $isp=`grep ISP /tmp/MC8090_3G_info.$pppoeportdev`;
    $isp=~s/ISP://;
    $isp=~s/"//; $isp=~s/"//;
    my $cell_id=`grep Cell_ID /tmp/MC8090_3G_info.$pppoeportdev`;
    $cell_id=~s/Cell_ID://;
    my $band=`grep Band /tmp/MC8090_3G_info.$pppoeportdev`;
    $band=~s/Band://;
    
    print qq ( $txrx,$status,$isp,$cell_id,$band );

