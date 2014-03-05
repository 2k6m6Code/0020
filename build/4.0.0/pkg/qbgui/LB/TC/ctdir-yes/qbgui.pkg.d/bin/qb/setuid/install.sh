#!/bin/sh
cp -a lantraffic.cgi ajax.cgi ajax1.cgi reset.sh opreset.sh sorttable.js /usr/local/apache/qb/ 
mkdir /usr/lib/perl5/site_perl/5.8.8/CGI
mkdir /usr/lib/perl5/site_perl/5.8.8/Class
mkdir /usr/lib/perl5/site_perl/5.8.8/Class/Accessor
cp -a Ajax.pm /usr/lib/perl5/site_perl/5.8.8/CGI/
cp -a Fast.pm Faster.pm /usr/lib/perl5/site_perl/5.8.8/Class/Accessor/
cp -a Accessor.pm /usr/lib/perl5/site_perl/5.8.8/Class/
