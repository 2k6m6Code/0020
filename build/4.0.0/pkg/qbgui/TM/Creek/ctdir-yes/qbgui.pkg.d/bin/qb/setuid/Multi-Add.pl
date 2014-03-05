#!/usr/bin/perl

require ("/usr/local/apache/qb/qbmod.cgi");

my @cgi=@ARGV;
my $action=$cgi[0];
my $file=$cgi[1];
my $filelist=XMLread("/usr/local/apache/qbconf/auth.xml");
my $list=$filelist->{user};

if ($action eq 'import')
{
    my $choose;
    my @subscharrary;
    my $schdule;
    foreach my $dd (@$list)
    {
       if ($dd->{schname} ne $file){next;}
       
       $choose=$dd->{member};
       my %newschedule;
       foreach my $user (@$choose)
       {
          if ($user->{idd} eq '' || $user->{pwd} eq ''){next;}
          $schdule=$user->{type};
          my %newschedule;
          $newschedule{ip}=$user->{ip};
          $newschedule{idd}=$user->{idd};
          $newschedule{pwd}=$user->{pwd};
          $newschedule{mail}=$user->{mail};
          $newschedule{type}=$user->{type};
          $newschedule{time}=$user->{time};
          push(@subscharray, \%newschedule); 
       }
        if (open(FILE,"/tmp/tmpupg/user.tmp"))
        {
    	    foreach $data (<FILE>)
    	    {
    	        $data=~s/\r//g;
    	        $data=~s/\n//g;
    	        if($data eq '' || $data eq null){next};
    	        if(grep(/END/,$data)){break;}
    	        my @tmp = split(/,/,$data);
    	        if ($tmp[1] eq 'Name' || $tmp[1] eq ''){next;}
    	        if ($tmp[2] eq 'Pwd' || $tmp[2] eq ''){next;}
    	        my %newschedule;
          	$newschedule{ip}=$tmp[0];
          	$newschedule{idd}=$tmp[1];
          	$newschedule{pwd}=$tmp[2];
          	$newschedule{mail}=$tmp[3];
          	$newschedule{type}=$schdule;
          	$newschedule{time}='';
          	push(@subscharray, \%newschedule); 
    	    }
    	}
    	close(FILE);
    }
    $newschedule{member}=\@subscharray;
    $newschedule{schname}=$file;
    $newschedule{description}=$schdule;
    foreach my $sh (@$list)
    {
        if ( $sh->{schname} eq $file )
        {
            $sh=\%newschedule;
        }
    }
    
    XMLwrite($filelist, "/usr/local/apache/qbconf/auth.xml");
}elsif ($action eq 'export' && $file ne '')
{
    my $menber;
    my @csv;
    foreach my $dd (@$list)
    {
        if ($dd->{schname} ne $file){next;}
        $menber=$dd->{member};  
        foreach my $data (@$menber)
	{
	    if ($data->{idd} eq '' || $data->{pwd} eq ''){next;}
	    my $tmp_data=$data->{ip}.",".$data->{idd}.",".$data->{pwd}.",".$data->{mail}."\n";
	    push(@csv,$tmp_data);
	}
    }
    open(FILE,">/usr/local/apache/qb/downloads/$file.csv");
    print FILE "IP,Name,Pwd,Mail\n";
    foreach my $input (@csv)
    {
        print FILE $input;
    }
    close(FILE);  
}
