#!/usr/bin/perl
use Data::Dumper;
use CGI;
require ("qbmod.cgi");
require ("./qblib/host.lib");
require ("./qblib/newhost.lib");


#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
my @host=$form->param('host');
$action{host}=\@host;
$action{type} = $form->param('type');

if($action{type} eq ''){$action{type}='4'}

#print qq (<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040" >);
print qq(<html><head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"><script type="text/javascript" src="jquery-1.9.1.min.js"></script></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<style type="text/css">button.menu{margin-right: 4px;height:18px;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;}</style>);
#print qq(<style type="text/css">\#abgne_float_ad {display: none;	position: absolute;} \#abgne_float_ad img {border: none;}</style>);
print qq(<style type="text/css">\#fiexd-header{position:fixed; left:10%; z-index:1; _position:absolute; _top:expression(documentElement.scrollTop+"px")}</style>);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainHost( %action ); }
#print qq (<button  onclick="parent.mainFrame.location='host.cgi'" hidefocus="true" class="menu">Host Object</button>);
#print qq (<button  onclick="parent.mainFrame.location='country.cgi'" hidefocus="true" class="menu">Country Object</button>);
print qq (<button  onclick="parent.mainFrame.location='host.cgi?type=4'" hidefocus="true" class="menu" style="width: 100">IPv4</button>);
print qq (<button  onclick="parent.mainFrame.location='host.cgi?type=6'" hidefocus="true" class="menu" style="width: 100">IPv6</button>);
print qq (<button  onclick="parent.mainFrame.location='host.cgi?type=mac'" hidefocus="true" class="menu" style="width: 100">MAC</button>);
print qq (<button  onclick="parent.mainFrame.location='host.cgi?type=fqdn'" hidefocus="true" class="menu" style="width: 100">FQDN</button>);

print qq(<div align="center" style="float: center;">);
#------- start to draw every form object to interact with users --------------------------------
print qq(<form name="hostform" method="post" action="host.cgi"><br>);
print qq (<table cellspacing="0" border="0">);
print qq (<tr><td>);
showHost(%action);
scriptHost();
print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" id="action" value="$action{action}">);
print qq(<input type="hidden" name="type" id="type" value="$action{type}">);
#print qq (<input class="qb" type="button" align="center" width="100" id="abgne_float_ad" value="$qblang[162]" onclick="Newhost(0);">);
print qq(</form></div>);
	
general_script();
print qq(</body></html>);


print << "QB";
<script language="javascript">

/* 	\$(window).load(function(){
		\$win = \$(window),
			\$ad = \$('#abgne_float_ad').css('opacity', 0).show(),
			_width = \$ad.width(),
			_height = \$ad.height(),
			_diffY = 100, _diffX = 100,
			_moveSpeed = 800;
		\$ad.css({
			top: \$(document).height(),
			left: \$win.width() - _width - _diffX,
			opacity: 1
		});
		\$win.bind('scroll resize', function(){
			var \$this = \$(this);
	 
			\$ad.stop().animate({
				top: \$this.scrollTop() + \$this.height() - _height - _diffY,
				left: \$this.scrollLeft() + \$this.width() - _width - _diffX
			}, _moveSpeed);
		}).scroll();
	}); */

</script>
QB
