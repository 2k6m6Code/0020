#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
use CGI::Ajax;
use Data::Dumper;
my $cgi = CGI-> new();
my $tm = $cgi->param("tm");
require ("/usr/local/apache/qb/qbmod.cgi");
my $authi=XMLin('/usr/local/apache/qbconf/auth.xml');
my $auth_list = $authi->{user};
my $quota=XMLin('/usr/local/apache/qbconf/quota.xml');
my $list = $quota->{quota};
print "Content-type: text/html\n\n";
print qq (<table bgcolor="#332211" width="100%" border="0" id="tables">);
# foreach my $title ( @titleHeadList ) { print qq (<td align="center" width="$titleWidth{$title}" id="$title">$title</td>); }
my @traffic_data_tmp=`/usr/local/apache/qb/setuid/run /sbin/iptables -t mangle -L -n|grep quota`;
print qq (<thead><tr><th style="width: 300px;">IP</th><th style="width: 300px;">Remaining Download Quota</th><th style="width: 200px;">Remaining Upload Quota</th><th style="width: 300px;">Out/In Quota</th><th style="width: 300px;">Download</th><th style="width: 300px;">Upload</th></tr></thead>);
print qq (<tfoot><tr><th>TOTAL:</th><th></th><th></th><th></th><th></th><th></th></tr></tfoot>);
$sum_dl = 0;
$sum_ul = 0;
my @data = split(/,/, $tm);
foreach $id (@data){
	$id =~ s/\/.*// ;
	runCommand(command=>'/usr/local/apache/qb/setuid/reset.sh ', params=>qq ($id));
	sleep 1;
	runCommand(command=>'cat' , params=>"/proc/net/ipt_account/$id > /tmp/lantraffic");
	$file="/tmp/lantraffic";
	if(-z $file) {next;};
	open(FILE,"<$file");
	my $line;
	my $lineCount = 0;
	my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
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
			    print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
			    my $quota_data = "0 / 0 / 0";
			    my $Uup='--';
			    my $Ddown='--';
			    my $mouse='';
			    if ($#list > 0)
			    {
			        foreach my $iip (@$list)
			    	{
			            if ($ip eq $iip->{ip})
			            {
			                my @tmp_up = split(/:/,$iip->{up});
			            	my @tmp_down = split(/:/,$iip->{down});
			            	$quota_data = data_quota($tmp_up[0],$tmp_up[1])."/".data_quota($tmp_down[0],$tmp_down[1]);
			            	$mouse="title='$iip->{name}'";
				    }            
			    	}
			    }
			    if ($mouse eq '' && $#auth_list >0)
			    {
			        foreach my $iip (@$auth_list)
			    	{
			    	    my $list_1=$iip->{member};
			    	    foreach my $iiip (@$list_1)
			    	    {
			                if ($ip eq $iiip->{ip} || $ip eq $iiip->{iip})
			                {
			            	    $mouse="title='$iiip->{idd}'";
			            	}
				    }            
			    	}
			    }
			    foreach (@traffic_data_tmp)
			    {
			        my @tmp=split(/\s+/,$_);
			        if ($tmp[3] eq $ip)
			        {
			            $Uup=traffic_quota($tmp[6]);
			        }elsif($tmp[4] eq $ip)
			        {
			            $Ddown=traffic_quota($tmp[6]);
			        }
			    }
			    print qq (<td width="200" align="center" $mouse>$ip</td>);
			    print qq (<td width="300" align="center" >$Ddown</td>);
			    print qq (<td width="300" align="center" >$Uup</td>);
			    print qq (<td width="300" align="center" >$quota_data</td>);
			    print qq (<td width="300" align="center" >$download Kbps</td>);
			    print qq (<td width="300" align="center" >$upload Kbps</td>);

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
}

sub traffic_quota
{
    my $a=shift;
    if ($a < "1048576")
    {
   	return sprintf("%.2f",($a/1024))."KB";
    }elsif ($a < "1073741824")
    {
       return sprintf("%.2f",($a/1048576))."MB"; 
    }elsif ($a < "1099511627776")
    {
       return sprintf("%.2f",($a/1073741824))."GB";
    }else
    {
   	return sprintf("%.2f",($a/1099511627776))."TB"; 
    }
    
}

sub data_quota
{
    my $o = shift;
    my $a = shift;
	
    if ($a eq "1024") 
    {
        return sprintf("%.2f",$o).'KB';
    }elsif ($a eq "1048576")
    {
        return sprintf("%.2f",$o).'MB';
    }elsif ($a eq "1073741824")
    {
        return sprintf("%.2f",$o).'GB';
    }elsif ($a eq "1099511627776")
    {
        return sprintf("%.2f",$o).'TB';
    }
}

# print qq (<table bgcolor="#332211" width="100%" border="0" ><tr>);
# print qq (<td align="center" width="200" >TOTAL:</td>);
# print qq (<td align="center" width="200" >$sum_dl Kbps</td>);
# print qq (<td align="center" width="200" >$sum_ul Kbps</td>);
# print qq (</tr></table>);
