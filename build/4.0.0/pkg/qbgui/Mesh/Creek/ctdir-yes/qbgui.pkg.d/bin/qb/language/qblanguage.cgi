#!/usr/bin/perl
# require ("/usr/local/apache/qb/language/qblanguage.cgi");
# @qblang = QBlanguage();
# Find String command : find .| xargs grep "qblang\[123\]"
#<meta charset="UTF-8">
sub QBlanguage{
use CGI;
$cgi = new CGI;
$langcookie = $cgi->cookie('locale');

my @qblanguage;
if($langcookie eq "en_US"){
$qblanguage[0]  ="Auto Refresh Per";   #dashboard.lib
$qblanguage[1]  ="seconds";
$qblanguage[2]  ="System Status";
$qblanguage[3]  ="System Time";
$qblanguage[4]  ="System Uptime";
$qblanguage[5]  ="Firmware Version";
$qblanguage[6]  ="System Usage";
$qblanguage[7]  ="CPU Usage";
$qblanguage[8]  ="Memory Usage";
$qblanguage[9]  ="Cache Usage";
$qblanguage[10] ="Ramdisk Usage";
$qblanguage[11] ="Active Sessions";
$qblanguage[12] ="Device Information";
$qblanguage[13] ="Host Name";
$qblanguage[14] ="Model Name";
$qblanguage[15] ="MAC Address Range";
$qblanguage[16] ="Register Information";
$qblanguage[17] ="Serial Number";
$qblanguage[18] ="Registered Date";
$qblanguage[19] ="Not registered";
$qblanguage[20] ="Register Within";
$qblanguage[21] ="License Expiry";
$qblanguage[22] ="Warranty Expiry";
$qblanguage[23] ="WAN Link";
$qblanguage[24] ="Status";

$qblanguage[25] ="Edit"; #showbasic.lib
$qblanguage[26] ="Enable";
$qblanguage[27] ="3G Information";
$qblanguage[28] ="Interface";
$qblanguage[29] ="Name";
$qblanguage[30] ="Gateway";
$qblanguage[31] ="System IP";
$qblanguage[32] ="Healthcheck IP";
$qblanguage[33] ="Subnet";
$qblanguage[34] ="Down/Up";
$qblanguage[35] ="Version";
$qblanguage[36] ="Additional Subnet";
$qblanguage[37] ="Additional Subnet2";
$qblanguage[38] ="Proxy IP";
$qblanguage[39] ="Proxy Name";
$qblanguage[40] ="Proxy Port";


$qblanguage[41] ="Link Health Check";   #hcconf.lib
$qblanguage[42] ="Link Check Method";
$qblanguage[43] ="Ping to Healthcheck IP";
$qblanguage[44] ="Ping and Trace Route to Healthcheck IP";
$qblanguage[45] ="Port Checking to Healthcheck IP";
$qblanguage[46] ="Port Checking and Trace Route to Healthcheck IP";
$qblanguage[47] ="Advanced Setting";
$qblanguage[48] ="Disable Passive Line Check";
$qblanguage[49] ="Port";
$qblanguage[50] ="Ping Time Out";
$qblanguage[51] ="Traceroute Time Out";
$qblanguage[52] ="Connection Time Out";
$qblanguage[53] ="Healthcheck Interval";
$qblanguage[54] ="Save";


$qblanguage[55] ="Public IP";     #vs.lib
$qblanguage[56] ="ISP ID";
$qblanguage[57] ="Add";
$qblanguage[58] ="Update";
$qblanguage[59] ="Multi-add";
$qblanguage[60] ="Link IP Binding";
$qblanguage[61] ="Public IP to bind";

$qblanguage[62] ="Link Configuration"; #showbasic.lib

$qblanguage[63] ="MPV Configuration"; #mpv.lib
$qblanguage[64] ="Enabled";
$qblanguage[65] ="ID";
$qblanguage[66] ="NIC";
$qblanguage[67] ="TVLI";
$qblanguage[68] ="TVRI";
$qblanguage[69] ="THLI";
$qblanguage[70] ="THRI";
$qblanguage[71] ="PORT";
$qblanguage[72] ="THRN";
$qblanguage[73] ="MTU";
$qblanguage[74] ="MSS";
$qblanguage[75] ="NAT";
$qblanguage[76] ="ENC";
$qblanguage[77] ="Algorithm";
$qblanguage[78] ="COMP";
$qblanguage[79] ="Add";

$qblanguage[80] ="Add";  #showbasic.lib
$qblanguage[81] ="TMV Configuration"; #tmv.lib

$qblanguage[82] ="Role"; #tmv.lib
$qblanguage[83] ="Add";

$qblanguage[84] ="THSI"; #ipsec.lib
$qblanguage[85] ="Isakmp_SA";  #ipsec.lib
$qblanguage[86] ="Ph1_Encryption";
$qblanguage[87] ="Hash";
$qblanguage[88] ="DH_Group";
$qblanguage[89] ="IPSec_SA";
$qblanguage[90] ="Ph2_Encryption";
$qblanguage[91] ="Authentition";
$qblanguage[92] ="PF_Group";
$qblanguage[93] ="IPSec Configuration";
$qblanguage[94] ="Add"; #ipsec.lib

$qblanguage[95] ="LAN IP binding, Static Routes and DHCP setting";   #zone.lib
$qblanguage[96] ="Related ISP";
$qblanguage[97] ="DHCP";
$qblanguage[98] ="Network";
$qblanguage[99] ="IPver";
$qblanguage[100]="On";
$qblanguage[101]="Off";
$qblanguage[102]="Auto";
$qblanguage[103]="Disabled";
$qblanguage[104]="None";
$qblanguage[105]="Internal Zone";
$qblanguage[106]="related to";
$qblanguage[107]="IP Version";
$qblanguage[108]="NIC Speed";
$qblanguage[109]="Interface IP";
$qblanguage[110]="Note";
$qblanguage[111]="Create";
$qblanguage[112]="Batch Create";
$qblanguage[113]="Set DHCP";   #zone.lib

$qblanguage[114]="Static MAC Binding"; #arp.lib
$qblanguage[115]="Multi-Add";
$qblanguage[116]="Restore"; #arp.lib dns.lib

$qblanguage[117]="Wireless LAN Configuration"; #wireless.lib
$qblanguage[118]="Basic Parameters";
$qblanguage[119]="Enable Wireless";
$qblanguage[120]="Wireless Name(SSID)";
$qblanguage[121]="Hide SSID";
$qblanguage[122]="Wireless Mode";
$qblanguage[123]="Channel Selection";
$qblanguage[124]="Operation Channel";
$qblanguage[125]="Security Parameters";
$qblanguage[126]="Encrypt Type";
$qblanguage[127]="Auth Mode";
$qblanguage[128]="The WEP keys are used to encrypt data.";
$qblanguage[129]="Clients must use the same key for data transmission.";
$qblanguage[130]="You can enter";
$qblanguage[131]="5 or 13 ASCII characters";
$qblanguage[132]='10 or 26 hexadecimal characters ("0-9","a-f","A-F").';
$qblanguage[133]="Key";
$qblanguage[134]="The key is used to encrypt data.";
$qblanguage[135]="Clients must use the same key for data transmission.";
$qblanguage[136]="8 to 63 ASCII characters";
$qblanguage[137]="64 hexadecimal characters";
$qblanguage[138]="Pre-Shared Key";
$qblanguage[139]="Apply";

$qblanguage[140]="ARP proxy"; #zone.lib

$qblanguage[141]="BRIDGE"; #zone.lib
$qblanguage[142]="ARPPROXY"; #zone.lib
$qblanguage[143]="Public IP reused as Pass Through IP for Bridge"; #zone.lib
$qblanguage[144]="Pass Through IP registration for ARP Proxy"; #zone.lib

$qblanguage[145]="VlanID"; #vlan.lib
$qblanguage[146]="MAC";
$qblanguage[147]="VLAN Setting";

$qblanguage[148]="Update"; #qoslan.lib
$qblanguage[149]="MPV Bandwidth Shaper"; #qosisp.lib

$qblanguage[150]="Source"; #qoslan.lib
$qblanguage[151]="Download";
$qblanguage[152]="Priority";
$qblanguage[153]="Type";
$qblanguage[154]="Download Bandwidth";
$qblanguage[155]="Upload Bandwidth";
$qblanguage[156]="Usage Type";
$qblanguage[157]="Share";
$qblanguage[158]="Individual";
$qblanguage[159]="IP Bandwidth Shaper";
$qblanguage[160]="Hosts"; #host.lib

$qblanguage[161]="Address Detail";
$qblanguage[162]="Add";

$qblanguage[163]="Service Configuration";
$qblanguage[164]="Service";
$qblanguage[165]="Delete";
$qblanguage[166]="Protocol";
$qblanguage[167]="Information";
$qblanguage[168]="Protocol defined";
$qblanguage[169]="Description";

$qblanguage[170]="Schedule";

$qblanguage[171]="Outbound Pool Configuration";
$qblanguage[172]="Pool ID";
$qblanguage[173]="Link Info";
$qblanguage[174]="Backup Pool";
$qblanguage[175]="By Packet";
$qblanguage[176]="By Connection";
$qblanguage[177]="Balance Mode";
$qblanguage[178]="Pool Name";
$qblanguage[179]="Balance Algorithm";
$qblanguage[180]="Weight";
$qblanguage[181]="DSIP";

$qblanguage[182]="QoS Class";

$qblanguage[183]="Server Mapping";
$qblanguage[184]="Virtual IP";
$qblanguage[185]="Real Servers";
$qblanguage[186]="Real Service";

$qblanguage[187]="Policy Routing";
$qblanguage[188]="Advanced Setting";

$qblanguage[189]="Application Filtering";

$qblanguage[190]="L2TP IPsec VPN Configuration";
$qblanguage[191]="Enable L2TP IPsec";
$qblanguage[192]="VPN Server IP";
$qblanguage[193]="IP release range";
$qblanguage[194]="Pre-share key";

$qblanguage[195]="L2TP IPsec Authentication";
$qblanguage[196]="Username";
$qblanguage[197]="Assigned IP";
$qblanguage[198]="Login IP";
$qblanguage[199]="Use device";
$qblanguage[200]="Kick Out";
$qblanguage[201]="Password";
$qblanguage[202]="Confirm Password";
$qblanguage[203]="Assign IP";

$qblanguage[204]="PPTP Server Configuration";
$qblanguage[205]="Enable QB PPTP Server";
$qblanguage[206]="PPTP Encryption";
$qblanguage[207]="PPTP Compression";
$qblanguage[208]="Authentication Method";
$qblanguage[209]="Max client connections";
$qblanguage[210]="Disconnect idle time";
$qblanguage[211]="DNS IP";
$qblanguage[212]="IP release range";

$qblanguage[213]="PPTP User Authentication";
$qblanguage[214]="SSL Configuration";
$qblanguage[215]="SSL Server State";
$qblanguage[216]="Enable QB SSL Server";
$qblanguage[217]="General Setting";
$qblanguage[218]="VPN Server IP";
$qblanguage[219]="VPN Net Range";
$qblanguage[220]="VPN Netmask";
$qblanguage[221]="Full Access Settings";
$qblanguage[222]="MAX Client";
$qblanguage[223]="Available Subnet";
$qblanguage[224]="Lease Subnet";
$qblanguage[225]="SSL User Authentication";
$qblanguage[226]="Real IP";
$qblanguage[227]="VPN IP";
$qblanguage[228]="Bytes Received";
$qblanguage[229]="Bytes Sent";
$qblanguage[230]="SSL Portal Setting";
$qblanguage[231]="General Setting";
$qblanguage[232]="Window title";
$qblanguage[233]="Login Page Message";
$qblanguage[234]="Login Logo";

$qblanguage[235]="Multi-DNS Configuration";
$qblanguage[236]="General Setting";
$qblanguage[237]="ISP Selection";
$qblanguage[238]="Domain Selection";
$qblanguage[239]="Domain";
$qblanguage[240]="Domain IP";
$qblanguage[241]="Domain Level Settings";
$qblanguage[242]="Host Properties";
$qblanguage[243]="Host";
$qblanguage[244]="Value";

$qblanguage[245]="DoS Prevention";
$qblanguage[246]="Privileged List to bypass checks below";
$qblanguage[247]="Connection Overflow Detection";
$qblanguage[248]="Privileged List to bypass COD";
$qblanguage[249]="Log Rate";
$qblanguage[250]="minute";
$qblanguage[251]="hour";
$qblanguage[252]="Log Prefix";
$qblanguage[253]="Drop Packet if matched";
$qblanguage[254]="Can not go over";
$qblanguage[255]="Connections per IP";
$qblanguage[256]="Fuzzy Ping Flooding Detection";
$qblanguage[257]="Privileged List to bypass FPFD";
$qblanguage[258]="Lower";
$qblanguage[259]="Upper";
$qblanguage[260]="Port Scan Detection";
$qblanguage[261]="Privileged List to bypass PSD";
$qblanguage[262]="Weight Threshold";
$qblanguage[263]="High Port Weight";
$qblanguage[264]="Low Port Weight";
$qblanguage[265]="Delay Thershold";
$qblanguage[266]="Quota Overflow Detection";
$qblanguage[267]="Privileged List to bypass QOD";
$qblanguage[268]="If quota";
$qblanguage[269]="Set TOS value as";
$qblanguage[270]="DROP Them";

$qblanguage[271]="HA Config";
$qblanguage[272]="High Availablility is not enabled.";
$qblanguage[273]="Enable HA";
$qblanguage[274]="High Availability";
$qblanguage[275]="HA Management Message";
$qblanguage[276]="Launch HA on Boot";
$qblanguage[277]="Primary";
$qblanguage[278]="Secondary";
$qblanguage[279]="Auto Fail Over";
$qblanguage[280]="Auto Switch Back";
$qblanguage[281]="Fail on LAN Interface";
$qblanguage[282]="Host FAILOVER Timeout";
$qblanguage[283]="Network FAILOVER Timeout";
$qblanguage[284]="Enable Virtual MAC";
$qblanguage[285]="Floating IP";
$qblanguage[286]="Standby IP of Primary";
$qblanguage[287]="Standby IP of Secondary";
$qblanguage[288]="HA LAN Check Targets";
$qblanguage[289]="Check Mode";
$qblanguage[290]="Show Status";
$qblanguage[291]="Force Change Mode";
$qblanguage[292]="Save Setting";
$qblanguage[293]="Apply Setting";

$qblanguage[294]="Admin Setting";
$qblanguage[295]="Maximum User";
$qblanguage[296]="Edit User Account";
$qblanguage[297]="Https Port Number";
$qblanguage[298]="Hostname";
$qblanguage[299]="Hostname on LCM";
$qblanguage[300]="E-mail Alert";

$qblanguage[301]="Appliance Registration";
$qblanguage[302]="Company Name";
$qblanguage[303]="Contact E-mail";
$qblanguage[304]="Serial Number";
$qblanguage[305]="Registered Date";
$qblanguage[306]="Register";
$qblanguage[307]="QB Serial Number";

$qblanguage[308]="Firmware";
$qblanguage[309]="Configuration";
$qblanguage[310]="UPG and CMS Key";
$qblanguage[311]="Upload Config";
$qblanguage[312]="Upload Firmware";
$qblanguage[313]="Menu for Firmware";
$qblanguage[314]="Menu for Config";
$qblanguage[315]="Menu for CMS";
$qblanguage[316]="Menu for Config";
$qblanguage[317]="Menu for Firmware";
$qblanguage[318]="Upload Upgrade Package";
$qblanguage[319]="Upload Fs/Lib Image Package";
$qblanguage[320]="Launch Upgrade Process";
$qblanguage[321]="Backup Config";
$qblanguage[322]="FTP Server";
$qblanguage[323]="Auto Save";
$qblanguage[324]="Upload Management Key";
$qblanguage[325]="Download Management Key";
$qblanguage[326]="Upload UPG";
$qblanguage[327]="Select Config. Set";
$qblanguage[328]="Config. Set";
$qblanguage[329]="Save As";
$qblanguage[330]="Config. File";
$qblanguage[331]="Upload to";
$qblanguage[332]="Please Choose!!";
$qblanguage[333]="Select Upgrade Package";
$qblanguage[334]="Upgrade File";
$qblanguage[335]="Select Upgrade Image";
$qblanguage[336]="Launching Upgrade Procedure";
$qblanguage[337]="Select Upload Key";
$qblanguage[338]="Export Config. to FTP Server";
$qblanguage[339]="FTP Mode";
$qblanguage[340]="Server address";
$qblanguage[341]="Login username";
$qblanguage[342]="Login password";
$qblanguage[343]="Upload directory";
$qblanguage[344]="Enable Auto-Save";
$qblanguage[345]="Configuration Via CMS";
$qblanguage[346]="Note:This Function is only for Bonding Client to Server with CMS!!";
$qblanguage[347]="Select Upload UPG";
$qblanguage[348]="Select Number";
$qblanguage[349]="Start";
$qblanguage[350]="Stop";
$qblanguage[351]="Back";

$qblanguage[352]="DNS resolver";
$qblanguage[353]="QB works as DNS Server";
$qblanguage[354]="with Authoritative DNS";
$qblanguage[355]="Dynamic Routing Configuration";
$qblanguage[356]="Dynamic Routing State";
$qblanguage[357]="Enable Dynamic Routing";
$qblanguage[358]="Method";
$qblanguage[359]="Route Metric";
$qblanguage[360]="Route Update Time";
$qblanguage[361]="Monitor";
$qblanguage[362]="Monitor Port";

$qblanguage[363]="External Storage";
$qblanguage[364]="Format Hard Disk";
$qblanguage[365]="Analyser Hard Disk";

$qblanguage[366]="Miscellaneous";
$qblanguage[367]="Modify MSS ...";
$qblanguage[368]="User define";
$qblanguage[369]="Default";
$qblanguage[370]="UDP cache timeout";

$qblanguage[371]="TCP Optimization";
$qblanguage[372]="Enable TCP Optimization";
$qblanguage[373]="Destination";
$qblanguage[374]="Destination Port";

$qblanguage[375]="Time Setting";
$qblanguage[376]="Local Time";
$qblanguage[377]="Firmware License Expiry";
$qblanguage[378]="Firmware Warranty Expired";
$qblanguage[379]="Time Zone";
$qblanguage[380]="NTP Time Server";
$qblanguage[381]="Sync";


$qblanguage[382]="Snmp Administration Console";
$qblanguage[383]="Enable SNMP";
$qblanguage[384]="Enable SNMP trap";
$qblanguage[385]="Snmp Manager IP 1";
$qblanguage[386]="Snmp Manager IP 2";
$qblanguage[387]="Snmp Community String";
$qblanguage[388]="System Information";
$qblanguage[389]="System Name";
$qblanguage[390]="System Contact";
$qblanguage[391]="System Location";

$qblanguage[392]="VOIP Setting";
$qblanguage[393]="H.323";
$qblanguage[394]="H.323 NAT Support";
$qblanguage[395]="SIP";
$qblanguage[396]="SIP NAT Support";

$qblanguage[397]="Web Cache Configuration";
$qblanguage[398]="Enable QB Proxy Server";
$qblanguage[399]="Maximum Object Size";
$qblanguage[400]="Minimum Object Size";
$qblanguage[401]="Object Replacement";
$qblanguage[402]="Proxy Cache Size";
$qblanguage[403]="Maxsize";

$qblanguage[404]="Reboot";
$qblanguage[405]="Reboot QB at";
$qblanguage[406]="the moment";
$qblanguage[407]="Go";

$qblanguage[408]="Real Time Traffic";
$qblanguage[409]="Query by Defined Time Frame";
$qblanguage[410]="Query by Custom Time Frame";
$qblanguage[411]="Total Volume Pie Chart";
$qblanguage[412]="Sessions Pie Chart by Src IP";
$qblanguage[413]="Sessions Pie Chart by Nat IP";

$qblanguage[414]="Real Time Traffic";
$qblanguage[415]="Real Time Traffic Pie Chart";
$qblanguage[416]="Real Time Traffic Bar Chart";
$qblanguage[417]="Historical traffic";
$qblanguage[418]="Volume Pie Chart by Subnet";
$qblanguage[419]="Volume Bar Chart by Subnet";

$qblanguage[420]="Diagnostic Tools";
$qblanguage[421]="Tool Selection";
$qblanguage[422]="Show & Set NIC";
$qblanguage[423]="Traceroute";
$qblanguage[424]="Ping by Arp Packet";
$qblanguage[425]="Packet Sniffer";
$qblanguage[426]="Show ARP Cache";
$qblanguage[427]="Open Port Check";
$qblanguage[428]="Measure Download Speed";
$qblanguage[429]="Measure Tunnel Speed by Link";
$qblanguage[430]="Measure Tunnel Speed by Pool";
$qblanguage[431]="Tunnel Bandwidth Autotuning";
$qblanguage[432]="Tunnel Packet Lost Detection";
$qblanguage[433]="Alter ARP Table";
$qblanguage[434]="Restart QB Engine";
$qblanguage[435]="Options of Ping";
$qblanguage[436]="Options";
$qblanguage[437]="Count";
$qblanguage[438]="Through";
$qblanguage[439]="Options of NIC";
$qblanguage[440]="Duplex";
$qblanguage[441]="Speed";
$qblanguage[442]="Auto Negotiation";
$qblanguage[443]="Target of traceroute";
$qblanguage[444]="Options of Arping";
$qblanguage[445]="Source IP";
$qblanguage[446]="Destination IP";
$qblanguage[447]="Options of Packet Captor";
$qblanguage[448]="Show ARP Cache";
$qblanguage[449]="Options of Check Info";
$qblanguage[450]="Port Number";
$qblanguage[451]="Options of Measure Info";
$qblanguage[452]="Local IP";
$qblanguage[453]="Remote File";
$qblanguage[454]="Login User";
$qblanguage[455]="Link ID";
$qblanguage[456]="Latency";
$qblanguage[457]="Options of Detection Info";
$qblanguage[458]="Options of Host Info";
$qblanguage[459]="Packets";
$qblanguage[460]="Target IP";
$qblanguage[461]="Target MAC";
$qblanguage[462]="Restart QB Engine";

$qblanguage[463]="Syslog Administration Console";
$qblanguage[464]="Enable QB Server log";
$qblanguage[465]="Enable QB Traffic log";
$qblanguage[466]="Enable QB Proxy log";
$qblanguage[467]="Enable Log on Local";
$qblanguage[468]="Enable Remote Syslog Server";
$qblanguage[469]="Enable Remote FTP Server";
$qblanguage[470]="Local syslog storage";
$qblanguage[471]="FTP Login Username";
$qblanguage[472]="FTP Login Password";
$qblanguage[473]="FTP Upload Directory";
$qblanguage[474]="Frequency of FTP Server";

$qblanguage[475]="Config. Management";
$qblanguage[476]="Load";
$qblanguage[477]="Save";
$qblanguage[478]="Delete";
$qblanguage[479]="Template";
$qblanguage[480]="Dashboard";
$qblanguage[481]="Update Config";
$qblanguage[482]="Logout";

$qblanguage[483]="ARP porxy On";
$qblanguage[484]="Rules";
$qblanguage[485]="DHCP";
$qblanguage[486]="ARP Table";
$qblanguage[487]="Authentication";

}
if($langcookie eq "zh_TW"){
$qblanguage[0]="自動更新每";
$qblanguage[1]="秒";
$qblanguage[2]="系統狀態";
$qblanguage[3]="系統時間";
$qblanguage[4]="系統已開機時間";
$qblanguage[5]="韌體版本";
$qblanguage[6]="系統使用率";
$qblanguage[7]="CPU使用率";
$qblanguage[8]="記憶體使用率";
$qblanguage[9]="快取記憶體使用率";
$qblanguage[10]="Ramdisk使用率";
$qblanguage[11]="活動中的Sessions";
$qblanguage[12]="設備資訊";
$qblanguage[13]="主機名稱";
$qblanguage[14]="型號名稱";
$qblanguage[15]="硬體位址";
$qblanguage[16]="註冊資訊";
$qblanguage[17]="序號";
$qblanguage[18]="註冊日期";
$qblanguage[19]="未註冊";
$qblanguage[20]="註冊期間";
$qblanguage[21]="授權到期日";
$qblanguage[22]="保固到期日";
$qblanguage[23]="廣域網路";
$qblanguage[24]="狀態";
$qblanguage[25]="編輯";
$qblanguage[26]="啟用";
$qblanguage[27]="3G資訊";
$qblanguage[28]="Interface";
$qblanguage[29]="名稱";
$qblanguage[30]="閘道";
$qblanguage[31]="系統 IP";
$qblanguage[32]="狀況檢查 IP";
$qblanguage[33]="子網路";
$qblanguage[34]="Down/Up";
$qblanguage[35]="版本";
$qblanguage[36]="附加子網路";
$qblanguage[37]="附加子網路2";
$qblanguage[38]="代理伺服器IP";
$qblanguage[39]="代理伺服器名稱";
$qblanguage[40]="代理伺服器通訊埠";

$qblanguage[41]="連線檢查參數";
$qblanguage[42]="連線檢查方式";
$qblanguage[43]="根據 Ping";
$qblanguage[44]="根據 Ping 和 Traceroute";
$qblanguage[45]="根據連線到特定埠號";
$qblanguage[46]="根據連線到特定連接埠號和 Traceroute";
$qblanguage[47]="進階設定";
$qblanguage[48]="關閉被動式連線檢查";
$qblanguage[49]="連接埠號";
$qblanguage[50]="Ping 逾時";
$qblanguage[51]="Traceroute 逾時";
$qblanguage[52]="連線特定埠號逾時";
$qblanguage[53]="線路檢查間距";
$qblanguage[54]="儲存";


$qblanguage[55]="Public IP";
$qblanguage[56]="ISP ID";
$qblanguage[57]="新增";
$qblanguage[58]="更新";
$qblanguage[59]="新增多個";
$qblanguage[60]="Link IP Binding";
$qblanguage[61]="Public IP to bind";

$qblanguage[62]="連結設定";

$qblanguage[63]="MPV 設定";
$qblanguage[64]="啟用";
$qblanguage[65]="ID";
$qblanguage[66]="NIC";
$qblanguage[67]="TVLI";
$qblanguage[68]="TVRI";
$qblanguage[69]="THLI";
$qblanguage[70]="THRI";
$qblanguage[71]="PORT";
$qblanguage[72]="THRN";
$qblanguage[73]="MTU";
$qblanguage[74]="MSS";
$qblanguage[75]="NAT";
$qblanguage[76]="ENC";
$qblanguage[77]="演算法";
$qblanguage[78]="COMP";
$qblanguage[79]="新增 MPV";

$qblanguage[80]="新增連接";
$qblanguage[81]="TMV 設定";

$qblanguage[82]="角色";
$qblanguage[83]="新增 TMV";

$qblanguage[84]="THSI";
$qblanguage[85]="Isakmp_SA";
$qblanguage[86]="Ph1_Encryption";
$qblanguage[87]="Hash";
$qblanguage[88]="DH_Group";
$qblanguage[89]="IPSec_SA";
$qblanguage[90]="Ph2_Encryption";
$qblanguage[91]="Authentition";
$qblanguage[92]="PF_Group";
$qblanguage[93]="IPSec Configuration";
$qblanguage[94]="新增 IPSec";

$qblanguage[95]="區網設定,靜態路由和DHCP設定";
$qblanguage[96]="關連ISP";
$qblanguage[97]="DHCP";
$qblanguage[98]="Network";
$qblanguage[99]="IPver";
$qblanguage[100]="開";
$qblanguage[101]="關";
$qblanguage[102]="自動";
$qblanguage[103]="不啟用";
$qblanguage[104]="無";
$qblanguage[105]="內部區域";
$qblanguage[106]="關連到";
$qblanguage[107]="IP版本";
$qblanguage[108]="NIC 速度";
$qblanguage[109]="Interface IP";
$qblanguage[110]="註記";
$qblanguage[111]="新增";
$qblanguage[112]="批量新增";
$qblanguage[113]="設定 DHCP";

$qblanguage[114]="靜態 ARP 設定";
$qblanguage[115]="新增多個";
$qblanguage[116]="恢復";

$qblanguage[117]="無線網路設定";
$qblanguage[118]="基本參數";
$qblanguage[119]="啟用無線網路";
$qblanguage[120]="無線網路名稱(SSID)";
$qblanguage[121]="隱藏 SSID";
$qblanguage[122]="無線網路模式";
$qblanguage[123]="頻道選擇";
$qblanguage[124]="運行頻道";
$qblanguage[125]="安全參數";
$qblanguage[126]="加密類型";
$qblanguage[127]="認證模式";
$qblanguage[128]="啟用金鑰加密資料";
$qblanguage[129]="用戶端也必須使用相同的金鑰傳輸資料";
$qblanguage[130]="您可以輸入";
$qblanguage[131]="5個或13個 ASCII 字";
$qblanguage[132]='10個或26個十六進位字 ("0-9","a-f","A-F")';
$qblanguage[133]="金鑰";
$qblanguage[134]="此金鑰用來加密資料.";
$qblanguage[135]="用戶端也必須使用相同的金鑰傳輸資料";
$qblanguage[136]="8個或63個 ASCII 字";
$qblanguage[137]="64個十六進位字";
$qblanguage[138]="預先共用金鑰";
$qblanguage[139]="套用";

$qblanguage[140]="透通設定";

$qblanguage[141]="BRIDGE";
$qblanguage[142]="ARPPROXY";

$qblanguage[143]="Public IP reused as Pass Through IP for Bridge";
$qblanguage[144]="Pass Through IP registration for ARP Proxy";

$qblanguage[145]="VlanID";
$qblanguage[146]="MAC";
$qblanguage[147]="VLAN Setting";

$qblanguage[148]="上傳";
$qblanguage[149]="MPV Bandwidth Shaper";

$qblanguage[150]="Source";
$qblanguage[151]="下載";
$qblanguage[152]="Priority";
$qblanguage[153]="類型";
$qblanguage[154]="下載頻寬";
$qblanguage[155]="上傳頻寬";
$qblanguage[156]="使用類型";
$qblanguage[157]="分享";
$qblanguage[158]="個人";
$qblanguage[159]="IP Bandwidth Shaper";
$qblanguage[160]="Hosts";

$qblanguage[161]="詳細位置";
$qblanguage[162]="新增";

$qblanguage[163]="服務配置";
$qblanguage[164]="服務";
$qblanguage[165]="刪除";
$qblanguage[166]="協議";
$qblanguage[167]="資訊";
$qblanguage[168]="協議定義";
$qblanguage[169]="描述";

$qblanguage[170]="排程物件";

$qblanguage[171]="Outbound Pool Configuration";
$qblanguage[172]="Pool ID";
$qblanguage[173]="Link Info";
$qblanguage[174]="Backup Pool";
$qblanguage[175]="By Packet";
$qblanguage[176]="By Connection";
$qblanguage[177]="Balance Mode";
$qblanguage[178]="Pool Name";
$qblanguage[179]="Balance Algorithm";
$qblanguage[180]="Weight";
$qblanguage[181]="DSIP";

$qblanguage[182]="QoS Class";

$qblanguage[183]="Server Mapping";
$qblanguage[184]="Virtual IP";
$qblanguage[185]="Real Servers";
$qblanguage[186]="Real Service";

$qblanguage[187]="Policy Routing";
$qblanguage[188]="Advanced Setting";

$qblanguage[189]="應用程式過濾";

$qblanguage[190]="L2TP IPsec VPN Configuration";
$qblanguage[191]="Enable L2TP IPsec";
$qblanguage[192]="VPN Server IP";
$qblanguage[193]="IP release range";
$qblanguage[194]="預先共用金鑰";

$qblanguage[195]="L2TP IPsec Authentication";
$qblanguage[196]="使用者名稱";
$qblanguage[197]="分配 IP";
$qblanguage[198]="登入 IP";
$qblanguage[199]="使用設備";
$qblanguage[200]="登出";
$qblanguage[201]="密碼";
$qblanguage[202]="確認密碼";
$qblanguage[203]="Assign IP";

$qblanguage[204]="PPTP 伺服器配置";
$qblanguage[205]="啟用 QB PPTP 伺服器";
$qblanguage[206]="PPTP 加密";
$qblanguage[207]="PPTP 壓縮";
$qblanguage[208]="驗證方法";
$qblanguage[209]="最大用戶連接";
$qblanguage[210]="閒置離線時間";
$qblanguage[211]="DNS IP";
$qblanguage[212]="IP release range";

$qblanguage[213]="PPTP 使用者配置";
$qblanguage[214]="SSL 設定";
$qblanguage[215]="SSL 伺服器狀態";
$qblanguage[216]="啟用 QB SSL 伺服器";
$qblanguage[217]="General Setting";
$qblanguage[218]="VPN Server IP";
$qblanguage[219]="VPN Net Range";
$qblanguage[220]="VPN Netmask";
$qblanguage[221]="Full Access Settings";
$qblanguage[222]="MAX Client";
$qblanguage[223]="Available Subnet";
$qblanguage[224]="Lease Subnet";
$qblanguage[225]="SSL User Authentication";
$qblanguage[226]="Real IP";
$qblanguage[227]="VPN IP";
$qblanguage[228]="Bytes Received";
$qblanguage[229]="Bytes Sent";
$qblanguage[230]="SSL Portal Setting";
$qblanguage[231]="General Setting";
$qblanguage[232]="Window title";
$qblanguage[233]="Login Page Message";
$qblanguage[234]="Login Logo";

$qblanguage[235]="Multi-DNS 配置";
$qblanguage[236]="General Setting";
$qblanguage[237]="ISP Selection";
$qblanguage[238]="Domain Selection";
$qblanguage[239]="網域";
$qblanguage[240]="網域 IP";
$qblanguage[241]="Domain Level Settings";
$qblanguage[242]="Host Properties";
$qblanguage[243]="Host";
$qblanguage[244]="Value";

$qblanguage[245]="DoS 防止";
$qblanguage[246]="略過下列清單";
$qblanguage[247]="溢出連接偵測";
$qblanguage[248]="Privileged List to bypass COD";
$qblanguage[249]="Log Rate";
$qblanguage[250]="分鐘";
$qblanguage[251]="小時";
$qblanguage[252]="Log Prefix";
$qblanguage[253]="Drop Packet if matched";
$qblanguage[254]="Can not go over";
$qblanguage[255]="Connections per IP";
$qblanguage[256]="Fuzzy Ping Flooding Detection";
$qblanguage[257]="Privileged List to bypass FPFD";
$qblanguage[258]="Lower";
$qblanguage[259]="Upper";
$qblanguage[260]="Port Scan Detection";
$qblanguage[261]="Privileged List to bypass PSD";
$qblanguage[262]="Weight Threshold";
$qblanguage[263]="High Port Weight";
$qblanguage[264]="Low Port Weight";
$qblanguage[265]="Delay Thershold";
$qblanguage[266]="Quota Overflow Detection";
$qblanguage[267]="Privileged List to bypass QOD";
$qblanguage[268]="If quota";
$qblanguage[269]="Set TOS value as";
$qblanguage[270]="DROP Them";

$qblanguage[271]="HA 配置";
$qblanguage[272]="高可用性功能未啟動";
$qblanguage[273]="使用 HA";
$qblanguage[274]="高可用性";
$qblanguage[275]="HA 管理訊息";
$qblanguage[276]="開機啟動 HA";
$qblanguage[277]="主要的";
$qblanguage[278]="次要的";
$qblanguage[279]="自動故障復原";
$qblanguage[280]="自動切換機器";
$qblanguage[281]="Fail on LAN Interface";
$qblanguage[282]="Host FAILOVER Timeout";
$qblanguage[283]="Network FAILOVER Timeout";
$qblanguage[284]="Enable Virtual MAC";
$qblanguage[285]="Floating IP";
$qblanguage[286]="Standby IP of Primary";
$qblanguage[287]="Standby IP of Secondary";
$qblanguage[288]="HA LAN Check Targets";
$qblanguage[289]="Check Mode";
$qblanguage[290]="Show Status";
$qblanguage[291]="Force Change Mode";
$qblanguage[292]="儲存設定";
$qblanguage[293]="套用設定";

$qblanguage[294]="Admin Setting";
$qblanguage[295]="最多使用者";
$qblanguage[296]="編輯使用者帳戶";
$qblanguage[297]="Https Port Number";
$qblanguage[298]="主機名稱";
$qblanguage[299]="Hostname on LCM";
$qblanguage[300]="E-mail 通知";

$qblanguage[301]="應用程式配置";
$qblanguage[302]="公司名稱";
$qblanguage[303]="聯絡 E-mail";
$qblanguage[304]="序號";
$qblanguage[305]="註冊日期";
$qblanguage[306]="註冊";
$qblanguage[307]="QB Serial Number";

$qblanguage[308]="韌體";
$qblanguage[309]="配置";
$qblanguage[310]="UPG and CMS Key";
$qblanguage[311]="上傳設定";
$qblanguage[312]="上傳韌體";
$qblanguage[313]="Menu for Firmware";
$qblanguage[314]="Menu for Config";
$qblanguage[315]="Menu for CMS";
$qblanguage[316]="Menu for Config";
$qblanguage[317]="Menu for Firmware";
$qblanguage[318]="Upload Upgrade Package";
$qblanguage[319]="Upload Fs/Lib Image Package";
$qblanguage[320]="Launch Upgrade Process";
$qblanguage[321]="Backup Config";
$qblanguage[322]="FTP Server";
$qblanguage[323]="自動存檔";
$qblanguage[324]="Upload Management Key";
$qblanguage[325]="Download Management Key";
$qblanguage[326]="Upload UPG";
$qblanguage[327]="Select Config. Set";
$qblanguage[328]="Config. Set";
$qblanguage[329]="另存新檔";
$qblanguage[330]="Config. File";
$qblanguage[331]="上傳到";
$qblanguage[332]="請選擇";
$qblanguage[333]="Select Upgrade Package";
$qblanguage[334]="升級檔案";
$qblanguage[335]="Select Upgrade Image";
$qblanguage[336]="Launching Upgrade Procedure";
$qblanguage[337]="Select Upload Key";
$qblanguage[338]="Export Config. to FTP Server";
$qblanguage[339]="FTP Mode";
$qblanguage[340]="伺服器網址";
$qblanguage[341]="登入名稱";
$qblanguage[342]="登入密碼";
$qblanguage[343]="上傳目錄";
$qblanguage[344]="Enable Auto-Save";
$qblanguage[345]="Configuration Via CMS";
$qblanguage[346]="Note:This Function is only for Bonding Client to Server with CMS!!";
$qblanguage[347]="選擇上傳 UPG";
$qblanguage[348]="選擇數值";
$qblanguage[349]="開始";
$qblanguage[350]="停止";
$qblanguage[351]="退回";

$qblanguage[352]="DNS resolver";
$qblanguage[353]="QB works as DNS Server";
$qblanguage[354]="with Authoritative DNS";
$qblanguage[355]="Dynamic Routing Configuration";
$qblanguage[356]="Dynamic Routing State";
$qblanguage[357]="Enable Dynamic Routing";
$qblanguage[358]="方法";
$qblanguage[359]="Route Metric";
$qblanguage[360]="Route Update Time";
$qblanguage[361]="Monitor";
$qblanguage[362]="Monitor Port";

$qblanguage[363]="External Storage";
$qblanguage[364]="Format Hard Disk";
$qblanguage[365]="Analyser Hard Disk";

$qblanguage[366]="Miscellaneous";
$qblanguage[367]="Modify MSS ...";
$qblanguage[368]="User define";
$qblanguage[369]="預設";
$qblanguage[370]="UDP cache timeout";

$qblanguage[371]="TCP Optimization";
$qblanguage[372]="Enable TCP Optimization";
$qblanguage[373]="Destination";
$qblanguage[374]="Destination Port";

$qblanguage[375]="時間設定";
$qblanguage[376]="本地時間";
$qblanguage[377]="Firmware License Expiry";
$qblanguage[378]="Firmware Warranty Expired";
$qblanguage[379]="時區";
$qblanguage[380]="NTP Time Server";
$qblanguage[381]="Sync";


$qblanguage[382]="Snmp Administration Console";
$qblanguage[383]="Enable SNMP";
$qblanguage[384]="Enable SNMP trap";
$qblanguage[385]="Snmp Manager IP 1";
$qblanguage[386]="Snmp Manager IP 2";
$qblanguage[387]="Snmp Community String";
$qblanguage[388]="System Information";
$qblanguage[389]="系統名稱";
$qblanguage[390]="系統內容";
$qblanguage[391]="系統位置";

$qblanguage[392]="VOIP Setting";
$qblanguage[393]="H.323";
$qblanguage[394]="H.323 NAT Support";
$qblanguage[395]="SIP";
$qblanguage[396]="SIP NAT Support";

$qblanguage[397]="Web Cache Configuration";
$qblanguage[398]="Enable QB Proxy Server";
$qblanguage[399]="Maximum Object Size";
$qblanguage[400]="Minimum Object Size";
$qblanguage[401]="Object Replacement";
$qblanguage[402]="Proxy Cache Size";
$qblanguage[403]="Maxsize";

$qblanguage[404]="重新啟動";
$qblanguage[405]="在什麼時候重開機";
$qblanguage[406]="現在";
$qblanguage[407]="執行";

$qblanguage[408]="Real Time Traffic";
$qblanguage[409]="Query by Defined Time Frame";
$qblanguage[410]="Query by Custom Time Frame";
$qblanguage[411]="Total Volume Pie Chart";
$qblanguage[412]="Sessions Pie Chart by Src IP";
$qblanguage[413]="Sessions Pie Chart by Nat IP";

$qblanguage[414]="Real Time Traffic";
$qblanguage[415]="Real Time Traffic Pie Chart";
$qblanguage[416]="Real Time Traffic Bar Chart";
$qblanguage[417]="Historical traffic";
$qblanguage[418]="Volume Pie Chart by Subnet";
$qblanguage[419]="Volume Bar Chart by Subnet";

$qblanguage[420]="診斷工具";
$qblanguage[421]="工具選擇";
$qblanguage[422]="Show & Set NIC";
$qblanguage[423]="Traceroute";
$qblanguage[424]="Ping by Arp Packet";
$qblanguage[425]="Packet Sniffer";
$qblanguage[426]="Show ARP Cache";
$qblanguage[427]="Open Port Check";
$qblanguage[428]="Measure Download Speed";
$qblanguage[429]="Measure Tunnel Speed by Link";
$qblanguage[430]="Measure Tunnel Speed by Pool";
$qblanguage[431]="Tunnel Bandwidth Autotuning";
$qblanguage[432]="Tunnel Packet Lost Detection";
$qblanguage[433]="Alter ARP Table";
$qblanguage[434]="Restart QB Engine";
$qblanguage[435]="Options of Ping";
$qblanguage[436]="選項";
$qblanguage[437]="次數";
$qblanguage[438]="通過";
$qblanguage[439]="Options of NIC";
$qblanguage[440]="雙工";
$qblanguage[441]="速度";
$qblanguage[442]="Auto Negotiation";
$qblanguage[443]="Target of traceroute";
$qblanguage[444]="Options of Arping";
$qblanguage[445]="來源 IP";
$qblanguage[446]="目的 IP";
$qblanguage[447]="Options of Packet Captor";
$qblanguage[448]="Show ARP Cache";
$qblanguage[449]="Options of Check Info";
$qblanguage[450]="Port Number";
$qblanguage[451]="Options of Measure Info";
$qblanguage[452]="本地檔案";
$qblanguage[453]="遠端檔案";
$qblanguage[454]="使用者登錄";
$qblanguage[455]="Link ID";
$qblanguage[456]="Latency";
$qblanguage[457]="Options of Detection Info";
$qblanguage[458]="Options of Host Info";
$qblanguage[459]="Packets";
$qblanguage[460]="Target IP";
$qblanguage[461]="Target MAC";
$qblanguage[462]="Restart QB Engine";

$qblanguage[463]="Syslog Administration Console";
$qblanguage[464]="Enable QB Server log";
$qblanguage[465]="Enable QB Traffic log";
$qblanguage[466]="Enable QB Proxy log";
$qblanguage[467]="Enable Log on Local";
$qblanguage[468]="Enable Remote Syslog Server";
$qblanguage[469]="Enable Remote FTP Server";
$qblanguage[470]="Local syslog storage";
$qblanguage[471]="FTP 登入名稱";
$qblanguage[472]="FTP 登入密碼";
$qblanguage[473]="FTP 上傳目錄";
$qblanguage[474]="Frequency of FTP Server";

$qblanguage[475]="設定檔管理";
$qblanguage[476]="載入";
$qblanguage[477]="儲存";
$qblanguage[478]="刪除";
$qblanguage[479]="載入樣板";
$qblanguage[480]="儀表板";
$qblanguage[481]="更新配置";
$qblanguage[482]="登出";

$qblanguage[483]="ARP porxy On";
$qblanguage[484]="Rules";
$qblanguage[485]="DHCP";
$qblanguage[486]="ARP Table";
$qblanguage[487]="Authentication";
}
if($langcookie eq "fr_FR"){

$qblanguage[0]  ="Auto Refresh Par";
$qblanguage[1]  ="deuxième";
$qblanguage[2]  ="l'état du système";
$qblanguage[3]  ="Système Time";
$qblanguage[4]  ="Système Uptime";
$qblanguage[5]  ="Firmware Version";
$qblanguage[6]  ="Système Usage";
$qblanguage[7]  ="CPU Usage";
$qblanguage[8]  ="Memory Usage";
$qblanguage[9]  ="Cache Usage";
$qblanguage[10] ="Ramdisk Usage";
$qblanguage[11] ="Actif Sessions";
$qblanguage[12] ="Appareil Information";
$qblanguage[13] ="Nom de l'hôte";
$qblanguage[14] ="Nom du modèle";
$qblanguage[15] ="MAC Plage d'adresses";
$qblanguage[16] ="Register Information";
$qblanguage[17] ="numéro de série";
$qblanguage[18] ="inscrit le";
$qblanguage[19] ="non enregistré";
$qblanguage[20] ="S'inscrire De Etats";
$qblanguage[21] ="Licence d'expiration";
$qblanguage[22] ="Garantie d'expiration";
$qblanguage[23] ="WAN Link";
$qblanguage[24] ="statut";

$qblanguage[25] ="éditer";
$qblanguage[26] ="permettre";
$qblanguage[27] ="3G Information";
$qblanguage[28] ="Interface";
$qblanguage[29] ="prénom";
$qblanguage[30] ="Gateway";
$qblanguage[31] ="System IP";
$qblanguage[32] ="Healthcheck IP";
$qblanguage[33] ="Subnet";
$qblanguage[34] ="Down/Up";
$qblanguage[35] ="Version";
$qblanguage[36] ="supplémentaire Subnet";
$qblanguage[37] ="supplémentaire Subnet2";
$qblanguage[38] ="Proxy IP";
$qblanguage[39] ="Proxy Name";
$qblanguage[40] ="Proxy Port";


$qblanguage[41] ="Lien Vérifiez Paramètres";
$qblanguage[42] ="Lien Vérifiez Méthode";
$qblanguage[43] ="By Ping";
$qblanguage[44] ="By Ping and Trace Route";
$qblanguage[45] ="By Connection to Specified Port";
$qblanguage[46] ="By Connection and Trace Route";
$qblanguage[47] ="Paramètres avancés";
$qblanguage[48] ="Disable Passive Line Check";
$qblanguage[49] ="Port";
$qblanguage[50] ="Ping Time Out";
$qblanguage[51] ="Traceroute Time Out";
$qblanguage[52] ="Connection Time Out";
$qblanguage[53] ="Check Time Interval";
$qblanguage[54] ="sauver";


$qblanguage[55] ="Public IP";
$qblanguage[56] ="ISP ID";
$qblanguage[57] ="ajouter";
$qblanguage[58] ="mettre à jour";
$qblanguage[59] ="Multi-add";
$qblanguage[60] ="Link IP Binding";
$qblanguage[61] ="Public IP to bind";

$qblanguage[62] ="Link Configuration";

$qblanguage[63] ="MPV Configuration";
$qblanguage[64] ="Activé";
$qblanguage[65] ="ID";
$qblanguage[66] ="NIC";
$qblanguage[67] ="TVLI";
$qblanguage[68] ="TVRI";
$qblanguage[69] ="THLI";
$qblanguage[70] ="THRI";
$qblanguage[71] ="PORT";
$qblanguage[72] ="THRN";
$qblanguage[73] ="MTU";
$qblanguage[74] ="MSS";
$qblanguage[75] ="NAT";
$qblanguage[76] ="ENC";
$qblanguage[77] ="Algorithm";
$qblanguage[78] ="COMP";
$qblanguage[79] ="Add";

$qblanguage[80] ="Ajouter un lien";
$qblanguage[81] ="TMV Configuration";

$qblanguage[82] ="rôle";
$qblanguage[83] ="ajouter TMV";

$qblanguage[84] ="THSI";
$qblanguage[85] ="Isakmp_SA";
$qblanguage[86] ="Ph1_Encryption";
$qblanguage[87] ="Hash";
$qblanguage[88] ="DH_Group";
$qblanguage[89] ="IPSec_SA";
$qblanguage[90] ="Ph2_Encryption";
$qblanguage[91] ="Authentition";
$qblanguage[92] ="PF_Group";
$qblanguage[93] ="IPSec Configuration";
$qblanguage[94] ="ajouter IPSec";

$qblanguage[95] ="LAN IP binding, Static Routes and DHCP setting";
$qblanguage[96] ="connexe ISP";
$qblanguage[97] ="DHCP";
$qblanguage[98] ="Network";
$qblanguage[99] ="IPver";
$qblanguage[100]="allumer";
$qblanguage[101]="éteindre";
$qblanguage[102]="Auto";
$qblanguage[103]="handicapé";
$qblanguage[104]="aucun";
$qblanguage[105]="Internal Zone";
$qblanguage[106]="lié à";
$qblanguage[107]="IP Version";
$qblanguage[108]="NIC Speed";
$qblanguage[109]="Interface IP";
$qblanguage[110]="Note";
$qblanguage[111]="créer";
$qblanguage[112]="Batch Create";
$qblanguage[113]="Set DHCP";

$qblanguage[114]="Static ARP Configuration";
$qblanguage[115]="Multi-Add";
$qblanguage[116]="Restore";

$qblanguage[117]="Wireless LAN Configuration";
$qblanguage[118]="Basic Parameters";
$qblanguage[119]="Enable Wireless";
$qblanguage[120]="Wireless Name(SSID)";
$qblanguage[121]="Hide SSID";
$qblanguage[122]="Wireless Mode";
$qblanguage[123]="canal sélection";
$qblanguage[124]="opération canal";
$qblanguage[125]="Security Parameters";
$qblanguage[126]="Encrypt Type";
$qblanguage[127]="Auth Mode";
$qblanguage[128]="The WEP keys are used to encrypt data.";
$qblanguage[129]="Clients must use the same key for data transmission.";
$qblanguage[130]="You can enter";
$qblanguage[131]="5 or 13 ASCII characters";
$qblanguage[132]='10 or 26 hexadecimal characters ("0-9","a-f","A-F").';
$qblanguage[133]="Key";
$qblanguage[134]="The key is used to encrypt data.";
$qblanguage[135]="Clients must use the same key for data transmission.";
$qblanguage[136]="8 to 63 ASCII characters";
$qblanguage[137]="64 hexadecimal characters";
$qblanguage[138]="Pre-Shared Key";
$qblanguage[139]="appliquer";

$qblanguage[140]="Réglage transparent";

$qblanguage[141]="BRIDGE";
$qblanguage[142]="ARPPROXY";

$qblanguage[143]="Public IP reused as Pass Through IP for Bridge";
$qblanguage[144]="Pass Through IP registration for ARP Proxy";

$qblanguage[145]="VlanID";
$qblanguage[146]="MAC";
$qblanguage[147]="VLAN Setting";

$qblanguage[148]="Upload";
$qblanguage[149]="MPV Bandwidth Shaper";

$qblanguage[150]="Source";
$qblanguage[151]="télécharger";
$qblanguage[152]="Priority";
$qblanguage[153]="Type";
$qblanguage[154]="Download Bandwidth";
$qblanguage[155]="Upload Bandwidth";
$qblanguage[156]="Usage Type";
$qblanguage[157]="partager";
$qblanguage[158]="Individual";
$qblanguage[159]="IP Bandwidth Shaper";
$qblanguage[160]="Objet hôtes";

$qblanguage[161]="Détail d'adresses";
$qblanguage[162]="nouvelle entrée";

$qblanguage[163]="Configuration des services";
$qblanguage[164]="Service";
$qblanguage[165]="effacer";
$qblanguage[166]="Protocol";
$qblanguage[167]="Information";
$qblanguage[168]="Protocol defined";
$qblanguage[169]="Description";

$qblanguage[170]="Horaire objet";

$qblanguage[171]="Outbound Pool Configuration";
$qblanguage[172]="Pool ID";
$qblanguage[173]="Link Info";
$qblanguage[174]="Backup Pool";
$qblanguage[175]="By Packet";
$qblanguage[176]="By Connection";
$qblanguage[177]="Balance Mode";
$qblanguage[178]="Pool nom";
$qblanguage[179]="Balance Algorithm";
$qblanguage[180]="poids";
$qblanguage[181]="DSIP";

$qblanguage[182]="QoS Class";

$qblanguage[183]="Server Mapping";
$qblanguage[184]="Virtual IP";
$qblanguage[185]="serveurs réels";
$qblanguage[186]="services réels";

$qblanguage[187]="Policy Routing";
$qblanguage[188]="Advanced Setting";

$qblanguage[189]="Application Filtering";

$qblanguage[190]="L2TP IPsec VPN Configuration";
$qblanguage[191]="Enable L2TP IPsec";
$qblanguage[192]="VPN Server IP";
$qblanguage[193]="IP release range";
$qblanguage[194]="Pre-share key";

$qblanguage[195]="L2TP IPsec Authentication";
$qblanguage[196]="Nom d'utilisateur";
$qblanguage[197]="Assigned IP";
$qblanguage[198]="Login IP";
$qblanguage[199]="Utilisez dispositif";
$qblanguage[200]="Kick Out";
$qblanguage[201]="mot de passe";
$qblanguage[202]="Confirm Password";
$qblanguage[203]="Assign IP";

$qblanguage[204]="PPTP Server Configuration";
$qblanguage[205]="Enable QB PPTP Server";
$qblanguage[206]="PPTP Chiffrement";
$qblanguage[207]="PPTP Compression";
$qblanguage[208]="Authentication méthode";
$qblanguage[209]="Max client connections";
$qblanguage[210]="Disconnect idle time";
$qblanguage[211]="DNS IP";
$qblanguage[212]="IP release range";

$qblanguage[213]="PPTP User Authentication";
$qblanguage[214]="SSL Configuration";
$qblanguage[215]="SSL Server State";
$qblanguage[216]="Enable QB SSL Server";
$qblanguage[217]="Configuration générale";
$qblanguage[218]="VPN Server IP";
$qblanguage[219]="VPN Net Range";
$qblanguage[220]="VPN Netmask";
$qblanguage[221]="Full Access Settings";
$qblanguage[222]="MAX Client";
$qblanguage[223]="disponible Subnet";
$qblanguage[224]="Lease Subnet";
$qblanguage[225]="SSL User Authentication";
$qblanguage[226]="Real IP";
$qblanguage[227]="VPN IP";
$qblanguage[228]="Bytes recevoir";
$qblanguage[229]="Bytes expédié";
$qblanguage[230]="SSL Portal Setting";
$qblanguage[231]="General Setting";
$qblanguage[232]="Window title";
$qblanguage[233]="Login Page Message";
$qblanguage[234]="Login Logo";

$qblanguage[235]="Multi-DNS Configuration";
$qblanguage[236]="Configuration générale";
$qblanguage[237]="ISP Selection";
$qblanguage[238]="Domain Selection";
$qblanguage[239]="Domain";
$qblanguage[240]="Domain IP";
$qblanguage[241]="Domain Level Settings";
$qblanguage[242]="Host Properties";
$qblanguage[243]="Host";
$qblanguage[244]="valeur";

$qblanguage[245]="DoS Prévention";
$qblanguage[246]="Privileged List to bypass checks below";
$qblanguage[247]="Connection Overflow Detection";
$qblanguage[248]="Privileged List to bypass COD";
$qblanguage[249]="Log Rate";
$qblanguage[250]="minute";
$qblanguage[251]="heure";
$qblanguage[252]="Log Prefix";
$qblanguage[253]="Drop Packet if matched";
$qblanguage[254]="Can not go over";
$qblanguage[255]="Connections per IP";
$qblanguage[256]="Fuzzy Ping Flooding Detection";
$qblanguage[257]="Privileged List to bypass FPFD";
$qblanguage[258]="Lower";
$qblanguage[259]="Upper";
$qblanguage[260]="Port Scan détection";
$qblanguage[261]="Privileged List to bypass PSD";
$qblanguage[262]="Weight Threshold";
$qblanguage[263]="High Port Weight";
$qblanguage[264]="Low Port Weight";
$qblanguage[265]="Retard Thershold";
$qblanguage[266]="Quota Overflow Detection";
$qblanguage[267]="Privileged List to bypass QOD";
$qblanguage[268]="If quota";
$qblanguage[269]="Set TOS value as";
$qblanguage[270]="DROP Them";

$qblanguage[271]="HA Config";
$qblanguage[272]="Availablility élevée n'est pas lancé.";
$qblanguage[273]="Enable HA";
$qblanguage[274]="Haute disponibilité";
$qblanguage[275]="HA Management Message";
$qblanguage[276]="Launch HA on Boot";
$qblanguage[277]="Primary";
$qblanguage[278]="secondaire";
$qblanguage[279]="Auto Fail Over";
$qblanguage[280]="Auto Switch Back";
$qblanguage[281]="Fail on LAN Interface";
$qblanguage[282]="Host FAILOVER Timeout";
$qblanguage[283]="Network FAILOVER Timeout";
$qblanguage[284]="Enable Virtual MAC";
$qblanguage[285]="Floating IP";
$qblanguage[286]="Standby IP of Primary";
$qblanguage[287]="Standby IP of Secondary";
$qblanguage[288]="HA LAN Check Targets";
$qblanguage[289]="Check Mode";
$qblanguage[290]="Afficher l'état";
$qblanguage[291]="Force Change Mode";
$qblanguage[292]="Enregistrer le réglage";
$qblanguage[293]="appliquer Réglage";

$qblanguage[294]="Admin Setting";
$qblanguage[295]="Maximum User";
$qblanguage[296]="Edit User Account";
$qblanguage[297]="Https Port Number";
$qblanguage[298]="Hostname";
$qblanguage[299]="Hostname on LCM";
$qblanguage[300]="E-mail Alert";

$qblanguage[301]="Appliance Registration";
$qblanguage[302]="Nom de la société";
$qblanguage[303]="Contact E-mail";
$qblanguage[304]="numéro de série";
$qblanguage[305]="inscrit le";
$qblanguage[306]="s'inscrire";
$qblanguage[307]="QB numéro de série";

$qblanguage[308]="Firmware";
$qblanguage[309]="Configuration";
$qblanguage[310]="UPG and CMS Key";
$qblanguage[311]="Upload Config";
$qblanguage[312]="Upload Firmware";
$qblanguage[313]="Menu for Firmware";
$qblanguage[314]="Menu for Config";
$qblanguage[315]="Menu for CMS";
$qblanguage[316]="Menu for Config";
$qblanguage[317]="Menu for Firmware";
$qblanguage[318]="Téléchargez Upgrade Package";
$qblanguage[319]="Forfait Image Upload Fs / Lib";
$qblanguage[320]="Lancement Mets Processus";
$qblanguage[321]="Sauvegarde config";
$qblanguage[322]="Serveur FTP";
$qblanguage[323]="Auto Save";
$qblanguage[324]="Téléchargez Key Management";
$qblanguage[325]="Télécharger Key Management";
$qblanguage[326]="Téléchargez UPG";
$qblanguage[327]="Sélectionnez Config. Set";
$qblanguage[328]="Config. Set";
$qblanguage[329]="Enregistrer en tant que";
$qblanguage[330]="Config. Dossier";
$qblanguage[331]="Upload to";
$qblanguage[332]="S'il vous plaît Choisir!!";
$qblanguage[333]="Sélectionnez Mise à niveau Forfait";
$qblanguage[334]="Mise à jour du fichier";
$qblanguage[335]="Sélectionnez Mise à niveau Image";
$qblanguage[336]="Lancement de la procédure de mise à niveau";
$qblanguage[337]="Sélectionnez Envoyer la clé";
$qblanguage[338]="Export Config. à un serveur FTP";
$qblanguage[339]="Mode FTP";
$qblanguage[340]="Adresse du serveur";
$qblanguage[341]="Connexion nom d'utilisateur";
$qblanguage[342]="Connexion Mot de passe";
$qblanguage[343]="Téléchargez répertoire";
$qblanguage[344]="Activer l'enregistrement automatique";
$qblanguage[345]="Configuration Via CMS";
$qblanguage[346]="Remarque:! Cette fonction est uniquement pour les clients de collage avec le serveur grâce CMS";
$qblanguage[347]="Sélectionnez Télécharger UPG";
$qblanguage[348]="Sélectionnez Numéro";
$qblanguage[349]="Start";
$qblanguage[350]="Stop";
$qblanguage[351]="Retour";

$qblanguage[352]="DNS résoudre";
$qblanguage[353]="QB travaille comme serveur DNS";
$qblanguage[354]="with Authoritative DNS";
$qblanguage[355]="Configuration du routage dynamique";
$qblanguage[356]="Routage dynamique État";
$qblanguage[357]="Activation du routage dynamique";
$qblanguage[358]="méthode";
$qblanguage[359]="Route métrique";
$qblanguage[360]="Route Mise à jour Temps";
$qblanguage[361]="Monitor";
$qblanguage[362]="Monitor Port";

$qblanguage[363]="de stockage externe";
$qblanguage[364]="Disque dur Format";
$qblanguage[365]="Disque dur Analyseur";

$qblanguage[366]="divers";
$qblanguage[367]="Modify MSS ...";
$qblanguage[368]="défini par l'utilisateur";
$qblanguage[369]="Default";
$qblanguage[370]="UDP cache temps mort";

$qblanguage[371]="TCP optimisation";
$qblanguage[372]="Enable TCP optimisation";
$qblanguage[373]="Destination";
$qblanguage[374]="Destination Port";

$qblanguage[375]="Réglage de l'heure";
$qblanguage[376]="Heure locale";
$qblanguage[377]="Firmware Licence d'expiration";
$qblanguage[378]="Firmware garantie Expiré";
$qblanguage[379]="fuseau horaire";
$qblanguage[380]="NTP Time Server";
$qblanguage[381]="Sync";


$qblanguage[382]="Snmp Administration Console";
$qblanguage[383]="Enable SNMP";
$qblanguage[384]="Enable SNMP trap";
$qblanguage[385]="Snmp Manager IP 1";
$qblanguage[386]="Snmp Manager IP 2";
$qblanguage[387]="Snmp Community String";
$qblanguage[388]="système d'information";
$qblanguage[389]="Nom du système";
$qblanguage[390]="contact système";
$qblanguage[391]="Emplacement du système";

$qblanguage[392]="VOIP mise";
$qblanguage[393]="H.323";
$qblanguage[394]="H.323 NAT soutenir";
$qblanguage[395]="SIP";
$qblanguage[396]="SIP NAT soutenir";

$qblanguage[397]="Web Cache Configuration";
$qblanguage[398]="Enable QB Proxy Server";
$qblanguage[399]="Maximum Object Size";
$qblanguage[400]="Minimum Object Size";
$qblanguage[401]="Object Replacement";
$qblanguage[402]="Proxy Cache Size";
$qblanguage[403]="Maxsize";

$qblanguage[404]="Reboot";
$qblanguage[405]="Reboot QB at";
$qblanguage[406]="the moment";
$qblanguage[407]="Go";

$qblanguage[408]="Trafic en temps réel";
$qblanguage[409]="Query by Defined Time Frame";
$qblanguage[410]="Query by Custom Time Frame";
$qblanguage[411]="Total Volume Pie Chart";
$qblanguage[412]="Sessions Pie Chart by Src IP";
$qblanguage[413]="Sessions Pie Chart by Nat IP";

$qblanguage[414]="Trafic en temps réel";
$qblanguage[415]="Trafic en temps réel Pie Chart";
$qblanguage[416]="Trafic en temps réel Bar Chart";
$qblanguage[417]="Historical traffic";
$qblanguage[418]="Volume Pie Chart by Subnet";
$qblanguage[419]="Volume Bar Chart by Subnet";

$qblanguage[420]="Diagnostic Tools";
$qblanguage[421]="sélection de l'outil";
$qblanguage[422]="Show & Set NIC";
$qblanguage[423]="Traceroute";
$qblanguage[424]="Ping by Arp Packet";
$qblanguage[425]="Packet Sniffer";
$qblanguage[426]="Show ARP Cache";
$qblanguage[427]="Open Port Check";
$qblanguage[428]="Measure Download Speed";
$qblanguage[429]="Measure Tunnel Speed by Link";
$qblanguage[430]="Measure Tunnel Speed by Pool";
$qblanguage[431]="Tunnel Bandwidth Autotuning";
$qblanguage[432]="Tunnel Packet Lost Detection";
$qblanguage[433]="Alter ARP Table";
$qblanguage[434]="Restart QB Engine";
$qblanguage[435]="Options de Ping";
$qblanguage[436]="Options";
$qblanguage[437]="compter";
$qblanguage[438]="Through";
$qblanguage[439]="Options de NIC";
$qblanguage[440]="Duplex";
$qblanguage[441]="Speed";
$qblanguage[442]="Auto Negotiation";
$qblanguage[443]="Target de traceroute";
$qblanguage[444]="Options de arping";
$qblanguage[445]="Source IP";
$qblanguage[446]="Destination IP";
$qblanguage[447]="Options of Packet Captor";
$qblanguage[448]="Show ARP Cache";
$qblanguage[449]="Options of Check Info";
$qblanguage[450]="Port Number";
$qblanguage[451]="Options of Measure Info";
$qblanguage[452]="Local IP";
$qblanguage[453]="Remote File";
$qblanguage[454]="Connexion utilisateur";
$qblanguage[455]="Link ID";
$qblanguage[456]="Latency";
$qblanguage[457]="Options of Detection Info";
$qblanguage[458]="Options of Host Info";
$qblanguage[459]="Packets";
$qblanguage[460]="Target IP";
$qblanguage[461]="Target MAC";
$qblanguage[462]="Restart QB Engine";

$qblanguage[463]="Syslog Administration Console";
$qblanguage[464]="permettre QB Server log";
$qblanguage[465]="permettre QB Traffic log";
$qblanguage[466]="permettre QB Proxy log";
$qblanguage[467]="permettre Log on Local";
$qblanguage[468]="permettre Remote Syslog Server";
$qblanguage[469]="permettre Remote FTP Server";
$qblanguage[470]="Local syslog storage";
$qblanguage[471]="FTP Login Username";
$qblanguage[472]="FTP Login Password";
$qblanguage[473]="FTP Upload Directory";
$qblanguage[474]="Frequency of FTP Server";

$qblanguage[475]="Config. Management";
$qblanguage[476]="charger";
$qblanguage[477]="sauver";
$qblanguage[478]="effacer";
$qblanguage[479]="Template";
$qblanguage[480]="tableau de bord";
$qblanguage[481]="Update Config";
$qblanguage[482]="Logout";

$qblanguage[483]="ARP porxy On";
$qblanguage[484]="Rules";
$qblanguage[485]="DHCP";
$qblanguage[486]="ARP Table";
$qblanguage[487]="Authentication";
}

return @qblanguage;



}




1
