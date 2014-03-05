#!/usr/bin/perl

my $now_TW=time()+(8*60*60);
my $now = gmtime($now_TW);
my $old;
my $now;
my $history;
my $point;
my ($sec, $min, $hour, $day, $mon, $year) = localtime(time);
$mon++;
if ($hour eq '0'){$hour = 24;}
$day = sprintf("%02d", $day);
$hour = sprintf("%02d", $hour);
$mon = sprintf("%02d", $mon);
$year +=1900;
if ($min < 30)
{
    $old = $year.$mon.$day.sprintf("%02d",($hour-1))."30";
    $now = $year.$mon.$day.$hour."00";
    $point = sprintf("%02d",($hour-1)).".50";
   
}else
{
    $old = $year.$mon.$day.$hour."00";
    $now = $year.$mon.$day.$hour."30";
    $point = $hour.".00";
}
print qq(/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$year/$mon/$day/nfcapd.$old:nfcapd.$now -n 10 -s record/flows -l 100000);
@traffic =`/usr/local/apache/qb/setuid/run /usr/local/bin/nfdump -R /mnt/tclog/nfcapd/$year/$mon/$day/nfcapd.$old:nfcapd.$now -n 10 -s record/flows -l 100000`;
foreach (@traffic)
{
    if (!grep(/Summary/,$_) || $_ eq ''){next;}
    $_=~s/Summary:||total||avg||\s+//g;
    $_=~s/\s+/\n/g;
    $history = $_;
print qq($history);
}
close(FLOWS);

my $check = 1;
my @check_data = `/usr/local/apache/qb/setuid/run /bin/cat /mnt/tclog/total_$year$mon$day`;
foreach (@check_data)
{
    if (grep(/$point/,$_)){$check= 0 ;break;}
}
if ($check)
{
    $history=~s/:/-/g;
    open(FILE,">>/mnt/tclog/total_$year$mon$day");
    print FILE "Time-:".$point.",".$history."\n";
    close(FILE);
}

my @check_data = `/usr/local/apache/qb/setuid/run /usr/local/apache/qb/status/rate.cgi`;
my $path = "/mnt/tclog/speed.log";
my $aas=1;
if(!-e $path){$aas=0;}
open(FILE,">>/mnt/tclog/speed.log");
foreach my $o (@check_data)
{
    if(!grep(/window.parent.gmaster.add/,$o)){next;}
    $o=~s/window.parent.gmaster.add//;
    $o=~s/\(||\)||;||"//g;
    my @dd=split(/, /,$o);
    if(!$aas)
    {
        foreach (0..((2*$hour)-1))
        {
    	    print FILE "name:".$dd[0].",up:0,down:0,loss:0,latency:0\n";
        }
    }
    print FILE "name:".$dd[0].",up:".$dd[3].",down:".$dd[4].",loss:".$dd[11].",latency:".$dd[12]."\n";
}
$aas = 1;
close(FILE);
