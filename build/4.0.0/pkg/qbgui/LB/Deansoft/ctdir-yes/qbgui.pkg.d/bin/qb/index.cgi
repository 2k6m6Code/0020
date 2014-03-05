#!/usr/bin/perl

require ("qbmod.cgi");

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
use JSON;
my $form=new CGI;
my $action1 = $form->param(action);
my $username=$form->param(username);
my $password=$form->param(password);
authenticate( action=>'LOGIN', username=>$username, password=>$password );

#這一行一定要放在 authenticate 後面
print "Content-type:text/html\n\n";

#假如認證失敗，就直接結束
if ( $gLOGINRESULT ) 
{
print << "QB_HOME";
    <html>
    <head>
        <title>Q-Balancer Configuration Center</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <script type="text/javascript" src="qb.js"></script>
        <script language="javascript">
              window.onunload =function() 
              { 
                  var clearcookie=getcookie('clearcookie');
                  if ( clearcookie=='false' ) { return; }
                  qbLogout(); 
              } 
              //automatically logout
        </script>
    </head>
    <frameset rows="*" cols="140,*" frameborder="AUTO" border="0" framespacing="0"> 
      <frame name="menuFrame" scrolling="YES" noresize src="menu.cgi" frameborder="NO">
      <frameset rows="50,*" frameborder="NO" border="0" framespacing="0" cols="*"> 
        <frame name="configFrame" src="config.cgi" scrolling="NO">
        <frameset rows="*" cols="*" frameborder="NO"> 
          <frame name="mainFrame" src="dashboard.php" frameborder="NO" noresize scrolling="AUTO">
        </frameset>
      </frameset>
    <frame src="right.htm" scrolling="NO">
    </frameset>
    </noframes> 
    </html>
QB_HOME
}
else 
{
    print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
    print qq(<body bgcolor="#003366" text="#ffffff" link="#000040" vlink="#400040"></body></html>);
}

general_script();

