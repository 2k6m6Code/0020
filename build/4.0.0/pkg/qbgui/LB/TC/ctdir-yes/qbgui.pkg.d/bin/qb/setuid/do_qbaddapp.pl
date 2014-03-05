#!/usr/bin/perl 
require ("/usr/local/apache/qb/qbmod.cgi");

my $iniroute=XMLread($gPATH."iniroute.xml");
my $viaroute=XMLread($gPATH."viaroute.xml");

my %class=(
                        advnace     =>  'system',
                        direction   =>  'system',
                        dirty       =>  '0',
                        method      =>  'system',
                        priority    =>  'system',
                        service     =>  'system',
                        source      =>  'system',
                        table       =>  'system',
            );
$iniroute->{app}->{class}[0]=\%class;
XMLwrite($iniroute, $gPATH."iniroute.xml");

my %class=(
		advance     => 'system',
		direaction  => 'system',
		dirty       => '0',
		method      => 'system',
		priority    => 'system',
		service     => 'system',
		source      => 'system',
		subnettype  => 'app',
		table       => 'system',
);
$viaroute->{app}->{class}[0]=\%class;
XMLwrite($viaroute, $gPATH."viaroute.xml");
		
