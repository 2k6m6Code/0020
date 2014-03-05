#!/usr/bin/perl 

print "Content-type:text/html\n\n";

use CGI;
my $cgi = new CGI;
my $view = $cgi->param("view");

#---------------------------css---------------------------------------------
print qq (<html><head><link rel="stylesheet" href="../gui.css" type="text/css"><style type="text/css">);
print qq (a:link:{color:#FFFFFF;} a:visited{color:#FFFFFF;});
print qq (.menu{margin-top:0px;margin-left:0px; float:left;});
print qq (.edit{width:100%;scrollbar-track-color:#336699;  scrollbar-Face-Color:#336699;scrollbar-Arrow-Color:#ffffff;  scrollbar-Highlight-Color:#ffffff;
                scrollbar-Shadow-Color:#ffffff; scrollbar-3dLight-Color:#336699;
                scrollbar-DarkShadow-Color:#336699; font-family: "Verdana"; font-size:12px; color: #ffffff;});
print qq (.tb{padding: 10px; margin: 0px auto; }</style>);
print qq (<script type="text/javascript" src ="jquery-1.8.1.min.js"></script>);
print qq (</head><body bgcolor="#336699" text="#ffffff" link="#000040" >);

#----------------------------menu------------------------------------------
#print qq (<table class="menu" width="10%" height="100%" border='0'>);
#print qq (<td valign="top">);
if ($view eq 'ICMP'){print qq (<input type="hidden"  id="enter" onclick="javascript:enter('ICMP')"></a>);}
if ($view eq 'SYN'){print qq (<input type="hidden"  id="enter" onclick="javascript:enter('SYN')"></a>);}
if ($view eq 'PSD'){print qq (<input type="hidden"  id="enter" onclick="javascript:enter('PSD')"></a>);}
if ($view eq 'COD'){print qq (<input type="hidden"  id="enter" onclick="javascript:enter('COD')"></a>);}
#print qq (<p ><a href="javascript:enter('LDOS')">Low-rate Denial-of-Service attacks</a>);
#print qq (<p ><a href="javascript:enter('SA')">starvation attacks</a>);
#print qq (<p ><a href="javascript:enter('PDSA')">Permanent denial-of-service attacks</a>);
#print qq (</table>); 

#---------------------------edit-------------------------------------------
print qq (<div style="position:absolute;"><table id='edit' class="edit" height="70%" border='0' style="margin-left:70px;">);
print qq (<tr><td align="center" ></td></tr>);
print qq (</table></div>);
print qq(</body></html>);

print << "QB_JAVASCRIPT"
<script language="javascript">

\$("#enter").click();

function enter(id,status,view)
{
    if (status == '1')
    {
       \$.get("edit.cgi",{view:'save',data:id,type:view},function fno (data){
           alert('Save is OK!!');
           \$("#edit").attr("disabled",false);
       });
    }
    else
    {
        \$.get("edit.cgi",{view:id},function fno (data){
            \$("#edit").html(data);
        });
    }

}

function Status()
{
    if ( \$("#logset").attr("checked"))
    {
        \$("#timenumber").attr("disabled",false);
        \$("#time").attr("disabled",false);
        \$("#logprefix").attr("disabled",false);
    }
    else
    {
        \$("#timenumber").attr("disabled",true);
        \$("#time").attr("disabled",true);
        \$("#logprefix").attr("disabled",true);
    }
}
function COD(ck,num,port)
{
    if (\$(ck).attr("checked"))
    {
        \$(num).attr("disabled",false);
        \$(port).attr("disabled",false);
    }
    else
    {
        \$(num).attr("disabled",true);
        \$(port).attr("disabled",true);
    }
}
function Statu()    
{
    if (\$("#matchenable").attr("checked"))
    {
        \$("#max").attr("disabled",false);
        \$("#r1").attr("disabled",false);
        \$("#r2").attr("disabled",false);
        \$("#num").attr("disabled",false);
        \$("#wt").attr("disabled",false);
        \$("#hw").attr("disabled",false);
        \$("#lw").attr("disabled",false);
        \$("#dt").attr("disabled",false);
        \$("#ipck").attr("disabled",false);
        \$("#portck").attr("disabled",false);
        \$("#icmp").attr("disabled",false);
        \$("#syn").attr("disabled",false);
        
    }
    else
    {
        \$("#max").attr("disabled",true);
        \$("#num").attr("disabled",true);
        \$("#r1").attr("disabled",true);
        \$("#r2").attr("disabled",true);
        \$("#wt").attr("disabled",true);
        \$("#hw").attr("disabled",true);
        \$("#lw").attr("disabled",true);
        \$("#dt").attr("disabled",true);
        \$("#ipck").attr("disabled",true);
        \$("#ipck").attr("checked",false);
        \$("#portck").attr("disabled",true);
        \$("#portck").attr("checked",false);
        \$("#portnum").attr("disabled",true);
        \$("#ipnum").attr("disabled",true);
        \$("#port").attr("disabled",true);
        \$("#icmp").attr("disabled",true);
        \$("#icmp").attr("checked",false);
        \$("#syn").attr("disabled",true);
        \$("#syn").attr("checked",false);
        \$("#icmpbox").attr("disabled",true);
        \$("#synbox").attr("disabled",true);
                                
    }
}

function SAVE(status)
{
    var msg = "";
    var view=status + '=';
    var time = "";
    var log = "";
    var match = "";
    
    \$("#edit").attr("disabled",true);
    for (i=0; typeof(\$("#enablelist").find("option").eq(i).val()) != 'undefined'; i++)
         msg += \$("#enablelist").find("option").eq(i).val() + ":";
    for (y=0; typeof(\$("#list").find("option").eq(y).val()) != 'undefined'; y++)
         view += \$("#list").find("option").eq(y).val() + ",";
    time=\$("#timenumber").val() + '/' + \$("#time").val();
    log=\$("#logprefix").val();
    
    if (\$("#matchenable").attr("checked"))
    {
        match=\$("#max").val();
    }
    msg+= ',' + time + ',' + log + ',' + match;
    enter(msg,'1',view);

}
function inser(des,src,add)
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

function DEL(src)
{
    var src = document.getElementById(src);
    if (src.selectedIndex != -1)
    {
        var opt = document.createElement("option");
        src.remove(src.selectedIndex);
    }
}

function ADD()
{
 if (Check(\$("#addlist").val()))
 {
   var des = document.getElementById("enablelist"); 
   var opt = document.createElement("option");
   opt.text = \$("#addlist").val();
   opt.value = \$("#addlist").val();
   des.options.add(opt);
  }
  else
  {
      alert("IP ERROR!!");
  }
  \$("#addlist").val("");
} 

function Check(ip)
{
    rule = /\\d{1,3}\.\\d{1,3}\.\\d{1,3}\.\\d{1,3}/g;
    var ck = ip.split("\.");
    for (var i = 0; i < 4; i++)
    {
        if (ck[i] > 255 || ck[i] < 0)
        {
            return 0;
        }
    }
    return rule.test(ip);
}                                                           
</script>

QB_JAVASCRIPT
