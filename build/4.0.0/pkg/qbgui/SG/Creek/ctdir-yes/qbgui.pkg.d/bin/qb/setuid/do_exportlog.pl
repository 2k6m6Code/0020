#!/usr/bin/perl
use XML::Simple;

my $gXMLLOCK='/usr/local/apache/qb/XMLLOCK';

#===============================================================================================
sub XMLread
{
    my ($filename)=@_;
    if ( !open(XMLLOCK, "< $gXMLLOCK") ) 
    { 
        $gLOGINRESULT=0;
        $gMSGPROMPT.=qq (Read Lock Error\\n); 
        return;
    }
    flock(XMLLOCK, 2); 
    my $ref=XMLin($filename, forcearray=>1);
    flock(XMLLOCK, 8); 
    close XMLLOCK;
    return $ref;
}
#XMLread

#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/overview.xml
#-------------------------------------------------------------------
my $OVERVIEW='/usr/local/apache/qbconf/overview.xml';

my $opt=XMLread($OVERVIEW);

my $LOGSERVER=$opt->{rmlogserver};

my $USERNAME=$opt->{rmusername};

my $PASSWORD=$opt->{rmpassword};

my $EXPORT_LOG_SHELL='/usr/local/apache/qb/setuid/exportlog.sh ';

my $EXPORT_PARAMS=$LOGSERVER.' '.$USERNAME.' '.$PASSWORD;

my $COMMAND=qq($EXPORT_LOG_SHELL$EXPORT_PARAMS);

my $RESULT=`$COMMAND`;

print qq ( $RESULT );

