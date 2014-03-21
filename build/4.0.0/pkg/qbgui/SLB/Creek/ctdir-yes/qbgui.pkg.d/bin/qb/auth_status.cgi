#!/usr/bin/perl
require ("/usr/local/apache/qb/language/qblanguage.cgi");
BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use Data::Dumper;
use CGI;
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type:text/html\n\n";
#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{refreshtime} = $form->param('refreshtime');
print qq (<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> );
print qq (<!DOCTYPE html><html><head><meta charset="UTF-8">);
print qq (<script type="text/javascript" src ="sorttable.js"></script><script type="text/javascript" src ="../qbjs/jquery.js"></script><style type="text/css">#tables_filter{text-align: left;} table.sortable thead{background-color:#eee;color:#666666;font-weight: bold;cursor: default;}button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style><link rel="stylesheet" href="../gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);
#print qq (<button  onclick="parent.mainFrame.location='auth_server.cgi'" hidefocus="true" class="menu">Server</button>);
#print qq (<button  onclick="parent.mainFrame.location='auth_user.cgi'" hidefocus="true" class="menu">Group</button>);
#print qq (<button  onclick="parent.mainFrame.location='auth_option.cgi'" hidefocus="true" class="menu">Option</button>);
#print qq (<button  onclick="parent.mainFrame.location='auth_status.cgi'" hidefocus="true" class="menu">Status</button>);
print qq(<div align="center" style="width: 600px; margin: 12px auto 5px auto;">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="lantgaffic" method="post" action="lantraffic.cgi" style="width:600">);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td class="bigtitle">Authentication Status</td></tr></table>);
print qq (<div style="width:600">);
print qq (<table width="100%" border="0"><tr>);
print qq (<td class="body" align="left">);
print qq (</select>);
print qq (&nbsp&nbspAuto Refresh Per);
print qq (<select name="refreshtime" id="refreshtime">);
my @time=(30,50,70,90);
foreach my $tm ( @time )
{
    my $status = ( $action{refreshtime} eq $tm ) ? ( 'selected' ) : ( '' );
    print qq(<option value="$tm" $status>$tm</option>);
}
print qq (</select>seconds&nbsp&nbsp);
print qq (<input type="button" value="Stop" class="qb" style="width:60" id="switch" onclick="Switch(this.value)">);
print qq (&nbsp&nbsp Kick Out for: );
print qq (<select id="kick_time" style="width:100px">);
print qq (<option value="none">Now</option>);
print qq (<option value="forever">Forever</option>);
foreach my $time (1..24)
{
    print qq (<option value="$time">$time hr</option>);
}
print qq (</select>);
print qq (</td></tr></table>);
print qq (</div>);

print << "QB_TRAFFIC";

<script type="text/javascript" language="javascript" src="../qbjs/jquery.dataTables.min.js"></script>
<script type="text/javascript" src="./grid.js"></script>
<script type="text/javascript" src="./qb.js"></script>
<script language="javascript">

function kick()
{
    var aa = document.getElementsByName('box');
    var bb = aa.length;
    var oo = document.getElementById("kick_time").value + ":";
    var nu = 0;
    for(var i = bb ; i > 1 ; i--)
    {
        if(aa[i-1].checked == true)
        {
            oo+=aa[i-1].value + ',';
            nu++;
        }
    }
    var a = confirm("Aru You Kick " + nu + " option ??" );
    if (a)
        Ajax(oo);    
}


(function (\$, document, undefined) {

	var pluses = /\\+/g;

	function raw(s) {
		return s;
	}

	function decoded(s) {
		return decodeURIComponent(s.replace(pluses, ' '));
	}

	var config = \$.cookie = function (key, value, options) {

		// write
		if (value !== undefined) {
			options = \$.extend({}, config.defaults, options);

			if (value === null) {
				options.expires = -1;
			}

			if (typeof options.expires === 'number') {
				var days = options.expires, t = options.expires = new Date();
				t.setDate(t.getDate() + days);
			}

			value = config.json ? JSON.stringify(value) : String(value);

			return (document.cookie = [
				encodeURIComponent(key), '=', config.raw ? value : encodeURIComponent(value),
				options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
				options.path    ? '; path=' + options.path : '',
				options.domain  ? '; domain=' + options.domain : '',
				options.secure  ? '; secure' : ''
			].join(''));
		}

		// read
		var decode = config.raw ? raw : decoded;
		var cookies = document.cookie.split('; ');
		for (var i = 0, parts; (parts = cookies[i] && cookies[i].split('=')); i++) {
			if (decode(parts.shift()) === key) {
				var cookie = decode(parts.join('='));
				return config.json ? JSON.parse(cookie) : cookie;
			}
		}

		return null;
	};

	config.defaults = {};

	\$.removeCookie = function (key, options) {
		if (\$.cookie(key) !== null) {
			\$.cookie(key, null, options);
			return true;
		}
		return false;
	};

})(jQuery, document);
function Switch (name)
{
	if ( name == "Stop"){
		 \$("#switch").val("Run");
	}else{
		 \$("#switch").val("Stop");
		 auto_refresh();
	}
}

function auto_refresh()
{	
//	var unixTimestamp = new Date(1377253505 * 1000);
//	commonTime = unixTimestamp.toLocaleString();
//	alert(commonTime);
    	setTimeout("Ajax();",(parseInt(\$("#refreshtime").val())-1)*1000);
}

function Ajax(aa)
{    
     var tmp = \$("#interface").val();
     var data="";
     var url = "object_auth_status.cgi";
     var db = tmp + "&time="+new Date().getTime();
     
     \$.get(url,{tm:aa},
	function fno(data)
	{	
        var status;
	\$("#table").html(data);
	
	var oTable =  \$('#tables').dataTable({
	"fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {
			
			
			/* Calculate the market share for browsers on this page */
			/*
			var iPageMarket = '';
			var iPageMarket2 = '';
			var iPageMarket3 = '';
			for ( var i=iStart ; i<iEnd ; i++ )
			{
				iPageMarket += aaData[ aiDisplay[i] ][0];
				iPageMarket2 += aaData[ aiDisplay[i] ][1];
				iPageMarket3 += aaData[ aiDisplay[i] ][2];
				alert(iPageMarket);
			}
			*/
			/* Modify the footer row to match what we want */
			/*
			var nCells = nRow.getElementsByTagName('th');
			nCells[1].innerHTML = iPageMarket.toFixed(2) ;
			nCells[2].innerHTML = iPageMarket2.toFixed(2) ;
			*/
		},
	"bPaginate": false,
		"bInfo": false,
		"aoColumns": [
            { "sType": 'html' },
            { "sType": 'string-case' },
            { "sType": 'string-case' }
        ]
	});
	jQuery.fn.dataTableExt.oSort['html-asc']  = function(x,y) {
	var xx1 = x.split('.');
	var yy1 = y.split('.');
	x = xx1[0]*255*255*255+xx1[1]*255*255+xx1[2]*255+xx1[3];
	y = yy1[0]*255*255*255+yy1[1]*255*255+yy1[2]*255+yy1[3];
	var ssv3 = x-y;
    return ssv3;
	};
	jQuery.fn.dataTableExt.oSort['html-desc']  = function(x,y) {
	var xx1 = x.split('.');
	var yy1 = y.split('.');
	x = xx1[0]*255*255*255+xx1[1]*255*255+xx1[2]*255+xx1[3];
	y = yy1[0]*255*255*255+yy1[1]*255*255+yy1[2]*255+yy1[3];
	var ssv3 = y-x;
    return ssv3;
	};
	jQuery.fn.dataTableExt.oSort['string-case-asc']  = function(x,y) {
	var ssv3 = x-y;
    return ssv3;
	};
	jQuery.fn.dataTableExt.oSort['string-case-desc'] = function(x,y) {
	var ssv3 = y-x;
    return ssv3;
	};
	\$("input[type='text']").val(\$.cookie("searchinput"));
	oTable.fnFilter( \$("input[type='text']").val());
	  \$("input[type='text']").keyup(function () { 
	\$.cookie("searchinput", \$("input[type='text']").val());
	});
	auto_refresh();
});
}
Ajax();
auto_refresh();



</script>

QB_TRAFFIC

print qq (<div class="divframe" style="width:600" id="table">);
print qq (</div></table>);
print qq(<input type="hidden" name="action" value="$action{action}">);
print qq(</form></div></body></html>);
