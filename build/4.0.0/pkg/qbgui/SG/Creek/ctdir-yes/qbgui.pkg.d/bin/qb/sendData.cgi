#!/usr/bin/perl
use CGI;
print "Content-type:text/html\n\n";
require ("/usr/local/apache/qb/qbmod.cgi");
my $ispref=XMLread('/usr/local/apache/active/basic.xml'); 
my $isplist=$ispref->{isp};
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);
if ( !$gENABLECMS ) { noneFunctionExit('Dispatch Config is an Option');} #No PPTP server
my $i = $a = 1;
my $y = $b = 100;
my $x = $c = $d = 0;
print qq (<button  onclick="parent.mainFrame.location='cmsCrmconfig.cgi?viewpoint=managerUPG'" hidefocus="true" class="menu">Upload</button>);
print qq (<button  onclick="parent.mainFrame.location='sendData.cgi'" hidefocus="true" class="menu">Upgrade</button>);

print qq(<div align="center" width="100%">);
print qq(<div align="center" id="all" style="width:700px">);
print qq(<table><td class="bigtitle" colSpan="2">Configuration File</td></table>);
print qq(<tr><hr size="2">);
foreach $isp (@$isplist)
{
#----------------------------------------------------------------------------------------------------------------------
    if ($isp->{isptype} eq "dtunnel" || $isp->{isptype} eq "tunnel")
    {
    	if ( $isp->{tunnel_role} eq "0" ){next;}
    	if($isp->{alive} eq "1" && $isp->{qbsn} ne "")
    	{
    	    for (my $z = 0; $z <= $#tmp; $z++)
    	    {
    	    	if ($tmp[$z] eq $isp->{qbsn}){$check = 1;}
     	    }
    	    if ($check eq "1"){next;}
    	    print qq(<div style="width:500px"><table border=1>);
    	    print qq(<td class="bigtitle" align=center>LOCAL </td>);
	    print qq(<td></td><td class="bigtitle" align=center>$isp->{qbsn}</td><tr> );
	    print qq(<input type="hidden" id="iid$i" value="$isp->{qbsn}">);
	    print qq(<td rowspan=4><form method="post" action="">);
	    print qq(<select id="list$i" size = 5 style="width:170px"> );
	    $file = join(",",glob('/mnt/qb/conf/cms/'.$isp->{qbsn}.'/*'));
	    @name = split(",",$file);
	    foreach $y (@name)
   	    {
    	    	$y =~ s/\/mnt\/qb\/conf\/cms\/$isp->{qbsn}\///;
    	    	if ($y eq "boot" || $y eq "default" || $y eq "active"){next;}
    	    	print qq(<option value="$y">$y);
	    }
	    print qq(</select>);
   	    print qq(</td><td></td>);
	    print qq(<td rowspan=4><form method="post">);
	    print qq(<select id="list$y" size = 5 style="width:170px" action=""> );
	    print qq(</select></td>);
	    print qq(<tr><td><input type="button" value=">>>" id="tran$i" onclick="inser('list$y','list$i');" style="width:80px" ></td>);
	    print qq(<tr><td><input type="button" value="<<<" id="trany$i" onclick="inser('list$i','list$y');" style="width:80px" ></td>);
	    print qq(<td rowspan=4 align="center"><input type="button" id="Save$x" value="Save" onclick="Save('iid$i','list$y','$i','tran$i','trany$i');" style="DISPLAY:none"></td></table></div>);
	    $tmp[$x] = $isp->{qbsn};
	    $d++;
        }
        $i++;
        $y++;
        $x++;
    }
}
if($d ne 0)
{
print qq(<input type="button" value="Save"  id="run" onclick="OK($x,'run');" style="width:80px" >);
#print qq(<input type="button" value="Query" id="run" onClick="savedata('query');" style="width:80px" >);
#print qq(<input type="button" value="File"  id="run" style="width:80px" ></div>);
}
$d = 0 ;
print qq(<div align="center" id="all" style="width:700px">);
print qq(<tr><tr><hr size="2">);
#---------------------------------------------------------------------------------------------------------------------
foreach $isp (@$isplist)
{
    if ($isp->{isptype} eq "dtunnel" || $isp->{isptype} eq "tunnel")
    {
        if ($isp->{tunnel_role} eq "0" && $isp->{alive} eq "1")
        {
            for (my $z = 0; $z <= $#tmp; $z++)
            {
            	if ($tmp[$z] eq $isp->{remote}){$check = 1;}
            }
            if ($check eq "1"){next;}
            print qq(<div style="width:500px"><table border=1>);
            print qq(<td class="bigtitle" align=center>$isp->{remote}</td> );
            print qq(<td></td><td class="bigtitle" align=center>LOCAL</td><tr>);
            print qq(<input type="hidden" id="iid$i" value="$isp->{remote}">);
            print qq(<td rowspan=4><form method="post" action="">);
            print qq(<select id="list$a" size = 5 style="width:170px"> );
            $file = join(",",glob('/mnt/qb/conf/set/*'));
            @name = split(",",$file);
            foreach $y (@name)
            {
            	$y =~ s/\/mnt\/qb\/conf\/set\///;
            	if ($y eq "boot" || $y eq "default" || $y eq "active"){next;}
            	print qq(<option value="$y">$y);
    	    }
    	    print qq(</select>);
   	    print qq(</td><td></td>);
   	    print qq(<td rowspan=4><form method="post">);
    	    print qq(<select id="list$b" size = 5 style="width:170px" action=""> );
       	    print qq(</select></td>);
    	    print qq(<tr><td><input type="button" value=">>>" id="tran$a" onclick="inser('list$b','list$a');" style="width:80px" ></td>);
       	    print qq(<tr><td><input type="button" value="<<<" id="trany$a" onclick="inser('list$a','list$b');" style="width:80px" ></td>);
    	    print qq(<td rowspan=4 align="center"><input type="button" id="Save$c" value="Save" onclick="Save('iid$a','list$b','$a','tran$a','trany$a');" style="DISPLAY:none"></td></table></div>);
    	    $tmp[$x] = $isp->{qbsn};
    	    $d++;
    	}
    	$a++;
    	$b++;
    	$c++;
    	
    }
}
if($d ne 0)
{
print qq(<input type="button" value="Save"  id="run" onclick="OK($c,'run');" style="width:80px" ></div></div>);               
}                                                                        
    
                                                                                         


#------------------------------------------------------------------------------------------------------------------------
                                                        
print << "QB";

<script type="text/javascript" src="../grid.js"></script>
<script language="javascript">

function OK(nb)
{   
    var x = nb;
    var all = document.getElementById("all");
    all.disabled = true;
    for (var i =0; i <= x;i++)
    {
        if (document.getElementById("Save"+i))
        {
            document.getElementById("Save"+i).click();
        }
    }
}
function inser(des,src)
{
    var des = document.getElementById(des);
    var src = document.getElementById(src);
    if (src.selectedIndex != -1)
    {
    	var opt = document.createElement("option");
    	des.options.add(opt);
    	opt.text = src.options[src.selectedIndex].text;
    	opt.value = src.options[src.selectedIndex].value;
    	src.remove(src.selectedIndex);
    }
}

function Save (ip,list,bt,tran,trany)
{
    
    var nb = bt;
    var ip = document.getElementById(ip);
    var list = document.getElementById(list);
    var listname = ip.value + "," + nb + ",";
    if (list.length == 0){auto_refresh();return;}
    for (var i = 0; i < list.length;i++)
    {
        listname += list.options[i].value + ",";
    }
    savedata(listname);
    auto_refresh(list.length);
}

var queryReqHandler;
function savedata(data)
{
    queryReqHandler = new ActiveXObject("Microsoft.XMLHTTP");
    queryReqHandler.onreadystatechange = fno;
    //if (data == "query"){queryReqHandler.open("GET","setuid/do_qbclient.pl" ,true);}
    queryReqHandler.open("GET","datawork.cgi?data=" + data + "&time="+ new Date().getTime() ,true);
    queryReqHandler.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    var str='';
    queryReqHandler.send(str);
}

function fno()
{    
    if(queryReqHandler.readyState == 4)
    {   
        queryReqHandler = null;
    }
}
function auto_refresh(index)
{

    setTimeout("start();",(index*6000));
}

function start()
{
    var all = document.getElementById("all");
    all.disabled = false;
}
</script>

QB










