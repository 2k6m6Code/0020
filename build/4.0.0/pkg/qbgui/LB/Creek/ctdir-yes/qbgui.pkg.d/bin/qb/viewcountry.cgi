#!/usr/bin/perl
use CGI;
require ("qbmod.cgi");
print "Content-type:text/html\n\n";
my $form=new CGI;
my $countryname=$form->param('countryname');

#=========================================================================================
#print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="stylesheet" href="gui.css" type="text/css"></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);


#------- start to draw every form object to interact with users ------------------------------------
print qq(<div align="center"><form name="mxform" method="post" action="qblistmx.cgi">);


#------- start show ip list 
    my $countryref=XMLread($gPATH.'country.xml');
    my $countrylist=$countryref->{country};
    foreach my $item ( @$countrylist )
    {
        if ( $item->{countryname} eq $countryname ) 
        { 
            print qq (<table class="body" bgcolor="#336699" cellspacing="5" cellpadding="0" border="0">);
            print qq (<tr>);
            #print qq (<td class="qbtext">);
            my @arry_country=split(/,/, $item->{countryaddress});
	    my $linecount=0;
            foreach my $arry_country_ip ( @arry_country )
            {
            	#print qq (   $arry_country_ip,);
            	print qq (<td align="left" class="qbtext" style="WIDTH: 120px" >$arry_country_ip</td>);
            	$linecount++;
            	if ($linecount eq '5')
            	{
            	    #print qq (\n);
            	    print qq (</tr>);
            	    print qq (<tr>);
            	    $linecount=0;
            	}
            }
            #print qq (</td>);
            print qq (</tr>);
            print qq (</table>);
        }
        
    }
	
	
	
	
	
	

print qq(</form></div></body></html>);


