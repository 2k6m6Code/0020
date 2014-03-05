#!/usr/bin/perl 

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

print "Content-type:text/html\n\n";

use CGI;
use Data::Dumper;
require ("/usr/local/apache/qb/qbmod.cgi");
my $cgi = new CGI;
my $view = $cgi->param("view");
my $data = $cgi->param("data");
my $tmp = $cgi->param("type");
my $FILETEST ="/usr/local/apache/qbconf/";

if ($view eq 'save')
{
    $data=~s/\s//g;
    my $dqos=XMLread('/usr/local/apache/qbconf/dqos.xml');
    my $hostList=$dqos->{dos};
    ($type,$list)=split(/=/,$tmp);
    
        
    if ( -e $FILETEST."dqos.sh" && $type eq 'COD')
    {
        my $file =  XMLread($FILETEST."dqos.xml");
        my $fileref = $file->{connlimit}->[0];
        if ($fileref->{exception} ne "")
        {
            my %newHost;
            $newHost{match}='ip='.$fileref->{above};
            $newHost{ip} = $fileref->{exception};
            $newHost{log}=$fileref->{logprefix};
            $newHost{time}=$fileref->{lograte};
            $newHost{type}='COD';
            push( @newhostlist, \%newHost);
        }
    }
    @datafile=split(/A/,$data);
    @listref=split(/,/,$list);
    foreach my $host ( @$hostList )
    {
        if ( $host->{type} ne $type )
        {
            my %hostTemplate;
            %hostTemplate=%$host;
            push(@newhostlist, \%hostTemplate);
        }
    }
    my %newHost;
    @data1=split(/,/,$data);
    $newHost{type}=$type;
    $newHost{ip}=$data1[0];
    $newHost{time}=$data1[1];
    $newHost{log}=$data1[2];
    if ($data1[3] =~ m/syn/ )
    {
       my ($icmp,$syn)=split (/:/,$data1[3]);
       $icmp =~ s/icmp=//g;
       $syn =~ s/syn=//g;
       $newHost{syn}=$syn;
       $newHost{icmp}=$icmp;
    }
    else
    {
        $newHost{match}=$data1[3];
    }
    push( @newhostlist, \%newHost); 
    foreach my $bb ( @listref )
    {
        
        my %newlist;
        if( $bb eq "" ){next;}
        $newlist{list}=$bb;
        push( @newlist, \%newlist);
    } 
    $targetdomain->{dos}=\@newhostlist;
    $targetdomain->{list}=\@newlist;
   
    XMLwrite($targetdomain, '/usr/local/apache/qbconf/dqos.xml');
    makeshell();
}elsif ($view ne "")
{
    my $dosref = XMLread('/usr/local/apache/qbconf/dqos.xml');
    my $ddos = $dosref->{dos};
    my $doslist = $dosref->{list};
    if ($view eq 'ICMP')
    {
    	$title = 'Flood';
    	$checked = 'checked';
    	$check = '';
    	$matchable = '';
    	$synck='';
    	$icmpck='';
    	$enabled='disabled';
    	$synenabled='disabled';
    	$icmpenabled='disabled';
    	$synvalue='1000';
    	$icmpvalue='1000';
    	$value = 'icmp_flood:';
    	$olddata = "icmp=1000:syn=1000";
    	foreach my $list (@$ddos)
    	{
    	    if ($list->{type} ne 'ICMP'){next;}
    	    if ($list->{log} ne '')
    	    {
    	        $check = 'checked';
    	        $checked = '';
    	        $enabled='';
    	        $value = $list->{log};
    	    }
    	    if ($list->{syn} ne '' || $list->{icmp} ne '')
    	    {
    	        $matchable='checked';
    	        if ($list->{syn} ne ''){$synck='checked';$synenabled='';$synvalue=$list->{syn};}
    	        if ($list->{icmp} ne ''){$icmpck='checked';$icmpenabled='';$icmpvalue=$list->{icmp};}
    	    }
    	    $olddata='icmp='.$list->{icmp}.':syn='.$list->{syn};
    	}
        $hiddenobj = '<input type="hidden" id="max" value=$olddata>';	            
    }
    if ($view eq 'SYN')
    {
        $title = 'SYN flood';
        $value = 'syn_flood:';
        $another = '<a>Can not go over :</a><input type="text" class="qbtext" id="max" value="1000" style="width:60" disabled="true"><a>Package per Sec.</a></td>';
    }
    if ($view eq 'LDOS')
    {
        $title = 'Low-rate DoS attacks';
        $value = 'Low_rate_DoS:';
        $match = 'Enable';
        $hiddenobj = '<input type="hidden" id="max" value="">';
    }
    if ($view eq 'COD')
    {
        $checked = 'checked';
        $check = '';
        $enabled='disabled';
        $value = 'cod:connectionoverflow';
        $maenabled='disabled';
        $ipable='disabled';
        $portable='disabled';
        $ipnum="50";
        $portnum="50";
        $portnn="80";
        $matchable='';
        $olddata="ip=50:port=50"; 
        foreach my $list (@$ddos)
        {
            if ($list->{type} ne 'COD'){next;}
            if ($list->{log} ne '')
            {
                $check = 'checked';
                $checked = '';
                $enabled='';
                $value = $list->{log};
            }
            if ($list->{match} ne '')
            {
                $maenabled='';   
                $matchable='checked';
           	my ($ip,$port,$portlimit)=split(/:/,$list->{match});
           	$ip =~ s/ip=//g;
           	$port =~ s/port=//g;
           	if ($ip ne ''){$ipable=''; $ipnum=$ip;$ipable='checked';}
           	if ($port ne '')
           	{
           	    $portable='';
           	    $portnum=$port;
           	    $portnn=$portlimit;
           	    $portable='checked';
           	}
            }
            $olddata = $list->{match};
        }
        $title = 'Connection Overflow';
        $hiddenobj = '<input type="hidden" value=$olddata id="max">';
    }
    if ($view eq 'PSD')
    {
        $checked = 'checked';
        $check = '';
        $value = 'psd:';
        $enabled='disabled';
        $maable='disabled';
        $a="21";
        $aa="1";
        $aaa="3";
        $aaaa="5";
        $olddata="21:1:3:5";            
        foreach my $list (@$ddos)
        {
            if ($list->{type} ne 'PSD' ){next;}
            if($list->{log} ne '')
            {
                $check = 'checked';
                $checked = '';
                $enabled='';
                $value = $list->{log};
            }
            if($list->{match} ne '') 
            {
                $matchable='checked';
                $maable='';
                ($a,$aa,$aaa,$aaaa)=split(/:/,$list->{match});
            }   
            $olddata = $list->{match}; 
        }
        $title = 'Port Scan';
        $hiddenobj = '<input type="hidden" value=$olddata id="max">';
         
    }
    print qq (<tr hight="10%"><td colspan=5><font class="bigtitle" align="center" >$title<font><hr size=1></td></tr>);
    print qq (<tr><td rowspan=1 width="20%" valign="top"><input type="checkbox" id="matchenable" onclick="Statu();" $matchable><a>Enable</a><p></td>);
#    if ($view eq 'PSD')
#    {
       # print qq (<a style="width:120">Weight Threshold</a> : <input type="text" id="wt" style="width:20%" class="qbtext" value=$a $maable onchange="\$('#max').val(\$('#hw').val() + ':' + \$('#hw').val() + ':' + \$('#lw').val() + ':' + \$('#dt').val());"><br>);
       # print qq (<a style="width:120">High Port Weight</a> : <input type="text" id="hw" style="width:20%" class="qbtext" value=$aa  $maable onchange="\$('#max').val(\$('#wt').val() + ':' + \$('#hw').val() + ':' + \$('#lw').val() + ':' + \$('#dt').val());"><br>);
       # print qq (<a style="width:120">Low Port Weight</a>  : <input type="text" id="lw" style="width:20%" class="qbtext" value=$aaa  $maable onchange="\$('#max').val(\$('#hw').val() + ':' + \$('#hw').val() + ':' + \$('#lw').val() + ':' + \$('#dt').val());"><br>);
       # print qq (<a style="width:120">Delay Thershold</a>  : <input type="text" id="dt" style="width:20%" class="qbtext" value=$aaaa  $maable onchange="\$('#max').val(\$('#hw').val() + ':' + \$('#hw').val() + ':' + \$('#lw').val() + ':' + \$('#dt').val());">Sec.<p>);
#    }
#    if ($view eq 'COD')
#    {
#        print qq (<input type="checkbox" id="ipck" $maenabled onclick="COD(ipck,ipnum);" $ipable><a>Can not go over :</a><br><input type="text" class="qbtext" id="ipnum" value=$ipnum style="width:25%" $ipable onchange=" \$('#max').val('ip=' + \$('#ipnum').val() +':port=' + \$('#portnum').val() + ':' + \$('#port').val());"><a>Connections per IP</a><p>);
#        print qq (<input type="checkbox" id="portck" $maenabled onclick="COD(portck,portnum,port);" $portable><a>Can not go over :</a><br>);
#        print qq (<a>Port Number :</a><input type="text" class="qbtext" id="port" $portable  style="width:50" value=$portnn onchange=" \$('#max').val('ip=' + \$('#ipnum').val() +':port=' + \$('#portnum').val() + ':' + \$('#port').val());"><br>);
#        print qq (<input type="text" class="qbtext" id="portnum" value=$portnum style="width:20%" $portable onchange=" \$('#max').val('ip=' + \$('#ipnum').val() +':port=' + \$('#portnum').val() + ':' + \$('#port').val());"><a>Connections per PORT</a></td>);
#    }
#    if ($view eq 'LDOS')
#    {
#        print qq (<a>RTO:</a><input type="radio" name="chs" id="r1" onclick="\$('#max').val('1');\$('#num').attr('disabled',true);" disabled="true" checked>Auto<input name="chs" type="radio" id="r2" disabled="true" onclick="\$('#num').attr('disabled',false);"><input type="text" class="qbtext" id="num" value="1" style="width:30" onchange="\$('#max').val(this.value)" disabled="true">Sec.</td>);
#    }
#    if ($view eq 'ICMP')
#    {
#        print qq(<input type="checkbox" id="icmp" onclick="COD(icmp,icmpbox);" $icmpck ><a>ICMP:</a><br><input type="text" class="qbtext" id="icmpbox" value=$icmpvalue style="width:60" $synenabled onchange="\$('#max').val('icmp=' + \$('#icmpbox').val() + ':' + 'syn=' + \$('#synbox').val());"><a>Package per Sec.</a><p>);
#	print qq(<input type="checkbox" id="syn"  onclick="COD(icmp,synbox);" $synck><a>SYN :</a><br><input type="text" class="qbtext" id="synbox" value=$synvalue style="width:60" $icmpenabled  onchange= "\$('#max').val('icmp=' + \$('#icmpbox').val() + ':' +'syn=' + \$('#synbox').val());"><a>Package per Sec.</a></td>);
#    }         
    print qq ($another);
    print qq (<td rowspan=1 width="20%" valign="top"><a>Log Rate:</a><br></td>);
    #print qq (<input type="checkbox" id="logset" onclick="Status()" $check >Enable<p>);
    #print qq (<a>Save per.</a><input type="text" class="qbtext" id="timenumber" style="width:50" value="1" $enabled> / <select id="time" class="qbopt" $enabled>><option value="h">Hours<option value="m" selected>Minute<option value="s">Second</select><p>);
    #print qq (<a>Log Prefix :</a><br><input type="text" class="qbtext" id="logprefix" style="width:60%" value=$value $enabled></td>);
    print qq (<td width="20%"><a style="margin-left:45px;">Select IP from:</a></td>);
    print qq (<td width="2%"></td>);
    print qq (<td width="20%" align="center"><a>Privileged List</a></td>);
    print qq (<td width="9%"></td></tr>);
    print qq (<td valign="top">);
    if ($view eq 'PSD')
    {
        print qq (<a style="width:120">Weight Threshold</a> : <input type="text" id="wt" style="width:20%" class="qbtext" value=$a $maable onchange="\$('#max').val(\$('#hw').val() + ':' + \$('#hw').val() + ':' + \$('#lw').val() + ':' + \$('#dt').val());"><br>);
        print qq (<a style="width:120">High Port Weight</a> : <input type="text" id="hw" style="width:20%" class="qbtext" value=$aa  $maable onchange="\$('#max').val(\$('#wt').val() + ':' + \$('#hw').val() + ':' + \$('#lw').val() + ':' + \$('#dt').val());"><br>);
        print qq (<a style="width:120">Low Port Weight</a>  : <input type="text" id="lw" style="width:20%" class="qbtext" value=$aaa  $maable onchange="\$('#max').val(\$('#hw').val() + ':' + \$('#hw').val() + ':' + \$('#lw').val() + ':' + \$('#dt').val());"><br>);
        print qq (<a style="width:120">Delay Thershold</a>  : <input type="text" id="dt" style="width:20%" class="qbtext" value=$aaaa  $maable onchange="\$('#max').val(\$('#hw').val() + ':' + \$('#hw').val() + ':' + \$('#lw').val() + ':' + \$('#dt').val());">Sec.<p>);
    } 
    if ($view eq 'COD')
    {
        print qq (<input type="checkbox" id="ipck" $maenabled onclick="COD(ipck,ipnum);" $ipable><a>Limit</a><input type="text" class="qbtext" id="ipnum" value=$ipnum style="width:25%" $ipable onchange=" \$('#max').val('ip=' + \$('#ipnum').val() +':port=' + \$('#portnum').val() + ':' + \$('#port').val());"><a>Connections per IP</a><p>);
        print qq (<input type="checkbox" id="portck" $maenabled onclick="COD(portck,portnum,port);" $portable><a>Limit</a>);
#        print qq (<input type="text" class="qbtext" id="port" $portable  style="width:50" value=$portnn onchange="\$('#max').val('ip=' + \$('#ipnum').val() +':port=' + \$('#portnum').val() + ':' + \$('#port').val());"><br>);
        print qq (<input type="text" class="qbtext" id="portnum" value=$portnum style="width:10%" $portable onchange=" \$('#max').val('ip=' + \$('#ipnum').val() +':port=' + \$('#portnum').val() + ':' + \$('#port').val());"><a>Connections for Port</a><input type="text" class="qbtext" id="port" $portable  style="width:15%" value=$portnn onchange="\$('#max').val('ip=' + \$('#ipnum').val() +':port=' + \$('#portnum').val() + ':' + \$('#port').val());"></td>);
    }   
    if ($view eq 'LDOS')
    {
        print qq (<a>RTO:</a><input type="radio" name="chs" id="r1" onclick="\$('#max').val('1');\$('#num').attr('disabled',true);" disabled="true" checked>Auto<input name="chs" type="radio" id="r2" disabled="true" onclick="\$('#num').attr('disabled',false);"><input type="text" class="qbtext" id="num" value="1" style="width:30" onchange="\$('#max').val(this.value)" disabled="true">Sec.</td>);
    }
    if ($view eq 'ICMP')
    {
        print qq(<input type="checkbox" id="icmp" onclick="COD(icmp,icmpbox);" $icmpck $icmpenabled><a>Drop When ICMP</a><br><a>Exceeds </a><input type="text" class="qbtext" id="icmpbox" value=$icmpvalue style="width:60" $synenabled onchange="\$('#max').val('icmp=' + \$('#icmpbox').val() + ':' + 'syn=' + \$('#synbox').val());"><a>Packets per Sec.</a><p>);
        print qq(<input type="checkbox" id="syn"  onclick="COD(icmp,synbox);" $synck $synenabled><a>Drop When SYN</a><br><a>Exceeds </a><input type="text" class="qbtext" id="synbox" value=$synvalue style="width:60" $icmpenabled  onchange= "\$('#max').val('icmp=' + \$('#icmpbox').val() + ':' +'syn=' + \$('#synbox').val());"><a>Packets per Sec.</a></td>);
    }
    print qq ($another);
    print qq (</td>);
    print qq (<td valign="top"><input type="checkbox" id="logset" onclick="Status()" $check >Enable<p><a>Save per.</a><input type="text" class="qbtext" id="timenumber" style="width:50" value="1" $enabled> / <select id="time" class="qbopt" $enabled>><option value="h">Hours<option value="m" selected>Minute<option value="s">Second</select><p><a>Log Prefix :</a><br><input type="text" class="qbtext" id="logprefix" style="width:60%" value=$value $enabled></td>);
    print qq (<td valign="top" align="center" rowspan=1><select type="exception" id="list" class="qbopt" multiple="true" size="20" style="width:170">);
    my $ispref = XMLread('/usr/local/apache/qbconf/zonecfg.xml');
    my $isplist = $ispref->{nat};
    foreach my $list (@$isplist)
    {
        if ($list->{network} eq ''){next;}
        foreach my $listiref (@$doslist)
        {
            if ($list->{network} eq $listiref->{list}){$prt = "1";}   
        }
        if ($prt ne '1'){print qq(<option value=$list->{network}>$list->{network});}
    }
    foreach my $list (@$doslist)
    {
	if ( $list->{list} eq "system" ) { next; }
        print qq(<option value=$list->{list}>$list->{list});
    }
    print qq (</select></td>);
    
    print qq (<td rowspan=1><input type="button" class="qbtext" id="add" value=">>" onclick="inser('enablelist','list','1');"><br>);
    print qq (<input type="button" class="qbtext" id="del" value="<<" onclick="inser('list','enablelist');"></td>);
    
    print qq (<td align="center" rowspan=3 valign="top"><select type="exception" id="enablelist" name="test" class="qbopt" multiple="true" size="20" style="width:170">);
    foreach my $list (@$ddos)
    {
        if( $list->{type} ne $view ){next;}
        $show=$list->{ip};
        @ipref=split(/:/,$show);
        foreach my $ip (@ipref){print qq(<option value=$ip>$ip);}
    } 
    print qq (</select></td></tr>);
    print qq (<tr><td colspan=2 rowspan=6>);
    if ($view eq 'PSD')
    {
        print qq (<div style="position:absolute;left:60px;top:220px;width:45%;height:auto;">);
        print qq (<blockquote style="color:#000000;font-size:13px;background-color:#ffffcc;margin-left:0px;margin-right:0px;-webkit-box-shadow:#333333 4px 4px 6px;padding:0px;border:1px dashed #aabbcc;" >);
        print qq (Weight Threshold :<br>The number of packets with different ports is allowed to send out from a single host.);
        print qq (</blockquote>);
        print qq (<blockquote style="color:#000000;font-size:13px;background-color:#ffffcc;margin-left:0px;margin-right:0px;-webkit-box-shadow:#333333 4px 4px 6px;padding:0px;border:1px dashed #aabbcc;">);
        print qq (High Port Weight :<br>Set to limit the number of that a single host is allowed to run port scan from ports 1025 to 65536.);
        print qq (</blockquote>);
        print qq (<blockquote style="color:#000000;font-size:13px;background-color:#ffffcc;margin-left:0px;margin-right:0px;-webkit-box-shadow:#333333 4px 4px 6px;padding:0px;border:1px dashed #aabbcc;">);
        print qq (Low Port Weight :<br>Set to limit the number of that a single host is allowed to run port scan from ports 0 to 1024.);
        print qq (</blockquote>);
        print qq (<blockquote style="color:#000000;font-size:13px;background-color:#ffffcc;margin-left:0px;margin-right:0px;-webkit-box-shadow:#333333 4px 4px 6px;padding:0px;border:1px dashed #aabbcc;">);
        print qq (Delay Thershold :<br>Set the time interval to allow running port scan on a single host.);
        print qq (</blockquote></div>);  
    }          
    print qq (</td>);
    print qq (<td align="center" valign="top"><input type="button" class="qbtext" id="DEL" value="DEL" onclick="DEL('list');" style="width:170"><br>);
    print qq (<a style="margin-left:0px;">Type in IP :</a><br><input type="text" class="qbtext" id="addlist" value="" style="width:170" maxlength="15"></td>);
    print qq (<td  valign="top"><br><br><input type="button" class="qbtext" id="ADD" onclick="ADD();" value=">>" ></td></tr>);
#    print qq (<tr><td ><a style="margin-left:45px;">Type in IP :</a></td>);
#    print qq (<tr><td align="center"><input type="text" class="qbtext" id="addlist" value="" style="width:170" maxlength="15"></td>);
#    print qq (<td><input type="button" class="qbtext" id="ADD" onclick="ADD();" value=">>" ></td></tr>);
    print qq (<tr><td colspan=3 align="right" ><input type="button" class="qbtext" id="SAVE" value="SAVE" style="width:170;margin-right:35px;" onclick="SAVE('$view');"></td></tr>);
    print qq ($hiddenobj);    
     
}    
    
sub makeshell    
{
    my $DQOSSHELL="/usr/local/apache/qbconf/dqos.sh";
    my $IPTCMD="/usr/local/sbin/iptables -t mangle";
    my $SHELLHEAD="#!/bin/sh ";
    my $LOGLEVEL="--log-level alert ";
    my $LIMITBURST=5;
    
    open(DQOS, ">$DQOSSHELL");
                
    my $dqos=XMLread('/usr/local/apache/qbconf/dqos.xml');

    print DQOS qq ($SHELLHEAD \n\n);

    my $dosref=$dqos->{dos};
    
    print DQOS qq ($IPTCMD -X DEF \n);
    print DQOS qq ($IPTCMD -N DEF \n);
    
    print DQOS qq ($IPTCMD -X COD \n);
    print DQOS qq ($IPTCMD -N COD \n);                
    
    print DQOS qq ($IPTCMD -X PSD \n);
    print DQOS qq ($IPTCMD -N PSD \n);
        
    print DQOS qq ($IPTCMD -X ICMP \n);
    print DQOS qq ($IPTCMD -N ICMP \n);
        
    foreach my $dos (@$dosref)
    {
       
        my $CMD=$IPTCMD." -A ".$dos->{type};
        my $LOGPREFIX=( $dos->{log} ) ? ( qq(--log-prefix $dos->{log}) ) : ('');
        
        if ($dos->{type} eq 'COD')
        {
            ($ipref,$portref,$portlimit)=split(/:/,$dos->{match});
            $ipref =~ s/ip=//;
            $portref =~ s/port=//;
            
            print DQOS qq($CMD -p tcp --syn -m connlimit --connlimit-above 50 -m limit -j LOG $LOGLEVEL --log-prefix cod:connectionoverflow \n);
            if ( !$dos->{match} ) { print DQOS qq($CMD -j ICMP \n\n); }
            else
            {
                my @avoidlist=split(/:/, $dos->{ip});
                foreach my $avoid ( @avoidlist )
                {
            	    print DQOS qq($CMD -s $avoid -j PSD \n);
             	    print DQOS qq($CMD -d $avoid -j PSD \n);
                }
                if($portlimit)
                {
                    print DQOS qq($CMD -p tcp --syn --dport $portlimit -m connlimit --connlimit-above $portref -m limit --limit $dos->{time} --limit-burst $LIMITBURST -j LOG --log-level alert  $LOGPREFIX \n);     
                }
                if ( $dos->{log} ) { print DQOS qq($CMD -p tcp --syn -m connlimit --connlimit-above $ipref -m limit --limit $dos->{time} --limit-burst $LIMITBURST -j LOG --log-level alert $LOGPREFIX \n); }
                print DQOS qq($CMD -p tcp --syn -m connlimit  --connlimit-above $ipref -j DROP \n);
                print DQOS qq($CMD -j PSD \n\n);
            }
        }
        if ($dos->{type} eq 'PSD')
        {
    	    print DQOS qq($CMD -m psd --psd-weight-threshold 21 --psd-delay-threshold 5 --psd-lo-ports-weight 3 --psd-hi-ports-weight 1 -m limit --limit 1/m --limit-burst $LIMITBURST -j LOG --log-level alert --log-prefix psd: \n); 
    	    if ( !$dos->{match} ) { print DQOS qq($CMD  -j DEF \n\n); }
    	    else
    	    {
    	        my @avoidlist=split(/:/, $dos->{ip});
    	        foreach my $avoid ( @avoidlist )
    	        {
    	            print DQOS qq($CMD -s $avoid -j ICMP \n);
    	            print DQOS qq($CMD -d $avoid -j ICMP \n);
    	        }
    	        if ( $dos->{log} )
    	        {
    	            @opt = split(/:/,$dos->{match});
    	            print DQOS qq($CMD -m psd --psd-weight-threshold $opt[0] --psd-delay-threshold $opt[3] );
    	            print DQOS qq(--psd-lo-ports-weight $opt[2] --psd-hi-ports-weight $opt[1] );
    	            print DQOS qq(-m limit --limit $dos->{time} --limit-burst $LIMITBURST -j LOG --log-level alert $LOGPREFIX \n);
    	        }
    	        print DQOS qq($CMD -m psd --psd-weight-threshold $opt[0] --psd-delay-threshold $opt[3] );
    	        print DQOS qq(--psd-lo-ports-weight $opt[2] --psd-hi-ports-weight $opt[1] -j DROP \n);
    	        print DQOS qq($CMD  -j ICMP \n\n);
    	    }        
        }
        if ($dos->{type} eq 'ICMP')
        {
            print DQOS qq($CMD -p icmp --icmp-type echo-request -m limit --limit 50/s -j LOG $LOGLEVE --log-prefix icmp_flood:\n);
            if ( !$dos->{syn} || !$dos->{icmp}) { print DQOS qq($CMD  -j DEF \n\n); }
            else
            {
                my @avoidlist=split(/:/, $dos->{ip});
                foreach my $avoid ( @avoidlist )
                {
                    print DQOS qq($CMD -s  $avoid -j DEF \n);
                    print DQOS qq($CMD -d  $avoid -j DEF \n);
                }
                if ( $dos->{icmp} )
                {
                    print DQOS qq($CMD -p icmp --icmp-type echo-request -m limit --limit $dos->{icmp}/s --limit-burst $LIMITBURST -j ACCEPT\n);
                    print DQOS qq($CMD -p icmp --icmp-type echo-request -m limit --limit $dos->{icmp}/s --limit-burst $LIMITBURST -j LOG --log-level alert $LOGPREFIX\n);
                    print DQOS qq($CMD -p icmp --icmp-type echo-request -j DROP \n);
                }
                if ( $dos->{syn} )
                {
                    print DQOS qq($CMD -p tcp -m state --state ESTABLISHED,RELATED -j ACCEPT \n);
                    print DQOS qq($CMD -p tcp --syn -m limit --limit $dos->{syn}/s --limit-burst $LIMITBURST -j ACCEPT\n);
                    print DQOS qq($CMD -p tcp --syn -m limit --limit $dos->{syn}/s --limit-burst $LIMITBURST -j LOG --log-level alert $LOGPREFIX\n);
                    print DQOS qq($CMD -p tcp -j DROP\n);
                     
                }
                    
             print DQOS qq($CMD  -j DEF \n); 
             print DQOS qq($CMD  -j DROP \n\n);
             }
        }
    }
    
    print DQOS qq ($IPTCMD -A DEF -j ACCEPT \n\n);
    
    print DQOS qq ($IPTCMD -A INPUT -p icmp -j ICMP \n\n);
    
    print DQOS qq ($IPTCMD -A INPUT -p tcp -j COD \n\n);
}
