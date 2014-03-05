#!/usr/bin/perl

use CGI;

my $form=CGI-> new();
my $name=$form->param("name");
my $option=$form->param("option");
print "Content-type: text/html\n\n";
if ($name ne '')
{
    my @data = `/usr/local/apache/qb/setuid/run  /usr/local/apache/qb/status/rate.cgi`;
    my $total_up=0;
    my $total_down=0;
    foreach my $o (@data)
    {
    	if(!grep(/window.parent.gmaster.add/,$o)){next;}
        $o=~s/window.parent.gmaster.add//;
        $o=~s/\(||\)||;||"//g;
        my @dd=split(/, /,$o);
        if ($dd[0] eq $name )	
        {
            if ($option eq 'up')
            {
            print $dd[3];
            }
            elsif ($option eq 'down')
            {
            print $dd[4];
            }
            elsif ($option eq 'latency')
            {
            print $dd[11];
            }
            elsif ($option eq 'loss')
            {
            print $dd[12];
            }elsif ($option eq 'up-total')
            {
                print $dd[8];
            }elsif ($option eq 'down-total')
            {
                print $dd[7];
            }
            
        }else
        {
            if ($option eq 'total_up')
            {
	        $total_up +=$dd[3];
	    }
            if ($option eq 'total_down')
            {
    		$total_down +=$dd[4];
            }
        }
    }
    if ($option eq 'total_up')
    {
        print $total_up;
    }
    if ($option eq 'total_down')
    {
        print $total_down ;
    }
}
