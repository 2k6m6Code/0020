package QB_Action;

my %data;

sub new 
{
    my $class=shift;
    my $self={};
    my ($sec, $min, $hour, $day, $mon, $year) = localtime(time);
    $data->{all} = join("/",($year+1900,$mon+1,$day))." ".join(":",($hour,$min,$sec));
    $data->{date} = join("/",($year+1900,$mon+1,$day));
    $data->{time} = join(":",($hour,$min,$sec));
    bless($self);
    return $self;
}

sub getall
{
    return $data->{all};
}

sub getdate
{
    return $data->{date};
}

sub gettime
{
    return $data->{time};
}

sub checkPath
{
    my ($object,$path)=@_;
    my @ar_path = split(/\//,$path);
    my $tmp_path = "/";
    foreach my $unit (@ar_path)
    {
        if (!$unit){next;}
        if (!-e "$tmp_path/$unit")
        {
            system("/bin/mkdir /tmp/$unit");
            system("/usr/local/apache/qb/setuid/run /bin/cp -a /tmp/$unit $tmp_path/");
        }
        $tmp_path .=$unit."/";
    }
}

sub getdir
{
    my ($object,$path)=@_;
    @FileList = split(/\s+/,`/usr/local/apache/qb/setuid/run /usr/bin/dir $path`);
    return @FileList;
}

sub getfile
{
    my ($object,$path)=@_;
    my @data;
    open(FILE,"<$path");
    while(<FILE>)
    {
        chomp;
        push(@data,$_);
    }
    close(FILE);
    return @data;
}

return 1;
