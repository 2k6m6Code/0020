#!/usr/bin/perl
use Data::Dumper;
use CGI;
my $cgi = new CGI;
print "Content-type:text/html\n\n";
my $action = $cgi->param("action");
system "/usr/local/apache/qb/setuid/run","chmod","777","/etc/crontab";
if ($action eq "ADD")
{
    system "date>>/usr/local/apache/qbconf/lantraffic";
    $action="OPEN";
}
if ($action eq "OPEN")
{
     $file = -e "/usr/local/apache/qbconf/lantraffic";
     if ($file)
     {
         open(FILE,">>/etc/crontab");
         my $info="*/1  * * * *  root      /usr/local/apache/qb/runiptables.cgi action=CHECK\n";
         print FILE $info;
         close(FILE);
         
     }
}   
elsif($action eq "DEL" )
{
    my @buff;
    system "/bin/rm","-f","/usr/local/apache/qbconf/lantraffic";
    open(FILE,"/etc/crontab");
    foreach my $data (<FILE>)
    {
        if(grep(/runiptables/,$data)){next;}
        push(@buff,$data);
    }
    close(FILE);
    open(FILE1,">/etc/crontab");
    print FILE1 @buff;
    close(FILE1);
}
system "/usr/local/apache/qb/setuid/run","chmod","644","/etc/crontab";
