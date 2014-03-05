#!/usr/bin/perl

open(FILE,"</usr/local/apache/qbconf/zonecfg.xml");
open(FILE1,">/tmp/zonecfg.xml");
my $isp;
my $inter;
foreach my $data (<FILE>)
{
    if (grep(/BRIDGE/,$data) && !grep(/interface/,$data))
    {
        my @tmp = split(/ /,$data);
	foreach my $data1 (@tmp)
	{
	    if (!grep(/isp/,$data1)){next;}
	    $data1=~s/isp="//g;
	    $data1=~s/"$//g;
	    $isp=$data1;
	}
	open(FILE2,"</usr/local/apache/active/basic.xml");
	foreach my $basic (<FILE2>)
	{
	   if (grep(/iid="$isp"/,$basic))
	   {
	       my @tmp1 = split(/ /,$basic);
	       foreach my $data2 (@tmp1)
	       {
	           if (!grep(/nic=/,$data2)){next;}
	           $data2=~s/nic="//g;
	           $data2=~s/"$//g;
	           $inter=$data2;
	       }
	   }
	}
	
	$data =~ s/enabled="1"/enabled="1" name="br0" interface="$inter"/g;
    }
    print FILE1 $data;
}
close(FILE);
close(FILE1);

if ((-e "/tmp/zonecfg.xml") || !(-z "/tmp/zonecfg.xml"))
{
    system("/bin/cp -a /tmp/zonecfg.xml /usr/local/apache/active/");
    system("/bin/cp -a /tmp/zonecfg.xml /usr/local/apache/qbconf/");
}
