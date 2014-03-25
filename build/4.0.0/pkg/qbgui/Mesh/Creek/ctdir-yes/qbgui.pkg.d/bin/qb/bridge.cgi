#!/usr/bin/perl
use Data::Dumper;
use CGI;
my $cgi = new CGI;
print "Content-type:text/html\n\n";
require ("/usr/local/apache/qb/qbmod.cgi");
my $zone = XMLread($gPATH.'zonecfg.xml');
my $action = $cgi->param("action");
if ($action ne "SAVE")
{
    print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"><script type="text/javascript" src="jquery-1.9.1.min.js"></script>);
	print qq(<style type="text/css">.dragDiv {width:250px; position:absolute;	right:50px;	top:100px;}</style>);
	print qq(</head>);
    print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
    print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);
    if($gENABLETUNNEL){
    	print qq (<button id="return" onclick="parent.location='zone10.cgi'" hidefocus="true" class="menu">Subnet on DMZ</button>);
    	print qq (<button  onclick="parent.location='extroute.cgi'" hidefocus="true" class="menu">Subnet on WAN</button>);
    }
    my $ispref=XMLread($gPATH.'basic.xml');
    my $ref=$zone->{dmz};
    my $isplist=$ispref->{isp};
    my $max;
    my $total;
    my $write="";
    my $min;
    my @tunnel;
    my @titlename=('Status','Interface','Bridge On','ID',);
    my @titlelist=('','Status','');
    my $f=0;
    my $name ="0";
    open ( FILE, '</opt/qb/registry');
    foreach my $line (<FILE>)
    {
    	if(grep(/^NUMOFPORT/,$line))
    	{
            $line=~s/^NUMOFPORT\s//g;
            $line=~s/\n//g;
            $line=~s/\s//g;
            $max=$line;
            $min=$max/2;
            last;
        }
    }
    close(FILE);
    foreach my $check (@$ref)
    {
        if ($check->{nic} ne "" && $check->{mode} ne 'ARPPROXY'){next;}
        foreach my $ispid (@$isplist)
        {
            if($ispid->{iid} ne $check->{isp}){next;}
            $ispnic=$ispid->{nic}.",";
        }
        $arp = $check->{nic}.",".$ispnic;
    }
    $arp=~s/,$//;
    print qq(<input type="hidden" id="arp" value="$arp">);
    print qq (<div class="divframe" align="center" id="all"><table class="sortable" cellspacing="0" border="0" width="50%" id="mytable">);
    print qq (<tr><td class="bigtitle" colspan="4" align="left">Bridge Mode<hr size=1></td></tr><tr bgcolor="#332211"> );
    foreach my $title (@titlename){print qq(<td width="25%">$title</td>);}
    print qq (<input id="total" value="$max" type="hidden">);
    print qq (<select class="qbopt" id="Tname" style="display:none"><option value=None>None</option>);
    foreach my $num (1..$max)
    {
    	print qq (<option value="port$num">port$num</option>);
    } 
    print qq (</select>);
    print qq (<select class="qbopt" id="Mname" style="display:none"><option value=None>None</option>");
    foreach my $num (1..$max)
    {
    	print qq (<option value="port$num">port$num</option>);
    }
    print qq (</select>);
    my $check="0";
    my $lineCount=0;
    foreach my $table (1..$max)
    {
    	my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
    	print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" >);
    	#print qq (<td><select class="qbopt" id="mode$table"><option value="None">OFF<option value="bridge">ON</select></td>);
    	print qq (<td><input type="radio" class="qbopt" id="mode$table" name="mode$table" value="bridge">ON<input type="radio" class="qbopt" id="mode$table$table" name="mode$table" value="None" checked>OFF</td>);
    	print qq (<td><a>Port$table</a>);
    	print qq (<td><select class="qbopt" id="port$table" disabled=true><option value="None">None<td>);
    	$table--;
    	foreach my $isp (@$isplist)
    	{
            if ( $isp->{nic} ne 'eth'.$table && $isp->{pppoeportdev} ne 'eth'.$table ){next;}
            print qq(<input type="hidden" id="isp$table" value="$isp->{iid}"><a>$isp->{ispname}</a><br>);
    	}
    	print qq(</td></select>);
    	print qq(</td></tr>);
    	$lineCount++;
    }
    print qq(<tr><td></td><td colspan=2><input class="qb" type="button" id="ok" value="SAVE" style="width:100%"></td><td></td></tr></div><tr bgcolor="#332211">);
    foreach my $title1 (@titlelist)
    {
        if($title1 eq "")
        {
            print qq(<td width="25%">$title1</td>);
        }
        else
        {
            print qq(<td colspan=2 align="center" width="50%">$title1</td>);
        }
    }
    foreach my $dmz (@$ref)
    {
        if ($dmz->{mode} ne "BRIDGE"){next;}
        $dmz->{interface}=~s/eth//g;
        $dmz->{nic}=~s/eth//g;
        my $inter = $dmz->{interface} +1;
        my $nic = $dmz->{nic} +1;
        print qq(<tr><td align="center"></td>);
        print qq(<td colspan=2 >Port$inter<>Port$nic</td></div></tr>);
        $tunnel[$f]=$dmz->{interface}."<>".$dmz->{nic};
        $f++;
    }
    foreach my $mintable (0..$min)
    {
        $write=$tunnel[$mintable];
        print qq(<input type="hidden" id="cell$mintable" value="$write">);
    }    
    print qq(<input type="hidden" id="restart">);
	print qq(<div class="dragDiv">);
	print qq(<blockquote style="color:#000000;font-size:13px;background-color:#ffffcc;margin-left:0px;margin-right:0px;-webkit-box-shadow:#333333 4px 4px 6px;padding:0px;border:1px dashed #aabbcc;" draggable=true>);
	print qq(<FONT SIZE="3"><B>Note:</B></FONT><br>If you wish to view the traffic detail from transparent subnets on Viewflow, please go to <I>Logs and Reports->General Setting->Transparent Subnets</I> to complete the setup.);
	print qq(</blockquote>);
	print qq(</div>);
	print qq(</body></html>);
}
if( $action eq "SAVE")
{
    my $zonelist = $zone->{dmz};
    my $data=$cgi->param("data");
    my $i = 0;
    $data =~ s/,$//g;
    @datalist = split(/,/,$data);
    foreach my $zoneref (@$zonelist)
    {
        if($zoneref->{mode} eq "BRIDGE")
        {
           my $subnet=maintainBasic(action=>'GETISPSUBNET', iid=>$zoneref->{isp} );
           maintainInterrt( action=>"DEL", isp=>$zoneref->{isp}, nic=>$zoneref->{nic}, subnet=>$subnet, gateway=>""); 
           next;
        }
        if($zoneref->{name} eq "None"){$zoneref->{name}=""};
        push(@zonelist,$zoneref);
    }
    $zone->{dmz}=\@zonelist;
    my $zonelistref = $zone->{dmz};
    my $zonenat = $zone->{nat};
    foreach my $dataref (@datalist)
    {
        my %savedata;
        ($datatmp,$isp)=split(/:/,$dataref);
        foreach my $dmzref (@$zonelist)
        {
            if ($isp ne $dmzref->{isp}){next;}
            $dmzref->{name}="None";
        }
        my @allDmzIPs=maintainIPBank(from=>"isp".$ISP."dmz", action=>"read");
        ($interface,$nic)=split(/<>/,$datatmp);
        $inter = "eth".($interface - 1);
        $dev = "eth".($nic - 1);
        $name = "br$i";
        my $subnet=maintainBasic(action=>'GETISPSUBNET', iid=>$isp );
        maintainInterrt( action=>"ADD", isp=>$isp, nic=>$dev, subnet=>$subnet, gateway=>"");
        my %savedata=(
        	isp	  => $isp,
    		interface => $inter,
        	nic       => $dev,
        	name      => $name,
        	mode	  => 'BRIDGE',
        	enabled   => '1'
        );
        push(@$zonelistref,\%savedata);
        $i++;
        foreach my $nat ( @$natarray )
        {
           $nat->{dirty}=0;
           if ( $nat->{enabled} ) 
           {
               maintainInterrt(action=>'DEL', isp=>"nat$nat->{natid}", nic=>$nat->{nic}, subnet=>$nat->{network}, gateway=>$nat->{gateway});
               maintainInterrt(action=>'ADD', isp=>"nat$nat->{natid}", nic=>$dev, subnet=>$nat->{network}, gateway=>$nat->{gateway});
           }
        }
        my %routetodel;
        foreach my $dmzip ( @allDmzIPs ) { $routetodel{$dmzip.'/32'}=1; }
        maintainInterrt( action=>"BATDEL", route=>\%routetodel);
                                 
    }
    XMLwrite($zone, $gPATH."zonecfg.xml");
    return; 
}
print << "QB";

<script type="text/javascript" src="qb.js"></script>
<script language="javascript">

\$(window).load(function(){
    var num = \$("#total").val()/2 ;
    for (i = 0; i < \$("#arp").val().length; i+=5 )
    {
        var arp = \$("#arp").val().charAt(i+3);
        arp++;
        \$("#Mname option[value=port" + arp + "]").remove();
        \$("#Tname option[value=port" + arp + "]").remove();
        \$("#mode"+ arp).attr("disabled",true);
        
    }
    for (y = 0; y < num;y++ )
    {
        if (\$("#cell" + y).val() != "")
        {
             var interface = \$("#cell" + y).val().charAt(0);
             var nic = \$("#cell" + y).val().charAt(3);
             nic++;
             interface++;
             \$("#mode" + interface ).attr("chicked",true);
             \$("#mode" + interface ).trigger("click");
             \$("#port" + interface +" option[value=port" + nic  + "]").attr("selected",true);
             \$("#port" + interface).trigger("change");
        }
    }
    for (x=0; x < \$("#total").val();x++)
    {
        if (\$("#isp" + x).length == 0)
            \$("#mode"+(x+1)).attr("disabled",true);
    }
});



\$("#ok").click(function(){
var privilege=getcookie('privilege');
    if(privilege!=1) {alert('You do not have Privilege to do it'); return;}
    var num = \$("#total").val()/2 ;
    var max = ((\$("#total").val()-0) + (4-0));
    \$("#all").attr("disabled",true);
    \$("#mytable tr[class=option]").remove();
    for (y = 0; y < num;y++ )
        \$("#cell" + y).val(""); 
    for (x=0; x < \$("#total").val();x++)
    {
        var interface = "port" + (x+1);
        var nic = \$("#port" + (x+1)).val();
        if (\$("#isp" + x).length > 0)
        {
            var isp = \$("#isp" + x).val();
        }
        else
        {
            var isp = "0";
        }
        var data;
        if (nic != "None")
        {
            if (interface.charAt(4) > nic.charAt(4))
                data =  nic.charAt(4) + "<>" + interface.charAt(4) + ":" + isp;
            if (interface.charAt(4) < nic.charAt(4))
                data = interface.charAt(4) + "<>" + nic.charAt(4) + ":" + isp;
            for (y = 0; y < num;y++ )
            {
                if ( (\$("#cell" + y).val() == "" && data.charAt(5) > 0)||(\$("#cell" + y).val().charAt(0) == data.charAt(0) && \$("#cell" + y).val().charAt(3) == data.charAt(3) && data.charAt(5) > 0))
                {    
                   \$("#cell" + y).val(data);
                   break;
                }
            }
        }
    }
    var nn=""
    for (i = \$("#mytable").find("tr").length; i >= max ; i--)
    {
        \$("#mytable").find("tr").eq(i).remove();
    }
    for (y = 0; y < num;y++ )
    {
        if (\$("#cell" + y).val() != "")
        {
            
            \$("#mytable").append('<tr class="option"><td align="center"></td><td colspan=2>Port' + \$("#cell" + y).val().charAt(0) + '<>Port' +\$("#cell" + y).val().charAt(3)+ '</td></tr>');
            nn += \$("#cell" + y).val() + ',';    
        }
    }
    if (nn == "")alert("Please ,Choose any one!!");
    \$.get("bridge.cgi",{action:'SAVE',data:nn},function(){
        \$("#all").attr("disabled",false);
        alert("SAVE OK");
        \$("#return").trigger("onclick");
    });
});

\$('input[name^="mode"]').each(function(x){
    \$(this).click(function(){
        var i = Math.floor(x/2);
        \$("#port"+(i+1)).attr("disabled",false);
        \$("#port"+(i+1)).empty();
        for (z=0; typeof(\$("#Tname").find("option").eq(z).val()) != 'undefined'; z++) 
        {
           var name = \$("#Tname").find("option").eq(z).val();
           if (name != "port"+(i+1))
               \$("#port"+(i+1)).append("<option value=" + name + '>' + name + "</option>");
        }
        if(\$(this).val() == "None")
        {
            \$("#port"+(i+1)).attr("disabled",true);
            \$("#port"+(i+1)).empty();
            \$("#port"+(i+1)).append("<option value=None>None</option>");
            \$("#port"+(i+1)).trigger("change");
        }
    });
});

\$("#restart").change(function(event,i){
    \$("#Tname").empty();
    for (z=0; typeof(\$("#Mname").find("option").eq(z).val()) != 'undefined'; z++)
    {
        var name = \$("#Mname").find("option").eq(z).val();
        \$("#Tname").append("<option value=" + name + '>' + name + "</option>");
    }
    for (x=0; x < \$("#total").val(); x++)
    {
        var port = "#port" + (x+1);
        var mode = "#mode" + (x+1);
        if (\$(port).val() != "None")
        {
            \$("#Tname option[value=" + \$(port).val() + "]").remove();
            \$("#Tname option[value=port" + (x + 1) + "]").remove();
        }
        //if (i != x && "port" + (x+1) != \$("#port"+(i+1)).val() && \$("#port"+(i+1)).val() != "None") 
        if (i != x && "port" + (x+1) != \$("#port"+(i+1)).val())
        {
            \$("#port" + (x + 1) +" option[value=" + \$(this).val() + "]").remove();
            \$("#port" + (x + 1) +" option[value=port" + (i + 1) + "]").remove();
        }
        if (\$(port+" option").length == 0)
        {
            \$(port).append("<option value=None>None</option>");
            if (typeof(\$("#isp"+x).val()) != "undefined")
                \$("#mode"+(x+1)).attr("disabled",false);
            \$("#mode" + (x+1) + (x+1)).attr("checked",true);
        }
        if (\$(port).val() == "None" && \$(mode).val() != "None")
        {
             \$(port).empty();
             for (z=0; typeof(\$("#Tname").find("option").eq(z).val()) != 'undefined'; z++)
             {
                 var name = \$("#Tname").find("option").eq(z).val();
                 if (name != "port"+(x + 1))
                     \$(port).append("<option value=" + name + '>' + name + "</option>");
             }
         }
    } 
});

\$('select[id^="port"]').each(function(i){
    \$(this).change(function(){
        \$("#restart").trigger("change",i);
	var sel = \$(this).val();
	var re=/port/gi;
	var a = sel.replace(re,"");
	\$("#"+sel).empty();
	\$("#" + sel).attr("disabled",true);
	\$("#mode" + a).attr("disabled",true);
	\$("#mode" + a).attr("checked",true);
	\$("#"+sel).append("<option value=port" + (i+1) + '>port' + (i+1) + "</option>");
	\$("#restart").trigger("change",i);
	
    });
});
</script>

QB

