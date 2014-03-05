#!/usr/bin/perl
use Data::Dumper;
use CGI;

#require ("qbmod.cgi");

#認證是否是經過正常且標準的程序登入進來的
#authenticate(action=>'RANDOMCHECK');

	print "Content-type:text/html\n\n";
	print qq (<html>);
	print qq (<head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
	print qq (<body bgcolor="#336699" text="#ffffff" link="#000040" >);
	

#假如認證失敗，就直接結束
#if ( !$gLOGINRESULT ) { general_script(); exit;}
	
#Title
	print qq (<table bgcolor="#336699" cellspacing="3" border="0" align="center">);
	print qq (<tr><td class="bigtitle">Black List );
	print qq (</td> </tr> </table>);
	print qq (<hr size=1 width="80%">);

#================== Start Show Black List =====================================

	print qq (<div align="center" id="all" class="divframe">);
	print qq (<form name="ispform" method="post" action="showblacklist.cgi">);
	print qq (<table cellspacing="0" border="0" width="100%">);
	
# Get Black List 
	#my $allblacklist=runCommand(command=>'cat' ,params=>'/usr/local/apache/active/userlock_list');
	#my $allblacklist=`cat /usr/local/apache/active/userlock_list`;
	my $allblacklist=`cat /tmp/userlock_list`;
	my @allblackarray=split('\n',$allblacklist);
	
	#print qq (<tr><td>);
	#print qq (<a>Search :</a><input class="qbopt" id="search" type="text" value="" style="width:60%">);
	#print qq (</td></tr>);
	print qq (<tr><td > Expain: Blocked IP [remaining time] min</td></tr>);
	#print qq (<tr><td align="left"> Expain: </td></tr>);
	#print qq (<tr><td align="right"> Blocked IP [remaining time] min </td></tr>);
	print qq (<tr><td><select class="qbopt1" multiple id="menu" size="15" style="width:75%">);

	foreach my $black (@allblackarray)
	{
	    if ( $black eq '' ) {next ; }
	    my @IP_time = split (/ /,$black);
	    my $remaining_time=`/usr/local/apache/qb/setuid/calculate_remaining_time.sh $IP_time[1]`;
	    print qq (<option value="$IP_time[0]">$IP_time[0] [ $remaining_time] min);
	}
	print qq(</select></td>);
	print qq (</tr>);
	print qq (<tr><td><input class="qb" id="del" type="button" value="Delete" style="float:center"/></td></tr>);

	print qq (</table>);
	print qq (</form></div>);
	print qq (</body></html>);
	
print << "BLACK";

<script type="text/javascript" src="jquery-1.9.1.min.js"></script>
<script language="javascript">

	\$("#search").change(function(){
	    var text = \$(this).val();
	    \$("#menu option[value='" + text + "']").attr("selected","selected");
	});

	\$("#del").click(function(){
	    var delip = \$("#menu").val();
	    //alert(delip.length);
	    for (var i = 0; i < delip.length; i++)
	    {
	      \$("#menu option[value='" + delip[i] + "']").remove();
	      var a=delip[i];
	      \$.get("delblacklist.cgi",{delip:a},function
	    	  (data){
	    	  }
	      );
            }
	});

</script>
BLACK

