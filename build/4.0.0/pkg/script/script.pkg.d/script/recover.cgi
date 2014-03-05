#!/usr/bin/perl
use CGI;

print "Content-type:text/html\n\n";

#read-in form information ------------------------------

my $gRUN='/opt/qb/bin/script/run ';        
my $form = new CGI;
my %action;

$action{action} = $form->param('action');
$action{passcode} = $form->param('passcode');


if ( $action{action} eq "DORECOVERY" ) 
{ 
    doRecovery(%action); 
}
else
{
    normalPage();
}


#==================================================================================================
# For first read  without  any request
sub normalPage
{
    print qq(<html><head><link rel="stylesheet" type="text/css"></head>);
    
    print qq(<body bgcolor="#225588" text="#ffffff" link="#000040" vlink="#400040">);
    
    recoveryScript();

    #------- start to draw every form object to interact with users --------------------------------
    print qq(<div align="center">);

    print qq(<form name="ispinfoform" method="post" action="recover.cgi" target="message">);

    print qq(<iframe name="message" style="background-color:red; width:500; height:100; filter:alpha(opacity=70);"></iframe><br>);
    
    print qq(Password:<input type="text" name="passcode" maxlength="10"><br>); 
    
    print qq(<input type="button" name="dorecovery" value="Click to start recovery process" onClick="goSubmit('DORECOVERY')">);

    print qq(<input type="hidden" name="action" value="">);
    
    print qq(</form>);
    
    print qq (</div>);

    print qq(</body></html>);
}
#normalPage



#==================================================================================================
# runCommand( %action=(command=>"", params=>"") ) 
# $action{command} => command to run  
sub runCommand
{
    my (%action)=@_;
    my @gTOOLPATH=('/opt/qb/bin/script/', '/opt/qb/bin/', '/opt/qb/sbin/', '/sbin/', '/bin/', '/usr/sbin/', '/usr/bin/', '/opt/qb/apps/');
    my $cmdPATH='';
    my $runstring='';
    my $result='';

    # search @gTOOLPATH to locate where $action{command} is located    
    foreach my $path ( @gTOOLPATH ) { if ( -e $path.$action{command} ) { $cmdPATH=$path; last; } }

    if ( $cmdPATH )
    {
        $runstring=$gRUN." ".$cmdPATH.$action{command}."  ".$action{params};
        $result=`$runstring`; 
    }
    else
    {
        $result="Command NOT Found !!";
    }

    return $result;

}
#runCommand


#=================================================================================================
# doRecovery( %action=(action=>'') )
# $action{action} => action to do
sub doRecovery()
{
    my $result='';

    print qq(<html><head><link rel="stylesheet" type="text/css"></head><body bgcolor="#445588" text="#ffffff" link="#000040" vlink="#400040">);
    
    if ( $action{passcode} ne "123" ) 
    { 
        print << "PASSWORDERROR";

        <script for='window' event='onload'>
            if((url = parent.location + ''))
            if(parent.location.href != window.location.href)
            parent.passwordError();
        </script>
PASSWORDERROR

        $result=qq(Password checking Error !!);
    }
    else
    {
        print << "RECOVERYOK";

        <script for='window' event='onload'>
            if((url = parent.location + ''))
            if(parent.location.href != window.location.href)
            parent.recoveryComplete();
        </script>
RECOVERYOK

        runCommand(command=>'reset.sh', params=>''); 

        $result=qq( Reset to Factory Default Successfully !! );
    }

    print $result;
    
    print qq (</body>);
    print qq (</html>);

}
#doRecovery


sub recoveryScript
{
    print << "RECOVERYSCRIPT";

    <script language="javascript">

        TIMER=0;

        function goSubmit(action_value)
        {
            var myform=window.document.forms[0];
            myform.action.value=action_value;
            myform.submit();
            myform.dorecovery.disabled=true; 
            countdownid=setInterval("countDown()",1000);
        } 
        
        function passwordError()
        {
            clearInterval(countdownid);
            var myform=window.document.forms[0];
            myform.dorecovery.value="Click to retry system recovery !!";
            myform.dorecovery.disabled=false;
            alert('Please key in the correct password !!');
        } 
        
        function recoveryComplete() 
        { 
            clearInterval(countdownid);
            var myform=window.document.forms[0];
            myform.dorecovery.value="System Recovery Completed !!";
            alert('System is going to  reboot now!! Please wait about one  minute ...');
        }

        function countDown()
        {
            var myform=window.document.forms[0];
            myform.dorecovery.value=printSymbol(TIMER);
            TIMER++;
        }

        function printSymbol(count)
        {   
            var symbolstr=' '+count+' sec ';
            for(var i=0; i<count;i++) { symbolstr='< '+symbolstr+' >';}
            return symbolstr;
        }
        

    </script>
    
RECOVERYSCRIPT
}
# recoveryScript


