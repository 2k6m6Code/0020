#!/usr/bin/perl
 
require ('/usr/local/apache/qb/qbmod.cgi');

my $QB_BASIC = "/usr/local/apache/qbconf/basic.xml";
my $QB_RACOON_CONF = "/etc/racoon/racoon.conf";
my $QB_SETKEY = "/etc/racoon/psk.txt";
my $ispinfo = XMLread($QB_BASIC);
my $isplist = $ispinfo->{isp};

#-----------------------------------------------------------------
if ( $ispinfo ) #if the string is NULL
{
    print "$QBHA_SNMP_FILE is NULL \n";
}
#------------------------------------------------------------------
if ( !open(RACOON,">$QB_RACOON_CONF") )
{
    print qq (Fail to Open RACOON Config file !!);
}
#------------------------------------------------------------------    

#------------------------------------------------------------------
if ( !open(PSK,">$QB_SETKEY") )
{
    print qq (Fail to Open PSK Config file !!);
}
#------------------------------------------------------------------
print RACOON qq "path pre_shared_key \"/etc/racoon/psk.txt\";\n";
print RACOON qq "path certificate \"/etc/racoon/certs\";\n";
#print RACOON qq "sainfo anonymous {\n";
#print RACOON qq "pfs_group 2;\n";
#print RACOON qq "lifetime time 3 min;\n";
#print RACOON qq "encryption_algorithm aes;\n";
#print RACOON qq "authentication_algorithm hmac_sha1, hmac_md5;\n";
#print RACOON qq "compression_algorithm deflate; }\n";
print RACOON qq "listen {\n";
#print RACOON qq "{\n";

foreach my $isp ( @$isplist )
{
	if ( $isp->{enc} || $isp->{isptype} eq "ipsec" )
	{
		if($isp->{isptype} eq "ipsec" && $isp->{enabled} eq "0"){next;}
		print RACOON qq	"\tisakmp $isp->{local} [500];\n";
          	if ( $isp->{mpv_nat} )
          	{
		print RACOON qq "\tisakmp_natt $isp->{local} [4500];\n";
		}
	}
}
print RACOON qq "\tadminsock \"\/var\/racoon\/racoon.sock\" \"root\" \"operator\" 0660;\n";
print RACOON qq "}\n\n";

#print RACOON qq "timer\n";
#print RACOON qq "{\n";
#print RACOON qq "\tcounter 6;\n";
#print RACOON qq "\tinterval 30 sec;\n";
#print RACOON qq "\tpersend 1;\n";
#print RACOON qq "\tphase1 20 sec;\n";
#print RACOON qq "\tphase2 30 sec;\n";
#print RACOON qq "}\n\n";

foreach my $isp ( @$isplist )
{
	if ( $isp->{enc} )
	{
		#postqb_general grep tunnel racoon.conf
		print RACOON qq "#ipsec mpv tunnel encrypt\n";
		print RACOON qq "remote $isp->{remote}\n";
		print RACOON qq "{\n";
		print RACOON qq "\texchange_mode main;\n";
		print RACOON qq "\tmy_identifier address;\n";
		print RACOON qq "\tproposal {\n";
		print RACOON qq "\tencryption_algorithm des;\n";
		print RACOON qq "\thash_algorithm sha1;\n";
		print RACOON qq "\tauthentication_method pre_shared_key;\n";
		print RACOON qq "\tdh_group 2;";
		print RACOON qq "\t}\n}\n\n";
		
		print RACOON qq "sainfo address $isp->{local}/32 any address $isp->{remote}/32 any\n";
		print RACOON qq "{\n";
		print RACOON qq "\tpfs_group 2;\n";
		print RACOON qq "\tlifetime time 3 hour;\n";
		print RACOON qq "\tencryption_algorithm $isp->{alg};\n";
		print RACOON qq "\tauthentication_algorithm hmac_sha1;\n";
		print RACOON qq "\tcompression_algorithm deflate;\n";
		print RACOON qq "}\n\n";
		
		print PSK qq "$isp->{remote}\tcreek26\n";
	}
	if ( $isp->{isptype} eq "ipsec" )
	{
		if($isp->{enabled} eq "0"){next;}
		#postqb_general grep tunnel racoon.conf
		print RACOON qq "#ipsec tunnel\n";
		if ( $isp->{remote} ne "0.0.0.0" ) #Brian 20130906 Brian For unknown NATed source IP
		{
		  print RACOON qq "remote $isp->{remote}\n";
		}else{
		  print RACOON qq "remote anonymous\n";
		}
		print RACOON qq "{\n";
		print RACOON qq "\texchange_mode $isp->{exchange};\n";
		print RACOON qq "\tmy_identifier $isp->{localid} \"$isp->{localdata}\";\n";
          	if ( $isp->{mpv_nat} )
          	{
		print RACOON qq "\tnat_traversal on;\n";
                }
		if ( $isp->{remote} eq "0.0.0.0" ) #Brian 20130906 Brian For unknown NATed source IP
		{
		print RACOON qq "\tgenerate_policy on;\n";
		print RACOON qq "\tpassive on;\n";
		}
		print RACOON qq "\tpeers_identifier $isp->{remoteid} \"$isp->{remotedata}\";\n";
		print RACOON qq "\tlifetime time $isp->{lifetime1} $isp->{timeformat1};\n";
		print RACOON qq "\tproposal {\n";
		print RACOON qq "\tencryption_algorithm $isp->{ph1alg};\n";
		print RACOON qq "\thash_algorithm $isp->{ph1hash};\n";
		print RACOON qq "\tauthentication_method pre_shared_key;\n";
		print RACOON qq "\t$isp->{dhgroup};\n";
		print RACOON qq "\t}\n}\n\n";
		
		print RACOON qq "sainfo address $isp->{localsubnet} any address $isp->{remotesubnet} any\n";
		print RACOON qq "{\n";
		if ( $isp->{pfgroup} ne "off" )
		{
			print RACOON qq "\t$isp->{pfgroup};\n";
		}
		print RACOON qq "\tlifetime time $isp->{lifetime2} $isp->{timeformat2};\n";
		print RACOON qq "\tencryption_algorithm $isp->{ph2alg};\n";
		print RACOON qq "\tauthentication_algorithm $isp->{ph2auth};\n";
		print RACOON qq "\tcompression_algorithm deflate;\n";
		print RACOON qq "}\n\n";
		
		if ( $isp->{remote} eq "0.0.0.0" ) #Brian 20130906 Brian For unknown NATed source IP
		{
		print PSK qq "\*\t$isp->{presharekey}\n";
		}else{
		print PSK qq "$isp->{remote}\t$isp->{presharekey}\n";
		}
	}
}
close(RACOON);
close(PSK);
runCommand(command=>"cat", params=>'/etc/racoon/racoon.l2tp'.' '.'>>/etc/racoon/racoon.conf');
