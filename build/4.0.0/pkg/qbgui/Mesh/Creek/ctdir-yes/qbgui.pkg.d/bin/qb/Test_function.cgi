#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }
#==================QB_Date.pm================

print "Testing QB_Action.pm \n";
use QB_Action;

my $day = QB_Action->new();

print "day->getall()   ";
if ($day->getall())
{
    print $day->getall()."--Yes\n";
}else
{
    print "No\n";
}

print "day->getdate()   ";
if ( $day->getdate() )
{
    print $day->getdate()."--Yes\n";
}else
{
    print "No\n";
}

print "day->gettime()   ";
if ($day->gettime())
{
    print $day->gettime()."--Yes\n";
}else
{
    print "No\n";
}

print "day->checkPath()   ";
$day->checkPath("/tmp/test_123/");
if (-e "/tmp/test_123")
{
    print "--Yes\n";
    system("/bin/rm -rf /tmp/test_123");
}else
{
    print "No\n";
}

print "day->getdir()   ";
my @dir = $day->getdir("/mnt/");
#foreach (@dir){print "$_\n";}
if ($#dir > 0){print "--YES\n";}

print "day->getfile()   ";
open(TEST,">/tmp/TEST_FILE");
print TEST "TEST\n";
print TEST "YES\n";
close(TEST);
my @data = $day->getfile("/tmp/TEST_FILE");
if ($#data ne 1){print "No\n";}
else
{
    if ($data[0] eq 'TEST' && $data[1] eq 'YES'){print "--YES\n";}
}
system("/bin/rm -f /tmp/TEST_FILE");

print "Testing QB_Action.pm End\n\n";

#==================QB_LOG.pm=================
print "Testing QB_LOG.pm \n";

use QB_LOG;

my $log = QB_LOG->new();

print "log->Save_Log()   ";
my $path = "/tmp/Log_Test1/".$day->getdate()."/";
$log->Save_Log($path,"Test_user","TEST");
if (-e $path)
{
    my @data = `/bin/cat $path/Test_user`;
    if (grep(/TEST/,@data))
    {
        print "--Yes\n";
        system("/bin/rm -rf $path/Test_user");
    }else
    {
        print "No\n";
    }
}

print "Testing QB_LOG.pm End\n\n";


