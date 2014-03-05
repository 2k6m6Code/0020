package QB_Xml;

use XML::Simple;
use Data::Dumper;

my $gXMLLOCK = '/usr/local/apache/qb/XMLLOCK';
my $xml = new XML::Simple;
sub new
{
    my $class=shift;
    my $self={};
    bless($self);
    return $self;
}

sub read
{
    my ($object,$filename)=@_;
    if ( (-e $filename) || (-s $filename) )
    {
	if ( !open(XMLLOCK, "< $gXMLLOCK") ){return;}
	flock(XMLLOCK, 2);
	my $ref=$xml->XMLin($filename, forcearray => 1);
	flock(XMLLOCK, 8);
	close XMLLOCK;
	return $ref;
    }
}

sub write
{
    my ($object,$ref, $filename)=@_;
    if ($ref eq ""){return;}
    system("/usr/local/apache/qb/setuid/run /bin/chmod 777 $filename");
    if ( !open(XMLLOCK, "> $gXMLLOCK") ){return;}
    flock(XMLLOCK, 2);
    if ( !open(XMLFILE, "> $filename") ){return;}
    my $result=$xml->XMLout($ref);
    print XMLFILE $result;
    close XMLFILE;
    flock(XMLLOCK, 8);
    close XMLLOCK;
}

return 1;
