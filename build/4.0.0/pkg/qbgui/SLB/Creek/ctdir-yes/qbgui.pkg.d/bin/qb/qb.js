
var meta = document.createElement('meta');
meta.setAttribute('http-equiv', 'Cache-Control');
meta.setAttribute('content', 'no-cache');
document.getElementsByTagName('head')[0].appendChild(meta);
var meta = document.createElement('meta');
meta.setAttribute('http-equiv', 'Pragma');
meta.setAttribute('content', 'no-cache');
document.getElementsByTagName('head')[0].appendChild(meta);
var meta = document.createElement('meta');
meta.setAttribute('http-equiv', 'Expires');
meta.setAttribute('content', '0');
document.getElementsByTagName('head')[0].appendChild(meta);


function checkIP(ip)
{
    if ( !ip ) { alert("IP is Empty"); return false; }
    if ( !isValidIP(ip) ) { alert("IP format error !!"); return false;}
    return true;
}


function checkSubnet(subnet)
{
    if ( !subnet ) { return false; }
    if ( !isValidSubnet(subnet) ) { return false;}
    return true;
}

function checkSubnet_v6(subnet)
{
    if ( !subnet ) { return false; }
    if ( !isValidSubnet_v6(subnet) ) { return false;}
    return true;
}
function checkPort(port)
{
    if ( !port ) { alert("Port Number is Empty !!"); return false; }
    if ( !isValidPort(port) ) { alert("Port format error !!"); return false; }
    return true;
}

function isValidMail (Email)
{
    if ( !Email ) { return false; }
    var Reason = "";
    var checkStr = Email;
    var ix = (checkStr.length - 4);
    var RC = true;
    var x = AtSignValid = DoublePeriod = PeriodValid = SpaceValid = ExtValid = RL = 0;
    for (i = 0;  i < checkStr.length;  i++)
    {
        if (checkStr.charAt(i) == '\@')
        AtSignValid++;
        else if (checkStr.charAt(i) == '.')
        {
            if (x == (i-1))
            DoublePeriod++;
            else { x = i; PeriodValid++; }
        }
        else if (checkStr.charAt(i) == ' ')
            SpaceValid ++;
    }
    
    if (AtSignValid != 1) RC=false;
    if (PeriodValid == 0) RC=false;
    if (SpaceValid > 0) RC=false;
    if (DoublePeriod > 0) RC=false;
    
    return RC
}

function general_onload()
{
    if(ERROR_report.length>0){alert(ERROR_report);}
    if(LOGIN_result==0){window.top.location.href="index.htm"; return;}
    if(LOGIN_result==2){window.top.location.href="index.htm"; return;}
    cgi_dep_onload();
}

function doSemaphore()
{
    if (submitclicked.value==1)
    {
            alert('Please wait previous submition to be completed ...');
            return false;
    }
    else
    {
            submitclicked.value=1;
            return true;
    }
}

function goSubmit(action_value)
{
    //20061003 Brian modify user's privilege.
    var privilege=getcookie('privilege');
    if(privilege!=1) {alert('You do not have Privilege to do it'); return;}
    var myform=document.forms[0];
    myform.action.value=action_value;
    myform.submit();
    for(i=0;i<myform.elements.length;i++) { myform.elements[i].disabled=true;myform.elements[i].style.color='white'; }
    if ( myform.SAVE ) { myform.SAVE.disabled=false; }
}  


function add_options_by_text(newvalue, to)
{
    var exist=0;
    for ( var i=0;  i < to.options.length; i++) { if ( to.options[i].value==newvalue) { exist=1; } }
    if ( !exist ) { to.options.add(new Option(newvalue, newvalue)); }
}    


function add_options(from, to)
{
    for ( var i=0; i < from.options.length; i++)
    {   
       if ( from.options[i].selected )
        {   
            var exist=0;
            for ( var j=0; j < to.options.length; j++)
            {
                if ( from.options[i].value==to.options[j].value ) { exist=1; }
            }
                
            var count=to.options.length;
            if ( !exist )
            {
                var newvalue=from.options[i].value;
                var newtext=from.options[i].text.slice(3,from.options[i].text.length)
                to.options[count]=new Option(newtext, newvalue);
            }
        }
    }
    
    own_deselect(from);
}


function del_options(target)
{
    var opttxts_after_del=new Array();
    for ( var i=0,j=0; i < target.options.length; i++)
    {
        if ( !target.options[i].selected )
        {
            opttxts_after_del[j++]=target.options[i].text;
        }
    }
    setOptionText(target, eval(opttxts_after_del));
    
    for ( var i=0; i < target.options.length; i++)
    {
        if ( target.options[i].text=="ANY" )
        {
            target.options[i].value="others";
        }
    }
}

function getRadioValue(radioObj)
{
    for(var i=0; i<radioObj.length; i++)
    {
        if ( radioObj[i].checked ) { return radioObj[i].value; }
    }
}

function setAllCheckBoxValue(checkboxname, boolvalue)
{
    var myform=window.document.forms[0];

    for ( var i=0; i < myform.elements.length; i++)
    {
        var ctrlobj=myform.elements[i];

        if (ctrlobj.name==checkboxname) 
        {
            ctrlobj.checked=boolvalue;
        }
    }
}

function mark_select(obj)
{
    var head_text="";
    for(var i=0;i<obj.options.length;i++)
    {
        head_text=obj.options[i].text.slice(0,3); 
        if (head_text=="[X]") { obj.options[i].selected=true; }
        else { obj.options[i].selected=false; }
    } 
}

function own_deselect(obj)
{
    var show_text;
    var head_text;
    for (var i=0; i<obj.options.length; i++)
    {
        head_text=obj.options[i].text.slice(0,3); 
        if (head_text=="[X]")
        {
            head_text="[ ]";
            show_text=obj.options[i].text.slice(3,obj.options[i].text.length);
            obj.options[i].text=head_text+show_text;
            obj.options.selectedIndex=-1;
        }
    }
}

function own_select(obj)
{
    var show_text=obj.options[obj.options.selectedIndex].text.slice(3,obj.options[obj.options.selectedIndex].text.length);
    var head_text=obj.options[obj.options.selectedIndex].text.slice(0,3); 
    
    if (head_text=="[X]") { head_text="[ ]"; }
    else { head_text="[X]"; } 
    obj.options[obj.options.selectedIndex].text=head_text+show_text;
    obj.options.selectedIndex=-1;
}

function flushOption(select)
{
    while(select.options.length) { select.options[0]=null; }
}

function setOptionText(the_select,the_array)
{
    while(the_select.options.length)
    {
        the_select.options[0]=null;
    }

    for (var loop=0;loop<the_array.length;loop++)
    {
        if(loop<the_array.length)
        {
            the_select.options[loop]=new Option(the_array[loop],the_array[loop]);
        }
    }
}

function openWin(targetfile, width, height)
{
    var winformat="";
    if ( !width ) { width=250; }
    if ( !height ) { height=200; }
    winformat=winformat+"width="+width+",";
    winformat=winformat+"height="+height+",";
    winformat=winformat+"left=420,";
    winformat=winformat+"top=280,";
    winformat=winformat+"titlebar=yes,";
    winformat=winformat+"menubar=no,";        
    winformat=winformat+"toolbar=no,";
    winformat=winformat+"location=no,";
    winformat=winformat+"scrollbars=yes,";
    winformat=winformat+"resizable=yes,";
    winformat=winformat+"status=no,";
    return window.open(targetfile, "new_win", winformat);
}

function qbListDNSOpt()
{
    var targetcgi='qblistdnsopt.cgi';
    var strFeatures='dialogWidth=300px;dialogHeight=300px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;'
    return window.showModalDialog(targetcgi, '', strFeatures);
}

function qbListMX(domain,countryname)
{
    var targetcgi='qblistmx.cgi'+'?domain='+domain+'&countryname='+countryname;
    var strFeatures='dialogWidth=200px;dialogHeight=300px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;'
    return window.showModalDialog(targetcgi, '', strFeatures);
}

function qbListNS(domain,countryname)
{
    var targetcgi='qblistns.cgi'+'?domain='+domain+'&countryname='+countryname;
    var strFeatures='dialogWidth=200px;dialogHeight=300px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;'
    return window.showModalDialog(targetcgi, '', strFeatures);
}

function qbDHCP(natid)
{
    var targetcgi='qbdhcp.cgi'+'?natid='+natid;
    var strFeatures='dialogWidth=500px;dialogHeight=500px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;'
    return window.showModalDialog(targetcgi, '', strFeatures);
}

function qbSetDate()
{
    var strFeatures='dialogWidth=400px;dialogHeight=200px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;'
    return window.showModalDialog('qbsetdate.cgi', '', strFeatures);
}

function qbListConfig(action)
{
    var targetcgi='qblistconfig.cgi'+'?action='+action;
    var strFeatures='dialogWidth=200px;dialogHeight=250px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;'
    return window.showModalDialog(targetcgi, '', strFeatures);
}

function qbCreateBatchNatZone(portnum) 
{ 
    var strFeatures='dialogWidth=500px;dialogHeight=450px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;'
    return window.showModalDialog("qbcrtbatnatzone.htm",portnum, strFeatures);
}

function qbBatchAddOne2One(obj)
{
    var strFeatures='dialogWidth=480px;dialogHeight=420px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;'
    return window.showModalDialog("qbone2one.htm",obj, strFeatures);
}

function qbStr2IPListHelp(obj)
{
    var strFeatures='dialogWidth=480px;dialogHeight=320px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;'
    window.showModalDialog("./help/qbstr2iplist.htm",obj, strFeatures);
}

function qbShowHelp(filename)
{
    var lang=getcookie('language');
    var helpfile=( lang == "chinese" ) ? ( '/help/ch_' + filename + '.htm' ) : ('/help/' + filename + '.htm');
    var strFeatures='dialogWidth=800px;dialogHeight=420px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;'
    window.showModalDialog(helpfile,'', strFeatures);
}

function qbPrompt(msg)
{
    var strFeatures='dialogWidth=300px;dialogHeight=150px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;edge=raised';
    return window.showModalDialog("qbprompt.htm", msg, strFeatures);
}

function qbAlert(msg) // nancy...20040526
{
    var strFeatures='dialogWidth=300px;dialogHeight=150px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;edge=raised';
    return window.showModalDialog("qbalert.htm", msg, strFeatures);
}

function qbConfirm(draw, msg)
{
    var msgObj=new Object();
    msgObj.draw=draw;
    msgObj.msg=msg;

    var strFeatures='dialogWidth=300px;dialogHeight=150px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;edge=raised';
    return window.showModalDialog("qbconfirm.htm", msgObj, strFeatures);
}

function qbCreateISP(draw, msg)
{
    var msgObj=new Object();
    msgObj.draw=draw;
    msgObj.msg=msg;

    var strFeatures='dialogWidth=300px;dialogHeight=150px;center=yes;'
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;edge=raised';
    return window.showModalDialog("createisp.htm", msgObj, strFeatures);
}

function qbLogout()
{
    var strFeatures='dialogWidth=200px;dialogHeight=200px;center=yes;';
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;edge=raised';
    window.showModalDialog("qblogout.htm",'', strFeatures);
}

function qbCleanUpModule(whattoclean)
{
    var strFeatures='dialogWidth=200px;dialogHeight=200px;center=yes;';
        strFeatures+='scrollbars=no;border=thin;help=no;status=no;edge=raised';
    return window.showModalDialog(whattoclean,'', strFeatures);
}

function isDecimal(cadena)
{
    var checkOK = "0123456789";
    var allValid = true;
    var allNum = "";
    
    if (!cadena) { return (false); }

    for (i = 0;  i < cadena.length;  i++)
    {
        ch = cadena.charAt(i);
        for (j = 0;  j < checkOK.length;  j++) if (ch == checkOK.charAt(j) || ch=='.' || ch==',') break;
        if (j == checkOK.length) { allValid = false; break; }
        allNum += ch;
    }

    if(allValid == true) return (true);
    if(allValid == false) return (false);
} 

function isDecimal_v6(cadena)
{
    var checkOK = /[a-fA-F0-9]{1,4}/;
    var allValid = true;
    var allNum = "";
    
    if (!cadena) { return (false); }
    if (!checkOK.test(cadena)){return (false);}
    
    if(allValid == true) return (true);
    if(allValid == false) return (false);
}
function isHexadecimal(inum) // nancy...200405
{
    var checkOK = "0123456789abcdefABCDEF";
    var allValid = true;
    var allNum = "";

    if (!inum) { return (false); }

    for (i = 0;  i < inum.length;  i++)
    {
        ch = inum.charAt(i);
        for (j = 0;  j < checkOK.length;  j++) if (ch == checkOK.charAt(j)) break;
        if (j == checkOK.length) { allValid = false; break; }
        allNum += ch;
    }

    if(allValid == true) return (true);
    if(allValid == false) return (false);
}

function isValidPort(port)
{
    var OK=true;

    if ( !port ) { OK=false; }

    var pattern=/^\d+$|^(\d)+\:(\d)+$/g; 
    var result=port.search(pattern); 
    if ( result == -1 )  OK=false; 

    var portparams=port.split(':');
    var front=parseInt(portparams[0]); 
    var end=parseInt(portparams[1]);
    
    if ( portparams.length==1 && ( front <= 0 || front >= 65536 ) )  {  OK=false; }

    if ( portparams.length==2 )
    {
        if ( front >= end )  OK=false; 
        if ( front <= 0 || front >= 65536  ) OK=false;
        if ( end <= 0 || end >= 65536  ) OK=false;
    }

    return OK;    
}

function isValidIP(ip)
{
    var OK=true;
    if ( !ip ) { OK=false; }
    var ipFields=ip.split(".");
    if ( ipFields.length !=4 ) { OK=false; }
    for(var i=0;i<4;i++)
    {
        
        if ( !isDecimal(ipFields[i]) ) { OK=false; break; }
        if ( ipFields[i] < 0 || ipFields[i] > 255 ) { OK=false; break; } 
    }
    return OK;
}

function isValidIP_v6(ip)
{
    var OK=true;
    
    if ( !ip ) { OK=false; }
    var check = /[A-Fa-f0-9]/ ; 
    var check1 = /^\w{1,4}$/ ;
    var ipFields=ip.split(":");
    var i=0;
    var y = 0;
    if ( ipFields.length > 8 ) { OK=false; }
    for(var i=0;i<ipFields.length;i++)
    {
        if (ipFields[i]=="")
        {
	     y++;
            if (y>1) { OK=false; break; }
        }else
        {
            if ( !isDecimal_v6(ipFields[i]) ) { OK=false; break; }
            if (!check1.test( ipFields[i]) || !check.test( ipFields[i])) { OK=false; break; }
        }
    }
    return OK;
}    

function isValidSubnet(subnet)
{
    var OK=true;
    if ( !subnet ) { OK=false; }
    var subnetFields=subnet.split("/");
    if ( subnetFields.length !=2 ) { OK=false; }
    if ( !isDecimal(subnetFields[1]) || subnetFields[1] < 0 || subnetFields[1] > 32 ) { OK=false; }
    if ( !isValidIP(subnetFields[0]) ) { OK=false;}
    return OK;
}

function isValidSubnet_v6(subnet)
{
    var OK=true;
    if ( !subnet ) { OK=false; }
    var subnetFields=subnet.split("/");
    if ( subnetFields.length !=2 ) { OK=false; }
    if ( !isDecimal_v6(subnetFields[1]) || subnetFields[1] < 0 || subnetFields[1] > 128 ) { OK=false; }
    if ( !isValidIP_v6(subnetFields[0]) ) { OK=false;}
    return OK;
}

function isValidMac(mac) // nancy...200405
{
    var OK=true;

    if ( !mac ) { OK=false; }
    var macFields=mac.split(":");
    //if ( macFields.length < 8 ) { OK=false; }

    for(var i=0;i<6;i++) 
    {
        if ( macFields[i].length > 2 || !isHexadecimal(macFields[i]) ) { OK=false; break; }
    }

    return OK;
}

function getcookie(name)
{
    var c=document.cookie.split("; ");
    for (var i=0; i<c.length; i++) 
    { 
        var b=c[i].split("="); 
        if(name==b[0]) { return unescape(b[1]); } 
    }

    return;
}
    
function go_to_console() { window.top.mainFrame.location.href="console.cgi"; }

