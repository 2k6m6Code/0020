#!/usr/bin/perl
require ("/usr/local/apache/qb/global.cgi");
use XML::Simple;
use Data::Dumper;
use CGI;

$cgi=new CGI;
@filenamearray=('english.xml','french.xml','chinese.xml','english_flow.xml');  #limit filename to display 
$filename = $cgi->param('name');
if(! grep { $_ eq $filename} @filenamearray){
	return;
}

# create object
$xml = new XML::Simple(NoSort => 1,ForceArray => 1);

# read XML file
$data = $xml->XMLin($filename);

print "Content-Type:text/xml\n\n";

if ($filename eq "english_flow.xml")
{
    print $xml->XMLout($data, XMLDecl => $dec, RootName => 'treemenu');
}
    

# print Dumper($data);
# $data->{'menu'}[1] = "";
# print Dumper($data->{'menu'}[0]);
# print $gENABLEQOS;

if(!$gENABLEWIRELESS){
$data->{'menu'}[2]->{'child'}[0]->{'menu'}[2] ="";  	#LAN Setup -> Wireless LAN Setting
$data->{'menu'}[3]->{'child'}[0]->{'menu'}[9] ="";  	#Interface -> Wireless LAN Setting
}

if(!$gENABLECMS){
$data->{'menu'}[22]->{'child'}[0]->{'menu'}[1] =""; 	#Firmware
$data->{'menu'}[22]->{'child'}[0]->{'menu'}[2] =""; 	#Config
}
if( -d '/mnt/tclog/analyser/etc/httpd'){

}else{
$data->{'menu'}[21]->{'child'}[0]->{'menu'}[4] =""; 	#Logs and Reports -> Traffic Analyzer
}
if($gTYPE ne "SG" && $gTYPE ne "Mesh"){
#$data->{'menu'}[12] =""; 				#Web Filtering
$data->{'menu'}[14]->{'child'}[0]->{'menu'}[0] =""; 	#L2TP IPsec VPN
$data->{'menu'}[14]->{'child'}[0]->{'menu'}[2] =""; 	#SSL Server
}
if($filename eq 'french.xml'){
 $dec = '<?xml version="1.0" encoding="ISO-8859-1"?>';
}else{
 $dec = '<?xml version="1.0" encoding="utf-8"?>';
}
if (!$gENABLETM)
{
$data->{'menu'}[0]->{'child'}[0]->{'menu'}[1] ="";      #Status -> Online User
$data->{'menu'}[0]->{'child'}[0]->{'menu'}[5] ="";      #Status -> Real-time Behaviors
$data->{'menu'}[0]->{'child'}[0]->{'menu'}[7] ="";      #Status -> Sessions
$data->{'menu'}[1]->{'child'}[0]->{'menu'}[5] ="";      #Link Setup -> IPSec
$data->{'menu'}[1]->{'child'}[0]->{'menu'}[6] ="";      #Link Setup -> MAC
$data->{'menu'}[1]->{'child'}[0]->{'menu'}[7] ="";      #Link Setup -> Quota
$data->{'menu'}[2]->{'child'}[0]->{'menu'}[1] ="";      #LAN Setup -> Static ARP Setting
#$data->{'menu'}[2]->{'child'}[0]->{'menu'}[2] ="";      #LAN Setup -> Wireless LAN Setting
$data->{'menu'}[2]->{'child'}[0]->{'menu'}[3] ="";      #LAN Setup -> Transparent Setting
$data->{'menu'}[2]->{'child'}[0]->{'menu'}[4] ="";      #LAN Setup -> Vlan Setting
$data->{'menu'}[3]->{'name'}[0] ="";			#Interface
$data->{'menu'}[4]->{'child'}[0]->{'menu'}[6] ="";      #Network -> SNMP
$data->{'menu'}[4]->{'child'}[0]->{'menu'}[7] ="";      #Network -> MPV
$data->{'menu'}[4]->{'child'}[0]->{'menu'}[8] ="";      #Network -> TMV
$data->{'menu'}[4]->{'child'}[0]->{'menu'}[9] ="";      #Network -> IP
$data->{'menu'}[5]->{'child'}[0]->{'menu'}[3] ="";      #Policy -> Service Grouping
$data->{'menu'}[5]->{'child'}[0]->{'menu'}[5] ="";      #Policy -> File Extension
$data->{'menu'}[5]->{'child'}[0]->{'menu'}[6] ="";      #Policy -> Layer7
$data->{'menu'}[7]->{'name'}[0] ="";                    #Authentication
$data->{'menu'}[9]->{'child'}[0]->{'menu'}[3] ="";  	#Bandwidth Management -> MPV
$data->{'menu'}[9]->{'child'}[0]->{'menu'}[4] ="";  	#Bandwidth Management -> TMV
$data->{'menu'}[9]->{'child'}[0]->{'menu'}[5] ="";  	#Bandwidth Management -> Policy for Real Servers
$data->{'menu'}[12]->{'name'}[0] ="";			#Internet to LAN
$data->{'menu'}[13]->{'child'}[0]->{'menu'}[0] ="";     #Web Filter -> General Setting
$data->{'menu'}[13]->{'child'}[0]->{'menu'}[5] ="";     #Web Filter -> HTTP Content Filtering
$data->{'menu'}[13]->{'child'}[0]->{'menu'}[6] ="";     #Web Filter -> Category
$data->{'menu'}[13]->{'child'}[0]->{'menu'}[7] ="";     #Web Filter -> Filtering By Category
$data->{'menu'}[16]->{'name'}[0] ="";			#Firewall
$data->{'menu'}[19]->{'child'}[0]->{'menu'}[3] =""; 	#System -> DNS
$data->{'menu'}[19]->{'child'}[0]->{'menu'}[4] =""; 	#System -> Dynamic Routing
$data->{'menu'}[19]->{'child'}[0]->{'menu'}[5] =""; 	#System -> External Storage 
#$data->{'menu'}[19]->{'child'}[0]->{'menu'}[10] =""; 	#System -> SNMP
$data->{'menu'}[19]->{'child'}[0]->{'menu'}[12] =""; 	#System -> Web Proxy
}
if ($gENABLETM){
$data->{'menu'}[0]->{'child'}[0]->{'menu'}[2] ="";      #Status -> Link
$data->{'menu'}[0]->{'child'}[0]->{'menu'}[3] ="";      #Status -> LAN host
$data->{'menu'}[0]->{'child'}[0]->{'menu'}[4]->{'name'}[0] ="Flow Status";      #change Name User Flow <-> Flow Status
$data->{'menu'}[0]->{'child'}[0]->{'menu'}[7] ="";      #Status -> Sessions
$data->{'menu'}[1] ="";  				#Link Setup
$data->{'menu'}[2] ="";  				#LAN Setup
$data->{'menu'}[3]->{'child'}[0]->{'menu'}[6]="";  	#Network -> Health Check
$data->{'menu'}[3]->{'child'}[0]->{'menu'}[7]="";  	#Network -> Link IP Binding
$data->{'menu'}[3]->{'child'}[0]->{'menu'}[8]="";  	#Network -> MPV
$data->{'menu'}[3]->{'child'}[0]->{'menu'}[9]="";  	#Network -> TMV
$data->{'menu'}[3]->{'child'}[0]->{'menu'}[10]="";  	#Network -> IPSec
$data->{'menu'}[3]->{'child'}[0]->{'menu'}[11]="";  	#Network -> Wireless
$data->{'menu'}[4] ="";  				#Bandwidth Shaper
$data->{'menu'}[5]->{'child'}[0]->{'menu'}[3] ="";      #Policy -> Service Grouping
$data->{'menu'}[5]->{'child'}[0]->{'menu'}[5] ="";      #Policy -> File Extension
$data->{'menu'}[5]->{'child'}[0]->{'menu'}[6] ="";      #Policy -> Layer7
$data->{'menu'}[6] ="";  				#Server Mapping
$data->{'menu'}[9]->{'child'}[0]->{'menu'}[3] ="";  	#Bandwidth Management -> MPV
$data->{'menu'}[9]->{'child'}[0]->{'menu'}[4] ="";  	#Bandwidth Management -> TMV
$data->{'menu'}[9]->{'child'}[0]->{'menu'}[5] ="";  	#policy for real servers
$data->{'menu'}[12] ="";  				#VPN
$data->{'menu'}[13]->{'child'}[0]->{'menu'}[0] ="";     #Web Filter -> General Setting
$data->{'menu'}[14] ="";  				#VPN
$data->{'menu'}[15] ="";  				#Inbound Multi-DNS
$data->{'menu'}[16] ="";  				#old Firewall
$data->{'menu'}[17] ="";  				#Authentication
$data->{'menu'}[18] ="";  				#HA
$data->{'menu'}[19]->{'child'}[0]->{'menu'}[3] =""; 	#System -> DNS
$data->{'menu'}[19]->{'child'}[0]->{'menu'}[4] =""; 	#System -> Dynamic Routing
$data->{'menu'}[19]->{'child'}[0]->{'menu'}[5] =""; 	#System -> External Storage 
$data->{'menu'}[19]->{'child'}[0]->{'menu'}[8] =""; 	#System -> TCP Optimization
$data->{'menu'}[19]->{'child'}[0]->{'menu'}[10] =""; 	#System -> SNMP
$data->{'menu'}[19]->{'child'}[0]->{'menu'}[12] =""; 	#System -> Web Proxy
$data->{'menu'}[22] =""; 				#Central Management
}

if ($filename ne "english_flow.xml")
{
print $xml->XMLout($data, XMLDecl => $dec, RootName => 'treemenu');
}

