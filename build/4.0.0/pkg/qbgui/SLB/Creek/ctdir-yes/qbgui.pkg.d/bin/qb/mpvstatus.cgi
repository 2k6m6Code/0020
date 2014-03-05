#!/usr/bin/perl
require ("qbmod.cgi");
print "Content-type:text/html\n\n";

#get all links status (alive or dead)

use CGI;
use Data::Dumper;

    # MPV Link
    
    my $ispref=XMLread('/usr/local/apache/active/basic.xml');
    my $isplist=$ispref->{isp};

    foreach my $isp ( @$isplist )
    {
        if ( $isp->{iid} eq 'system' ) { next; }
        #if ( $isp->{isptype} ne 'normal' &&  $isp->{isptype} ne 'ipsec' && $isp->{isptype} ne 'dtunnel' )
        if ( $isp->{isptype} eq 'tunnel' )
        {
            my $imgsrc = ( $isp->{alive} ) ? ( 'alive.png' ) : ( 'dead.png' );
            print qq ($isp->{systemip},$imgsrc,);
        }
    }
#
