#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
use QB_Action;

my $cgi = CGI->new();
my $act = QB_Action->new();
my $type = $cgi->param("type");
my $date = $cgi->param("date");
my $dig = $cgi->param("dig");

print "Content-type: text/html\n\n";
$date =~ s/\/0/\//g;
if ($type eq 'auth'){$PATH = "/mnt/tclog/auth/";}
my %name_index;
my @table_name;
my @title;
if (!$dig)
{
    my @auth_name = $act->getdir($PATH);
    foreach my $name (@auth_name)
    {
        my @index  = $act->getfile("$PATH"."$name"."/"."$date");
        $name_index{$name} = ($#index+1);
    }
    @title=('Top','Account','Count');
}else
{
    @table_name  = $act->getfile("$PATH"."$dig"."/"."$date");
    if ($dig eq 'suspicious'){@title=('Time','IP','Account','Status');}
    else{@title=('Time','IP','Status');}
}
print qq (<table bgcolor="#332211" width="100%" border="0" id="tables">);
my $lineCount = 1;
my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
#==========title===============================
print qq (<thead><tr>);
creat_title(@title);
print qq (</tr></thead>);
if (!$dig)
{
    foreach my $name (sort {$name_index{$b} <=> $name_index{$a}} keys %name_index)
    {
    	if ($name_index{$name} < 1 ){next;}
    	print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
    	print qq (<td width="200" align="center">$lineCount</td>);    
    	print qq (<td width="200" align="center">$name</td>);    
    	print qq (<td width="200" align="center"><a href="javascript:myapp.view.presenter.query(myapp.view.\$input_date.val(),'$name')">$name_index{$name}</a></td></tr>);
    	$lineCount++;
    }
}else
{
    foreach my $list (@table_name)
    {
        my @name = split(/\s+/,$list);
    	print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
    	print qq (<td width="200" align="center">$name[0] $name[1]</td>);    
    	print qq (<td width="200" align="center">$name[2]</td>);    
    	if ($dig eq 'suspicious'){print qq (<td width="200" align="center">$name[4]</td>);}
    	print qq (<td width="200" align="center">$name[3]</td>);    
    }
}    
print qq (</table>);

sub creat_title
{
    my (@title)=@_;
    foreach (@title){print qq (<th style="width: 200px;">$_</th>);}
}

