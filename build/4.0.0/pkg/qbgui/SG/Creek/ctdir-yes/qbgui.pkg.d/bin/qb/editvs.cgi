#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

#read-in form information ------------------------------
#a hash structure to  package form info and then pass it as parameter to  natnet_maintain()  ----
my $form=new CGI;
my %action;

$action{action}=$form->param('action'); 
$action{isp}=$form->param('isp');
$action{vip}=$form->param('vip');

my @servicelist=$form->param('service');
$action{service}=\@servicelist;

$action{local}=$form->param('local');
$action{natid}=$form->param('natid'); 
$action{batcrtdata}=$form->param('batcrtdata');

my $aa =$form->param("rservers");
if ($aa=~/\d{1,3}\./)
{
    my  @rservers = &str2IpList($form->param("rservers"));
    push ( @rservers, 'system' );
    $action{rservers} = \@rservers;
}else
{
  if ( $action{local} eq "localhost") { @rservers=('localhost', 'system'); }
  else 
  {
      $ff=$form->param("rservers");
      my @aa = split(/:/,$form->param("rservers"));
      if ($#aa ne 7)
      {
          my $bb = 8-$#aa;
          for (my $i =0;$i<$bb;$i++)
          {
              $cc.=":0";
          }
          $cc.=":";
          $ff =~s/::/$cc/;
      }
      @rservers = $ff;
      push ( @rservers, 'system' );
  }
  $action{rservers} = \@rservers;
}
$action{real_service}=$form->param('real_service');
if ( !$action{real_service} ) { $action{real_service}=''; }

if ( $action{local} eq "localhost") { @rservers=('localhost', 'system'); }

#-- Send html header --------------------------------------
print qq (<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body  style="overflow:hidden" bgcolor="#336699" text="#ffffff" link="#2030dd" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainVS( %action ); }

#------- pass form information to the procedure of updating  subnet.xml -----------------------------------
print qq(<div class="myframe">);
print qq (<form name="vsnetform" action="editvs.cgi" method="post">);

editVS( %action );

print qq(<input type="hidden" name="action" value="$action{action}">);
print qq(</form></div>);

general_script();

editVSScript();



print qq(</body></html>);
