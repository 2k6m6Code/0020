#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/pxyinit.lib";


#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

use CGI;
use Data::Dumper;

#---------------- read-in form information ------------------------------
my $form=new CGI;
my %action;

###############################################
#GENERAL
$action{action}=$form->param('action');

#$action{locallog}=($form->param('locallog')) ? (1) : (0);
$action{enablepxy}=($form->param('enablepxy')) ? (1) : (0);
$action{pxyhttpportno}=$form->param('pxyhttpportno');
$action{pxycachesize}=$form->param('pxycachesize');if ( !$action{pxycachesize} ) { $action{pxycachesize}=32; }
$action{replace_usage}=$form->param('replace_usage');if ( !$action{replace_usage} ) { $action{replace_usage}=70; }
$action{maxobj}=$form->param('maxobj');if ( !$action{maxobj} ) { $action{maxobj}=4096; }
$action{minobj}=$form->param('minobj');if ( !$action{minobj} ) { $action{minobj}=4; }


#$action{pxyhttpsportno}=$form->param('pxyhttpsportno');
#$action{pxyadmmail}=$form->param('pxyadmmail');
#$action{algorithm}=$form->param('algorithm');
#$action{pxypool}=$form->param('pxypool');
#$action{pxydatafrom}=$form->param('pxydatafrom');
#$action{pxycachesize}=$form->param('pxycachesize');if ( !$action{pxycachesize} ) { $action{pxycachesize}=0; }
#$action{replace_usage}=$form->param('replace_usage');if ( !$action{replace_usage} ) { $action{replace_usage}=70; }
#$action{maxobj}=$form->param('maxobj');if ( !$action{maxobj} ) { $action{maxobj}=4096; }
my @path;
my @iidlist=maintainBasic(action=>'GETIIDLIST');
foreach my $isp (@iidlist)
{
    my $weight=$form->param("weight"."$isp"); if ( !$weight ) { next };
    my %pathitem=(subnet=>$form->param("subnet"."$isp"), isp=>$isp, weight=>$weight);
    push(@path,\%pathitem)
}
$action{path}=\@path;
            
#=========================================================================================
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainPxyinit( %action ); }

#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="pxyinitform" method="post" action="pxyinit.cgi">);

pxyinitScript();

showPxyinit( %action ); 

print qq (<input type="hidden" name="action" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html>);

