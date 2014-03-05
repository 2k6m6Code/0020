#!/usr/bin/perl -w

use CGI;

require("/usr/local/apache/qb/qbmod.cgi");

my $q = new CGI;
print $q->header;
my $group = $q->param('group');
if ($file = $q->param('filename'))
{  
    	my $schref=XMLread('/usr/local/apache/qbconf/flow.xml');
    	my $schlist=$schref->{user};
    	my @subscharrary;
    	my %newschedule;
    	foreach my $flow (@$schlist)
    	{
    	    if ($flow->{schname} eq 'system'){next;}
    	    while(<$file>)
    	    {
    	    	my($ip,$name)=split(/,/,$_);
    	    	my %newschedule;
    	    	$newschedule{ip}=$ip;
    	    	$newschedule{mail}=$name;
    	    	push(@subscharray, \%newschedule);	
    	    }
    	    $newschedule{member}=\@subscharray;
    	    $newschedule{schname}=$flow->{schname};
    	    $newschedule{description}=$flow->{description};
    	    $flow=\%newschedule;
    	}
    	XMLwrite($schref, "/usr/local/apache/qbconf/flow.xml");
}
print qq (<script language="javascript">window.close();</script>);

