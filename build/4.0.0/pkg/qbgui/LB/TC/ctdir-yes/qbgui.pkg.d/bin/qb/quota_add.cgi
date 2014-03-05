#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
require ("qblib/proute.lib");

#認證是否是經過正常且標準的程序登入進來的
authenticate(action=>'RANDOMCHECK');

print "Content-type:text/html\n\n";

#---------------- Just for form to show available items of subnets and services ------------------
my  %action;
my  $form = new CGI;
$action{action} = $form->param('action');
$action{focusedvip} = $form->param('focusedvip');

my @publiciptodel=$form->param('publiciptodel');
$action{publiciptodel}=\@publiciptodel;

$action{isp_of_vip}=$form->param('isp_of_vip');

$action{viptoappend}=$form->param('set'.$action{isp_of_vip});

$action{dmit}=$form->param('dmit');
$action{dbps}=$form->param('dbps');
$action{umit}=$form->param('umit');
$action{ubps}=$form->param('ubps');
$action{cycle}=$form->param('cycle');
$action{chose}=$form->param('chose');
$action{hr}=$form->param('hr');
$action{sec}=$form->param('sec');
$action{bs}=$form->param('bs');
$action{ql}=$form->param('ql');
$action{lmit}=$form->param('lmit');

my $dmit,$dbps,$umit,$ubps,$cycle,$chose,$mhr,$msec,$bs,$ql,$lmit,$tmit,$tbps = '';
if($action{dmit} != ''){$dmit=$action{dmit};}
if($action{dbps} != ''){$dbps=$action{dbps};}
if($action{umit} != ''){$umit=$action{umit};}
if($action{ubps} != ''){$ubps=$action{ubps};}
if($action{cycle} != ''){$cycle=$action{cycle};}
if($action{chose} != ''){$chose=$action{chose};}
if($action{hr} != ''){$mhr=$action{hr};}
if($action{sec} != ''){$msec=$action{sec};}
if($action{bs} != ''){$bs=$action{bs};}
if($action{ql} != ''){$ql=$action{ql};}
if($action{lmit} != ''){$lmit=$action{lmit};}
if($action{lmit} == ''){$lmit='10';}
if($bs eq '1'){$tmit=$dmit;$tbps=$dbps;}

print qq (<html><head><meta charset="UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head><body bgcolor="#336699" text="#ffffff" link="#000040">);

#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainVS( %action ); }

print qq(<div align="center">);
#------- start to draw every form object to interact with users --------------------------------

print qq(<form name="quotaform" method="post">);
print qq (<table class="body" cellspacing="0" border="0">);
print qq (<tr><td>);

print qq (<tr><td class="bigtitle" colspan="2">Quota Setting);
print qq (<hr size=1>);

###################################################################################
	print qq (<tr>);
	print qq (<td>Limit :&nbsp; </td>);
	print qq (<td>);
	print qq (<select class="qb" id="bs" style="WIDTH:110px" onchange="bs_change()">);
	if ($bs eq '0')
	{
		print qq (<option value="0" Selected>by Up/Down</option>);
		print qq (<option value="1">by Total</option>);
	}
	if ($bs eq '1')
	{
		print qq (<option value="0">by Up/Down</option>);
		print qq (<option value="1" Selected>by Total</option>);
	}
	if (!$bs)
	{
		print qq (<option value="0">by Up/Down</option>);
		print qq (<option value="1">by Total</option>);
	}
	print qq (</select></td></tr>);
	
	print qq (<tr id="dview" style="display:'none';"><td width="auto">Limit Downlink at :</td>);
    	print qq (<td width="auto" align="center"><input type="text" class="qbtext" id="dmit" style="WIDTH:45px" maxlength="4" value="$dmit" onchange="U_change()"/>);
    	print qq (<select class="qb" id="dbps" style="WIDTH:60px" value="$dbps"><br>);
	if ($dbps eq '1024')
	{
		print qq (<option value="K" Selected>KB</option>);
		print qq (<option value="M">MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T">TB</option>);
	}
	if ($dbps eq '1048576')
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M" Selected>MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T">TB</option>);
	}
	if ($dbps eq '1073741824')
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M">MB</option>);
		print qq (<option value="G" Selected>GB</option>);
		print qq (<option value="T">TB</option>);
	}
	if ($dbps eq '1099511627776')
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M">MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T" Selected>TB</option>);
	}
	if (!$dbps)
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M" Selected>MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T">TB</option>);
	}
    print qq (</select></td></tr>);
    print qq (<tr id="uview" style="display:'none';"><td>Limit Uplink at : </td>);
    print qq (<td align="center"><input type="text" class="qbtext" id="umit" style="WIDTH:45px" maxlength="4" value="$umit"/>);
    print qq (<select class="qb" id="ubps" style="WIDTH:60px" value="$ubps"><br>);
	if ($ubps eq '1024')
	{
		print qq (<option value="K" Selected>KB</option>);
		print qq (<option value="M">MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T">TB</option>);
	}
	if ($ubps eq '1048576')
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M" Selected>MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T">TB</option>);
	}
	if ($ubps eq '1073741824')
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M">MB</option>);
		print qq (<option value="G" Selected>GB</option>);
		print qq (<option value="T">TB</option>);
	}
	if ($ubps eq '1099511627776')
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M">MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T" Selected>TB</option>);
	}
	if (!$ubps)
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M" Selected>MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T">TB</option>);
	}
    print qq (</select></td></tr>);
	print qq (<tr id="tview" style="display:'none';"><td>Limit Total at : </td>);
    print qq (<td align="center"><input type="text" class="qbtext" id="tmit" style="WIDTH:45px" maxlength="4" value="$tmit"/>);
    print qq (<select class="qb" id="tbps" style="WIDTH:60px" value="$tbps"><br>);
	if ($tbps eq '1024')
	{
		print qq (<option value="K" Selected>KB</option>);
		print qq (<option value="M">MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T">TB</option>);
	}
	if ($tbps eq '1048576')
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M" Selected>MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T">TB</option>);
	}
	if ($tbps eq '1073741824')
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M">MB</option>);
		print qq (<option value="G" Selected>GB</option>);
		print qq (<option value="T">TB</option>);
	}
	if ($tbps eq '1099511627776')
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M">MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T" Selected>TB</option>);
	}
	if (!$tbps)
	{
		print qq (<option value="K">KB</option>);
		print qq (<option value="M" Selected>MB</option>);
		print qq (<option value="G">GB</option>);
		print qq (<option value="T">TB</option>);
	}
    print qq (</select></td></tr>);
    print qq (<tr><td> Cycle : </td><td align="center"><select class="qb" id="cycle" style="WIDTH:105px" onChange="cycleChange();">);
	if ($cycle eq '0')
	{
		print qq (<option value="0" Selected>non-cyclic</option>);
		print qq (<option value="1">Daily</option>);
		print qq (<option value="7">Weekly</option>);
		print qq (<option value="30">Monthly</option>);
	}
	elsif ($cycle eq '1')
	{
		print qq (<option value="0">non-cyclic</option>);
		print qq (<option value="1" Selected>Daily</option>);
		print qq (<option value="7">Weekly</option>);
		print qq (<option value="30">Monthly</option>);
	}
	elsif ($cycle eq '7')
	{
		print qq (<option value="0">non-cyclic</option>);
		print qq (<option value="1">Daily</option>);
		print qq (<option value="7" Selected>Weekly</option>);
		print qq (<option value="30">Monthly</option>);
	}
	elsif ($cycle eq '30')
	{
		print qq (<option value="0">non-cyclic</option>);
		print qq (<option value="1">Daily</option>);
		print qq (<option value="7">Weekly</option>);
		print qq (<option value="30" Selected>Monthly</option>);
	}
	elsif (!$cycle)
	{
		print qq (<option value="0">non-cyclic</option>);
		print qq (<option value="1">Daily</option>);
		print qq (<option value="7">Weekly</option>);
		print qq (<option value="30">Monthly</option>);
	}
    # print qq (<option value="0">non-cyclic</option>);
    # print qq (<option value="1">Daily</option>);
    # print qq (<option value="7">Weekly</option>);
    # print qq (<option value="30">Monthly</option>);
    print qq (</select></td></tr>);
    print qq (<tr><td> Reset at :</td>);
    print qq (<td align="center"><select class="qb" id="hr" style="WIDTH:50px;">);
    foreach my $hr (0..23)
	{
		if($hr < 10)
		{
			$myhr = "0$hr";
			$myhr2 = "$mhr";
			if ($myhr eq $myhr2)
			{
				print qq(<option value="0$hr" Selected>0$hr</option>);
			}
			else
			{
				print qq(<option value="0$hr">0$hr</option>);
			}
		}
		if($hr > 9)
		{
			$myhr = "$hr";
			$myhr2 = "$mhr";
			if ($myhr eq $myhr2)
			{
				print qq(<option value="$hr" Selected>$hr</option>);
			}
			else
			{
				print qq(<option value="$hr">$hr</option>);
			}
		}
	}
    print qq (</select>:<select class="qb" id="sec" style="WIDTH:50px">);
    foreach my $sec (0..59)
	{
		if($sec > 9)
		{
			$mysec = "$sec";
			$mysec2 = "$msec";
			if ($mysec eq $mysec2)
			{
				print qq(<option value="$sec" Selected>$sec</option>);
			}
			else{print qq(<option value="$sec">$sec</option>);}
		}
	
		if($sec < 10)
		{
			$mysec = "0$sec";
			$mysec2 = "$msec";
			if ($mysec eq $mysec2)
			{
				print qq(<option value="0$sec" Selected>0$sec</option>);
			}
			else{print qq(<option value="0$sec">0$sec</option>);}
		}
	}
    print qq (</select></td></tr><tr>);
    my @week=("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
	my $weeknum=0;
	print qq (<td id="week" style="display:none;" colspan="2">);
    foreach my $day ( @week )
    {
         if ($cycle eq '7' && $weeknum eq $chose)
		{
			print qq (<INPUT type="radio" name="week" id="selectDay" value="$weeknum" checked/> $day&#32&#32);
		}
		else
		{
			print qq (<INPUT type="radio" name="week" id="selectDay" value="$weeknum" /> $day&#32&#32);
		}
		#print qq (<INPUT type="radio" name="week" id="selectDay" value="$day"/> $day&#32&#32);
		if($weeknum eq 3){print qq(<br>);}
		#if($weeknum eq 5){print qq(<br>);}
		$weeknum++;
    }
    print qq (</select></td></tr>);
	print qq (<tr id="monthly" style="visibility:hidden;"><td>Day : </td>);
    print qq (<td><select class="qb" id="number" style="WIDTH:50px">);
    foreach my $month (1..30)
    {
        if ($month < 10)
        {
            if ($cycle eq '30' && $month eq $chose)
			{
				print qq (<option value="$month" Selected>0$month</option>);
			}
			else
			{
				print qq (<option value="$month">0$month</option>);
			}
        }else
        {
            if ($cycle eq '30' && $month eq $chose)
			{
				print qq (<option value="$month" Selected>$month</option>);
			}
			else
			{
				print qq (<option value="$month">$month</option>);
			}
        }
    }
    print qq (</select></td></tr>);
	
	print qq (<td>When Quota full :&nbsp; </td>);
	print qq (<td>);
	print qq (<select class="qb" id="ql" style="WIDTH:110px" onchange="WQFChange()">);
	if ($ql eq '0')
	{
		print qq (<option value="0" Selected>Block</option>);
		print qq (<option value="1">Limit speed</option>);
	}
	if ($ql eq '1')
	{
		print qq (<option value="0">Block</option>);
		print qq (<option value="1" Selected>Limit speed</option>);
	}
	if (!$ql)
	{
		print qq (<option value="0">Block</option>);
		print qq (<option value="1">Limit speed</option>);
	}
	print qq (</select></td></tr>);
	print qq (<tr id="show_limit" style="visibility:hidden;"><td>Limit Speed at : </td>);
    print qq (<td><input type="text" class="qbtext" id="lmit" style="WIDTH:45px" maxlength="4" value="$lmit"/> Packet/s);
    print qq (</td></tr>);
###################################################################################

print qq (<tr><td colspan="2"><hr size=1></td></tr>);
print qq (<tr><td colspan="2">);
print qq (<div class="body" align="center">);
print qq (<input type="button" class="qb" align="center" value="Save" style="width:60" onClick="myalert()">);
print qq (<input type="button" class="qb" align="center" value="Cancel" style="width:60" onClick="window.close()">);
print qq (<div>);
print qq (</td></tr>);

iniroute_script();

print qq (</td></tr>);
print qq (</table>);

print qq(<input type="hidden" name="action" value="">);
print qq(</form></div>);

general_script();

print qq(<SCRIPT LANGUAGE="JavaScript">cycleChange(); U_change(); bs_change(); WQFChange();</SCRIPT>);
print qq(</body></html>);
