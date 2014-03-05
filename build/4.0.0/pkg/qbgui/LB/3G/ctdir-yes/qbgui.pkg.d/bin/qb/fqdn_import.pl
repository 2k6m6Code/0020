#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
use QB_Xml;
use QB_Action;
use XML::Simple;
use Data::Dumper;

my $cgi = CGI-> new();
my $db = $cgi->param("type");
my $act = QB_Action->new();
my $xml = QB_Xml->new();
my $PATH = "/mnt/tclog/blacklists/";
my $PATH_xml = "/usr/local/apache/qbconf/host.xml";

print "Content-type: text/html\n\n";

if ($db)
{
   my @name = split(/,/,$db);
   foreach my $file_name (@name)
   {
       my @data = $act->getfile("$PATH".$file_name."/domains");
       my $fqdn = join(",",@data);
       my $ref = $xml->read("$PATH_xml");
       my $host = $ref->{host}; 
       my $exist='0';
       my %save_data = (
           hostaddress	=>    $fqdn,
           hostname	=>    "host-$file_name",
      	   hosttype	=>    "fqdnlist", 
      	   type		=>    "fqdn"
       );
       
       foreach my $host_ary (@$host)
       {
           if ( $host_ary->{hostname} eq $file_name )
           {
               $exist='1';
               $host_ary=\%save_data;
       	   }
       }
       if ( $exist eq '0' ){push( @$host, \%save_data);}
       $xml->write($ref,$PATH_xml);
   }
}else
{
    my @dir = $act->getdir($PATH);
    my $row = 1;
    foreach my $option (@dir)
    {
        if ($row%5 eq 1){print qq (<tr>);}
        print qq (<td><input type="checkbox" value="$option">$option</td>);
        if ($row%5 eq 0){print qq (<tr>);}
        $row++;
    }
}
