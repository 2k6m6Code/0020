#!/usr/bin/perl 
require ('../qbmod.cgi');
print "Content-type:text/html\n\n";
my $uptime=readpipe 'uptime'; $uptime=~s/,\s+\d+\s+user.*$//g;
print qq (<html><head><link rel="stylesheet" href="../gui.css" type="text/css">);
print qq (<script type="text/javascript" src="../qb.js"></script></head>);
print qq (<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq (<style>body{ background:#336699; text-align:center; }</style></head><body>);

print qq(<font class="body">Uptime: $uptime</font>);
print qq(<a href="javascript:qbShowHelp('system')"><image src="/image/help.gif" border="0" title="Help"></a>);
print qq(<br><br>);
print qq(<DIV id="line1" class="gui_line" text="CPU Usage" cgipath="getsysstatus.cgi" interval="3000"></DIV><br>);

print qq(<DIV id="line2" class="gui_line" text="Memory Usage" cgipath="memory.status" interval="3000" attr0="Total" attr2="Available"></DIV><br>);

print qq(<DIV id="line3" class="gui_line" text="Ramdisk Usage" cgipath="ramdisk.status" attr0="Total" attr2="Available" interval="3000"></DIV><br>);

print qq(<DIV id="line4" class="gui_line" text="Concurrent Sessions" cgipath="session.status" interval="3000" attr0="Max" attr2="Concurrent"></DIV>);

print qq (</body></html>);
