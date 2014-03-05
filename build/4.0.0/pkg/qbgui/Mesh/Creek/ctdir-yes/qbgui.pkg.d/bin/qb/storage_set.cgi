#!/usr/bin/perl
require ("qbmod.cgi");
require "./qblib/storage_set.lib";


#認證是否是經過正常且標準的程序登入進來的
authenticate( action=>'RANDOMCHECK' );

print "Content-type:text/html\n\n";

use CGI;
use Data::Dumper;

#---------------- read-in form information ------------------------------
my $form=new CGI;
my %action;

###############################################
#GENERAL
$action{action}=$form->param('action');
$action{path}=$form->param('path');
$action{first}=$form->param('first');
$action{second}=$form->param('second');
$action{ser}=($form->param('Server')) ? (1) : (0);
$action{tra}=($form->param('Traffic')) ? (1) : (0);
$action{pro}=($form->param('Proxy')) ? (1) : (0);
$action{post}=($form->param('Post Scan')) ? (1) : (0);
$action{flood}=($form->param('Flood')) ? (1) : (0);
$action{conn}=($form->param('Connection Overflow')) ? (1) : (0);

$action{aim}=($form->param('aim')) ? (1) : (0);                  
$action{aimwebcontent}=($form->param('aimwebcontent')) ? (1) : (0);        
$action{applejuice}=($form->param('applejuice')) ? (1) : (0);           
$action{ares}=($form->param('ares')) ? (1) : (0);                 
$action{battlefield1942}=($form->param('battlefield1942')) ? (1) : (0);      
$action{battlefield2}=($form->param('battlefield2')) ? (1) : (0);         
$action{bgp}=($form->param('bgp')) ? (1) : (0);                  
$action{biff}=($form->param('biff')) ? (1) : (0);                 
$action{bittorrent}=($form->param('bittorrent')) ? (1) : (0);           
$action{chikka}=($form->param('chikka')) ? (1) : (0);               
$action{cimd}=($form->param('cimd')) ? (1) : (0);                 
$action{ciscovpn}=($form->param('ciscovpn')) ? (1) : (0);             
$action{citrix}=($form->param('citrix')) ? (1) : (0);               
#$action{counterstrike-source}=($form->param('counterstrike-source')) ? (1) : (0); 
$action{counterstrike}=($form->param('counterstrike')) ? (1) : (0); 
$action{cvs}=($form->param('cvs')) ? (1) : (0);                  
#$action{dayofdefeat-source}=($form->param('dayofdefeat-source')) ? (1) : (0);   
$action{dayofdefeat}=($form->param('dayofdefeat')) ? (1) : (0);   
$action{dhcp}=($form->param('dhcp')) ? (1) : (0);                 
$action{directconnect}=($form->param('directconnect')) ? (1) : (0);        
$action{dns}=($form->param('dns')) ? (1) : (0);                  
$action{doom3}=($form->param('doom3')) ? (1) : (0);                
$action{edonkey}=($form->param('edonkey')) ? (1) : (0);              
$action{fasttrack}=($form->param('fasttrack')) ? (1) : (0);            
$action{finger}=($form->param('finger')) ? (1) : (0);               
$action{freenet}=($form->param('freenet')) ? (1) : (0);              
$action{ftp}=($form->param('ftp')) ? (1) : (0);                  
$action{gkrellm}=($form->param('gkrellm')) ? (1) : (0);              
$action{gnucleuslan}=($form->param('gnucleuslan')) ? (1) : (0);          
$action{gnutella}=($form->param('gnutella')) ? (1) : (0);             
$action{goboogy}=($form->param('goboogy')) ? (1) : (0);              
$action{gopher}=($form->param('gopher')) ? (1) : (0);               
$action{h323}=($form->param('h323')) ? (1) : (0);                 
#$action{halflife2-deathmatch}=($form->param('halflife2-deathmatch')) ? (1) : (0); 
$action{halflife2}=($form->param('halflife2')) ? (1) : (0); 
$action{hddtemp}=($form->param('hddtemp')) ? (1) : (0);              
$action{hotline}=($form->param('hotline')) ? (1) : (0);              
$action{http-rtsp}=($form->param('http-rtsp')) ? (1) : (0);            
$action{http}=($form->param('http')) ? (1) : (0);                 
$action{ident}=($form->param('ident')) ? (1) : (0);                
$action{imap}=($form->param('imap')) ? (1) : (0);                 
$action{imesh}=($form->param('imesh')) ? (1) : (0);                
$action{ipp}=($form->param('ipp')) ? (1) : (0);                  
$action{irc}=($form->param('irc')) ? (1) : (0);                  
$action{jabber}=($form->param('jabber')) ? (1) : (0);               
$action{kugoo}=($form->param('kugoo')) ? (1) : (0);                
$action{live365}=($form->param('live365')) ? (1) : (0);              
$action{lpd}=($form->param('lpd')) ? (1) : (0);                  
$action{mohaa}=($form->param('mohaa')) ? (1) : (0);                
$action{msn-filetransfer}=($form->param('msn-filetransfer')) ? (1) : (0);     
$action{msnmessenger}=($form->param('msnmessenger')) ? (1) : (0);         
$action{mute}=($form->param('mute')) ? (1) : (0);                 
$action{napster}=($form->param('napster')) ? (1) : (0);              
$action{nbns}=($form->param('nbns')) ? (1) : (0);                 
$action{ncp}=($form->param('ncp')) ? (1) : (0);                  
$action{netbios}=($form->param('netbios')) ? (1) : (0);              
$action{nntp}=($form->param('nntp')) ? (1) : (0);                 
$action{ntp}=($form->param('ntp')) ? (1) : (0);                  
$action{openft}=($form->param('openft')) ? (1) : (0);               
$action{pcanywhere}=($form->param('pcanywhere')) ? (1) : (0);           
$action{poco}=($form->param('poco')) ? (1) : (0);                 
$action{pop3}=($form->param('pop3')) ? (1) : (0);                 
$action{qq}=($form->param('qq')) ? (1) : (0);                   
#$action{quake-halflife}=($form->param('quake-halflife')) ? (1) : (0);       
$action{quake}=($form->param('quake')) ? (1) : (0);       
$action{quake1}=($form->param('quake1')) ? (1) : (0);               
$action{radmin}=($form->param('radmin')) ? (1) : (0);               

$action{rdp}=($form->param('rdp')) ? (1) : (0);                   
$action{rlogin}=($form->param('rlogin')) ? (1) : (0);                
$action{rtsp}=($form->param('rtsp')) ? (1) : (0);                  
$action{shoutcast}=($form->param('shoutcast')) ? (1) : (0);             
$action{sip}=($form->param('sip')) ? (1) : (0);                   
#$action{skypeout}=($form->param('skypeout')) ? (1) : (0);              
#$action{skypetoskype}=($form->param('skypetoskype')) ? (1) : (0);          
$action{smb}=($form->param('smb')) ? (1) : (0);                   
$action{smtp}=($form->param('smtp')) ? (1) : (0);                  
$action{snmp}=($form->param('snmp')) ? (1) : (0);                  
$action{socks}=($form->param('socks')) ? (1) : (0);                 
$action{soribada}=($form->param('soribada')) ? (1) : (0);              
$action{soulseek}=($form->param('soulseek')) ? (1) : (0);              
$action{ssdp}=($form->param('ssdp')) ? (1) : (0);                  
$action{ssh}=($form->param('ssh')) ? (1) : (0);                   
$action{ssl}=($form->param('ssl')) ? (1) : (0);                   
$action{stun}=($form->param('stun')) ? (1) : (0);                  
$action{subspace}=($form->param('subspace')) ? (1) : (0);              
$action{subversion}=($form->param('subversion')) ? (1) : (0);            
$action{teamspeak}=($form->param('teamspeak')) ? (1) : (0);             
$action{telnet}=($form->param('telnet')) ? (1) : (0);                
$action{tesla}=($form->param('tesla')) ? (1) : (0);                 
$action{tftp}=($form->param('tftp')) ? (1) : (0);                  
$action{thecircle}=($form->param('thecircle')) ? (1) : (0);             
$action{tls}=($form->param('tls')) ? (1) : (0);                   
$action{tor}=($form->param('tor')) ? (1) : (0);                   
$action{tsp}=($form->param('tsp')) ? (1) : (0);                   
$action{uucp}=($form->param('uucp')) ? (1) : (0);                  
$action{validcertssl}=($form->param('validcertssl')) ? (1) : (0);          
$action{ventrilo}=($form->param('ventrilo')) ? (1) : (0);              
$action{vnc}=($form->param('vnc')) ? (1) : (0);                   
$action{whois}=($form->param('whois')) ? (1) : (0);                 
$action{worldofwarcraft}=($form->param('worldofwarcraft')) ? (1) : (0);       
$action{x11}=($form->param('x11')) ? (1) : (0);                   
$action{xboxlive}=($form->param('xboxlive')) ? (1) : (0);              
$action{xunlei}=($form->param('xunlei')) ? (1) : (0);                
$action{yahoo}=($form->param('yahoo')) ? (1) : (0);                 
$action{zmaap}=($form->param('zmaap')) ? (1) : (0);                 

$action{audiogalaxy}=($form->param('audiogalaxy')) ? (1) : (0);           
$action{http-dap}=($form->param('http-dap')) ? (1) : (0);              
$action{http-freshdownload}=($form->param('http-freshdownload')) ? (1) : (0);    
$action{http-itunes}=($form->param('http-itunes')) ? (1) : (0);           
$action{httpaudio}=($form->param('httpaudio')) ? (1) : (0);             
$action{httpcachehit}=($form->param('httpcachehit')) ? (1) : (0);          
$action{httpcachemiss}=($form->param('httpcachemiss')) ? (1) : (0);         
$action{httpvideo}=($form->param('httpvideo')) ? (1) : (0);             
$action{pressplay}=($form->param('pressplay')) ? (1) : (0);             
$action{quicktime}=($form->param('quicktime')) ? (1) : (0);             
$action{snmp-mon}=($form->param('snmp-mon')) ? (1) : (0);              
$action{snmp-trap}=($form->param('snmp-trap')) ? (1) : (0);

#=========================================================================================
print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css">);
print qq(<style type="text/css">table.sortable thead{background-color:#eee;color:#666666;font-weight: bold;cursor: default;});
print qq(button.menu{margin-right: 4px;height:18px;width:14%;font:10px Verdana;color:white;background:#336699;border:1px solid black;cursor:hand;});
print qq(</style></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq (<button  onclick="parent.mainFrame.location='l7log.cgi'" style="width:170" hidefocus="true" class="menu">Log Configuration</button>);
print qq (<button  onclick="parent.mainFrame.location='flow_user.cgi'" style="width:170" hidefocus="true" class="menu">Unit</button>);
print qq (<button  onclick="parent.mainFrame.location='flow_user_sec.cgi'" style="width:170" hidefocus="true" class="menu">Transparent Subnets</button>);
print qq (<button  onclick="parent.mainFrame.location='storage_set.cgi'" style="width:170" hidefocus="true" class="menu">Storage</button>);
#假如認證失敗，就直接結束
if ( !$gLOGINRESULT ) { general_script(); exit;}

if ( $action{action} ) { maintainL7log( %action ); }

#------- start to draw every form object to interact with users ------------------------------------
print qq (<div align="center">);
print qq (<form name="l7logform" method="post" action="storage_set.cgi">);

l7logScript();

showl7log( %action ); 

print qq (<input type="hidden" name="action" id="action" value="">);
print qq (<input type="hidden" name="path" id="path" value="">);
print qq (</form>);
print qq (</div>);

general_script();

print qq(</body></html>);
