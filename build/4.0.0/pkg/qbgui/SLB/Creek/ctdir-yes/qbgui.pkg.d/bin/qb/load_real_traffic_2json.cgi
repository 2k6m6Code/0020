#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
use CGI::Ajax;
use Data::Dumper;
$cgi = CGI-> new();
$tm = $cgi->param("tm");
$ty = $cgi->param("ty");
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type:application/json\n\n";
# my @titleHeadList=('IP', 'Download', 'Upload');
# my %titleWidth=('IP'=>200, 'Download'=>200, 'Upload'=>200);
# print qq (<table bgcolor="#332211" width="100%" border="0" id="tables">);
# foreach my $title ( @titleHeadList ) { print qq (<td align="center" width="$titleWidth{$title}" id="$title">$title</td>); }

# print qq (<thead><tr><th style="width: 200px;">IP</th><th style="width: 200px;">Download</th><th style="width: 200px;">Upload</th></tr></thead>);
# print qq (<tfoot><tr><th>TOTAL:</th><th></th><th></th></tr></tfoot>);
$sum_dl = 0;
$sum_ul = 0;
my $zone=XMLread('/usr/local/apache/qbconf/zonecfg.xml');
my $zonelist=$zone->{nat};
foreach my $nic ( @$zonelist )
{
    if ($nic->{natid} eq 'system' || $nic->{network} eq ""){next;}
    my $status = ( $action{interface} eq $nic->{network} ) ? 'selected' : '';
    # print qq (<option $status id="T" value="$nic->{network}">$nic->{network}</option>);
    $name = $nic->{network};
    $name =~ s/\/.*//;
    runCommand(command=>'/usr/local/apache/qb/setuid/opreset.sh ', params=>qq ($nic->{network}).' '.qq ($name));
}

# foreach $id (@$zonelist){
# print $id->{network};
# }
# my @data = split(/,/, $tm);
@fsup;
@fsdl;
foreach $nic (@$zonelist){
    $id = $nic->{network};
	$id =~ s/\/.*// ;
	runCommand(command=>'/usr/local/apache/qb/setuid/reset.sh ', params=>qq ($id));
	sleep 1;
	runCommand(command=>'cat' , params=>"/proc/net/ipt_account/$id > /tmp/lantraffic");
	$file="/tmp/lantraffic";
	if(-z $file) {next;};
	open(FILE,"<$file");
	my $line;
	my $lineCount = 0;
	# my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
	my $tmpip = '';
	while ( $line = <FILE> ) {
		my @record = split(/ /, $line);
		my $ip = $record[2];
		if ( $tmpip ne $ip )
		{
			my $total = `grep $ip $file`;
			my @total_data = split(/ /, $total);
			my @number = split(/\./, $ip);
			my $nb = $number[3];
			my $download = sprintf (("%.2f", ( $total_data[19]/1024)*8));
			my $upload = sprintf (("%.2f", ($total_data[5]/1024)*8));
			if ($nb ne "0")
			{
				push(@fsdl,'{"label":"'.$ip.'-Download(Kbps)",'.'"data":'.$download.'}');
				push(@fsup,'{"label":"'.$ip.'-Upload(Kbps)",'.'"data":'.$upload.'}');
				# print '{"label":"'.$ip.'-Download(Kbps)",';
			    # print '"data":'.$download.'}';
			    # print qq (<span width="200" align="center" >$upload Kbps</span>);

			    # print qq (</div>);
			}
			if ($nb eq "0")
			{
			    $sum_dl +=$download;
			    $sum_ul +=$upload ;
			}
			$tmpip = $ip;
			$lineCount++;
		}
	}
	close(FILE);
}
# if($ty eq "a"){
print "[";
print join(",",@fsdl);
print ",";
print join(",",@fsup);
print "]";
# }
# if($ty eq "b"){
# print "[";
# print join(",",@fsup);
# print "]";
# }
# print qq (<table bgcolor="#332211" width="100%" border="0" ><tr>);
# print qq (<td align="center" width="200" >TOTAL:</td>);
# print qq (<td align="center" width="200" >$sum_dl Kbps</td>);
# print qq (<td align="center" width="200" >$sum_ul Kbps</td>);
# print qq (</tr></table>);
