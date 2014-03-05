#!/usr/bin/perl
use CGI;
my $form=new CGI;
my $access_this_ip=$form->param('delip');

`/usr/local/apache/qb/setuid/run /usr/local/apache/qb/setuid/delblacklist.sh $access_this_ip`;


