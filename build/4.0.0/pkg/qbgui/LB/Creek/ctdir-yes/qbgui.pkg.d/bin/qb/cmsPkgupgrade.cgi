#!/usr/bin/perl

use CGI;

print "Content-type:text/html\n\n";

my  $form = new CGI;

$ccstr = $form->param('client');


# print $ccstr;


require ("qbmod.cgi");  #XMLread include


# pkgradeclient.sh
$ccstr.=",dsaf9";
@tmpqb=split(/,/ ,$ccstr);
pop @tmpqb;
# foreach $clientIP ( @tmpqb ){
# print $clientIP;

# print "<br />";
# }

my $ispref=XMLread($gACTIVEPATH.'basic.xml');
my $isplist=$ispref->{isp};

foreach my $isp ( @$isplist )
{
	if( grep { $_ eq $isp->{qbsn}} @tmpqb){
	# print $isp->{qbsn};
	
	runCommand(command=>'/usr/local/apache/qb/setuid/pkgradeclient.sh', params=>"$isp->{gateway}");
	$logtext = runCommand(command=>'cat', params=>"/tmp/".$isp->{gateway}."/log");
	if($logtext ne ""){
	print " ".$isp->{qbsn}."[done]\n";
	print $logtext."\n";
	
	}
	
	}
	
}
	



