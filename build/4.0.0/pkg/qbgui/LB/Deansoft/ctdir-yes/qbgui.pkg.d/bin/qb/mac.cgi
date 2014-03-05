#!/usr/bin/perl 
use Data::Dumper;
use XML::Simple;
use CGI;
my $cgi = new CGI;
print "Content-type:text/html\n\n";
#require ("/usr/local/apache/qb/qbmod.cgi");

my $xml;
my $action = $cgi->param("action");


# Display Title
print qq (<div align="center">);
print qq (<tr align="center"><td height="10" align="center">);
print qq (<font class="bigtitle" align="center" >MAC Clone</font> );
print qq (<br></td></tr>);
print qq (<tr><td><hr size=1 style="width: 500px"></td></tr>);
print qq (</div><br>);

if ($action eq "" && $action ne "SAVE")
{ 
    my $xmllive=-e "/usr/local/apache/qbconf/mac.xml";
    if ($xmllive)
    {
        #my $ref = XMLread("/usr/local/apache/qbconf/mac.xml");
        flock(XMLLOCK, 2);
        my $ref=XMLin("/usr/local/apache/qbconf/mac.xml", forcearray=>1);
        flock(XMLLOCK, 8);
        close XMLLOCK;
        my $macref= $ref->{mac};
    }
    print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"><script type="text/javascript" src="jquery-1.9.1.min.js"></script></head>);
    print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
    print qq(<div align="center">);
    print qq (<table id="mytable" cellspacing="0" border="0" width="100%" >);

    open ( FILE, '</opt/qb/registry') or "Open File Error";
    foreach my $line (<FILE>)
    {
        if(grep(/^NUMOFPORT/,$line))
        {
    	    $line=~s/^NUMOFPORT\s//g;
    	    $line=~s/\n//g;
    	    $line=~s/\s//g;
    	    $max=$line;
    	    last;
        }
    }
    close(FILE);
    print qq(<input type="hidden" id="total" value="$max">);
    #runCommand(command=>"/sbin/ifconfig" , params=>"|grep eth >>/tmp/mac");
    `/sbin/ifconfig |grep eth >>/tmp/mac`;

    open ( MACFILE, '</tmp/mac') or "Open File Error";
    foreach my $mac (<MACFILE>)
    {
        if(grep(/eth/,$mac))
        {
            $mac=~s/\sLink encap:Ethernet//g;
            my @tmp  = split(" ",$mac);
            print qq(<input type="hidden" id="$tmp[0]" value="$tmp[2]">);
        }
    }     
    close(MACFILE);        
    #runCommand(command=>"/bin/rm" , params=>"/tmp/mac");
    `/bin/rm /tmp/mac`;
    foreach my $isp (1..$max)
    {
        my $port = "Port$isp";
        $isp--;
   	print qq (<tr>);
   	print qq (<td class="body" align="right" width="6%"><a class="body">$port</a></td><td width="1%"></td>);
   	print qq (<td class="body" id="$isp" width="3%"> </td>);
   	print qq (<td align="center" width="1%">></td>);
   	print qq (<td width="8%" colspan=2 ><input type="text" id="port$isp" value=""></td>);
   	print qq (</tr>);
    
    }
    print qq (</table>);
    print qq (<table border="0" width="50%">);
    print qq (<br>);
    print qq (<tr><td align="center"><hr size="1" width="500px"></td></tr>);
    print qq(<tr><td colspan=2 align="center"><input id="ok" type="button" class="qb" value="SAVE" style="width:10%"></td>);
    foreach my $mac (@$macref)
    { 
        if ($mac->{mac} && $mac->{nic})
        {
            $xml.=$mac->{nic}.",".$mac->{mac}."-";
        }
    }
    $xml =~s/-$//g;
    print qq(<input type="hidden" id="xml" value="$xml">);
    print qq (</table></body></html>) ;
}
if ($action eq "SAVE")
{
    my $data = $cgi->param("data");
    my $comup;
    my $comdown;
    my $commac;
    $data =~s/-$//g;
    my @datalist = split("-",$data);
    open(FILE,">/usr/local/apache/qbconf/mac.xml") or "Open File Error";
    open(MACFILE,">/usr/local/apache/qbconf/mac.sh") or "Open File Error";
    $info = '<opt file="eth">';
    print FILE "$info\n";
    foreach my $list (@datalist)
    {
        ($eth,$mac)=split(",",$list);
        my $info = '<mac nic="'.$eth.'" mac="'.$mac.'"/>';
        $comup = "/sbin/ifconfig ".$eth." up";
        $comdown = "/sbin/ifconfig ".$eth." down";
        $commac = "/sbin/ifconfig ".$eth." hw ether ".$mac;
        print FILE "$info\n";
        print MACFILE "$comdown\n";
        print MACFILE "$commac\n";
        print MACFILE "$comup\n";
    }
    print FILE '</opt>';
    close(MACFILE);
    close(FILE);
    #runCommand(command=>"chmod" , params=>"777 /usr/local/apache/qbconf/mac.sh");
    `/bin/chmod 777 /usr/local/apache/qbconf/mac.sh`;
    return ;
}

print << "QB";
<script language="javascript">

\$(window).load(function(){
    var xml = \$("#xml").val();
    var xmlAR = new Array();
    var Dxml = new Array();
    xmlAR=xml.split("-");
    for(var i = 0; i < \$("#total").val(); i++)
    {
        if (\$("#eth" + i).val() == "")
        {
            \$("#" + i).val("ERROR");
            \$("#port" + i).val("ERROR");
            \$("#port" + i).attr("disabled",true);
        }
        else
        {
            \$("#" + i).html(\$("#eth" + i).val());
            for ( var x = 0;x < xmlAR.length;x++)
            {
                Dxml = xmlAR[x].split(",");
                if (Dxml[0] == "eth" + i && \$("#eth" + i).val() != Dxml[1])
                {
                    \$("#port" + i).val(Dxml[1]);
                }
                else
                {
                    \$("#port" + i).val(\$("#eth" + i).val());
                }
            }
        }
        if ( i == "0" || i == "1")
        {
            \$("#port" + i).attr("disabled",true);
            \$("#port" + i).val(\$("#eth" + i).val());
        }
    }
});

\$("#ok").click(function(){
    var data="";
    var point= "0" ;
    for(var i = 0; i < \$("#total").val(); i++)
    {
        if (\$("#port" + i).val() != "" &&  i != 0 && i != 1 && \$("#port" + i).val() != "ERROR" && \$("#port" + i).val() != \$("#eth" + i).val())
        {
            if (checkmac(\$("#port" + i).val(),i))
            {
                data += "eth" + i + "," + \$("#port" + i).val() + "-";
            }
            else
            {
                alert("MAC [" + \$("#port" + i).val()  + "] ERROR!?");
                point = "1";
            }
        }
    }
    if (point == "0")
    {
        \$.get("mac.cgi",{action:"SAVE",data:data},function(){
            alert("Change Success!! Restart Become Effective!!");
        });
    }
});

function checkmac(mac,im)
{
    var word=/([a-fA-F0-9]+):([a-fA-F0-9]+):([a-fA-F0-9]+):([a-fA-F0-9]+):([a-fA-F0-9]+):([a-fA-F0-9]+)/; 
    if(!word.test(mac))
        return false;
    if( mac.split("").length != 17)
        return false;
    for(var i = 0; i < \$("#total").val(); i++)
    {
        if (im != i && (\$("#port" + i).val() == mac || \$("#eth" + i).val() == mac ))
            return false
    } 
    return true;
}
</script>
QB
