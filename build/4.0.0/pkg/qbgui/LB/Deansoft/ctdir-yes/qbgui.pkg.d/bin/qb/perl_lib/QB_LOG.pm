package QB_LOG;

use QB_Action;

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

sub new 
{
    my $class=shift;
    my $self={};
    bless($self);
    return $self;
}

sub Save_Log
{
    my ($object,$path,$file,$data)=@_;
    my $action = QB_Action->new();
    $path=~s/\/$//g;
    $action->checkPath($path);
    open(LOG,">>$path/$file");
    print LOG $action->getall()." $data\n";
    close(LOG);
}

return 1;
