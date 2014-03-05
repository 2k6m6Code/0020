#!/usr/bin/perl

use CGI;

my $form=CGI->new();
my $name = $form->param("idd");
my $op = $form->param("op");
print "Content-type:text/html\n\n";
if ($name ne '')
{
    my @data = `/usr/local/apache/qb/setuid/run /bin/cat /mnt/tclog/speed.log`;
    my $p_d;
    foreach my $o (@data)
    {
	if ($o eq ''){next;}
	if (!grep(/$name/,$o)){next;}
	my @dd = split(/,/,$o);
	if ($op eq 'loss')
	{
	    if ($dd[3] ne '')
	    {
	        $dd[3] =~ s/.*://;
	        $p_d .= $dd[3].",";    
	    }
	}    
	if ($op eq 'pk')    
	{    
	    if ($dd[4] ne '')
	    {
	        $dd[4] =~ s/.*://;
	        $dd[4] =~ s/\s+//g;
	        $p_d .= $dd[4].",";
	    }
	}
    }
    print $p_d;
}
