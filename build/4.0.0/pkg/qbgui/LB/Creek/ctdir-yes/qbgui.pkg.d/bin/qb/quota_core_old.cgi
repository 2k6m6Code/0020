#!/usr/bin/perl

use CGI;
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type:text/html\n\n";

my $ispref=XMLread($gPATH.'basic.xml');
my $quotaref=XMLread($gPATH.'quota.xml');
my $isplist=$ispref->{isp};
my $quotalist=$quotaref->{quota};
my $lineCount=0;
my @title=('Edit','Enable','Available','','MAX','Cycle','ISP ID','Interface','Name','Gateway','Syatem IP','Subnet');
my @week=("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css">);
print qq(<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css"/>);
print qq(<script type="text/javascript" src="jquery-1.9.1.min.js"></script>);
print qq(<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>);
print qq(<style type="text/css">);
print qq(button.menu{width:70;height:18;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;margin-right: 5px;});

print qq(body { font-size: 80%; });
print qq(label{ display:block; });
print qq(input.text { margin-bottom:12px; width:95%; padding: .4em; });
print qq(fieldset { padding:0; border:0; margin-top:25px; });
print qq(h1 { font-size: 1.2em; margin: .6em 0; });
print qq(th { width:100px; });
#print qq(td { text-align: center; });
print qq(div#users-contain { width: 350px; margin: 20px 0; });
print qq(div#users-contain table { margin: 1em 0; border-collapse: collapse; width: 100%; });
print qq(div#users-contain table td, div#users-contain table th { border: 1px solid #eee; padding: .6em 10px; text-align: left; });
print qq(.ui-dialog .ui-state-error { padding: .3em; });
print qq(.validateTips { border: 1px solid transparent; padding: 0.3em; });

print qq(</style></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<div class="divframe" align="center" id="main"><table width="80%" class="sortable" cellspacing="0" border="0">);
print qq(<tr><td class="bigtitle" colspan="12" align="left">Bandwidth Quota<hr size=1></td></tr><tr bgcolor="#332211"> );
foreach my $title (@title ){print qq(<td width="auto" align="center" style="white-space: nowrap;">$title);}
print qq(</td></tr>);
foreach my $isp(@$isplist)
{
    if( $isp->{iid} eq 'system' ) { next; }
    #if ( $isp->{isptype} eq "tunnel" || $isp->{isptype} eq "ipsec" || $isp->{isptype} eq "dtunnel" ) { next; }
    
    my $time = "--";
    my $cycle = "--";
    my $max = "--";
    my $min = "--";
    my $originalColor=my $bgcolor=($lineCount%2) ? ( '#334455' ) : ( '#556677' );
    print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor">);
    
    print qq (<td align="center" width="$titleWidth{Edit}" height="25">);
    print qq (<a name="ISP$lineCount">);
    print qq (<img src="image/edit.gif" title="Edit host properties" border="0"></a></td>);
    foreach my $quota (@$quotalist)
    {
        if ($quota->{gateway} eq "system" || $quota->{gateway} ne $isp->{gateway}){next;}
        if ($quota->{cycle} eq "1"){$cycle = "Daily";}
        if ($quota->{cycle} eq "7"){$cycle =  "Weekly";}
        if ($quota->{cycle} eq "30"){$cycle = "Monthly";}
        #if ($quota->{up})
        #{
        #    my ($num,$oo)=split(":",$quota->{up});
        #    if ($oo eq "1024"){$min = $num."KB";}
        #    if ($oo eq "1048576"){$min = $num."MB";}
        #    if ($oo eq "1073741824"){$min = $num."GB";}
        #    if ($oo eq "1099511627776"){$min = $num."TB";}
        #}
        if ($quota->{down})
        { 
            my ($num,$oo)=split(":",$quota->{down});
            if ($oo eq "1024"){$max = $num."KB";}
            if ($oo eq "1048576"){$max = $num."MB";}
            if ($oo eq "1073741824"){$max = $num."GB";}
            if ($oo eq "1099511627776"){$max = $num."TB";}
        }
        $time = $quota->{date};
        $now = $quota->{gateway};
        $enabled = $quota->{enabled};
    }
    
    print qq (<td align="center" width="50" height="25">);
    if ($enabled eq '1'){print qq (<input type="checkbox" id="enabled$lineCount" checked value="1"></td>);}
    if ($enabled eq '0'){print qq (<input type="checkbox" id="enabled$lineCount" value="0"></td>);}
    if ($enabled eq '') {print qq (<input type="checkbox" id="enabled$lineCount" checked value="1"></td>);}
            
    print qq (<td align="center" width="auto" height="25" class="$isp->{nic}" >--</td>);
    print qq (<td><a name="reset$lineCount"><img src="image/Reset.gif" title="Reset" border="0"></a></td>);
                    
    print qq (<td align="center" width="auto" height="25" class="down$lineCount" >$max</td>);
    
    print qq (<td align="center" width="auto" height="25" class="time$lineCount" >$time [$cycle]</td>);
    
    print qq (<td align="center" width="auto" height="25">ISP$isp->{iid}</td>);
    
    $PORT = $isp->{nic};
    if (grep(/eth/,$isp->{nic}))
    {
        my $linenum=$isp->{nic}; 
        $linenum=~s/eth//;
        my $PORT=( $linenum ne '-1' ) ? ( 'PORT '.++$linenum ) : ( 'None' );
    }
    print qq (<input id="port$lineCount" type="hidden" value="$isp->{nic}"/>);
    print qq (<td align="center" width="auto" height="25" >$PORT</td>);
    
    print qq (<td align="center" width="auto" height="25" >$isp->{ispname}</td>);
    
    print qq (<td align="center" width="auto" height="25">$isp->{gateway});
    print qq (<input type="hidden" id="gateway$lineCount" value="$isp->{gateway}" ></td>);
    
    print qq (<td align="center" width="auto" height="25" >$isp->{systemip}</td>);
    
    print qq (<td align="center" width="auto" height="25" >$isp->{subnet}</td>);
    
    print qq (</tr>);
    #---------------------------------------------------------------------------------
    # Edit quota
    #---------------------------------------------------------------------------------
    print qq (<tr id="ISP$lineCount" style="display:none">);
    print qq (<td colspan="5">Limit :);
    print qq (<input type="text" class="qbtext" id="dmit$lineCount" style="WIDTH:45px" maxlength="4" value=""/>);
    print qq (<select class="qbopt" id="dbps$lineCount" style="WIDTH:60px"><option value="0">None</option><option value="1024">KB</option>);
    print qq (<option value="1048576">MB</option><option value="1073741824">GB</option><option value="1099511627776">TB</option></select></td>);
    #print qq (<td colspan=2></td>);
    #print qq (<td colspan="2">Upload Limit :);
    #print qq (<input type="text" class="qbtext" id="umit$lineCount" style="WIDTH:45px" maxlength="4" value=""/>);
    #print qq (<select class="qbopt" id="ubps$lineCount" style="WIDTH:60px"><option value="0">None</option><option value="1024">KB</option>);
    #print qq (<option value="1048576">MB</option><option value="1073741824">GB</option><option value="1099511627776">TB</option></select></td>);
    #----------------------------------------------------------------------------------
    # Repeat time and cycle
    #----------------------------------------------------------------------------------
    print qq (<td colspan="5">Cycle : <select class="qbopt" id="hr$lineCount" style="WIDTH:40px">);
    foreach my $hr (0..23)
    {
        if($hr > 10){print qq(<option value="$hr">$hr</option>);}
        if($hr < 10){print qq(<option value="0$hr">0$hr</option>);}
    }
    print qq (</select>:<select class="qbopt" id="sec$lineCount" style="WIDTH:40px">);
    foreach my $sec (0..59)
    {
       if($sec > 10){print qq(<option value="$sec">$sec</option>);}
       if($sec < 10){print qq(<option value="0$sec">0$sec</option>);}
    }
    print qq (</select> Repeat :);
    print qq (<select class="qbopt" id="cycle$lineCount" style="WIDTH:70px"><option value="1">Daily</option>);
    print qq (<option value="7">Weekly</option><option value="30">Monthly</option></select></td>);
    #print qq (<td>ALert :<select id="alert$lineCount" class="qbopt"><option value="0">None</option>);
    #for(my $i = 10;$i <101; $i+=10)
    #{
    #    print qq (<option value="$i">$i%</option>); 
    #}
    #print qq (</select></td>);
    print qq (<td><input type="button" class="qb" id="save$lineCount" value="Save" style="width:100%"/></tr>);
    #--------------------------------------------------------------------------------------
    # Weekly Option
    #--------------------------------------------------------------------------------------
    print qq (<tr id="weekly$lineCount" name="hide" style="display:none"><td colspan="11">);
    my $x = 0;
    foreach my $day ( @week )
    {
        print qq (<input type="radio" name="week" id="selectDay$lineCount" value="$x" /> $day);
        $x++;
    }
    print qq (</td></tr>);
    
    #--------------------------------------------------------------------------------------
    # Monthly Option
    #--------------------------------------------------------------------------------------
    print qq (<tr id="monthly$lineCount" name="hide" style="display:none">);
    print qq (<td colspan="6"></td><td colspan="3">Number : <select class="qbopt" id="number$lineCount" style="WIDTH:40px">);
    foreach my $month (1..30)
    {
        if ($month < 10){print qq (<option value="$month">0$month</option>);}
        if ($month > 10){print qq (<option value="$month">$month</option>);}
    }
    print qq (</select></td></tr>); 
    
    print qq (<input type="hidden" id="data$lineCount" value=""/>);
    
    $lineCount++;
    
}

print qq(</table></div>);


print qq(<div id="new-data" title="Create new IP">);
print qq(<form><fieldset>);
print qq(<div id="radio">);
print qq(<label for="ip">IP</label><input type="radio" name="status" id="ip" value="0" checked="checked"/>);
print qq(<label for="sip">Subnet</label><input type="radio" name="status" id="sip" value="0"/>);
print qq(<label for="rip">IP-Range</label><input type="radio" name="status" id="rip" value="0"/>);
print qq(<label for="gip">IP-Group</label><input type="radio" name="status" id="gip" value="0"/>);
print qq(<label for="mac">Mac</label><input type="radio" name="status" id="mac" value="0"/>);
print qq(</div>);
print qq(<div id="input"></div>);
print qq(<label for="limit_text">Limit:</label><input type="text" id="limit_text" style="WIDTH:60px"/>);
print qq(<select class="qbopt" id="limit_bps" style="WIDTH:60px"><option value="0">None</option><option value="1024">KB</option>);
print qq(<option value="1048576">MB</option><option value="1073741824">GB</option><option value="1099511627776">TB</option></select>);
print qq(<label for="radio_plan">Repeat:</label>);
print qq(<div id="radio_plan">);
print qq(<label for="input_day">Daily</label><input type="radio" name="plan" id="input_day" value="0" checked="checked"/>);
print qq(<label for="input_week">Weekly</label><input type="radio" name="plan" id="input_week" value="0" />);
print qq(<label for="input_month">Monthly</label><input type="radio" name="plan" id="input_month" value="0" />);
print qq(</div>);
print qq(<select class="qbopt" id="input_hr" style="WIDTH:60px">);
foreach my $hr (0..23)
{
    if($hr > 10){print qq(<option value="$hr">$hr</option>);}
    if($hr < 10){print qq(<option value="0$hr">0$hr</option>);}
}
print qq (</select>:<select class="qbopt" id="sec" style="WIDTH:60px">);
foreach my $sec (0..59)
{
    if($sec > 10){print qq(<option value="$sec">$sec</option>);}
    if($sec < 10){print qq(<option value="0$sec">0$sec</option>);}
}
print qq(</select>);
print qq(<div id="plan_week" style="display:none" >);
my $x = 0;
foreach my $day ( @week )
{
    print qq (<input type="radio" name="week" id="week_$x" value="$x" /> $day);
    $x++;
}
print qq(</div>);
print qq(<div id="plan_monthy" style="display:none" >);
print qq(Month Day : <select class="qbopt" id="month_day" style="WIDTH:60px">);
foreach my $month (1..30)
{
    if ($month < 10){print qq (<option value="$month">0$month</option>);}
    if ($month > 10){print qq (<option value="$month">$month</option>);}
}
print qq(</select></div>);
print qq(</fieldset></form></div>);

print qq(<div align="center" width="75%">);
print qq(<div id="mainpage" class="ui-widget" >);
print qq(<h1>Other Quota</h1>);
print qq(<table id="table" class="ui-widget ui-widget-content" border="1" >);
print qq(<thead><tr class="ui-widget-header ">);
print qq(<th>Enable</th>);
print qq(<th>IP</th>);
print qq(<th>Available</th>);
print qq(<th>MAX</th>);
print qq(<th>Cycle</th>);
print qq(<th><img src="image/del.gif" title="Delete" border="0" onClick="del('all')"></th>);
print qq(</tr></thead>);
print qq(<tbody>);



print qq(</tbody></table></div>);
print qq(<button id="create-user">Create new IP</button>);
print qq(</body></html>);


print << "QB";

<script language="javascript">

jQuery( "#new-data" ).dialog({
   autoOpen: false,
   height: 500,
   width: 400,
   modal: true,
   buttons: 
   {
       "Create": function(){
           var bValid= true;
            
           
           if (bValid)
           {
               
               jQuery( this ).dialog( "close" );
           }
       },
       Cancel: function() 
       {
           jQuery( this ).dialog( "close" );
       }
   },
   close: function() 
   {
   }
});
jQuery( "#create-user" )
    .button()
    .click(function() 
    {
        jQuery( "#new-data" ).dialog( "open" );
        jQuery("input[id='ip']").click();
    });



jQuery("input[name^='status']").click(function(){

    if ( jQuery(this).attr("id") == "ip" )
    {
        jQuery("#input").html("<label for='input_ip'>IP:</label><input type='text' calss='text ui-widget-content ui-corner-all' id='input_ip' />");
    }else if ( jQuery(this).attr("id") == "sip" )
    {
        jQuery("#input").html("<label for='input_sip'>Subnet:</label><input type='text' calss='text ui-widget-content ui-corner-all' id='input_sip' />");
    }else if ( jQuery(this).attr("id") == "rip" )
    {
        jQuery("#input").html("<label for='input_rfip'>IP From:</label><input type='text' calss='text ui-widget-content ui-corner-all' id='input_rfip' /> \\
	<label for='input_rtip'>IP End:</label><input type='text' calss='text ui-widget-content ui-corner-all' id='input_rtip' />");
    }else if ( jQuery(this).attr("id") == "gip" )
    {
        jQuery("#input").html("<label for='input_gip'>IP Group:</label><textarea calss='text ui-widget-content ui-corner-all' id='input_gip' />");
    }else if ( jQuery(this).attr("id") == "mac" )
    {
        jQuery("#input").html("<label for='input_mac'>Mac:</label><input type='text' calss='text ui-widget-content ui-corner-all' id='input_mac' />");
    }
});

jQuery("input[name^='plan']").click(function(){
    if ( jQuery(this).attr("id") == "input_day" )
    {
        jQuery("#plan_week").attr("style","display:none");
        jQuery("#plan_monthy").attr("style","display:none");
    }else if ( jQuery(this).attr("id") == "input_week" )
    {
        jQuery("#plan_week").attr("style","display:block");
        jQuery("#plan_day").attr("style","display:none");
        jQuery("#plan_monthy").attr("style","display:none");
    }else if ( jQuery(this).attr("id") == "input_month" )
    {
        jQuery("#plan_monthy").attr("style","display:block");
        jQuery("#plan_day").attr("style","display:none");
        jQuery("#plan_week").attr("style","display:none");
    }
    

});

jQuery( "#radio" ).buttonset();

jQuery( "#radio_plan" ).buttonset();

\$(document).ready(function() {
    function reset(){
        var yy=new Array;
        \$.get("activequota.pl",function(da){
             yy=da.split(":");
             for(var i = 0 ;yy[i] != null;i++)
             {
                 var xx=new Array;
                 xx=yy[i].split(",");
                 for(var t=0;\$("#gateway" + t).val() != null;t++)
                 {
                     var asd = xx[0];
                     \$("." + asd).html(xx[1]);
                 }
             } 
        }); 
        setTimeout(reset, 1000);
    }
    reset();    
});

\$('select[id^="cycle"]').each(function(i){
    \$(this).change(function(){
        \$('tr[name^="hide"]').attr("style","display:none");
    	if (\$(this).val() == 30)
            \$("#monthly" + i).attr("style","display:block");
    	if (\$(this).val() == 7)
            \$("#weekly" + i).attr("style","display:block");
    });
});

\$('a[name^="ISP"]').each(function(x){
    \$(this).click(function(){
        if(\$("#ISP" + x).attr("style") == "DISPLAY: block")
        {
            \$('tr[id^="ISP"]').attr("style","display:none");
        }
        else
        {
            \$('tr[id^="ISP"]').attr("style","display:none");
            \$('tr[id^="weekly"]').attr("style","display:none");
            \$('tr[id^="monthly"]').attr("style","display:none");
            \$("#ISP" + x).attr("style","display:block");
        }
    });
});

\$('a[name^="reset"]').each(function(u){
    \$(this).click(function(){
        var link = \$("#gateway" + u).val();
        \$("#main").attr("disabled",true);
        \$.get("quotawork.pl",{action:"CREAT",LINK:link},function(check){
            if (check == '1')
                alert("Reset " + link + " OK!!");
            if (check == '0')
                alert("Reset " + link + " FAIL!!");
            \$("#main").attr("disabled",false);
        });
    });
});
\$('input[id^="enabled"]').each(function(p){
    \$(this).click(function(){
        var data;
        var link = \$("#gateway" + p).val() + "," + \$("#port" + p).val();
        if (\$(this).val() == 0)
        {
            \$(this).val('1');
            data='1';
        }
        else
        {
            \$(this).val('0');
            data='0';
        }
        \$(this).attr("disabled",true);
        \$.get("quotawork.pl",{action:"ENABLED",LINK:data,CHECK:link},function(f){
            if (f == '1')
                alert("ENABLE SUCCESS!! ");
            if (f == '0')
                alert("DISENABLE SUCCESS!! ");
	   \$(this).attr("disabled",false);
        });
    });
});

\$('input[id^="save"]').each(function(y){
    \$(this).click(function(){
        var down = (\$("#dmit" + y).val() + ":" + \$("#dbps" + y).val());
        //var up = (\$("#umit" + y).val() + ":" + \$("#ubps" + y).val());
        var up = "1";
        var hr = (\$("#hr" + y).val() + ":" + \$("#sec" + y).val());
        var gateway = \$("#gateway" + y).val();
        var port = \$("#port" + y).val();
        var alerttime = \$("#alert" + y).val();
        var enabled = \$("#enabled" + y).val();;
        var cycle = \$("#cycle" + y).val();
        var weekly = \$('input[name^="week"]:checked').val();
        var monthly = \$("#number" + y).val();
        var data = "";
        var chose = "";
        var tmp = new Array;
        //var RightNow = new Date();
        var ddown = \$("#dmit" + y).val() + \$("#dbps" + y + " option:selected").html();
        var ttime = hr + "[" + \$("#cycle" + y + " option:selected").html() + "]";
        tmp = gateway.split(".");
        var gateway_16 = "";
        for (var z = 0; z < 4;z++)
        {
            if (parseInt(tmp[z],10) > 16)
                gateway_16+=parseInt(tmp[z],10).toString(16);
            if (parseInt(tmp[z],10) < 16)
                gateway_16+= "0" + parseInt(tmp[z],10).toString(16);
        }
        if (down == 0 || up == 0)
        {
            alert("Please enter your limit!!");
            return;
        }
        if (cycle == 7 && !weekly)
        {
            alert("Please enter your days!!");
            return;
        }
        
        /*
        var da = RightNow.getDate().toString();    
        if (cycle == 1)
        {
            da++;
            if (RightNow.getDate() < 10 )
                da = "0"+da;
        }
        
        var month = (RightNow.getMonth()+1).toString();
        if (cycle == 30)
        {
            if ((RightNow.getMonth()+2) < 10 )
                month = "0" + (RightNow.getMonth()+2).toString();
            var date = RightNow.getFullYear().toString() + month + monthly + " " + hr;
        }
        else
        {
            var date = RightNow.getFullYear().toString() + month + da + " " + hr;
        }
        */
        
        var date = hr;
        
        \$("#ISP" + y).attr("disabled",true);
        
        if (cycle == 7) 
            chose = weekly;
        
        if (cycle == 30)
        {
            chose = monthly;
            chose--;
        }
            
        data = gateway + "," + port + "," + down + "," + up + "," + date + "," + cycle + "," + alerttime + "," + gateway_16 + "," + chose + "," + enabled;
            
        \$("#data" + y).val(data);
        
        submit(data,y,ddown,ttime,gateway);
    });
});
 
function submit(data,y,ddown,ttime,gateway)
{        
    \$.get("quotawork.pl",{action:"SAVE",DATA:data},function(aa){
        if(aa == '1')
        {
 	    alert("SAVE " + gateway + " Success!!");
 	    \$(".down"+y).html(ddown);
 	    \$(".time"+y).html(ttime);
 	}
        else
            alert("SAVE " + gateway + " FAIL!!");
        \$("#ISP" + y).attr("disabled",false);
        \$("#ISP" + y).attr("style","display:none");
        \$("#weekly" + y).attr("style","display:none");
        \$("#monthly" + y).attr("style","display:none");
    });
}

</script>    
QB
