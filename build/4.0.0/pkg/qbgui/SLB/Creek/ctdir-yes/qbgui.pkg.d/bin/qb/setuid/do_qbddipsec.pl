#!/usr/bin/perl
 
require ('/usr/local/apache/qb/qbmod.cgi');

my $QB_BASIC = "/usr/local/apache/qbconf/basic.xml";
my $ispinfo = XMLread($QB_BASIC);
my $isplist = $ispinfo->{isp};
my $transport = "ipsec esp/transport//require ah/transport//require";
my $transport_ipcomp = "ipsec ipcomp/transport//use esp/transport//require ah/transport//require";
my $ispid = $ARGV[0];
#-----------------------------------------------------------------
if ( $ispinfo ) #if the string is NULL
{
    print "$QB_BASIC_FILE is NULL \n";
}
#------------------------------------------------------------------    
       
foreach my $isp ( @$isplist )
{
    if ( ($isp->{iid} == $ispid) && ( $isp->{enc} ))
    {
        my $QB_IPSEC_DELCONF = "/etc/racoon/delipsec." . $isp->{ispname};
 	my $QB_IPSEC_ADDCONF = "/etc/racoon/addipsec." . $isp->{ispname};
        if ( !open(IPSECADD,">$QB_IPSEC_ADDCONF") )
        {
            print qq (Fail to Open IPSEC AddConfig file !!);
	}
        if ( !open(IPSECDEL,">$QB_IPSEC_DELCONF") )
        {
            print qq (Fail to Open IPSEC DelConfig file !!);
	}
	my $ipsecmode = ( $isp->{ipcom} ) ? ( $transport_ipcomp ) : ( $transport );
	print IPSECADD qq "#!/sbin/setkey -f\n";
        print IPSECADD qq "spdadd $isp->{local} $isp->{remote} any -P out $ipsecmode;\n";
        print IPSECADD qq "spdadd $isp->{remote} $isp->{local} any -P in $ipsecmode;\n";
	print IPSECDEL qq "#!/sbin/setkey -f\n";
        print IPSECDEL qq "spddelete $isp->{local} $isp->{remote} any -P out $ipsecmode;\n";
        print IPSECDEL qq "spddelete $isp->{remote} $isp->{local} any -P in $ipsecmode;\n";
        close(IPSECADD);
        close(IPSECDEL);
    }
    if ( ($isp->{iid} == $ispid) && ( $isp->{isptype} eq "ipsec" ))
    {
    	my $QB_IPSEC_DELCONF = "/etc/racoon/delipsec." . $isp->{ispname};
    	my $QB_IPSEC_ADDCONF = "/etc/racoon/addipsec." . $isp->{ispname};
    	if ( !open(IPSECADD,">$QB_IPSEC_ADDCONF") )
    	{
    		print qq (Fail to Open IPSEC AddConfig file !!);
    	}
    	if ( !open(IPSECDEL,">$QB_IPSEC_DELCONF") )
    	{
    	        print qq (Fail to Open IPSEC DelConfig file !!);
    	}
 	my $out = $isp->{local} . "-" . $isp->{remote};
 	my $in = $isp->{remote} . "-" . $isp->{local};   	   
 	print IPSECADD qq "#!/sbin/setkey -f\n";
 	print IPSECADD qq "spdadd $isp->{localsubnet} $isp->{remotesubnet} any -P out ipsec ";                                                                             
 	print IPSECADD qq "$isp->{protocol}/tunnel/$out/unique;\n";
 	print IPSECADD qq "spdadd $isp->{remotesubnet} $isp->{localsubnet} any -P in ipsec ";
 	print IPSECADD qq "$isp->{protocol}/tunnel/$in/unique;\n";
 	print IPSECDEL qq "#!/sbin/setkey -f\n";
 	print IPSECDEL qq "spddelete $isp->{localsubnet} $isp->{remotesubnet} any -P out ipsec ";
 	print IPSECDEL qq "$isp->{protocol}/tunnel/$out/unique;\n";
 	print IPSECDEL qq "spddelete $isp->{remotesubnet} $isp->{localsubnet} any -P in ipsec ";
 	print IPSECDEL qq "$isp->{protocol}/tunnel/$in/unique;\n";
 	close(IPSECADD);
 	close(IPSECDEL);
    }
}
