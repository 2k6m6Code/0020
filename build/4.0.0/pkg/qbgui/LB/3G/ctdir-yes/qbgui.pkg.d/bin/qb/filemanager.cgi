#!/usr/bin/perl
use CGI;
use Data::Dumper;
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type: text/html\n\n";
print qq(<form><table><td class="bigtitle" colSpan="2">CMS Configure</td></table>);
print qq(<tr><hr size="2">);
print qq(<div style="width:500px"><table border=1><tr>);
print qq(<td><select id="iid$i" style="width:160px" onChange="this.form.paths.value=this.valuei;savedata(this.value);">);
$filename = join(",",glob('/mnt/qb/conf/cms/*'));
@filedir = split(",",$filename);
print qq(<option>Please Choose!!</option>);
print qq(<option value="local">Local</option>);
foreach $z (@filedir)
{
    $z =~ s/\/mnt\/qb\/conf\/cms\///;
    if ($z eq "boot" || $z eq "default" || $z eq "active"){next;}
    print qq(<option value="$z">$z</option>);
}
print qq(</select</td><td></td>);
print qq(<td><select id="iid$y" style="width:160px"  onChange="this.form.pathd.value=this.value;savedata(this.value);">);
print qq(<option>Please Choose!!</option>);
foreach $z (@filedir)
{
    $z =~ s/\/mnt\/qb\/conf\/cms\///;
    if ($z eq "boot" || $z eq "default" || $z eq "active"){next;}
    print qq(<option value="$z">$z</option>);
}
print qq(<tr><td rowspan=4><form method="post" action="">);
print qq(<select id="surlist" size = 15 style="width:150px"> );
print qq(</select>);
print qq(</td><td></td>);
print qq(<td rowspan=4><form method="post">);
print qq(<select id="deslist" size = 15 style="width:150px" action=""> );
print qq(</select></td>);
print qq(<tr><td><input type="button" value=">>>" id="tran$i" onclick="inser('deslist','surlist');" style="width:80px" ></td>);
print qq(<tr><td><input type="button" value="<<<" id="trany$i" onclick="inser('surlist','deslist');" style="width:80px" ></td></div>);
print qq(<input type="hidden" value="" id="paths">);
print qq(<input type="hidden" value="" id="pathd"></form>);
                                                 
                                                                                                            
