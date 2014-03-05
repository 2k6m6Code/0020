#!/usr/bin/perl
use CGI;

require ("/usr/local/apache/qb/qbmod.cgi");
my $iplist=XMLread($gPATH.'ipmac.xml');
my $list=$iplist->{num};
my $line=0;
my $enable,$enabled;
print "Content-type:text/html\n\n";

print qq(<html><head><link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css"/>);
print qq(<script src="http://code.jquery.com/jquery-1.9.1.js"></script>);
print qq(<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>);
#print qq(<link rel="stylesheet" href="/resources/demos/style.css" />);
print qq(<style>);

print qq(body { font-size: 80%; });
print qq(label, input { display:block; });
print qq(input.text { margin-bottom:12px; width:95%; padding: .4em; });
print qq(fieldset { padding:0; border:0; margin-top:25px; });
print qq(h1 { font-size: 1.2em; margin: .6em 0; });
print qq(th { width:100px; });
print qq(td { text-align: center; });
print qq(div#users-contain { width: 350px; margin: 20px 0; });
print qq(div#users-contain table { margin: 1em 0; border-collapse: collapse; width: 100%; });
print qq(div#users-contain table td, div#users-contain table th { border: 1px solid #eee; padding: .6em 10px; text-align: left; });
print qq(.ui-dialog .ui-state-error { padding: .3em; });
print qq(.validateTips { border: 1px solid transparent; padding: 0.3em; });

print qq(</style></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);

print qq(<div id="new-data" title="Create new IP">);
print qq(<form><fieldset>);
print qq(<label for="ip">IP</label>);
print qq(<input type="text" name="ip" id="ip" class="text ui-widget-content ui-corner-all" />);
print qq(<label for="mac">Mac</label>);
print qq(<input type="text" name="mac" id="mac" class="text ui-widget-content ui-corner-all" />);
print qq(<label for="radio">Status</label>);
print qq(<div id="radio">);
#print qq(<input type="radio" name="status" id="status1" value="0" checked="checked"/>);
#print qq(<label for="status1">DROP</label>);
print qq(<input type="radio" name="status" id="status2" value="1" checked="checked"/>);
print qq(<label for="status2">ACCEPT</label>);
print qq(</div>);
print qq(</fieldset></form></div>);

print qq(<div id="dialog-confirm" title="" >);
print qq(<p>Are you sure want to delete ??</p>);
print qq(</div>);

print qq(<div align="center" width="75%">);
print qq(<div id="mainpage" class="ui-widget" >);
print qq(<h1>IP/MAC</h1>);

foreach my $ip (@$list)
{
    if ($ip->{ip} eq 'system' && $ip->{mac} eq 'system')
    {
        ($ip->{status} eq '1')?($enable="checked='checked'"):($enabled="checked='checked'")
    }
}

print qq(<div id="enable">);
print qq(<label for="enabled_on">Enabled</label>);
print qq(<input type="radio" name="enabled" id="enabled_on" $enable/>);
print qq(<label for="enabled_off">Disabled</label>);
print qq(<input type="radio" name="enabled" id="enabled_off" $enabled/>);
print qq(</div>);

print qq(<table id="table" class="ui-widget ui-widget-content" border="1" >);
print qq(<thead><tr class="ui-widget-header ">);
print qq(<th>IP</th>);
print qq(<th>Mac</th>);
print qq(<th>Status</th>);
print qq(<th><img src="image/del.gif" title="Delete" border="0" onClick="del('all')"></th>);
print qq(</tr></thead>);
print qq(<tbody>);
foreach my $ip (@$list)
{
    if ($ip->{ip} eq "" && $ip->{mac} eq "" && $ip->{status} eq "" || $ip->{ip} eq "system" || $ip->{mac} eq "system"){next;}
    print qq(<tr onMouseOver="over(this)" onMouseOut="out(this)">);
    print qq(<td onClick="alter(this)" >$ip->{ip}</td>); 
    print qq(<td onClick="alter(this)" >$ip->{mac}</td>);
    my $status = ($ip->{status} eq '1') ? ('ACCEPT'):('DROP');
    print qq(<td onClick="alter(this)" >$status</td>);
    print qq(<td onClick='del(this)'><a><img src="image/del.gif" title="Delete" border="0" ></a>);
    print qq(<input type="hidden" value="$line"/></td>);
    print qq(</tr>);
    $line++;
}
print qq(</tbody></table></div>);
print qq(<button id="create-user">Create new IP</button>);

print << "QB";

<script language="javascript">

var dvalue;
var avalue;
var ajax_check;

function alter(a)
{
    var fa=jQuery(a).parent("tr");
    var ip=jQuery(fa).find("td").eq(0).text();
    var mac=jQuery(fa).find("td").eq(1).text();
    var status=jQuery(fa).find("td").eq(2).text();
    var line=jQuery(fa).find("input").eq(0).val();
    
    jQuery("#ip").val(ip);
    jQuery("#mac").val(mac);
    
    avalue=line;
    
    if (status == "DROP")
    {
        jQuery("label[for='status1']").attr("class","ui-button ui-widget ui-state-default ui-button-text-only ui-corner-left ui-state-active");
        jQuery("label[for='status2']").attr("class","ui-button ui-widget ui-state-default ui-button-text-only ui-corner-left");
    }
    else
    {
        jQuery("label[for='status2']").attr("class","ui-button ui-widget ui-state-default ui-button-text-only ui-corner-left ui-state-active");
        jQuery("label[for='status1']").attr("class","ui-button ui-widget ui-state-default ui-button-text-only ui-corner-left");
    }
    
    jQuery( "#new-data" ).dialog( "open" ); 
}

function over(a)
{
    a.bgColor="#00BFFF";
}

function out(a)
{
    a.bgColor="#FFFFFF";
}

function del(a)
{
    if (a == 'all')
    {
       dvalue='all';
    }
    else
    {
        dvalue=a;
    }
    jQuery( "#dialog-confirm" ).dialog( "open" );
}



function submit(n,o)
{
    if (jQuery("label[for='enabled_on']").attr("class") == "ui-button ui-widget ui-state-default ui-button-text-only ui-corner-left ui-state-active")
        var enabled = '1';
    else
        var enabled = '0';
        
    jQuery.get("data_search.pl",{action:n,file:"ipmac.xml",data:o,enable:enabled},function(x)
    {
   	if ( x == '1')
   	    alert("Swtich Enable/Disable!!");
   	else if (x != '')
   	{
   	    jQuery("tbody tr").remove();
   	    jQuery( "#table tbody" ).append(x);
   	    alert(n + " Success!!");
   	}    
   	else
   	{
   	    alert(n + " Fail!!");
   	}
    });
}

jQuery( "#dialog-confirm" ).dialog({
    autoOpen: false,
    resizable: false,
    height:140,
    modal: true,
    buttons: {
        "Delete":function()
        {
	    if( dvalue == 'all')
	    {
	        data = "{ip:0.0.0.0,mac:00:00:00:00:00:00}-{ip:0.0.0.0,mac:00:00:00:00:00:00}";
	        submit("DEL",data)
	        //jQuery("tbody tr").remove();
	    }else
	    { 
	        data = "{ip:" +  jQuery(dvalue).parent("tr").find("td").eq(0).text() +",mac:" + jQuery(dvalue).parent("tr").find("td").eq(1).text() + "}";
	        submit("DEL",data)
	        //jQuery(dvalue).parent("tr").remove();
	    }
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
                                                                                                                                                       

jQuery("input[name='enabled']").click(function(){
	var data='';
	submit('SEARCH',data);
});

jQuery(function(){
    var ip=jQuery("#ip"),mac=jQuery("#mac"),status=jQuery("#status"),
    allFields = jQuery( [] ).add( ip ).add( mac ).add( status ),
    tips = "New";
    
    function updateTips( t ) 
    {
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
	    updateTips( "Length of " + n + " is wrong!!");
	    alert(n + " wrong");
	    return false;
	}else
	{
	    return true;
	}
    }
    
    function checkRegexp( o, regexp, n ) 
    {
	if ( !( regexp.test( o.val() ) ) ) 
	{
	    o.addClass( "ui-state-error" );
	    updateTips( n );
	    alert(n);
	    return false;
	}else{
    	    return true;
	}
    }
    
    function checkIP( o, regexp, n )
    {
	var reg = new RegExp(regexp);
	var arr = reg.exec(o.val());
	if (arr != null && arr.length == 8) {
	    if (arr[1]>255 || arr[1]==0 || arr[3]>255 || arr[5]>255 || arr[7]>255 || arr[7]==0) 
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
    
    function check(o,n)
    {
        for (var i = 0; jQuery( "#table tbody" ).find("td").eq(i).text() != o.val(); i+=4)
        {
            if (i > 200) 
                return true;
        }
        alert("IP Repeat");
        return false; 
    }

    jQuery( "#radio" ).buttonset();
    jQuery( "#enable" ).buttonset();
    
    jQuery( "#new-data" ).dialog({
    	autoOpen: false,
    	height: 500,
    	width: 400,
    	modal: true,
    	buttons: {
    		"Create an IP": function(){
    		   var bValid= true;
    		   var data;
    		   allFields.removeClass( "ui-state-error" );
    		   
    		   bValid = bValid && checkLength( ip, "IP", 7, 15 );
    		   bValid = bValid && checkLength( mac, "MAC", 17, 17 );
    		   bValid = bValid && checkIP( ip, /^([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})\$/,"IP have a wrong ?!" );
    		   bValid = bValid && checkRegexp( ip, /^([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})([.])([\\d]{1,3})\$/,"IP have a wrong ?!" );
    		   bValid = bValid && checkRegexp( mac, /^([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2}):([a-fA-F0-9]{1,2})\$/i , "Mac have a wrong?!");
    		   if (avalue == '' || avalue == null)
    		   	bValid = bValid && check(ip,mac);
    		    
    		   if (bValid)
    		   {
    		       /*if (jQuery("label[for='status2']").attr("class") != "ui-button ui-widget ui-state-default ui-button-text-only ui-corner-right ui-state-active")
    		       {
    		           status = "DROP";
    		       }else if (jQuery("label[for='status1']").attr("class") != "ui-button ui-widget ui-state-default ui-button-text-only ui-corner-right ui-state-active")
    		       {
    		           status = "ACCEPT";
    		       }*/
    		       status = "1"; 
    		       
    		       if (avalue == '' || avalue == null)
    		       { 
    		           data = "{ip:" + ip.val() + ",mac:" + mac.val() + ",status:" + status + "}";
    		           submit("SAVE",data)
    		           /*
    		           if (ajax_check)
    		           { 
    		               jQuery( "#table tbody" ).append( "<tr onMouseOver='over(this)' onMouseOut='out(this)'>" +
    		               "<td onClick='alter(this)'>" + ip.val() + "</td>" +
    		               "<td onClick='alter(this)'>" + mac.val() + "</td>" +
    		               "<td onClick='alter(this)'>ACCEPT</td>" +
    		       	       //"<td onClick='alter(this)'>" + status "</td>" +
    		               "<td onClick='del(this)'><a><img src='image/del.gif' title='Delete' border='0'></a><input type='hidden' value='" + 
    		               line + "' /></td>" + "</tr>" );
    		           }
    		           */
    		       }else if (avalue >= 0)
    		       {
    		           for (var i = 0; jQuery( "#table tbody" ).find("input").eq(i).val() != avalue ; i++)
    		           {
    		               if (i > 500)
    		                   return;
    		           }
    		           var ob=jQuery( "#table tbody" ).find("input").eq(i).parent("td");
    		           data = "{ip:" + ob.parent("tr").find("td").eq(0).text() + ",mac:" + ob.parent("tr").find("td").eq(1).text() + ",status:" + ob.parent("tr").find("td").eq(2).text() + "}-";
    		           data += "{ip:" + ip.val() + ",mac:" + mac.val() + ",status:" + status + "}";
    		           submit("CHE",data)
    		           /*
    		           if (ajax_check)
    		           {
    		               var ob=jQuery( "#table tbody" ).find("input").eq(i).parent("td");
    		               ob.parent("tr").find("td").eq(0).text(ip.val());
    		               ob.parent("tr").find("td").eq(1).text(mac.val());
    		               ob.parent("tr").find("td").eq(2).text(status);
    		           }
    		           */
    		       }
    		       avalue='';
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
    		  allFields.val( "" ).removeClass( "ui-state-error" );
    	      }
    	    });
    	    
    	    jQuery( "#create-user" )
    	        .button()
    	        .click(function() 
    	        {
    	            jQuery( "#new-data" ).dialog( "open" );
    	        });
    });
    
</script>

QB

print qq(</div></body></html>);

