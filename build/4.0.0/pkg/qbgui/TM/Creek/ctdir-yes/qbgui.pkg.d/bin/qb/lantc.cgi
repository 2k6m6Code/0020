#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }
              
use CGI;
use CGI::Ajax;
use Data::Dumper;
$cgi=CGI->new();
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type: text/html\n\n";
$id = $cgi->param("id");
$id =~ s/\/.*// ;
runCommand(command=>'/usr/local/apache/qb/setuid/reset.sh ', params=>qq ($id));
sleep 1;
my @titleHeadList=('IP', 'Download', 'Upload');
my %titleWidth=('IP'=>200, 'Download'=>200, 'Upload'=>200);
print qq (<table bgcolor="#332211" width="100%" border="0" id="tables"><tr>);
foreach my $title ( @titleHeadList ) { print qq (<td align="center" width="$titleWidth{$title}" id="$title">$title</td>); }
print qq (</tr>);
runCommand(command=>'cat' , params=> "/proc/net/ipt_account/$id > /tmp/aa");
my $file = "/tmp/aa" ;
open(FILE,"<$file");
my $line;
my $lineCount = 0;
my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
my $tmpip = '';
$sum_dl = 0;
$sum_ul = 0;
while ( $line = <FILE> ) {
        my @record = split(/ /, $line);
        my $ip = $record[2];
        if ( $tmpip ne $ip )
        {
        	my $total = `grep $ip $file`;
                my @total_data = split(/ /, $total);
                my @number = split(/\./, $ip);
                my $nb = $number[3];
                my $download = sprintf ("%.2f",(($total_data[19]/1024)*8));
                my $upload = sprintf ("%.2f",(($total_data[5]/1024)*8));
                if ($nb ne "0")
                {
                    print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
                    print qq (<td width="200" align="center" id="$nb" >$ip</td>);
                    print qq (<td width="200" align="center" >$download Kbps</td>);
                    print qq (<td width="200" align="center" >$upload Bbps</td>);
                    print qq (</tr>);
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
print qq (<table bgcolor="#332211" width="100%" border="0" ><tr>);
print qq (<td align="center" width="200" >TOTAL:</td>);
print qq (<td align="center" width="200" >$sum_dl Kbps</td>);
print qq (<td align="center" width="200" >$sum_ul Kbps</td>);
print qq (</tr></table>);
