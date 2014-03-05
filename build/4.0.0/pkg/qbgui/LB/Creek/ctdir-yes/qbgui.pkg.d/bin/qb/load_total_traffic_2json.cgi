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
$ty = $cgi->param("ty");
$ti = $cgi->param("ti");
# runCommand(command=>'/usr/local/apache/qb/setuid/reset.sh ', params=>qq ($tm));
	# sleep 1;
$queryip = $tm;
@splitip = split(/\./,$tm);
$tm = $splitip[0].'.'.$splitip[1].'.'.$splitip[2].'.'."0";

$info=runCommand(command=>'cat', params=>"/mnt/log/Log_file/$tm");
# $file="/tmp/lantraffic";
# $info='<pre>'.$info.'</pre>';
%arraydata;

%arraydatau;
# print $info;
my @total_data = split("\n", $info);
if(!defined($ti)){
	for($nnd =0;$nnd<=$#total_data;$nnd++){

		if(!grep(/gettime:/,$total_data[$nnd])){
		@dldata = split(/ /, $total_data[$nnd] );
		my $download = sprintf (("%.2f", ( $dldata[19]/1024)*8));	
		# print $download."],\n";
		my $upload = sprintf (("%.2f", ($dldata[5]/1024)*8));
		@ippzero = split(/\./,$dldata[2]);
		if($ippzero[3] ==0){
		next;
		}

		$sumdownload = $arraydata{$dldata[2]}+$download;
		$sumupload = $arraydatau{$dldata[2]}+$upload;
		%arraydata =(%arraydata,$dldata[2],$sumdownload);
		%arraydatau =(%arraydatau,$dldata[2],$sumupload);

		}


	}
}else{
	for($nnd =0;$nnd<=$#total_data;$nnd++){
	if(grep(/gettime:/,$total_data[$nnd])){
	$total_data[$nnd] =~s /gettime://;
	# print "[".$total_data[$nnd].",";
	$getiptime =$total_data[$nnd];
		if($ti<$getiptime){
		$getiptimeindex = $nnd;
		last;
		}
	}
	
	}
	# print $getiptime."-".$getiptimeindex;
	for($nnd =$getiptimeindex;$nnd<=$#total_data;$nnd++){

		if(!grep(/gettime:/,$total_data[$nnd])){
		@dldata = split(/ /, $total_data[$nnd] );
		my $download = sprintf (("%.2f", ( $dldata[19]/1024)*8));	
		# print $download."],\n";
		my $upload = sprintf (("%.2f", ($dldata[5]/1024)*8));
		@ippzero = split(/\./,$dldata[2]);
		if($ippzero[3] ==0){
		next;
		}

		$sumdownload = $arraydata{$dldata[2]}+$download;
		$sumupload = $arraydatau{$dldata[2]}+$upload;
		%arraydata =(%arraydata,$dldata[2],$sumdownload);
		%arraydatau =(%arraydatau,$dldata[2],$sumupload);

		}


	}
	
}
sub hashValueDescendingNum  {
   $arraydata{$b} <=> $arraydata{$a};
}
sub hashValueDescendingNum2  {
   $arraydatau{$b} <=> $arraydatau{$a};
}
# $countip = 0;

if($ty eq "a"){
print '['."\n";
foreach $key (sort hashValueDescendingNum  (keys(%arraydata))) {
   # if($countip < 7){
   print '{"label":"'.$key.'-Download",';
    print "\n".'"data"'.": ".int $arraydata{$key};
	print "},\n";
   # }
   # if($countip == 7){
   # print '{"label":"'.$key.'-Download",';
    # print "\n".'"data"'.": ".int $arraydata{$key};
	# print "}]\n";
   # }
   # $countip++;
   
}
 print '{"label":"","data": 0}'."]\n";
}
if($ty eq "b"){
print '['."\n";
foreach $key (sort hashValueDescendingNum2  (keys(%arraydatau))) {
   # if($countip < 7){
   print '{"label":"'.$key.'-Upload",';
    print "\n".'"data"'.": ".int $arraydatau{$key};
	print "},\n";
}
 print '{"label":"","data": 0}'."]\n";
}
# print '[{'."\n";
 # print '"label":"'.$queryip.'-Download(Kbps)",';
# print "\n".'"data"'.": [".join(",",@arraydata).']';
# print '"label":"'.$total_data[2].'-Download(Kbps)",';
# my $download = sprintf (("%.2f", ( $total_data[19]/1024)*8));
# my $upload = sprintf (("%.2f", ($total_data[5]/1024)*8));
# for($ff = 0;$ff<=$#total_data;$ff++){
# print $total_data[$ff]."[$ff]";

# }"data": [[1999, 3.0], [2000, 3.9]
# print  "\n".'"data":[['.time.','.$download .']]';

# print "\n".'},';
# print "\n{"."\n";
 # print '"label":"'.$queryip.'-Upload(Kbps)",';
# print "\n".'"data"'.": [".join(",",@arraydatau).']';
# print "\n".'}]';