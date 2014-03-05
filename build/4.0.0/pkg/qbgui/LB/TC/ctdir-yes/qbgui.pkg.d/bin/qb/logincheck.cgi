#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");


#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');
print "Content-type:text/html\n\n";

#read-in form information ------------------------------
#a hash structure to  package form info and then pass it as parameter to  subnet_maintain()  --------------            
my $form = new CGI;

#=========================================================================================
#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) {
print qq(0);
} else {
print qq(1);
}

#------- start to draw every form object to interact with users ------------------------------------






