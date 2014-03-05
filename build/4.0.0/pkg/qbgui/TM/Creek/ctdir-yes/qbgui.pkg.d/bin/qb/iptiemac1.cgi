#!/usr/bin/perl
use CGI;

print "Content-type:text/html\n\n";
print qq(<html><head>);
print qq(<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" media="screen"/>);
print qq(<link rel="stylesheet" href="ui.jqgrid.css" media="screen" />);
print qq(<link rel="stylesheet" href="ui.multiselect.css" media="screen" />);	
print qq(<script src="http://code.jquery.com/jquery-1.9.1.js"></script>);
print qq(<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>);
print qq(<script src="grid.locale-en.js"></script>);
print qq(<script type="text/javascript">);
print qq(jQuery.jgrid.no_legacy_api = true;);
print qq(jQuery.jgrid.useJSON = true;);
print qq(</script>);
print qq(<script src="jquery.jqGrid.min.js" type="text/javascript"></script>);
print qq(<script src="jquery.tablednd.js" type="text/javascript"></script>);
print qq(<script src="jquery.contextmenu.js" type="text/javascript"></script>);
print qq(<script src="ui.multiselect.js" type="text/javascript"></script>);
print qq(<link rel="stylesheet" href="/resources/demos/style.css" />);
print qq(<style>);

print qq(</style></head>);
print qq(<body bgcolor="#336699" text="#ffffff" link="#000040" vlink="#400040">);
print qq(<table id="gridid"></table>);
print qq(<div id="gridid1"></div>);
print qq(<table id="grid1_id"></table>);
print qq(<div id="page"></div>);
print qq(<input type="button" id="new" value="ADD"/>);
print qq(<input type="button" id="del" value="DEL"/>);
print qq(<input type="button" id="info" value="INFO"/>);
print qq(</body></html>);

print << "QB";

<script language="javascript">

jQuery(document).ready(function() 
{
    jQuery("#gridid").jqGrid({
       url:'datasend.cgi',
       datatype: "json",
       colNames:['IP/Subnet','Mac','Status','Note'],
       colModel:[
           {name:'ip',index:'ip', width:60},
           {name:'mac',index:'mac', width:60},
           {name:'status',index:'status', width:100},
           {name:'note',index:'note', width:100}
       ],
       rowNum:10,
       heigh: "auto",
       autowidth: true,
       pager: '#gridid1',
       multiselect: true,
       sortorder: "desc",
       viewrecords: true,
       editurl:"bridge.cgi",
       caption: "Manipulating Array Data"
    });
    
jQuery("#gridid").jqGrid('navGrid',"#gridid1",{edit:false,add:false,del:false});


    var mydata = [
        {ip:"192.168.1.123",mac:"00:60:98:54:23:11",status:"ACCEPT"},
    	{ip:"192.168.1.124",mac:"00:60:98:54:23:11",status:"DROP"},
    	{ip:"192.168.1.125",mac:"00:60:98:54:23:11",status:"ACCEPT"},
    	{ip:"192.168.1.126",mac:"00:60:98:54:23:11",status:"DROP"},
    	{ip:"192.168.1.0/24",note:"+"}
    	];
    
    for(var i=0;i < mydata.length;i++) 
	jQuery("#gridid").jqGrid('addRowData',i+1,mydata[i]);

});

jQuery("#info").click(function(){
    var s;
    var id = jQuery("#gridid").jqGrid('getGridParam','selarrrow');
    if (id)	
    {
        var ret = jQuery("#gridid").jqGrid('getRowData',id);
        alert("ip="+ret.ip + " mac="+ret.mac+" status="+ret.status);
    }else{alert("Please select row");}
});


jQuery("#del").click(function(){
    var id = jQuery("#gridid").jqGrid('getGridParam','selrow');
    if (id)
    {
        var ret = jQuery("#gridid").jqGrid('delRowData',id);
        alert("Delete");
    }else{alert("Please select row");}
}); 

jQuery("#new").click(function(){
    jQuery("#gridid").jqGrid('editGridRow',"new",{height:280,reloadAfterSubmit:false});
});

</script>

QB

