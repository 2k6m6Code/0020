#!/usr/bin/perl

require ("qbmod.cgi");

use CGI;

#這一行一定要放在 authenticate 後面
print "Content-type:text/html\n\n";

#假如認證失敗，就直接結束
if (1) 
{
print << "QB_HOME";
    <html>
    <head>
        <title>Q-Balancer Configuration Center</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <script type="text/javascript" src="qb.js"></script>
        <script language="javascript">
            document.cookie="flow=1";
        </script>
    </head>
    <frameset rows="*" cols="140,*" frameborder="AUTO" border="0" framespacing="0"> 
      <frame name="menuFrame" scrolling="YES" noresize src="menu.cgi" frameborder="NO">
      <frameset rows="50,*" frameborder="NO" border="0" framespacing="0" cols="*"> 
        <frame name="configFrame" src="tmp_config.php" scrolling="NO">
        <frameset rows="*" cols="*" frameborder="NO"> 
          <frame name="mainFrame" src="search.cgi?option=query_host" frameborder="NO" noresize scrolling="AUTO">
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

#general_script();

