#!/usr/bin/perl
use CGI;
require ('../qbmod.cgi');


my $mangle=(`../setuid/run /usr/local/bin/iptables -t mangle -L -v -n`);
my @manglerecord=split(/\n/, $mangle);
open(MANGLE, "> mangle.txt");
# print field names
print MANGLE "Packets, Bytes, Protocal, Source, Sport, Destination, Dport\n";
print MANGLE "0, 0, 0, 0, 0, 0, 0\n";

foreach my $data ( @manglerecord ) 
{ 
    if ( $data=~m/Chain|target/ || !$data ) { next; }
    $data=~/\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/;
    my @datafields=split(/\s+/, $data);
    (my $packets)=$datafields[0];
    (my $bytes)=$datafields[1];
    (my $protocal)=$datafields[3];
    (my $src)=$datafields[7];
    (my $dst)=$datafields[8];
    (my $sport)=($data=~/spt:(\S+)/);
    (my $dport)=($data=~/dpt:(\S+)/);
    print MANGLE qq ($packets, $bytes, $protocal, $src, $sport, $dst, $dport)."\n";
}
close ( MANGLE );

print "Content-type:text/plain\n\n";
print  << 'FORMAT';  

<html>
<body>
<script>
Sel_Name = new Array();
Sel_Name.push(	new Array("Packets"	,	140,	1,	"center")	);
Sel_Name.push(	new Array("Bytes"	,	140,	1,	"center")	);
Sel_Name.push(	new Array("Protocol"	,	140,	1,	"center")	);
Sel_Name.push(	new Array("Source"	,	140,	1,	"center")	);
Sel_Name.push(	new Array("Sport"	,	140,	1,	"center")	);
Sel_Name.push(	new Array("Destination"	,	140,	1,	"center")	);
Sel_Name.push(	new Array("Dport"	,	140,	1,	"center")	);
window.parent.ShowData(Sel_Name,"mangle.txt");
</script>
</body>
</html>

FORMAT

