#!/usr/bin/perl
        
BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
require ("/usr/local/apache/qb/qbmod.cgi");
$cgi=CGI->new();
$action=$cgi->param("action");
if ($action eq "CHECK")
{
    my $sleepfile = runCommand(command=>'/bin/ls',params=>'/tmp/ |grep sleep' );
    if ($sleepfile eq "")
    {
        runCommand(command=>'/bin/mkdir',params=>'sleep' );
    }
    else
    {
	$sleepfile =~ s/sleep//;
	$sleepfile =~ s/\s//;
	if ($sleepfile eq 10)
	{
	    $action = "RESET";
	}
	else
	{
	    $sleeptmp = $sleepfile;
	    $sleeptmp++;
	    system "/bin/mv","/tmp/sleep$sleepfile","/tmp/sleep$sleeptmp";
	}
    }
}
if ($action eq "UPDATE")
{
        my $zone=XMLread('/usr/local/apache/qbconf/zonecfg.xml');
        my $zonelist=$zone->{nat};
        foreach my $nic ( @$zonelist )
        {
            if ($nic->{natid} eq 'system' || $nic->{network} eq ""){next;}
            $name = $nic->{network};
            $name =~ s/\/.*//;
            $datadir = -e "/usr/local/apache/qb/Log_file";
            if (!$datadir){runCommand(command=>'/bin/mkdir', params=>"/usr/local/apache/qb/Log_file");}
            runCommand(command=>'/usr/local/apache/qb/setuid/lantrafficlog.sh ', params=>qq ($nic->{network}).' '.qq ($name));
        }
}
elsif ($action eq "RESET")
{
    @filestr = ();
    my @file = runCommand(command=>'ls',params=>'/proc/net/ipt_account/');
    foreach my $name (@file)
    {
        $size = -s "/usr/local/apache/qb/Log_file/$name";
    	if($size >307220)
    	{  
            open(FILE,"/usr/local/apache/qb/Log_file/$name") or  "open file error" ; 
            while(<FILE>)
            { 
	    	my $input=<FILE>;
	    	push(@filestr,$input);
            }
            close (FILE);
	
            open(write_file,">/usr/local/apache/qb/Log_file/$name") or  "open file error" ;
	
            splice(@filestr,0,$#filestr-256);
            print write_file  @filestr; 
            close (write_file);
    	}
    	runCommand(command=>'/usr/local/apache/qb/setuid/lantrafficlog.sh ', params=>qq(qq("None").' '.qq ($name)));
    }
}
