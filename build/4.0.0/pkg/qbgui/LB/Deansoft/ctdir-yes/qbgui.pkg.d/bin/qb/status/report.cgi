#!/usr/bin/perl
use CGI;
require ('../qbmod.cgi');
my $form=new CGI;
my $target=$form->param('name'); if ( !$target ) { $target='connection'; }
my $MAX_CONNECTION_TO_SHOW=$form->param('top');


if ( $target=~m/connection/i )
{
    my $conntrack=runCommand(command=>'cat', params=>'/proc/net/ip_conntrack');
    my @conntrackrecord=split(/\n/, $conntrack);
    my @allconnections;

    open(CONNTRACK,    "> conntrack.web");
    open(CONNTRACKCSV, "> conntrack.csv");

    print CONNTRACK "State,Protocol,Src1,Sport1:Int,Dst1,Dport1:Int,Src2,Sport2:Int,Dst2,Dport2:Int,Rqst(KB):Int,Rply(KB):Int\n";
    print CONNTRACKCSV "State,Protocol,Src1,Sport1:Int,Dst1,Dport1:Int,Src2,Sport2:Int,Dst2,Dport2:Int,Rqst(KB):Int,Rply(KB):Int\n";

    @conntrackrecord=sort sort_by_request_and_reply @conntrackrecord;

    my $numtoshow=( $MAX_CONNECTION_TO_SHOW < @conntrackrecord ) ? ( $MAX_CONNECTION_TO_SHOW ) : ( @conntrackrecord ); $numtoshow--;

    my $totalrecord=@conntrackrecord-1;

    for ( my $count=0; $count <=$numtoshow; $count++ ) 
    {   
        my $data=$conntrackrecord[$count];
        (my $pronum, $volumn)=($data=~/(\d+)\s+(\d+)/);
        (my $state)=($data=~/\[(\S+)\]/); 
        (my $pro)=($data=~/(udp|tcp)/);
        (my $src1, $src2)=($data=~/src=(\S+).+src=(\S+)/);
        (my $dst1, $dst2)=($data=~/dst=(\S+).+dst=(\S+)/);
        (my $sport1, $sport2)=($data=~/sport=(\S+).+sport=(\S+)/);
        (my $dport1, $dport2)=($data=~/dport=(\S+).+dport=(\S+)/);
        #(my $request, $reply)=($data=~/ORI-byte=(\S+).+RPY-byte=(\S+)/); $request=int($request/1024); $reply=int($reply/1024); 
        #20080212 Brian for new ip_conntrack in kernel 2.6
        (my $request, $reply)=($data=~/bytes=(\S+).+bytes=(\S+)/); $request=int($request/1024); $reply=int($reply/1024); 
        print CONNTRACK    qq($state,$pro,$src1,$sport1,$dst1,$dport1,$src2,$sport2,$dst2,$dport2,$request,$reply)."\n";
        print CONNTRACKCSV qq($state,$pro,$src1,$sport1,$dst1,$dport1,$src2,$sport2,$dst2,$dport2,$request,$reply)."\n";
    }
    close (CONNTRACK);

    for ( my $count=$numtoshow+1; $count <=$totalrecord; $count++ ) 
    {   
        my $data=$conntrackrecord[$count];
        (my $pronum, $volumn)=($data=~/(\d+)\s+(\d+)/);
        (my $state)=($data=~/\[(\S+)\]/); 
        (my $pro)=($data=~/(udp|tcp)/);
        (my $src1, $src2)=($data=~/src=(\S+).+src=(\S+)/);
        (my $dst1, $dst2)=($data=~/dst=(\S+).+dst=(\S+)/);
        (my $sport1, $sport2)=($data=~/sport=(\S+).+sport=(\S+)/);
        (my $dport1, $dport2)=($data=~/dport=(\S+).+dport=(\S+)/);
        #(my $request, $reply)=($data=~/ORI-byte=(\S+).+RPY-byte=(\S+)/); $request=int($request/1024); $reply=int($reply/1024); 
        #20080212 Brian for new ip_conntrack in kernel 2.6
        (my $request, $reply)=($data=~/bytes=(\S+).+bytes=(\S+)/); $request=int($request/1024); $reply=int($reply/1024); 
        print CONNTRACKCSV qq($state,$pro,$src1,$sport1,$dst1,$dport1,$src2,$sport2,$dst2,$dport2,$request,$reply)."\n";
    }
    close ( CONNTRACKCSV );
}
elsif ( $target=~m/mangle/i )
{
    my $mangle=runCommand(command=>'iptables', params=>' -t mangle -L -v -n ');
    my @manglerecord=split(/\n/, $mangle);
    open(MANGLE, "> mangle.txt");
    # print field names
    print MANGLE "Packets,Bytes,Protocal,Source,Sport,Destination,Dport\n";
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
        print MANGLE qq ($packets,$bytes,$protocal,$src,$sport,$dst,$dport)."\n";
    }
    close ( MANGLE );
}

print "Content-type:text/html\n\n";
print qq (<html><body><script>

parent.FXLoadData();


</script></body></html>);

sub sort_by_request_and_reply
{
    #20080212 Brian for new ip_conntrack in kernel 2.6
    (my $requesta, $replya)=($a=~/bytes=(\S+).+bytes=(\S+)/); my $totala=$requesta+$replya; 
    (my $requestb, $replyb)=($b=~/bytes=(\S+).+bytes=(\S+)/); my $totalb=$requestb+$replyb; 
    
    #(my $requesta, $replya)=($a=~/ORI-byte=(\S+).+RPY-byte=(\S+)/); my $totala=$requesta+$replya; 
    #(my $requestb, $replyb)=($b=~/ORI-byte=(\S+).+RPY-byte=(\S+)/); my $totalb=$requestb+$replyb; 
    $totalb<=>$totala;
}


