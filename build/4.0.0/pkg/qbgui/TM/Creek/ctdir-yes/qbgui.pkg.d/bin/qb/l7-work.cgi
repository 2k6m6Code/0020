#!/usr/bin/perl

use CGI;
use File::Find;

print "Content-type:text/html\n\n";
require ("/usr/local/apache/qb/qbmod.cgi");
my $cgi = new CGI;
my $action = $cgi->param("action");
my $path = $cgi->param("PATH");
my $path1 = $cgi->param("PATH");
my $id = $cgi->param("ID");
my $back = '0';

$id =~ s/\.pat//g;
$path1 =~ s/$id\.pat//g;

if ($action eq 'show')
{
    open(FILE,"<$path");
    foreach my $data (<FILE>)
    {
        if (grep(/\#/,$data) || $data eq "\n" || grep(/^$id\n$/,$data)){next;}
        print qq($data);  
    }
    close(FILE);
}elsif ($action eq 'delete')
{
    system("/usr/local/apache/qb/setuid/run /bin/rm $path");
    
    find( { wanted => sub { push(@FileList, $_) }, no_chdir => 1 }, $path1 );
    foreach my $data (@FileList)
    {
        if ($data eq $path){next;}
        $back = '1';
    } 
    print $back;
}elsif ($action eq 'save')
{
    my $data = $cgi->param("DATA");
    
    open(FILE1,">$path");
    print FILE1 "$id\n";
    print FILE1 "$data\n";
    close(FILE1);
    
    find( { wanted => sub { push(@FileList, $_) }, no_chdir => 1 }, $path1 );
    foreach my $data1 (@FileList)
    {
        if ($data1 eq $path){$back = '1';}
    }
    
    print $back;
}

