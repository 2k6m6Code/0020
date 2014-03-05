#!/usr/bin/perl
use CGI;
$basedir = '/tmp';
print "Content-type: text/html\n\n";
my $req = new CGI;
my $file = $req->param("filename");
my $group = $reg->param("group");
my $message;
if ($file ne "") 
{
    my $fileName = $file;
    $fileName =~ s/^.*(\\|\/)//;
    open (OUTFILE, ">$basedir/$fileName");
    binmode(OUTFILE);
    while (my $bytesread = read($file, my $buffer, 1024)) { 
        print OUTFILE $buffer;
    }
    close (OUTFILE);
    $message = "$fileName upload OK";
}
