#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

require ("/usr/local/apache/qb/qbmod.cgi");

use CGI;
use Data::Dumper;
$cgi = CGI-> new();
$tm = $cgi->param("tm");
my $reflist = XMLread("/usr/local/apache/qbconf/auth.xml");
my $list = $reflist->{user};
require ("/usr/local/apache/qb/qbmod.cgi");
print "Content-type: text/html\n\n";
if ($tm ne '')
{
    my $path="/mnt/qb/conf/auth/";
    my @FileList;
    find( { wanted => sub { push(@FileList, $_) }, no_chdir => 1 }, $path );
    my $title = $FileList[1];
    $title=~s/\/mnt\/qb\/conf\/auth\///g;
    $title=~s/\.message//g;
    my ($type,$tmp)=split(/:/,$tm);
    my $time = time();
    
    if ($type eq 'none')
    {
        $time='';
    }elsif ($type eq 'forever')
    {
        $time += 1000000000; 
    }elsif ($type ne '' )
    {
        $time += ($type*3600);
    }
    
    $tmp=~s/,$//g;
    my @namelist = split(/,/,$tmp);
    foreach my $group (@$list)
    {
    	if ($group->{schname} eq 'system'){next;}
    	my $userlist=$group->{member};	
    	foreach $user (@$userlist)
    	{
       	    if (!grep(/^$user->{idd}$/,@namelist)){next;} 
           $user->{time} = $time;
           system("/usr/local/apache/qb/setuid/run /usr/bin/mutt -s \" $title \" $user->{mail} < $FileList[1] &");
           my $ip = $user->{ip};
           if ($ip eq ''){$ip = $user->{iip};}
           system("/usr/local/apache/qb/setuid/run /sbin/iptables -t nat -D AUTH -s $ip -j ACCEPT");
           
    	}
    }
XMLwrite($reflist, $gPATH."auth.xml");
}
print qq (<table bgcolor="#332211" width="100%" border="0" id="tables">);
print qq (<thead><tr><th style="width: 200px;">IP</th><th style="width: 200px;">Name</th><th style="width: 200px;">Time</th><th style="width: 200px;"><input type="button" value="Kick" onclick="kick();"><input type="checkbox" name="box" onClick="setAllCheckBoxValue('box', this.checked)"></th></tr></thead>);
my $lineCount = 0;
my $now_time = time()+(8*60*60);
foreach my $group (@$list)
{
    if ($group->{schname} eq 'system'){next;}
    my $userlist=$group->{member};	
    foreach $user (@$userlist)
    {
	if ($user->{idd} eq '' ){next;}
	if (($now_time - $user->{time}) < 0 || $user->{time} eq '' || ($now_time - $user->{time}) > 43200){next;}
	my $originalColor=my $bgcolor=($lineCount%2) ? ( '#556677' ) : ( '#334455' );
	print qq (<tr bgcolor="$bgcolor" originalColor="$originalColor" onmouseover="focusedColor(this)" onmouseout="blurColor(this)">);
	my $ip;
	if ($user->{ip} eq ''){$ip= "*".$user->{iip};}
	else{$ip= $user->{ip};}
	print qq (<td width="200" align="center" id="$nb">$ip</td>);
	print qq (<td width="200" align="center" >$user->{idd}</td>);
	my $oot=($user->{time})?($user->{time}):($user->{old_time});
	my $time = gmtime($oot);
	print qq (<td width="200" align="center" >$time</td>);
	#print qq (<td width="200" align="center" >$user->{time}</td>);
	print qq (<td width="200" align="center" >);
	print qq (<input type="checkbox" name="box" value="$user->{idd}"></td>);
	print qq (<td style="display:none"><a onclick="kick('$user->{idd}')" ><img src="../image/kick.png"></a></td>);
	print qq (</tr>);
	$lineCount++;
    }
}

