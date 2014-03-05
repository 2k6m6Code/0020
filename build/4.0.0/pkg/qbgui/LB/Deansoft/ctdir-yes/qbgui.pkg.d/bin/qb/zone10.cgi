#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
print "Content-type:text/html\n\n";
print qq(<html><head><TITLE></TITLE>);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);
if($gENABLETUNNEL)
{
    print qq(<FRAMESET ROWS="*,*"><FRAME SRC="bridge.cgi"><FRAME SRC="zone2.cgi?viewpoint=dmz">);
}
else { print qq(<FRAMESET ><FRAME SRC="bridge.cgi">); }

print qq(</FRAMESET"></FRAMESET"></html>);
