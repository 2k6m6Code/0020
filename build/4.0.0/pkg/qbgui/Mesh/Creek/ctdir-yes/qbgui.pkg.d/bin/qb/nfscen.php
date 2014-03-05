<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
        <meta HTTP-EQUIV="Cache-Control" content="no-cache">
        <meta HTTP-EQUIV="Pragma" CONTENT="no-cache">
        <link rel="stylesheet" type="text/css" href="/usr/local/apache/qb/nfsen/css/nfsen.css">
	<link rel="stylesheet" type="text/css" href="/usr/local/apache/qb/nfsen/css/profileadmin.css">                        
        <script language="Javascript" src="/usr/local/apache/qb/nfsen/js/global.js" type="text/javascript">
        </script>
        <script language="Javascript" src="/usr/local/apache/qb/nfsen/js/menu.js" type="text/javascript">
        </script>
                                                

<?php
session_start();
include ("/usr/local/apache/qb/nfsen/conf.php");
include ("/usr/local/apache/qb/nfsen/nfsenutil.php");
include ("/usr/local/apache/qb/nfsen/navigator.php");

require ("/usr/local/apache/qb/nfsen/overview.php");
DisplayGraphs("flows");

?>
<div id="hintbox"></div>
</body>
</html>
