#!/usr/bin/perl

use CGI;
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type:text/html\n\n";

#my $ispref=XMLread($gPATH.'basic.xml');
#my $quotaref=XMLread($gPATH.'quota.xml');
#my $isplist=$ispref->{isp};
#my $quotalist=$quotaref->{quota};

my @week=("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
print qq(<html><head>);
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

print qq(<div id="new-data" title="Create new IP">);
print qq(<form><fieldset>);
print qq(<label for="host">Host:</label>);
print qq(<select id="host" >);
my $hostref=XMLread($gPATH.'host.xml');
my $hostlist=$hostref->{host};
foreach my $host (@$hostlist)
{
    $host->{hostname}=~ s/host-//g;
    print qq(<option value="$host->{hostaddress}">$host->{hostname}</option>);
}
print qq(</select>);
print qq(<label for="limit_down">Download:</label>);
print qq(<input type="text" id="limit_down" style="WIDTH:60px"/>);
print qq(<select class="qbopt" id="down_bps" style="WIDTH:60px"><option value="1024">KB</option>);
print qq(<option value="1048576">MB</option><option value="1073741824">GB</option><option value="1099511627776">TB</option></select>);

print qq(<label for="limit_upload">Upload:</label>);
print qq(<input type="text" id="limit_upload" style="WIDTH:60px"/>);
print qq(<select class="qbopt" id="upload_bps" style="WIDTH:60px"><option value="1024">KB</option>);
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
    print qq (<input type="checkbox" name="week" id="week_$x" value="$x" /> $day);
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

print qq(<div id="openpage" align="center" width="75%" style="display:none">);
print qq(<div id="mainpage" class="ui-widget" >);
print qq(<h1>Bandwith Quota</h1>);
print qq(<table id="table" class="ui-widget ui-widget-content" border="1" >);
print qq(<thead><tr class="ui-widget-header ">);
print qq(<th>Enable</th>);
print qq(<th>Type</th>);
print qq(<th>MAX</th>);
print qq(<th>Cycle</th>);
print qq(<th><img src="image/del.gif" title="Delete" border="0" onClick="del('all')"></th>);
print qq(</tr></thead>);
print qq(<tbody>);
print qq(</tbody></table></div>);

print qq(<div id="dialog-confirm" title="" >);
print qq(<p>Are you sure want to delete ??</p>);
print qq(</div>);

print qq(<button id="create-user">Create new IP</button>);

print << "QB";

<script language="javascript">

var dvalue;
var avalue;
var data='';
var enabled='';
var ajax_check;

function check(o, regexp)
{
    var reg = new RegExp(regexp);
    var arr = reg.exec(o);
    if ( !( regexp.test( o ) ) )
        return false;
    else
        return true;
}

function alter(a)
{
    var fa=jQuery(a).parent("tr");
    var ip=jQuery(fa).find("td").eq(1).text();
    enabled=jQuery(fa).find("input").eq(1).val();
    var max=jQuery(fa).find("input").eq(1).val();
    var cycle=jQuery(fa).find("input").eq(2).val();
    avalue=jQuery(fa).find("input").eq(3).val();
    var tmp = new Array;
    tmp = ip.split(/-/);
    data = "{ip:"+ ip + "}=";
    if ( tmp.length == 1 && tmp != null)
    {
        if (check( tmp,/^([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})\$/))
        {    
           jQuery("input[id='ip']").click();
            jQuery("#input_ip").val(tmp);
        }else if (check( tmp, /^([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})\\/([\\d]{1,2})\$/))
        {
            jQuery("input[id='sip']").click();
            jQuery("#input_sip").val(tmp);
        }else if (check( tmp,/^([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2})\$/i ))
        {
            jQuery("input[id='mac']").click();
            jQuery("#input_mac").val(tmp);
            
        }else
        {
            tmp = ip.split(/~/);
            if (tmp.length == 2)
            {
                jQuery("input[id='rip']").click();
                jQuery("#input_rfip").val(tmp[0]);
                jQuery("#input_rtip").val(tmp[1]);
            }
        }
    }else if ( tmp.length > 1)
    {
        jQuery("input[id='gip']").click();
        jQuery("#input_gip").val(ip);
    }
    tmp = max.split(/-/);
    
    jQuery("#limit_down").val(tmp[0]);
    jQuery("#down_bps option[value='" + tmp[1] + "']").attr("selected",true);
    jQuery("#limit_upload").val(tmp[2]);
    jQuery("#upload_bps option[value='" + tmp[3] + "']").attr("selected",true);
    
    tmp = cycle.split(/-/);
    
    
    jQuery("input[id='input_day']").click();
    jQuery("#input_hr option[value='" + tmp[0] + "']").attr("selected",true);
    jQuery("#sec option[value='" + tmp[1] + "']").attr("selected",true);
    
    if (tmp[3] != '' && tmp[3] != null)
    {
        jQuery("input[id='input_month']").click();
        jQuery("#month_day option[value='" + tmp[3] + "']").attr("selected",true);
    }else if (tmp[2] != '' && tmp[2] != null)
    {
        var aa = new Array;
        aa = tmp[2].split(/,/);
        jQuery("input[id='input_week']").click();
        for(var i = 0 ; i < aa.length ; i++)
            jQuery("#week_" + aa[i]).click();
    }
    jQuery( "#new-data" ).dialog("open"); 
}

jQuery( "#new-data" ).dialog({
   autoOpen: false,
   height: 500,
   width: 400,
   modal: true,
   buttons: 
   {
       "Create": function(){
           var bValid= true;
           var down_limit = jQuery("#limit_down").val();
           var up_limit = jQuery("#limit_upload").val();
           var down_bps = jQuery("#down_bps").val();
           var up_bps = jQuery("#upload_bps").val();
           var time = jQuery("#input_hr").val() + "-" + jQuery("#sec").val();
           var week = "",month = "",type='';
           var gateway = jQuery("#host").val();
           if (up_limit == '' || up_limit == null)
               up_limit = '0';
            
/*
               if (jQuery("#input_ip").attr("id"))
               {
                   var ip = jQuery("#input_ip");
                   bValid = bValid && checkIP( ip,/^([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})\$/,"IP have a wrong ?!" );
                   gateway=ip.val();
                   type='ip';
               }else if (jQuery("#input_sip").attr("id"))
               {
                   var ip = jQuery("#input_sip");
                   bValid = bValid && checkIP( ip, /^([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})\\/([\\d]{1,2})\$/,"Subnet have a wrong ?!" );
                   gateway=ip.val();
                   type='sip';
               }else if (jQuery("#input_gip").attr("id"))
               {
                   var ip = jQuery("#input_gip");
                   var tmp = new Array;
                   tmp = ip.val().split(/-/);
                   for(var i = 0 ; i < tmp.length; i++)
                   {
                       var tip = jQuery("#input_gtip"); 
                       tip.val(tmp[i]);
                       bValid = bValid && checkIP( tip, /^([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})\$/,"IP have a wrong ?!" );
                   
                   }
                   gateway=ip.val();
                   type='gip';
               }else if (jQuery("#input_rfip").attr("id"))
               {
                   var fip = jQuery("#input_rfip");
                   bValid = bValid && checkIP( fip,/^([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})\$/,"IP have a wrong ?!" );
                   var tip = jQuery("#input_rtip");
                   bValid = bValid && checkIP( tip,/^([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})\$/,"IP have a wrong ?!" );
                   if (fip.val() == tip.val())
                   {
                       alert("From IP:" + fip.val() + " and To IP:" + tip.val() + " is some!!");
                       bValid = false;
                   }
                   gateway=fip.val() + "~" + tip.val();
                   type='rip';
               }else if (jQuery("#input_mac").attr("id"))
               {
                   var mac = jQuery("#input_mac");
                   bValid = bValid && checkIP( mac,/^([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2})\$/i , "Mac have a wrong?!"); 
                   gateway=mac.val();
                   type='mac';
               }
*/           
               if (jQuery("label[for='input_week']").attr("class") == "ui-button ui-widget ui-state-default ui-button-text-only ui-state-active")
               {
                   for(var i = 0; i < 7 ;i++)
                   {
                       if (jQuery("#week_" + i).attr("checked"))
                          week+= jQuery("#week_" + i).val() + "-";
                   }
               }else if (jQuery("label[for='input_month']").attr("class") == "ui-button ui-widget ui-state-default ui-button-text-only ui-corner-right ui-state-active")
               {
                   month = jQuery("#month_day").val();
               }

           if (bValid)
           {
               if (avalue)
               {
                   data += "{ip:" + gateway + ",down:" + down_limit + "-" + down_bps + ",up:" + up_limit + "-" + up_bps +
           	          ",time:" + time + ",week:" + week + ",month:" + month + ",enabled:" + enabled  + ",type:" + type +"}";
           	   submit('CHE',data);
               }else
               {
                   data = "{ip:" + gateway + ",down:" + down_limit + "-" + down_bps + ",up:" + up_limit + "-" + up_bps +
           	          ",time:" + time + ",week:" + week + ",month:" + month + ",enabled:" + enabled  + ",type:" + type +"}";
           	          
                   submit('SAVE',data); 
               }
               avalue='';
               jQuery( this ).dialog( "close" );
           }
       },
       Cancel: function() 
       {
           avalue='';
           jQuery( this ).dialog( "close" );
       }
   },
   close: function() 
   {
   }
});

jQuery("input[id^='week']").each(function(){
    jQuery(this).click(function(){
        if (jQuery(this).attr("checked") == false || jQuery(this).attr("checked") == null)
            jQuery(this).attr("checked",true);
        else
            jQuery(this).attr("checked",false);
    });
});

function over(a)
{
    a.bgColor="#00BFFF";
}
    
function out(a)
{
    a.bgColor="#FFFFFF";
}
        


jQuery( "#create-user" )
    .button()
    .click(function() 
    {
        jQuery( "#new-data" ).dialog( "open" );
        jQuery("input[id='ip']").click();
        jQuery("#limit_down").val('');
        jQuery("#limit_upload").val('');
        jQuery("option[value='1024']").attr("selected",true);
        jQuery("input[id='input_day']").click();
    });

function updateTips( t )
{
    var tips="NEW";
    tips
       .text( t )
       .addClass("ui-state-highlight");
    setTimeout(function() {
       tips.removeClass("ui-state-highlight",1500);
   },500);
}

function checkLength( o, n, min, max )
{
    if ( o.val().length > max || o.val().length < min )
    {
        o.addClass( "ui-state-error" );
        alert(n + " wrong");
        updateTips( n );
        return false;
    }else
    {
        return true;
    }
}

function checkIP( o, regexp, n )
{
    var reg = new RegExp(regexp);
    var arr = reg.exec(o.val());
    if ( !( regexp.test( o.val() ) ) )
    {
        o.addClass( "ui-state-error" );
        updateTips( n );
        alert(n);
        return false;
    }
    if (arr.length == 7)
        return true;
    if (arr != null && arr.length == 8 || arr.length == 9) 
    {
        if (arr[8]>32 || arr[8]==0)
        {
            o.addClass( "ui-state-error" );
            updateTips( n );
            alert("IP wrong");
            return false;
        }
    	if (arr[1]>255 || arr[1]==0 || arr[3]>255 || arr[5]>255 || arr[7]>255 )
    	{
            o.addClass( "ui-state-error" );
            updateTips( n );
            alert("IP wrong");
            return false;
    	}else
    	{
            return true;
    	}
    } 
}    

jQuery("input[name^='status']").click(function(){

    if ( jQuery(this).attr("id") == "ip" )
    {
        jQuery("#limit_upload").attr("disabled",false);
        jQuery("#input").html("<label for='input_ip'>IP:</label><input type='text' calss='text ui-widget-content ui-corner-all' id='input_ip' />");
    }else if ( jQuery(this).attr("id") == "sip" )
    {
        jQuery("#limit_upload").attr("disabled",false);
        jQuery("#input").html("<label for='input_sip'>Subnet:</label><input type='text' calss='text ui-widget-content ui-corner-all' id='input_sip' />");
    }else if ( jQuery(this).attr("id") == "rip" )
    {
        jQuery("#limit_upload").attr("disabled",false);
        jQuery("#input").html("<label for='input_rfip'>IP From:</label><input type='text' calss='text ui-widget-content ui-corner-all' id='input_rfip' /> \\
	<label for='input_rtip'>IP End:</label><input type='text' calss='text ui-widget-content ui-corner-all' id='input_rtip' />");
    }else if ( jQuery(this).attr("id") == "gip" )
    {
        jQuery("#limit_upload").attr("disabled",false);
        jQuery("#input").html("<label for='input_gip'>IP Group:</label><textarea calss='text ui-widget-content ui-corner-all' id='input_gip' style='height:100;'/>\\
                   <input type='hidden' id='input_gtip'/>");
    }else if ( jQuery(this).attr("id") == "mac" )
    {
        jQuery("#limit_upload").attr("disabled",true);
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
        for(var x = 0 ; x < 7 ; x++)
        {
            if (jQuery("#week_" + x).attr("checked"))
                jQuery("#week_" + x).click();
        }
                                                    
    }else if ( jQuery(this).attr("id") == "input_month" )
    {
        jQuery("#plan_monthy").attr("style","display:block");
        jQuery("#plan_day").attr("style","display:none");
        jQuery("#plan_week").attr("style","display:none");
    }
   

});

jQuery( "#radio" ).buttonset();

jQuery( "#radio_plan" ).buttonset();

jQuery(document).ready(function() {
    jQuery("#openpage").attr("style","display:block");
    submit("SEARCH",'');
});

/*
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
*/
function del(a)
{
    if (a == 'all')
    {
        dvalue='all';
    }else
    {
        dvalue=a;
    }
    jQuery( "#dialog-confirm" ).dialog( "open" );
}

jQuery( "#dialog-confirm" ).dialog({
    autoOpen: false,
    resizable: false,
    height:150,
    modal: true,
    buttons: {
        "Delete":function()
        {
            if( dvalue == 'all')
            {
                data ="{ip:0.0.0.0}"; 
            }else
            {
                data = "{ip:" +  jQuery(dvalue).parent("tr").find("td").eq(1).text() + "}"; 
            }
            submit("DEL",data) 
	    dvalue='';
	    jQuery( this ).dialog( "close" );
	},
	Cancel: function()
	{
	    jQuery( this ).dialog( "close" );
	    dvalue='';
	}
    }
});

function submit(action,data)
{        
    \$.get("quotawork.pl",{action:action,file:"quota.xml",DATA:data},function(aa){
        if (aa != '' && data == '')
        {
            jQuery("tbody tr").remove();
            jQuery( "#table tbody" ).append(aa); 
        }else if(aa != '')
        {
 	    alert("SAVE Success!!");
 	    jQuery("tbody tr").remove();
 	    jQuery( "#table tbody" ).append(aa);
 	}
        else if (aa == '' && data != '')
            alert("SAVE FAIL!!");
    });
}

</script>    
QB
print qq(</body></html>);

