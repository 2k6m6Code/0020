#!/usr/bin/perl 
require ("../qbmod.cgi");
use CGI;
my $form= new CGI;
my $action=$form->param('action');
my $whattodo=$form->param('whattodo');
my $configuration=$form->param('configuration');

print "Content-type:text/html \n\n";
print qq (<html><head><link rel="stylesheet" href="../gui.css" type="text/css"></head><body class='message'>);

if ( $action eq "start" )
{
    my $result=runCommand(command=>"cpconfsetforupg.sh", params=>qq( $configuration  to));
    
    my $setver=getSetVersion($configuration);
    
    my $targetver=getTargetVersion();
    
    print qq ($result );

    if ( $whattodo eq "showversion")
    {
        print qq( Config. set version of \" $configuration \"  is $setver<br>);
        print qq( The config. version needed now is $targetver<br>);
        runCommand(command=>"cpconfsetforupg.sh", params=>qq( $configuration  delete));
    }
    elsif ( $whattodo eq "doupgrade" )       
    {
        if ( $setver=~m/0.0.0.0000/ )
        {
            from_0_0_0_0000_to_2_1_5_0000($configuration);
            from_2_1_5_0000_to_2_2_0_0000($configuration);
        }
        elsif ( $setver=~m/2.1.5.0000|2.2.0.0000/ )
        {
            from_2_1_5_0000_to_2_2_0_0000($configuration);
        }

        runCommand(command=>"cpconfsetforupg.sh", params=>qq( $configuration  back));
    }

    qbSync();
}

print qq (</body></html>);
