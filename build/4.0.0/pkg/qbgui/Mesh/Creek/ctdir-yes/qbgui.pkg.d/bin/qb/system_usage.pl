#!/usr/bin/perl

use CGI;

my $form=new CGI;
my $id = $form->param("id");

print "Content-type:text/html\n\n";

if ($id ne '')
{
    if ($id eq 'cpu')
    {
        get_data('cpu','Cpu_User.log')
    }
    elsif ($id eq 'mem')
    {
        get_data('mem','Mem_User.log')
    }
    elsif ($id eq 'cache')
    {
        get_data('cache','Cache_User.log')
    }
    elsif ($id eq 'ram')
    {
        get_data('ram','Ram_User.log')
    }
    elsif ($id eq 'session')
    {
        get_data('session','Session_User.log')
    }
}


sub get_data
{
    my ($name,$file)=@_;
    print `/usr/local/apache/qb/setuid/run /bin/cat /mnt/log/$file`;
}
##
1
