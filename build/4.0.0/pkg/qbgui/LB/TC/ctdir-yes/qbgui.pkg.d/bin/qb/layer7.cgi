#!/usr/bin/perl
use CGI;
use Data::Dumper;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

my $form=new CGI;
my %action;
$action{action}=$form->param('action');

$action{src_subnet}=$form->param('src_subnet');
$action{dst_subnet}=$form->param('dst_subnet');
$action{l7service}=$form->param('l7service');
$action{l7action}=$form->param('l7action');
$action{key}=$form->param('key');
$action{value}=$form->param('value');

# Creating key of policy rule to matched rule
my $keyofrule='';
$keyofrule=$action{src_subnet}.$action{dst_subnet}.$action{l7service}.$action{l7action};
#$action{keyofrule}=( $form->param('keyofrule') ) ?  ( $form->param('keyofrule') ) : ( $keyofrule ) ;
$action{keyofrule}=$keyofrule;

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body  bgcolor="#336699">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

layer7Script();

editLayer7( %action );

print qq (<div align="center">);
print qq (<form name="editLayer7" method="post" action="layer7.cgi">);
listLayer7( %action );
print qq (<input type="hidden" name="action" value="$action{action}">);
print qq (<input type="hidden" name="layer7" value="">);
print qq (<input type="hidden" name="keyofrule" value="$keyofrule">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html> );  

