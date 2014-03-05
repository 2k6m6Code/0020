#!/usr/bin/perl
use CGI;
require ('qbmod.cgi');
my $form=new CGI;
my $MAX_CONNECTION_TO_SHOW=$form->param('top');


runCommand(command=>'/bin/sh', params=>'/usr/local/apache/qb/setuid/UserFlowSort '.$MAX_CONNECTION_TO_SHOW);

print "Content-type:text/html\n\n";
print qq (<html><body><script>


parent.FXLoadData();


</script></body></html>);

sub sort_by_request_and_reply
{
    #20080212 Brian for new ip_conntrack in kernel 2.6
    (my $requesta, $replya)=($a=~/bytes=(\S+).+bytes=(\S+)/); my $totala=$requesta+$replya; 
    (my $requestb, $replyb)=($b=~/bytes=(\S+).+bytes=(\S+)/); my $totalb=$requestb+$replyb; 
    
    $totalb<=>$totala;
}


