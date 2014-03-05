#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start
# --------------------------------------------------------------
my $QB_SQUID="/usr/local/squid/etc/";
my $QB_CONTENT_XMLCONF="/usr/local/apache/qbconf/content.xml";
my $QB_SQUIDURL_XMLCONF="/usr/local/apache/qbconf/squidurl.xml";
my $QB_ZONE_XMLCONF="/usr/local/apache/qbconf/zonecfg.xml";
my $QB_SQUID_CONF="/etc/squid/squid.conf";
my $QB_CONTENT_SH=$QB_SQUID."content.sh";
my $QB_DELCONTENT_SH=$QB_SQUID."delcontent.sh";
my $QB_SQUID_XMLCONF="/usr/local/apache/qbconf/squidgen.xml";
my $QB_SQUID_KEYWORD=$QB_SQUID."keyword.txt";

my $squidgen=XMLread($QB_SQUID_XMLCONF);

if( !$squidgen ) #if the string is NULL
{
    print "$QB_SQUID_XMLCONF is NULL \n";
}
    


#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/content.xml
#------------------------------------------------------------------
my $content=XMLread($QB_CONTENT_XMLCONF);

if( !$content ) #if the string is NULL
{
    print "$QB_CONTENT_XMLCONF is NULL \n";
}

my $keyword=$content->{keyword}->[0]->{name};

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/squidurl.xml
#------------------------------------------------------------------
my $squidurl=XMLread($QB_SQUIDURL_XMLCONF);

if( !$squidurl ) #if the string is NULL
{
    print "$QB_SQUIDURL_XMLCONF is NULL \n";
}

my $exempt=$squidurl->{exempt}->[0]->{net};


#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/zonecfg.xml
#------------------------------------------------------------------
my $zone=XMLread($QB_ZONE_XMLCONF);

if( !$zone ) #if the string is NULL
{
    print "$QB_ZONE_XMLCONF is NULL \n";
}
my $natarray=$zone->{nat};

my %netarray;
foreach my $nat ( @$natarray )
{
    my @tmparray;
    my $isend = 0;
    
    push(@tmparray, 1);
    if( $nat->{natid} eq "system" ) { next; }
    foreach my $net ( @$exempt ) 
    {
         my @range=split(/\-/, $net->{ip});
         my @iparray1=split(/\./, $range[0]);
         my $subnet=$iparray1[0]."\.".$iparray1[1]."\.".$iparray1[2]."\.0/24";
         
         if ( $nat->{network} eq $subnet )
         {
             my @iparray2=split(/\./, $range[1]);
             
             if ( $iparray1[3] eq "1" )
             {
                 shift @tmparray;
                 push(@tmparray, $iparray2[3] + 1);
                 next;
             }
             if ( $iparray2[3] eq "254" )
             {
                 $isend=1;
                 push(@tmparray, $iparray1[3] - 1);
                 next;
             }
             push(@tmparray, $iparray1[3] - 1);
             push(@tmparray, $iparray2[3] + 1);
             #runCommand(command=>"echo", params=>$tmparray[1].' '.'>/tmp/bb');
         }
    }
    if ( $isend eq '0' ) { push(@tmparray, 254); }
    
    @tmparray = sort { $a <=> $b } @tmparray;
    
    my $tmpsubnet=$nat->{network};
    my $arraynum=$#tmparray + 1;
    unshift(@tmparray, $arraynum);
    $tmpsubnet=~s/\/24//g;
    @tmphead=split(/\./, $tmpsubnet);
    my $netkey=$tmphead[0]."\.".$tmphead[1]."\.".$tmphead[2];
    $netarray{"$netkey"}=\@tmparray;
}

#------------------------------------------------------------------
# block keyword content
#------------------------------------------------------------------
if ( !open(CONTENT,">$QB_CONTENT_SH") )
{
    print qq (Fail to Open QB_CONTENT_SH Config file !!);
}
if ( !open(DELCONTENT,">$QB_DELCONTENT_SH") )
{
    print qq (Fail to Open QB_CONTENT_SH Config file !!);
}

foreach my $netkey ( keys %netarray )
{
    runCommand(command=>"echo", params=>$netarray{$netkey}[0].' '.'>>/tmp/lll'); 
    foreach (1...$netarray{$netkey}[0])
    {
       if ( ($_ % 2) eq 1 )
       {
           my $iprange1=$netkey."\.".$netarray{$netkey}[$_];
           my $iprange2=$netkey."\.".$netarray{$netkey}[$_ + 1];
           foreach my $word ( @$keyword )
           {
               if ( $word->{keywordname} eq "system" ) { next; } 
               #print CONTENT qq "/sbin/iptables -m iprange --dst-range $iprange1-$iprange2 -A OUTPUT -p tcp --sport 3128 -m string --algo bm --string \"$word->{keywordname}\" -j DROP\n";
               #print DELCONTENT qq "/sbin/iptables -m iprange --dst-range $iprange1-$iprange2 -D OUTPUT -p tcp --sport 3128 -m string --algo bm --string \"$word->{keywordname}\" -j DROP\n";
           }
       }
    
    }
}

if ( !open(KEYWORD,">$QB_SQUID_KEYWORD") )
{
    print qq (Fail to Open KEYWORD Config file !!);
}
runCommand(command=>"cat", params=>'/dev/null > /usr/local/squid/etc/keyword.txt'); 
foreach my $word ( @$keyword )
{
    if ( $word->{keywordname} eq 'system' ) { next; }
    print KEYWORD qq "$word->{keywordname}\n";
}

if ( $squidgen->{proxy} eq '1' )
{
    print CONTENT qq "/sbin/iptables -t mangle -A PREROUTING -p tcp --destination-port 1024:65535  -m state --state NEW,ESTABLISHED ";
    print CONTENT qq "-m string --algo bm --string \"Proxy-Connection\" -j DROP\n";
    #print CONTENT qq "/sbin/iptables -t mangle -A PREROUTING -p tcp --destination-port 3129:65535  -m state --state NEW,ESTABLISHED ";
    #print CONTENT qq "-m string --algo bm --string \"Proxy-Connection\" -j DROP\n";
    print DELCONTENT qq "/sbin/iptables -t mangle -D PREROUTING -p tcp --destination-port 1024:65535  -m state --state NEW,ESTABLISHED ";
    print DELCONTENT qq "-m string --algo bm --string \"Proxy-Connection\" -j DROP\n";
    #print DELCONTENT qq "/sbin/iptables -t mangle -D PREROUTING -p tcp --destination-port 3129:65535  -m state --state NEW,ESTABLISHED ";
    #print DELCONTENT qq "-m string --algo bm --string \"Proxy-Connection\" -j DROP\n";
}

close(CONTENT);
close(DELCONTENT);
chmod(0777, $QB_CONTENT_SH);
chmod(0777, $QB_DELCONTENT_SH);




