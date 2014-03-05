#!/usr/bin/perl

require ("qbmod.cgi");

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
my $service=XMLread($gPATH.'flow.xml');
my $flow=$service->{user};
my $cgi = CGI-> new();
my $tm_time = $cgi->param("time");
my $tm_ip = $cgi->param("ip");
my $tm_limit = $cgi->param("limit");
my $tm_top = $cgi->param("top");
my $tm_symd = $cgi->param("symd");
my @limit = split(/,/,$tm_limit);
my $search='';

if ($limit[1] ne '')
{
    if ($limit[0] eq 'packets')
    {
        $search="-l $limit[1]";
    }elsif ($limit[0] eq 'traffic')
    {
        $search="-L $limit[1]";
    }
}        
print "Content-type: text/html\n\n";
system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp");
system("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip > /tmp/test_nfdump");
#print qq("/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$tm_symd/$tm_time $tm_top $tm_limit $tm_ip > /tmp/test_nfdump");
system("/usr/local/apache/qb/setuid/run /bin/chmod 777 /tmp/test_nfdump");

print qq (<table bgcolor="#332211" width="100%" border="0" id="tables">);
open(FILE,"/tmp/test_nfdump");
my $lineCount = 0;
my $top = '1';
my $time = '0';
my $title='0';
my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
my @tmp_data;
foreach my $data (<FILE>)
{
    if (grep(/Top/,$data) || grep(/Blocks/,$data) || grep(/Time/,$data)){next;}
    if (grep(/Summary/,$data)|| grep(/Aggregated/,$data)){next;}
    elsif (grep(/Date/,$data))
    {
        my @tmp = split(/\s{2}/,$data);
	print qq (<thead><tr>);
	print qq(<th style="width: 200px;">Top</th>);
	foreach my $title (@tmp)
	{
	    if ($title eq '' || $title eq 'Date first seen' || $title eq 'Duration'){next;}
	    #$title=~s/Src||Dst//g;
	    if (grep(/IP Addr/,$title))
	    {
	        print qq(<th style="width: 200px;">Unit Name</th>);
	    }
	    elsif (grep(/Bpp Flows/,$title))
	    {
	        my @tmp = split(/ /,$title);
	        print qq(<th style="width: 200px;">$tmp[0]</th>);
	        print qq(<th style="width: 200px;">$tmp[1]</th>);
	    }
	    else
	    {
	        print qq(<th style="width: 200px;">$title</th>);
	    }
	}
	print qq (</tr></thead>);
    }
    elsif (grep(/Sys/,$data))
    {
    	$data =~ s/^.*Wall://g;
    	$data =~ s/flows\/second:.*$//g;
    	$time = $data;
    	if (grep(/0.000s/,$data))
    	{
    	    $time = '0.001s';
    	}
    	$title = $top - 1;
    }else
    {
        if (grep(/No matched flows/,$datai)){next;}
        if (!grep(/\w+/,$data)){next;}
        push(@tmp_data,$data);
    }
    
}
close(FILE);

foreach my $file (@$flow)
{
    if ($file->{schname} eq 'system'){next;}
    my $menber = $file->{member};
    my $packets=0;
    my $bytes=0;
    my $bps=0;
    my $bpp=0;
    my $flows=0;
    my $index_all= 1;
    foreach my $user (@$menber)
    {
        foreach my $database (@tmp_data)
        {
            if (grep(/(\d+)\.(\d+)\.(\d+)\.(\d+)/,$database))
            {
                $database=~s/(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)\.(\d+)\s+(\d+)\.(\d+)//g;
                my @traffic = split(/\s{2,}/,$database);
                if ( $user->{ip} eq $traffic[1])
                {
                    $packets+=$traffic[2];
                    if (grep(/^(\d+)[A-Z]$/,$traffic[3]))
                    {
                        my @bytes_tmp=split(/ /,$traffic[3]);
                        if( $bytes_tmp eq 'M'){$bytes=($bytes_tmp[0] * 1000000);}
                    }else
                    {
                        $bytes+=$traffic[3];
                    }
                    $bps+=$traffic[4];
                    $bpp+=$traffic[5];
                    $flows+=$traffic[6];
                    splice(@tmp_data, $ary_index);
                }
            }
            $ary_index++;
        }
    }
    if ($bytes > 0 && $packets > 0)
    {
	print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
	print qq (<td width="200" align="center">$top</td>);
       	print qq (<td width="200" align="center">$file->{schname}</td>);
       	print qq (<td width="200" align="center">$packets</td>);
       	print qq (<td width="200" align="center">$bytes</td>);
       	print qq (<td width="200" align="center">$bps</td>);
       	print qq (<td width="200" align="center">$bpp</td>);
       	print qq (<td width="200" align="center">$flows</td></tr>); 
       	$top++;
    }
}
$packets=0;
$bytes=0;
$bps=0;
$bpp=0;
$flows=0;
foreach my $database (@tmp_data)
{
   $database=~s/(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)\.(\d+)\s+(\d+)\.(\d+)//g;
   my @traffic = split(/\s{2,}/,$database);
   $packets+=$traffic[2];
   if (grep(/^(\d+)[A-Z]$/,$traffic[3]))
   {
       my @bytes_tmp=split(/ /,$traffic[3]);
       if( $bytes_tmp eq 'M'){$bytes=($bytes_tmp[0] * 1000000);}
   }else
   {
       $bytes+=$traffic[3];
   }
   $bps+=$traffic[4];
   $bpp+=$traffic[5];
   $flows+=$traffic[6];
}
print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
print qq (<td width="200" align="center">$top</td>);
print qq (<td width="200" align="center">Other</td>);
print qq (<td width="200" align="center">$packets</td>);
print qq (<td width="200" align="center">$bytes</td>);
print qq (<td width="200" align="center">$bps</td>);
print qq (<td width="200" align="center">$bpp</td>);
print qq (<td width="200" align="center">$flows</td></tr>); 


print qq (<FONT SIZE=4>Query Completed (Time used $time Seconds) Data transfer completed (Total $title Records)</FONT>);
#system("/usr/local/apache/qb/setuid/run /bin/rm -rf /tmp/test_nfdump");
