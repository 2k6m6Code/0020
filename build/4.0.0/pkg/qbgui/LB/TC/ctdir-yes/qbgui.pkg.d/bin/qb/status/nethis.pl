#!/usr/local/sbin/perl
push(@INC, "/usr/local/apache/qb/status");
require 'nethis.lib';
use checker;
# package checker;

my $DAYSTOKEEP = 7;


# key --  "prto,srcip,dstip,srcprt,dstprt,sprts,dprts,icmpid"
# value --  "pkts,bytes"

# input arguments:
# $_[0]: hash to push records into
#
# $_[1]: pointer to fwmark
sub packIntoHash
{
    my $fd = checker::fwmark_fw_get($_[1]);

    my $srcnet = checker::fwmarkData_csSrcNet_get($fd);
    my $dstnet = checker::fwmarkData_csDstNet_get($fd);
    $srcnet = "0.0.0.0/0" if ($srcnet eq '');
    $dstnet = "0.0.0.0/0" if ($dstnet eq '');
    $srcnet = $1 if ($srcnet =~ /(.*)\/32/);
    $dstnet = $1 if ($dstnet =~ /(.*)\/32/);
    my $srcport;
    my $dstport;
    my $srcports;
    my $dstports;

    if (checker::fwmarkData_csSrcPort_get($fd) =~ /:/)
    {
        $srcports = "spts:" . checker::fwmarkData_csSrcPort_get($fd);
    }
    else
    {
        $srcport = checker::fwmarkData_csSrcPort_get($fd);
        $srcport = "spt:$srcport" if ($srcport ne '');
    }

    if (checker::fwmarkData_csDstPort_get($fd) =~ /:/)
    {
        $dstports = "dpts:" .  checker::fwmarkData_csDstPort_get($fd);
    }
    else
    {
        $dstport = checker::fwmarkData_csDstPort_get($fd);
        $dstport = "dpt:$dstport" if ($dstport ne '');
    }

    my $proto = checker::fwmarkData_csProto_get($fd);
    $proto = 'all' if ($proto eq '');

    my $pcnt = checker::fwmark_pcnt_get($_[1]);
    my $bcnt = checker::fwmark_bcnt_get($_[1]);

    $_[0]->{"$proto,$srcnet,$dstnet,$srcport,$dstport,$srcports,$dstports,"} = "$pcnt,$bcnt";
}


# add values in two CSV hashes
# $_[0]: hash1
# $_[1]: hash2
# return a hash contains the addition of them all
sub addHashes()
{
    my $a = $_[0];
    my $b = $_[1];
    my %c;

    while (my ($key, $value) = each(%$a))
    {
        # if such key also exists in hash b
        # add them, else just put value in %c
        if (exists $b->{$key})
        {
            $value =~ m#(.*),(.*)#; # parse hash a value
            my $a_pkts = $1;
            my $a_bytes = $2;
            $b->{$key} =~ m#(.*),(.*)#; # parse hash b value
            my $b_pkts = $1;
            my $b_bytes = $2;
            my $c_pkts = $a_pkts + $b_pkts;
            my $c_bytes = $a_bytes + $b_bytes;

            $c{$key} = "$c_pkts,$c_bytes";

            # once matched, take the one in b out
            delete $b->{$key}
        }
        else { $c{$key} = $value; }
    }

    # now if anything else is left in %b, it's something that wasn't in a
    # and just copy right to %c

    while (my ($key, $value) = each(%$b))
    {
        $c{$key} = $value;
    }

    return %c;
}

sub logmin()
{
    my %records;
    $fn = checker::parseMangle();
    for ($i = 0; $i < $checker::fwlist_size; $i++)
    {
        my $fnitem = checker::get_fn($fn, $i);
        my $fw = checker::fwmarkNode_data_get($fnitem);
        my $fd = checker::fwmark_fw_get($fw);
        packIntoHash(\%records, $fw);
    }
    # reset to 0
    `/usr/local/sbin/iptables -t mangle -Z`;

    logRules(\%records);

    my %date_time = date(time);
    $date_time{'date_ftag'} =~ m#(....)(..)(..)_(..)(..)#;
    my $midnight_time = mktime(0, 0, 0, $3, $2-1, $1 - 1900);
    my $timenow = mktime(0, $5, $4, $3, $2-1, $1 - 1900);

    writeCSVFile(\%records, "$CSVPATH/qbnethis/new/$midnight_time", $timenow);
}

# check modified time for files
# if modified time is over a week ago, delete
sub rollOver()
{
    my @dirlist;
    my @templist;

    opendir(DIR, "$CSVPATH/qbnethis/new/") || die "opendir: $!";
    @templist = readdir(DIR);
    for (my $i = 0; $i < scalar(@templist); $i++)
    {
        $templist[$i] = "$CSVPATH/qbnethis/new/" . $templist[$i];
    }
    @dirlist = (@dirlist, @templist);
    closedir(DIR);

    foreach $file (@dirlist)
    {
        if (($file ne ".") && ($file ne ".."))
        {
            my ($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size, $atime,$mtime,$ctime,$blksize,$blocks)
                = stat("$file");

            # if ove a week ago
            if ((time - $mtime) > (86400 * $DAYSTOKEEP)) { unlink("$file"); }
        }
    }
}

mkdir("$CSVPATH/qbnethis") unless (-e "$CSVPATH/qbnethis");
mkdir("$CSVPATH/qbnethis/new") unless (-e "$CSVPATH/qbnethis/new");
unless (-e "$CSVPATH/qbnethis/rules")
{
    open(FD, ">$CSVPATH/qbnethis/rules") || die "Cannot create rule file\n";
    close(FD);
}

system("chmod 777 $CSVPATH/qbnethis");
system("chmod 777 $CSVPATH/qbnethis/new");
system("chmod 777 $CSVPATH/qbnethis/rules");

if (@ARGV[0] eq 'logmin') { logmin(); }
elsif (@ARGV[0] eq 'rollover') { rollOver(); }
else
{
    print "nethis.pl [logmin | rollover]\n";
}
