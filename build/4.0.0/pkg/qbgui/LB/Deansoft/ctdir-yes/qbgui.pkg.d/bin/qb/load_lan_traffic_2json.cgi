#!/usr/bin/perl
        
# BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

# use Data::Dumper;
# use CGI;
# use CGI::Ajax;
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type:application/json\n\n";

use CGI;
$cgi = CGI-> new();
$tm = $cgi->param("tm");
# runCommand(command=>'/usr/local/apache/qb/setuid/reset.sh ', params=>qq ($tm));
	# sleep 1;
$queryip = $tm;
@splitip = split(/\./,$tm);
$tm = $splitip[0].'.'.$splitip[1].'.'.$splitip[2].'.'."0";
my $zone=XMLread('/usr/local/apache/qbconf/zonecfg.xml');
my $zonelist=$zone->{nat};
foreach my $nic ( @$zonelist )
{
 if ($nic->{natid} eq 'system' || $nic->{network} eq ""){next;}
    my $status = ( $action{interface} eq $nic->{network} ) ? 'selected' : '';
    # print qq (<option $status id="T" value="$nic->{network}">$nic->{network}</option>);
    $name = $nic->{network};
	
    $name =~ s/\/.*//;
	$info=runCommand(command=>'cat', params=>"/mnt/log/Log_file/$name");
	if($info =~ /($splitip[0]+\.$splitip[1]+\.$splitip[2]\.$splitip[3]\s)/){
	last;
	
	
	}


}
# $file="/tmp/lantraffic";
# $info='<pre>'.$info.'</pre>';
@arraydata =();

@arraydatau =();
# print $info;
my @total_data = split("\n", $info);
for($nnd =0;$nnd<=$#total_data;$nnd++){

if(grep(/gettime:/,$total_data[$nnd])){
$total_data[$nnd] =~s /gettime://;
# print "[".$total_data[$nnd].",";
$getiptime =$total_data[$nnd];
push(@arraydata,"[".$getiptime."000,0]");
push(@arraydatau,"[".$getiptime."000,0]");
}
if($getiptime == undef){
next;
}
$iptmp = $total_data[$nnd];

if($iptmp =~ /($splitip[0]+\.$splitip[1]+\.$splitip[2]\.$splitip[3]\s)/){
pop(@arraydata);
pop(@arraydatau);
@dldata = split(/ /, $iptmp );
my $download = sprintf (("%.2f", ( $dldata[19]/1024)*8));	
# print $download."],\n";
my $upload = sprintf (("%.2f", ($dldata[5]/1024)*8));
push(@arraydata,"[".$getiptime."000,".$download."]");
push(@arraydatau,"[".$getiptime."000,".$upload."]");
# print $iptmp."\n".$queryip;
}



}

print '[{'."\n";
 print '"label":"'.$queryip.'-Download(Kbps)",';
print "\n".'"data"'.": [".join(",",@arraydata).']';
# print '"label":"'.$total_data[2].'-Download(Kbps)",';
# my $download = sprintf (("%.2f", ( $total_data[19]/1024)*8));
# my $upload = sprintf (("%.2f", ($total_data[5]/1024)*8));
# for($ff = 0;$ff<=$#total_data;$ff++){
# print $total_data[$ff]."[$ff]";

# }"data": [[1999, 3.0], [2000, 3.9]
# print  "\n".'"data":[['.time.','.$download .']]';

print "\n".'},';
print "\n{"."\n";
 print '"label":"'.$queryip.'-Upload(Kbps)",';
print "\n".'"data"'.": [".join(",",@arraydatau).']';
print "\n".'}]';