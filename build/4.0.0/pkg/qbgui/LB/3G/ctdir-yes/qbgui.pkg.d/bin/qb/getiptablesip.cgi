#!/usr/bin/perl
        
BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use Data::Dumper;
use CGI;
use CGI::Ajax;
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type:text/html\n\n";
my $zone=XMLread('/usr/local/apache/qbconf/zonecfg.xml');
my $isp=XMLread('/usr/local/apache/qbconf/basic.xml');
my $isplist=$isp->{isp};
my $zonelist=$zone->{nat};
my $dmzlist=$zone->{dmz};
my  %action;
my  $form = new CGI;
@filestr;
$varr;
foreach my $nic ( @$zonelist )
{
    if ($nic->{natid} eq 'system' || $nic->{network} eq ""){next;}
    my $status = ( $action{interface} eq $nic->{network} ) ? 'selected' : '';
    # print qq (<option $status id="T" value="$nic->{network}">$nic->{network}</option>);
    $name = $nic->{network};
	
    $name =~ s/\/.*//;
	# $size = -s "/usr/local/apache/qb/Log_file/$name";
	# print $size.'[]';
	# print $size.'[]';
	open(FILE,"/mnt/log/Log_file/$name") or  "open file error" ; 
	
	while($line = <FILE>){
		if(grep(/ip/,$line)){
		@record = split(/ /, $line);
		# $ipd = $record[2];
		$filestr[$varr]=$record[2];
		$varr++;
		
		
		}
	}
	# print $filestr[5];
	# print join("\n",@filestr);
	
	
	close FILE;
	
	# open(write_file,">/usr/local/apache/qb/Log_file/allip") or  "open file error" ;
	
	# print write_file  @filestr; 
	# close;
	
	
    # runCommand(command=>'/usr/local/apache/qb/setuid/lantrafficlog.sh ', params=>qq ($nic->{network}).' '.qq ($name));
}
	my %count;
	my @uniq_times = grep { ++$count{ $_ } < 2; } @filestr; 
	# print "___";
	print join(",",@uniq_times);
