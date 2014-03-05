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
#print << "QB_HOME";
print qq(<html>);
print qq(<head>);
print qq(<title>Q-Balancer Configuration Center</title>);
print qq(<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">);
print qq(<script type="text/javascript" src="qb.js"></script>);
print qq(<script language="javascript">);
print qq(window.onunload =function(){);
print qq(var clearcookie=getcookie('clearcookie'););
print qq(if ( clearcookie=='false' ) { return; });
print qq(qbLogout(); });
print qq(</script>);
print qq(</head>);
print qq(<frameset rows="*" cols="140,*" frameborder="AUTO" border="0" framespacing="0">);
print qq(<frame name="menuFrame" scrolling="YES" noresize src="menu.cgi" frameborder="NO">);
print qq(<frameset rows="50,*" frameborder="NO" border="0" framespacing="0" cols="*"> );
print qq(<frame name="configFrame" src="config.cgi" scrolling="NO">);
print qq(<frameset rows="*" cols="*" frameborder="NO">);


if ($action1 > 8)
{
    print qq(<frame name="mainFrame" src="dashboard.php" frameborder="NO" noresize scrolling="AUTO">);
}else
{
    print qq(<frame name="mainFrame" src="dashboard.cgi" frameborder="NO" noresize scrolling="AUTO">);
}
print qq(</frameset>);
print qq(</frameset>);
print qq(<frame src="right.htm" scrolling="NO">);
print qq(</frameset>);
print qq(</noframes>);
print qq(</html>);
}
else 
{
    print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
    print qq(<body bgcolor="#003366" text="#ffffff" link="#000040" vlink="#400040"></body></html>);
}

general_script();

