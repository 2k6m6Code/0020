#!/usr/bin/perl
use CGI;
print "Content-type:text/html\n\n";

print qq(<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">);
print qq(<html lang="en">);
print qq(<head>);
print qq(<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">);
print qq(	<title>CMS Image Upload</title>);
print qq(<style type="text/css">
button.menu {
    background: none repeat scroll 0 0 #336699;
    border: 1px solid black;
    color: white;
    font: 10px Verdana;
    height: 18px;
    margin-right: 4px;
}
</style>);
print qq(</head>);
print qq(<body style="background-color:#336699;">);
print qq (<button  onclick="parent.mainFrame.location='cmsFrmconfig.cgi?viewpoint=managerUPG'" hidefocus="true" class="menu">Upload UPG</button>);
print qq (<button  onclick="parent.mainFrame.location='cmsPkg.cgi'" hidefocus="true" class="menu">Upload Image</button>);
print qq (<button  onclick="parent.mainFrame.location='upgmanager.cgi'" hidefocus="true" class="menu">Upgrade</button>);
print qq(<div style="width: 750px; margin: auto; color:white; font-weight: bold; font-size: 16px;">Upload Firmware<br /><hr></div>);
print qq(<div style="width: 750px; margin: auto; color:white; font-weight: bold; font-size: 16px;">);

print qq(<div><fieldset class="fieldset"><legend class="subtitle" style="color:white;" >Menu for Firmware</legend><form action="cmspkgsave.php"  enctype="multipart/form-data" method="post" target="resultframe">
		Upload Image <input type="file" name="pkgfile" id="inpf" /><input type="radio" name="pkglocal" value="PKG1">Image1<input type="radio" name="pkglocal" value="PKG2">Image2
		<input type="submit" value="Upload" />
		</form></fieldset></div>);
print qq(<div style="margin:10px"><iframe src="" frameborder="1" style="background-color:#C2D1E1; width:725px; height:350px; filter:alpha(opacity=70);" name="resultframe"></iframe></div>);
print "</div>";
print qq(</body></html>);
