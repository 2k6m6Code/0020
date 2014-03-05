#!/usr/bin/perl  
use CGI;
require ("/usr/local/apache/qb/qbmod.cgi");

authenticate(action=>'RANDOMCHECK');

my $form = new CGI;
#my $clientaddr = $form->param('clientaddr');
#my $clientname = $form->param('clientname');
#my $clientuser = $form->param('clientuser');
#my $clientgroup = $form->param('clientgroup');
my $targetgroup = $form->param('targetgroup');
my $url = $form->param('url');


print "Content-type:text/html\n\n";
#page css
print qq(<html><head>);
print qq(<title>ERROR: The requested URL could not be retrieved</title>);
print qq(<style type="text/css"><!--BODY{background-color:#ffffff;font-family:verdana,sans-serif}PRE{font-family:sans-serif}--></style>);
print qq(</head>);
print qq(<body>); 
#deny message
my $DENY_MSG = "/usr/local/apache/qbconf/deny";
my $DENY = runCommand(command=>'cat', params=>$DENY_MSG);
$DENY =~ s/{url}/$url/g;
$DENY =~ s/{category}/$targetgroup/g;
print qq($DENY);
=cut
print qq($clientaddr<br>);
print qq($clientname<br>);
print qq($clientuser<br>);
print qq($clientgroup<br>);
print qq($targetgroup<br>);
print qq($url<br>);
print qq(</form>);
=cut

#XMLread
1
