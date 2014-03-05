#!/usr/bin/perl -w
require ("/usr/local/apache/qb/qblib/cookie.lib"); 

#============================================================================================
# For reference the method of "floor" in get_allocated_ip
use POSIX;
use XML::Simple;
use Data::Dumper;


#========================================================================
$gNEWNATID;
$gNEWVSID;
$gNEWTABLEID;


#==========================================================================
#PATH Definition
#$gUPGINFO       =   '/var/upg/pkginfo';
#$gUPGRADE       =   '/var/upg/upgrade.sh';
$gUPGINFO       =   '/tmp/tmpupg/upg/pkginfo';
$gUPGRADE       =   '/tmp/tmpupg/upg/upgrade.sh';


if ( -e "/opt/qb/conf/registry" )
{
    $gREGISTRY      =   '/opt/qb/conf/registry';
}
elsif ( -e "/opt/qb/registry" )
{
    $gREGISTRY      =   '/opt/qb/registry';
}
else 
{
    $gREGISTRY      =   '/mnt/conf/registry';
}

&GetCookies('language'); 
$gLANGUAGE=$Cookies{language};

$gDEFAULTVALUE  =   2; # for policy qos default filter priority
$gDOMCONFPATH   =   '/mnt/qb/conf/set/';
$gHACONFIGPATH  =   '/mnt/qb/conf/ha/';
$gDOMCONFPATH   =   '/mnt/qb/conf/set/';
$gHACONFIGPATH  =   '/mnt/qb/conf/ha/';
$gAFSPATH       =   '/usr/afs/';
$gUIVER         =   '/usr/local/apache/qb/UIVERSION';
$gXMLVER        =   '/usr/local/apache/qb/XMLVERSION';
$gPKGINFO       =   '/mnt/conf/pkginfo';
$gXMLTEMPLATE   =   '/tmp/xmltemplate/';
$gPATH          =   '/usr/local/apache/qbconf/';  
$gACTIVEPATH    =   '/usr/local/apache/active/';  
$gINITPATH      =   '/usr/local/apache/config/';  
$gSETUIDPATH    =   '/usr/local/apache/qb/setuid/';
$gBTKAVGLOG     =   ' /var/log/btkavg.log ';
$gALERTLOG      =   ' /mnt/log/alert.log ';
$gTUNNELLOG     =   ' /var/log/bw-measure.log ';
$gDAEMONLOG     =   ' /var/log/daemon.log ';
$gIPCHANGELOG   =   ' /var/log/ipchange.log ';
$gDIAGNOSELOG   =   ' /var/log/diagnose.log ';
$gXMLLOCK       =   ' /usr/local/apache/qb/XMLLOCK ';
$gQBSERVERVER   =   ' /var/log/version  ';
$gQBRUNWAYVER   =   ' /var/log/rw_ver   ';
$gZONEINFO      =   ' /usr/share/zoneinfo/zone.tab ';
$gQBDATRP       =   ' /opt/qb/modules/qbdatrp.o ';
$gCLOCK         =   ' /etc/sysconfig/clock ';
$gTCSCRIPT      =   '/usr/local/apache/qbconf/tcscript';
$gPTCSCRIPT     =   '/usr/local/apache/qbconf/ptcscrpt';
@gTOOLPATH      =   ('/opt/qb/sbin/', '/sbin/', '/bin/', '/usr/sbin/', '/usr/bin/', '/opt/qb/apps/', '/opt/snmpd/' , $gSETUIDPATH, $gAFSPATH);
$gUSERACTIONLOG =   '/tmp/user.log';
$gUSERACTIONLOG_Read =   '/mnt/log/user.log';

#============================================================================================
#Command Definition
$gTOOLBOX='/opt/qb/sbin/';
$gRUN=' /usr/local/apache/qb/setuid/run  ';

#============================================================================================
# Routing Tables Related
$gALLPATH=100;
$gRRG=200;
$gBALANCE=30;
$gDROP=255;

#============================================================================================
$gFIFOTIMEOUT=30;
$gNEWISPID;
$gTIMEOUT=30*60; #seconds;
$gLOGINRESULT=1;

#============================================================================================
# $gFWMARKSTARTVALUE=10000;
$gFWMARKSTARTVALUE=10005; # nancy 050203...avoid DROP of ANY(RQST) match with system fwmark 0x8FF2710.
$gFWMARKINTERVAL=5000;
$gBLACKHOLE=999;

#============================================================================================
# Chinese Language Related
$gBIG5="[\xA1-\xF9][\x40-\x7E\xA1-\xFE]";

#============================================================================================
# Global message log variable for recording events 
#
$gMSGPROMPT;
$gMSGLOG;

#==================# Glocal variables declaration #========================
# System Information
#
$gMODEL="2400";
$gTYPE="LB";

#=========================================================================
# Limitations  
#
$gMAXVS=100;
$gMAXNAT=100;
$gMAXPOLICY=1000;
$gMAXDOMAIN=1000;
$gMAXISP=100;
$gMAXNORMALISP=100;
$gMAX3GISP=2;
$gMAXMPVISP=100;
$gMAXPPTPISP=2;
$gMAXTABLENUM=99;
$gNUMOFPORT=4;
$gNUMOFCOMPORT=2;
$gRESERVEDLANPORT=0;
$gMAXIMUMUSER=3;
$gMAXNUMTC = 500;
$gMAXETHBW = 5; # Mbits, equiv. to 5 mb


#=========================================================================
# Function Enable or Disable
#
$gENABLEBYPACKET=1;
$gENABLEBYBTK=1;
$gENABLEINBOUND=1; # $gENABLEINBOND=1...error spelling041014
$gENABLEFULLINBOUND=0;
$gENABLEHA=1;
$gENABLEQOS=1; 
$gENABLEDHCP=1;
#============= if Registry File exists, parse it to value of each change global variable
my %reghash;

if ( -r $gREGISTRY )
{
    if ( open(REGISTRY, "< $gREGISTRY " ) ) 
    {
        while (<REGISTRY>)
        {
            chomp;

            if ( $_=~m/^#/ || $_ eq '' ) { next; }

            if ( !($_=~m/(.+?)\s+(\S+)\s*/) ) { next; }

            $reghash{$1}=$2;
        }
        close(REGISTRY);
    }

    #============================================================================
    #            Glocal variables redeclaration
    #============================================================================

    foreach my $regval ( keys %reghash )
    {
        my $givevalue='$g'.$regval.'=( exists($reghash{'.$regval.'}) ) ? ( $reghash{'.$regval.'} ) : ($g'.$regval.');'; 
        eval $givevalue;
    }
}
else
{
    $gMSGPROMPT.=qq(Registry File Not Found !! \\n);
    $gMSGPROMPT.=qq(Use default values to work\\n);
}


#=============2006/11/02 Brian to prevent firmware abuse. 
$gUPGVERSION="2.5.0";
if ( -r $gUPGINFO )
{
    if ( !open(UPGINFO, "< $gUPGINFO " ) ) 
    {
        $gMSGPROMPT.= qq (\\n Open UPGinfo  Failed \\n);
        return;
    }
        $gUPGVERSION=<UPGINFO>;
        chomp $gUPGVERSION;
        close(UPGINFO);
}

#@gDOWNUPRATE=("D512Kbit/U512Kbit", "D512Kbit/U64Kbit", "D768Kbit/U128Kbit", "D768Kbit/U384Kbit", "D1536Kbit/U384Kbit", "D512Kbit/U128Kbit", "D1024Kbit/U384Kbit","D1536Kbit/U512Kbit"); 
@gDOWNUPRATE=("D512Kbit/U512Kbit", "D512Kbit/U64Kbit", "D768Kbit/U128Kbit", "D768Kbit/U384Kbit", "D1536Kbit/U384Kbit", "D512Kbit/U128Kbit", "D1024Kbit/U384Kbit", "D1536Kbit/U512Kbit", "D1024Kbit/U256Kbit", "D2048Kbit/U256Kbit", "D2048Kbit/U512Kbit", "D8192Kbit/U640Kbit", "D4096Kbit/U512Kbit", "D10240Kbit/U1024Kbit", "D10240Kbit/U2048Kbit", "D10240Kbit/U10240Kbit", "D20480Kbit/U20480Kbit", "D40960Kbit/U40960Kbit");

%gMODEHASH=(
            'WRR'       =>'Weighted Round Robin', 
            'WLC'       =>'Weighted Least Connection',
            'BSWLT'     =>'Bidirectional Sensitive Weighted Leasted Traffic',
            'FRTT'      =>'Fastest Roud Trip Time',
            'WLT'       =>'Weighted Least Traffic', 
            'BTK'       =>'Bottleneck Monitor', 
            'FAST'      =>'Fastest Way By Destination',
            'REDIRECT'  =>'Just a Redirect' 
            );

%gMODEHASH_v2=(
            'WRR'                =>'Weighted Round Robin IP Persistant', 
            'WRR_AGGREGATE'      =>'Weighted Round Robin By Connection', 
            'WRR_EQUALIZE'       =>'Weighted Round Robin By Packet (For MPV/TMV Only)', 
            'WRR_LATENCY'        =>'Bonding By Latency (For MPV/TMV Only)',
            'WRR_LCY_PKT'        =>'Bonding By Latency and Packet Loss(For MPV/TMV Only)',
            #'BTK_EQUALIZE'       =>'Bandwidth Measure WRR By Packet (For MPV/TMV Only)', 
            'BSWLT'              =>'Bidirectional Sensitive Weight Leasted Traffic',
            'DSWLT'              =>'Downlink Sensitive Weighted Least Traffic',
            'USWLT'              =>'Uplink Sensitive Weighted Least Traffic',
            'FRTT'               =>'ISP Response Time',
            'WLT_EQUALIZE'       =>'Weighted Least Traffic By Packet (For MPV/TMV Only)', 
            #'FAST'               =>'Fastest Way By Destination',
            'REDIRECT'           =>'Redirect To Transparent Proxy',
            'TB'		 =>'TCP Bonding (For MPV/TMV Only)'	 
);

%gL7PROTOCOLHASH=(
            'aim'                  =>'AIM - AOL instant messenger(ICQ)', 
            'aimwebcontent'        =>'AIM web content', 
            'applejuice'           =>'Apple Juice - P2P filesharing', 
            'ares'                 =>'Ares - P2P filesharing', 
            'battlefield1942'      =>'Battlefield 1942 - An EA game', 
            'battlefield2'         =>'Battlefield 2 - An EA game',
            'bgp'                  =>'BGP - Border Gateway Protocol',
            'biff'                 =>'Biff - new mail notification',
            'bittorrent'           =>'Bittorrent - P2P filesharing(ABC,Azureus,Bittorrent)',
            'chikka'               =>'Chikka - SMS service can be used without phones', 
            'cimd'                 =>'CIMD - An SMSC protocol by Nokia', 
            'ciscovpn'             =>'Cisco VPN client software', 
            'citrix'               =>'Citrix ICA remote desktop application', 
            #'counterstrike-source'=>'Counterstrike - Game', 
            'counterstrike'        =>'Counterstrike - Game', 
            'cvs'                  =>'CVS - Concurrent Versions System',
            #'dayofdefeat-source'  =>'Day of Defeat: Half-Life 2 mod', 
            'dayofdefeat'          =>'Day of Defeat: Half-Life 2 mod', 
            'dhcp'                 =>'DHCP - Dynamic Host Configuration Protocol', 
            'directconnect'        =>'Direct Connect - P2P filesharing', 
            'dns'                  =>'DNS - Domain Name System', 
            'doom3'                =>'Doom 3 - A computer game', 
            'edonkey'              =>'eDonkey2000 - P2P filesharing(eMule)', 
            'fasttrack'            =>'FastTrack - P2P filesharing(Kazaa)', 
            'finger'               =>'Finger - User information server', 
            'freenet'              =>'Freenet - Anonymous information retrieval', 
            'ftp'                  =>'FTP - File Transfer Protocol', 
            'gkrellm'              =>'Gkrellm - a system monitor', 
            'gnucleuslan'          =>'GnucleusLAN - LAN P2P filesharing', 
            'gnutella'             =>'Gnutella - P2P filesharing', 
            'goboogy'              =>'GoBoogy - a Korean P2P protocol', 
            'gopher'               =>'Gopher - A precursor to HTTP', 
            'h323'                 =>'H.323 - Voice over IP', 
           # 'halflife2-deathmatch'=>'Half-Life 2 Deathmatch', 
            'halflife2'            =>'Half-Life 2 Deathmatch', 
            'hddtemp'              =>'Hddtemp - Hard drive temperature reporting', 
            'hotline'              =>'Hotline - An old P2P filesharing protocol', 
           # 'http-rtsp'            =>'RTSP tunneled within HTTP', 
            'http'                 =>'HTTP - HyperText Transfer Protocol', 
            'ident'                =>'Ident - Identification Protocol', 
            'imap'                 =>'IMAP - Internet Message Access Protocol', 
            'imesh'                =>'iMesh - a P2P application', 
            'ipp'                  =>'IP printing - a new standard for UNIX printing', 
            'irc'                  =>'IRC - Internet Relay Chat', 
            'jabber'               =>'Jabber - open instant messenger protocol', 
            'kugoo'                =>'KuGoo - a Chinese P2P program', 
            'live365'              =>'live365 - An Internet radio site', 
            'lpd'                  =>'LPD - Line Printer Daemon Protocol', 
            'mohaa'                =>'Medal of Honor Allied Assault - an Electronic Arts game',
           # 'msn-filetransfer'     =>'MSN Messenger file transfers', 
            'msnmessenger'         =>'MSN Messenger - Microsoft Network chat client', 
            'mute'                 =>'MUTE - P2P filesharing', 
            'napster'              =>'Napster - P2P filesharing', 
            'nbns'                 =>'NBNS - NetBIOS name service', 
            'ncp'                  =>'NCP - Novell Core Protocol', 
            'netbios'              =>'NetBIOS - Network Basic Input Output System', 
            'nntp'                 =>'NNTP - Network News Transfer Protocol', 
            'ntp'                  =>'(S)NTP - (Simple) Network Time Protocol', 
            'openft'               =>'OpenFT - P2P filesharing',
            'pcanywhere'           =>'pcAnywhere - Symantec remote access program', 
            'poco'                 =>'POCO and PP365 - Chinese P2P filesharing', 
            'pop3'                 =>'POP3 - Post Office Protocol version 3', 
            'qq'                   =>'Tencent QQ - Chinese instant messenger protocol', 
           #'quake-halflife'       =>'HL1 games(HL1,Quake2/3/World,Counterstrike1.6)',
            'quake'                =>'HL1 games(HL1,Quake2/3/World,Counterstrike1.6)',
            'quake1'               =>'Quake 1 - A popular computer game', 
            'radmin'               =>'RDP software - Famatech Remote Administrator', 
            'rdp'                  =>'RDP - Remote Desktop Protocol', 
            'rlogin'               =>'Rlogin - remote login', 
            'rtsp'                 =>'RTSP - Real Time Streaming Protocol', 
            'shoutcast'            =>'Shoutcast and Icecast - streaming audio', 
            'sip'                  =>'SIP - Session Initiation Protocol', 
            #Skype is an Overmatching pattern
            #'skypeout'             =>'Skype to phone - UDP voice call', 
            #'skypetoskype'         =>'Skype to Skype - UDP voice call', 
            'smb'                  =>'Samba/SMB - Server Message Block', 
            'smtp'                 =>'SMTP - Simple Mail Transfer Protocol', 
            'snmp'                 =>'SNMP - Simple Network Management Protocol', 
            'socks'                =>'SOCKS Version 5 - Firewall traversal protocol', 
            'soribada'             =>'Soribada - A Korean P2P filesharing program', 
            'soulseek'             =>'Soulseek - P2P filesharing', 
            'ssdp'                 =>'SSDP - Simple Service Discovery Protocol', 
            'ssh'                  =>'SSH - Secure SHell', 
            'ssl'                  =>'SSL - Secure Socket Layer', 
            'stun'                 =>'STUN - Simple Traversal of UDP Through NAT', 
            'subspace'             =>'Subspace - 2D asteroids-style space game', 
            'subversion'           =>'Subversion - a version control system', 
            'teamspeak'            =>'TeamSpeak - VoIP group communications software', 
            'telnet'               =>'Telnet - Insecure remote login', 
            'tesla'                =>'Tesla Advanced Communication - P2P filesharing', 
            'tftp'                 =>'TFTP - Trivial File Transfer Protocol', 
            'thecircle'            =>'The Circle - P2P application', 
            #'tls'                  =>'TLS - Transport Layer Security', 
            'tor'                  =>'Tor - The Onion Router - used for anonymization', 
            'tsp'                  =>'TSP - UNIX Time Synchronization Protocol', 
            'uucp'                 =>'UUCP - nix to Unix Copy', 
            'validcertssl'         =>'Valid certificate SSL', 
            'ventrilo'             =>'Ventrilo - VoIP group communications software', 
            'vnc'                  =>'VNC - Virtual Network Computing', 
            'whois'                =>'Whois - query/response system', 
            'worldofwarcraft'      =>'World of Warcraft - popular network game', 
            'x11'                  =>'X Windows Version 11', 
            'xboxlive'             =>'XBox Live - Console gaming', 
            'xunlei'               =>'Xunlei - Chinese P2P filesharing', 
            'yahoo'                =>'Yahoo messenger - an instant messenger protocol', 
            'zmaap'                =>'Zeroconf Multicast Address Allocation Protocol', 
            'audiogalaxy'          =>'Audiogalaxy - P2P filesharing',
           # 'http-dap'             =>'HTTP by Download Accelerator Plus',
           # 'http-freshdownload'   =>'HTTP by Fresh Download',
           # 'http-itunes'          =>'HTTP - iTunes (Apple music program)', 
            'httpaudio'            =>'HTTP - Audio over HTTP', 
            'httpcachehit'         =>'HTTP - Proxy Cache hit for HTTP', 
            'httpcachemiss'        =>'HTTP - Proxy Cache miss for HTTP', 
            'httpvideo'            =>'HTTP - Video over HTTP', 
            'pressplay'            =>'pressplay - A legal music distribution site', 
            'quicktime'            =>'Quicktime HTTP', 
            #'snmp-mon'             =>'SNMP Monitoring', 
            #'snmp-trap'            =>'SNMP Traps' 
);
%gL7FILEHASH=(
            'exe'                =>'Executable - Microsoft PE file format',
            'flash'              =>'Flash - Macromedia Flash',
            'gif'                =>'GIF - Popular Image format',
            'html'               =>'(X)HTML - (Extensible) Hypertext Markup Language',
            'jpeg'               =>'JPEG - Joint Picture Expert Group image format',
            'ogg'                =>'Ogg - Ogg Vorbis music format',
            'pdf'                =>'PDF - Portable Document Format',
            'perl'               =>'Perl - A scripting language by Larry Wall',
            'postscript'         =>'Postscript - Printing Language',
            'rar'                =>'RAR - The WinRAR archive format',
            'rpm'                =>'RPM - Redhat Package Management packages',
            'rtf'                =>'RTF - Rich Text Format - an open document format',
            'tar'                =>'Tar - tape archive. Standard UNIX file archiver',
            'zip'                =>'ZIP - (PK|Win)Zip archive format'
);
%gL7IMHASH=(
            'aim'                  =>'AIM - AOL instant messenger(ICQ)', 
            'aimwebcontent'        =>'AIM web content',
          # 'msn-filetransfer'     =>'MSN Messenger file transfers', 
            'msnmessenger'         =>'MSN Messenger - Microsoft Network chat client', 
            'qq'                   =>'Tencent QQ - Chinese instant messenger protocol',
            'yahoo'                =>'Yahoo messenger - an instant messenger protocol', 
);
%gL7P2PHASH=(
            'applejuice'           =>'Apple Juice - P2P filesharing', 
            'ares'                 =>'Ares - P2P filesharing',
            'audiogalaxy'          =>'Audiogalaxy - P2P filesharing', 
            'bittorrent'           =>'Bittorrent - P2P filesharing(ABC,Azureus,Bittorrent)',
            'directconnect'        =>'Direct Connect - P2P filesharing', 
            'edonkey'              =>'eDonkey2000 - P2P filesharing(eMule)', 
            'fasttrack'            =>'FastTrack - P2P filesharing(Kazaa)', 
            'gnucleuslan'          =>'GnucleusLAN - LAN P2P filesharing', 
            'gnutella'             =>'Gnutella - P2P filesharing', 
            'goboogy'              =>'GoBoogy - a Korean P2P protocol',
            'hotline'              =>'Hotline - An old P2P filesharing protocol',
            'imesh'                =>'iMesh - a P2P application',
            'kugoo'                =>'KuGoo - a Chinese P2P program',
            'mute'                 =>'MUTE - P2P filesharing', 
            'napster'              =>'Napster - P2P filesharing',
            'openft'               =>'OpenFT - P2P filesharing',
            'poco'                 =>'POCO and PP365 - Chinese P2P filesharing', 
            'soribada'             =>'Soribada - A Korean P2P filesharing program', 
            'soulseek'             =>'Soulseek - P2P filesharing',
            'tesla'                =>'Tesla Advanced Communication - P2P filesharing',
            'thecircle'            =>'The Circle - P2P application',
            'xunlei'               =>'Xunlei - Chinese P2P filesharing',
); 
%gL7GAMEHASH=(
            'battlefield1942'      =>'Battlefield 1942 - An EA game', 
            'battlefield2'         =>'Battlefield 2 - An EA game',
            'counterstrike'        =>'Counterstrike - Game',
           #'dayofdefeat-source'   =>'Day of Defeat: Half-Life 2 mod', 
            'dayofdefeat'          =>'Day of Defeat: Half-Life 2 mod', 
            'doom3'                =>'Doom 3 - A computer game', 
          # 'halflife2-deathmatch' =>'Half-Life 2 Deathmatch',
            'halflife2'            =>'Half-Life 2 Deathmatch',
            'mohaa'                =>'Medal of Honor Allied Assault - an Electronic Arts game',
          # 'quake-halflife'       =>'HL1 games(HL1,Quake2/3/World,Counterstrike1.6)',
            'quake'                =>'HL1 games(HL1,Quake2/3/World,Counterstrike1.6)',
            'quake1'               =>'Quake 1 - A popular computer game',  
            'subspace'             =>'Subspace - 2D asteroids-style space game',
            'worldofwarcraft'      =>'World of Warcraft - popular network game', 
            'xboxlive'             =>'XBox Live - Console gaming',
);
%gL7VOICEHASH=(
            'h323'                 =>'H.323 - Voice over IP', 
            'sip'                  =>'SIP - Session Initiation Protocol', 
            #Skype is an Overmatching pattern
            #'skypeout'             =>'Skype to phone - UDP voice call', 
            #'skypetoskype'         =>'Skype to Skype - UDP voice call', 
            'teamspeak'            =>'TeamSpeak - VoIP group communications software', 
            'ventrilo'             =>'Ventrilo - VoIP group communications software', 
);
%gL7OTHERHASH=(
            'bgp'                  =>'BGP - Border Gateway Protocol',
            'biff'                 =>'Biff - new mail notification',
            'chikka'               =>'Chikka - SMS service can be used without phones', 
            'cimd'                 =>'CIMD - An SMSC protocol by Nokia', 
            'ciscovpn'             =>'Cisco VPN client software', 
            'citrix'               =>'Citrix ICA remote desktop application', 
            'cvs'                  =>'CVS - Concurrent Versions System',
            'dhcp'                 =>'DHCP - Dynamic Host Configuration Protocol', 
            'dns'                  =>'DNS - Domain Name System', 
            'finger'               =>'Finger - User information server', 
            'freenet'              =>'Freenet - Anonymous information retrieval', 
            'ftp'                  =>'FTP - File Transfer Protocol', 
            'gkrellm'              =>'Gkrellm - a system monitor', 
            'gopher'               =>'Gopher - A precursor to HTTP', 
            'hddtemp'              =>'Hddtemp - Hard drive temperature reporting', 
          # 'http-rtsp'            =>'RTSP tunneled within HTTP', 
            'http'                 =>'HTTP - HyperText Transfer Protocol', 
            'ident'                =>'Ident - Identification Protocol', 
            'imap'                 =>'IMAP - Internet Message Access Protocol', 
            'ipp'                  =>'IP printing - a new standard for UNIX printing', 
            'irc'                  =>'IRC - Internet Relay Chat', 
            'jabber'               =>'Jabber - open instant messenger protocol', 
            'live365'              =>'live365 - An Internet radio site', 
            'lpd'                  =>'LPD - Line Printer Daemon Protocol', 
            'nbns'                 =>'NBNS - NetBIOS name service',
            'ncp'                  =>'NCP - Novell Core Protocol', 
            'netbios'              =>'NetBIOS - Network Basic Input Output System', 
            'nntp'                 =>'NNTP - Network News Transfer Protocol', 
            'ntp'                  =>'(S)NTP - (Simple) Network Time Protocol', 
            'pcanywhere'           =>'pcAnywhere - Symantec remote access program', 
            'pop3'                 =>'POP3 - Post Office Protocol version 3', 
            'radmin'               =>'RDP Software - Famatech Remote Administrator', 
            'rdp'                  =>'RDP - Remote Desktop Protocol', 
            'rlogin'               =>'Rlogin - remote login', 
            'rtsp'                 =>'RTSP - Real Time Streaming Protocol', 
            'shoutcast'            =>'Shoutcast and Icecast - streaming audio', 
            'smb'                  =>'Samba/SMB - Server Message Block', 
            'smtp'                 =>'SMTP - Simple Mail Transfer Protocol', 
            'snmp'                 =>'SNMP - Simple Network Management Protocol', 
            'socks'                =>'SOCKS Version 5 - Firewall traversal protocol', 
            'ssdp'                 =>'SSDP - Simple Service Discovery Protocol', 
            'ssh'                  =>'SSH - Secure SHell', 
            'ssl'                  =>'SSL - Secure Socket Layer', 
            'stun'                 =>'STUN - Simple Traversal of UDP Through NAT', 
            'subversion'           =>'Subversion - a version control system', 
            'telnet'               =>'Telnet - Insecure remote login', 
            'tftp'                 =>'TFTP - Trivial File Transfer Protocol', 
          # 'tls'                  =>'TLS - Transport Layer Security', 
            'tor'                  =>'Tor - The Onion Router - used for anonymization', 
            'tsp'                  =>'TSP - UNIX Time Synchronization Protocol', 
            'uucp'                 =>'UUCP - nix to Unix Copy', 
            'validcertssl'         =>'Valid certificate SSL', 
            'vnc'                  =>'VNC - Virtual Network Computing', 
            'whois'                =>'Whois - query/response system', 
            'x11'                  =>'X Windows Version 11', 
            'zmaap'                =>'Zeroconf Multicast Address Allocation Protocol', 
          # 'http-dap'             =>'HTTP by Download Accelerator Plus',
          # 'http-freshdownload'   =>'HTTP by Fresh Download',
          # 'http-itunes'          =>'HTTP - iTunes (Apple music program)',
            'httpaudio'            =>'HTTP - Audio over HTTP', 
            'httpcachehit'         =>'HTTP - Proxy Cache hit for HTTP', 
            'httpcachemiss'        =>'HTTP - Proxy Cache miss for HTTP', 
            'httpvideo'            =>'HTTP - Video over HTTP', 
            'pressplay'            =>'pressplay - A legal music distribution site', 
            'quicktime'            =>'Quicktime HTTP', 
           #'snmp-mon'             =>'SNMP Monitoring', 
           #'snmp-trap'            =>'SNMP Traps' 
);

%gDNSMODE=('WRR'=>'Weighted Round Robin', 'WLT'=>'Weighted Least Traffic', 'BTK'=>'Bottleneck Monitor', 'FAILOVER'=>'Fail Over'); 
#%gFSTYPE=('ext2'=>'Second Extended Filesystem', 'ext3'=>'Third Extended Filesystem', 'vfat'=>'Virtual File Allocation Table'); 
%gFSTYPE=('ext2'=>'Second Extended Filesystem', 'ext3'=>'Third Extended Filesystem'); 
%gTCP_OPT=('none'=>'None', 'cubic'=>'Algorithm for ADSL Links', 'westwood'=>'Algorithm for Wireless Links'); 

%gUSBmodem=(
            'E161'                 =>'Huawei E161/EC169', 
            'E1612'                =>'Huawei E1612', 
            'E169'                 =>'Huawei E169', 
            'E1690'                =>'Huawei E173/173U/1690/1692/1552', #Also support E1762
            'E173s'                =>'Huawei E173s', #E173s-6
            'E169G'                =>'Huawei E169G', 
            'E1750'                =>'Huawei E1550/1750', 
            'E1762'                =>'Huawei E1762', 
            'E180'                 =>'Huawei E180', 
            'E1820'                =>'Huawei E182/270+/372/1820', #Also support E1762 
            'E220'                 =>'Huawei E220/270/870', 
            'E303'                 =>'Huawei E303', 
            'E367'                 =>'Huawei E367', 
            'E630'                 =>'Huawei E630', 
#            'EM770W'               =>'Huawei EM770W/EM772W', 
            'K3765'                =>'Huawei K3765', 
            'K4505'                =>'Huawei K4505', 
            'K4605'                =>'Huawei K4605', 
            'U7510'                =>'Huawei U7510', 
            'MF190'                =>'ZTE MF190', 
            'MF627'                =>'ZTE MF627', 
			'MC8090'               =>'Sierra MC8090',
            'H20'                  =>'Qisda H20',
            'T77Z'                 =>'Sierra T77Z', 
            'HP10'                 =>'AMO HP10' 
);

%gModemAction=(
            'Reset All'            =>'Reset All Modem', 
            'Reset All_PW'         =>'Reset All Modem by Power', 
            'Reset Hub'            =>'Reset 3G Motherboard', 
            'Reset Modem 1'        =>'Reset Modem 1', 
            'Reset Modem 2'        =>'Reset Modem 2', 
            'Reset Modem 3'        =>'Reset Modem 3', 
            'Reset Modem 4'        =>'Reset Modem 4', 
            'Reset Modem 5'        =>'Reset Modem 5', 
            'Reset Modem 6'        =>'Reset Modem 6', 
            'Reset Modem 7'        =>'Reset Modem 7', 
            'Pwoff All'            =>'Power off All Modem', 
            'Pwon All'             =>'Power on All Modem' 
);

%gSingle_Config_hash=(
            'Static_PPPoE_USB3G'                 =>'Single Site', 
            'Static_DHCP_USB3G'                  =>'Single Site', 
            'Static_PPPoE_USB3G_L2TP'            =>'Single Site', 
            'Static_DHCP_USB3G_PPTP'             =>'Single Site', 
            'Static_PPPoE_USB3G_QoS_Filtering'   =>'Single Site'
); 
%gBonding_Client_Config_hash=(
            'Bonding_Client_2Static_2MPV'         =>'VPN Bonding Client',
            'Bonding_Client_2PPPoE_2MPV'          =>'VPN Bonding Client',
            'Bonding_Client_2USB3G_2MPV'          =>'VPN Bonding Client'
);
%gBonding_Center_Config_hash=(
            'Bonding_Center_2MPV'                 =>'VPN Bonding Center' 
);
%gNIC_speed_hash=(
            'Auto'                               =>'Auto Negotiate', 
            '1000F'                              =>'1000Mbps - Full Duplex', 
            '100F'                               =>'100Mbps - Full Duplex', 
            '100H'                               =>'100Mbps - Half Duplex', 
            '10F'                                =>'10Mbps - Full Duplex', 
            '10H'                                =>'10Mbps - Half Duplex'
); 
%gband_2G3G_hash=(
            'GSM850'                             =>'GSM 850', 
            'GSM900'                             =>'GSM 900', 
            'GSM1800'                            =>'GSM 1800', 
            'GSM1900'                            =>'GSM 1900', 
            'UMTS850'                            =>'UMTS 850', 
            'UMTS900'                            =>'UMTS 900', 
            'UMTS1900'                           =>'UMTS 1900', 
            'UMTS2100'                           =>'UMTS 2100' 
); 
%gmode_2G3G_hash=(
            'GSM'                                =>'GSM Only', 
            'WCDMA'                              =>'WCDMA Only' 
); 
%gRouting_method=(
            'RIP1'                               =>'RIP Version 1', 
            'RIP2'                               =>'RIP Version 2',
            'OSPF'                               =>'Open Shortest Path First' 
); 
#
1
