#!/usr/bin/perl
require ('../qbmod.cgi');

print "Content-type:text/html\n\n";

#=========================================================================================
print qq (<html><head><link rel="stylesheet" href="../gui.css" type="text/css"></head> );
print qq (<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040"> );
maintainBasic(action=>"REPORT");
maintainDNS(action=>"REPORT");
maintainNAT(action=>"REPORT");
maintainDMZ(action=>"REPORT");
maintainVS(action=>"REPORT");
maintainRtable(action=>"REPORT");
maintainZone(action=>"REPORT");
maintainIniroute(action=>"REPORT");
maintainService(action=>"REPORT");
editUsers(action=>"REPORT");
print qq (</html>);


