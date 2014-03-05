#!/usr/bin/perl
use CGI;
use File::Find;

print "Content-type:text/html\n\n";
#require ("/usr/local/apache/qb/qbmod.cgi");

my $path='/usr/local/apache/qbconf/l7-object/';

find( { wanted => sub { push(@FileList, $_) }, no_chdir => 1 }, $path );

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"><script type="text/javascript" src="jquery-1.9.1.min.js"></script>);
print qq(<style type="text/css">);
print qq(.right{width:59%;float:right;height:300px});
print qq(.left{width:40%;float:right;height:300px});
print qq(.example{width:50%;});
print qq(.bottom{width:100%;});
print qq(</style></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<div align="center" id="all" class="divframe"><table width="75%"><tr><td class="">Layer 7<hr size="1"></td></table>);

print qq(<div class="right" align="left"><table width="75%">);
print qq(<tr><td><a>Name :</a><input type="text" id="name" value="" style="width:75%"></td>);
print qq(<tr><td>Explanation</td>);
print qq(<tr><td><p align="left" style="border: 5px double rgb(109, 2, 107); cellpadding="1" cellspacing="1" frame="border" rules="none">
        Pattern is a regular expression used to define a software or protocol<br><br>
	An example to define your own pattern:<br>
	To define the HTML Patten.<br>
	1\)Use the <a href="http://www.wireshark.org/">Wireshark</a> or some other softwares which support to catch a certain number of packets.<br>
	2\)Find out the rule from the packets.<br>
	In this example, it is "&lt;html .*&gt;&lt;head&gt;".<br>
	You can type "&lt;html .*&gt;&lt;head&gt;" on the pattern field and give it a name.
</p></td>);
print qq (<tr><td>);
print qq (<input class="qb" id="add" type="button" value="ADD" style="float:left"/>);
print qq (<input class="qb" id="del" type="button" value="DELE" style="float:left"/>);
print qq (<input class="qb" id="save" type="button" value="SAVE" style="float:right"/>);
print qq (<input class="qb" id="back" type="button" value="BACK" style="float:right"/>);
print qq (</td></table></div>);

print qq(<div class="left" align="right"><table width="70%">);
print qq(<tr><td><a>Search :</a><input class="qbopt" id="search" type="text" value="" style="width:70%"></td>);
print qq(<tr><td><select class="qbopt" id="menu" size="15" style="width:80%">);
foreach my $aa (@FileList)
{
    $aa =~ s/$path//g;
    if (!grep(/\.pat/,$aa)){next;}
    $aa =~ s/\.pat//g;
    print qq(<option value="$aa" >$aa);
}
print qq(</select></td>);
print qq(</table></div>);


print qq(<div class="bottom"><table width="50%">);
print qq(<tr><td></td>);
print qq(<tr><td><input type="text" id="data" value="" style="width:100%" /></td>);
print qq(</table></div>);

print qq(<input type="hidden" id="path" value="$path"/>);

print qq(</div></body></html>);

print << "QB";

<script language="javascript">

\$("#search").change(function(){
    var text = \$(this).val();
    \$("#menu option[value^=" + text + "]").attr("selected","selected");
    \$("#menu").trigger("change");
});

\$("#menu").change(function(){
    var name = \$(this).val();
    var path = \$("#path").val();
    \$("#all").attr("disabled",true); 
    \$.get("l7-work.cgi",{action:'show',PATH:path + name + ".pat",ID:name},function(data){
        if (data != "")
        {
            \$("#menu option[value='new']").remove();
            \$("#data").val(data);
            \$("#name").val(name);
            \$("#name").attr("disabled",true);
        }else
        {
            alert("ERROR!!");
        }
        \$("#all").attr("disabled",false);
    });
});

\$("#add").click(function(){
    var name = \$("#name").val();
    \$("#menu").append("<option value='new'>New Object");
    \$("#menu option[value='new']").attr("selected","selected");
    \$("#name").attr("disabled",false);
    \$("#name").val("");
    \$("#data").val("");
});

\$("#del").click(function(){
    var name = \$("#name").val();
    var path = \$("#path").val();
    if (name == '')
    {
        alert("Please,Choose anyone first!!"); 
        return;
    }
    \$("#all").attr("disabled",true);
    \$.get("l7-work.cgi",{action:'delete',PATH:path+name+'.pat',ID:name},function(data){
        if (data == '1')
        {
            alert("DELETE " + name + " is Success!!");
            \$("#menu option[value='" + name + "']").remove();
            \$("#name").attr("disabled",false);
            \$("#name").val("");
            \$("#data").val("");
        }else
            alert("DELETE " + name + " is Fail!!");
        \$("#all").attr("disabled",false);
    });
});

\$("#save").click(function(){
    var name = \$("#name").val();
    var path = \$("#path").val();
    var data = \$("#data").val();
    var show;
    var judge = /\.pat/;
    var judge1 = /\.pat/gi;
    var user = /_UD/;
   
    name = name.replace(judge1,"");
    
    if (!user.test(name))
    {
        name += "_UD";
        \$("#name").val(name);
   	show=name;     
    }
    
    name += "\.pat";
    
    if(data == "")
    {
        alert("Rule can't be Empty!!");
        return;
    }
    
    \$("#all").attr("disabled",true);
    \$.get("l7-work.cgi",{action:'save',PATH:path+name,ID:name,DATA:data},function(check){
       if (check == '1')
       {
           alert("SAVE " + name + " is Success!!");
           \$("#menu option[value='new']").remove();
           \$("#menu").append("<option value=" + name + ">" + show);
           \$("#menu option[value='" + name + "']").attr("selected","selected");
           \$("#name").attr("disabled",true);
       }
       else
           alert("SAVE " + name + " is Fail!!"); 
       \$("#all").attr("disabled",false);
    });
});

\$("#back").click(function(){
    \$("#all").attr("disabled",true);
    window.location.href="newappgroup.cgi";
});

</script>

QB




