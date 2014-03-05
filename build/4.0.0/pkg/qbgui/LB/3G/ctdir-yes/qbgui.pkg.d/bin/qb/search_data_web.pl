#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
my $cgi = CGI-> new();
#my $start = $cgi->param("time_1");
#my $end = $cgi->param("time_2");
my $tm_option = uc($cgi->param("option"));
my $search='';

print "Content-type: text/html\n\n";
print qq (<table bgcolor="#332211" width="100%" border="0" id="tables">);
my $lineCount = 0;
my $ttime = '0.001s';
my $title='0';
my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
my @title;
my @file;
if ($tm_option eq 'Filter')
{
    @file=`/usr/local/apache/qb/setuid/run /bin/cat /usr/local/squidGuard/log/blockaccesses`;
    @title =('Time','Request','GET REDIRECT');
}else
{
    @file=`/usr/local/apache/qb/setuid/run /bin/cat /mnt/tclog/squid/log/access.log`;
    @title =('IP','Time','Action');
}
print qq (<thead><tr>);
foreach my $tt (@title){print qq (<th style="width: 200px;">$tt</th>);}
print qq (</tr></thead>);
foreach my $data (@file)
{
    my @data_splic=split(/\s+/,$data);
    $ttable = "";
    $ttable .="<tr bgcolor='$bgcolor' originalColor='$originalColor' onmouseover='focusedColor(this)' onmouseout='blurColor(this)'><th style='width: 200px;'>";
    $ttable .=$colstring[0]." ";
    $ttable .=$colstring[1]."</th><th>";
    $colstring[3] =~s/Request\(//;
    $colstring[3] =~s/\/-\)//;
    $ttable .=$colstring[3].'</th><th style="width: 200px;word-break: break-all;">';
    $ttable .=$colstring[4];
    $ttable .="</th></tr>";
    $newinfo .=$ttable;
    print $newinfo;
}
print qq (<FONT SIZE=4>Query Completed (Time used $ttime Seconds)</FONT>);

