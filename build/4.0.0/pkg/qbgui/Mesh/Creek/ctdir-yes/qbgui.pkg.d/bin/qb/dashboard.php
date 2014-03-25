<!DOCTYPE html><html><head><meta charset="UTF-8">
<link rel="stylesheet" href="gui.css" type="text/css"/>
<script type="text/javascript" src="jquery-1.10.2.js"></script>
<script type="text/javascript" src="jquery-ui-1.10.3.custom.js"></script>
<script type="text/javascript" src="qbjs/jquery.dataTables.min.js"></script>
<script type="text/javascript" src="jquery.sparkline.js"></script>
<script type="text/javascript" src="qbjs/sorttable.js"></script>
<link rel="stylesheet" href="/resources/demos/style.css" />
<style>
#sortable { list-style-type: none; margin: 0; padding: 0; width: 75%; }
#sortable li { margin: 10px 10px 10px 0; padding: 0px; float: left; width: 48%; 
               height: 150px; text-align: center;
               border: 0px 0px 0px 0px;
             }
</style></head>
<body bgcolor="#336699" text="#ffffff" link="#000040" >
        <div align="center">
            <span calss="body">Auto Refresh Per</span>
            <select id="re_time">
                <option value=30>30</option>
                <option value=60>60</option>
            </select>
            <span calss="body">seconds&nbsp;&nbsp; Remaining <a id="sec"></a> Sec.
            </span>
            <button id="format" type="button">Save Format</button>
    	    <button type="button" id='clear'>Reset</button>
        </div>
        <div align="center">
	<ul id="sortable">
	
<?php
    $title=array('System Status'=>'','System Usage'=>'','Device Information'=>'','Security Status'=>'dos.cgi',
    		 'User Flow Ranking'=>'userflow.htm','Connections'=>'/status/report.htm','Register Information'=>'regist.cgi','WAN Link'=>'showbasic.cgi',
    		 'LAN'=>'zone.cgi?viewpoint=nat','Bandwidth Management'=>'lantraffic.cgi','Transparent'=>'zone10.cgi');
    $title_ary=array('dashboard_0'=>'System Status','dashboard_1'=>'System Usage','dashboard_2'=>'Device Information','dashboard_3'=>'Security Status',
    		 'dashboard_4'=>'User Flow Ranking','dashboard_5'=>'Connections','dashboard_6'=>'Register Information','dashboard_7'=>'WAN Link',
    		 'dashboard_8'=>'LAN','dashboard_9'=>'Bandwidth Management','dashboard_10'=>'Transparent');
    $index=0;
    foreach ($title as $key => $value) 
    {
        echo '<li class=\'ui-state-default\' ><div>';
        echo '<table bgcolor=\'#332211\' width=\'100%\' border=\'0\'>';
        echo '<tr id="tmp_d'.$index.'" onclick="" ><td id=\'tmp_t'.$index.'\' width=\'100%\' class=\'body\'>';
        if ( $value != '')
        {
            echo '<a id=\'tmp_a'.$index.'\' href=\'\' style=\'text-decoration:none\' >';
            echo '<img src=\'image/link.gif\' width=\'12\' height=\'12\' border=\'0\' /></a>';
        }
        echo '</td>';
	echo '<tr><td width=\'100%\' class=\'body\' ><div id=\'tmp'.$index.'\'></div></td></tr>';
        echo '</table></div>';
        echo '</li>';
        $index++;
    }
?>

	</ul>
    </div>
</body>                    
<script>
    /*var option= new Array('System Status','System Usage','Device Information','Security Status',
    		 'User Flow Ranking','Connections','Register Information','WAN Link',
    		 'LAN','Bandwidth Management','Transparent');
    */
var title={'System Status':'','System Usage':'','Device Information':'','Security Status':'dos.cgi',
    		 'User Flow Ranking':'userflow.htm','Connections':'/status/report.htm','Register Information':'regist.cgi','WAN Link':'showbasic.cgi',
    		 'LAN':'zone.cgi?viewpoint=nat','Bandwidth Management':'lantraffic.cgi','Transparent':'zone10.cgi'};
var title_ary={'dashboard_0':'System Status','dashboard_1':'System Usage','dashboard_2':'Device Information','dashboard_3':'Security Status',
    		 'dashboard_4':'User Flow Ranking','dashboard_5':'Connections','dashboard_6':'Register Information','dashboard_7':'WAN Link',
    		 'dashboard_8':'LAN','dashboard_9':'Bandwidth Management','dashboard_10':'Transparent'};
$(document).ready(function() {
    clear_pl();
    
    var format_a =new format();
    format_a.change(format_a.getsave());
    $( "#sortable" ).sortable();
    $( "#sortable" ).disableSelection();
    show_table('dashboard_',11);
});

function clear_pl()
{
    $.ajax({
        url:'dashboard.sh',
        cache:false,
        dataType: 'html',
        type:'GET',
        data: {},
        error: function(xhr){
        },
        success: function(response) {
        }
    });
}

$(window).bind('beforeunload', function (e) {
    clear_pl();                                                                    
});

$("#re_time").change(function()
{
    $("#sec").text($(this).val());
});
$("#format").click(function()
{
    var format_box= new format();
    format_box.length=$("li").find("div").length;
    format_box.getary(0);
    format_box.save(format_box.ary);

});
$("#clear").click(function(){
    var format_box= new format();
    format_box.clear();
});
function format()
{
    this.length='';
    this.ary=new Array();
    this.clear=(function (){
        localStorage.clear();
    });
    this.getary=(function(o){
        if($("li").find("div").eq(o).attr("id"))
        {
            if ($("li").find("div").eq(o).attr("id").match("dashboard"))
                this.ary.push($("li").find("div").eq(o).attr("id"));
        }
        if ( o <= this.length)
        {
            o++;
            this.getary(o);
        }
    });
    this.save=(function(o){
        localStorage.lastname=o;
        alert("Save OK");
        //document.write(localStorage.lastname);
    });
    
    this.getsave=(function(){
        return localStorage.lastname;
    });
    
    this.change=(function(o){
        var name=new Array();
        if (o)
        {
            name = o.split(/,/);
            var num=name.length;
        }
        else
            var num=11;
        for (var i=0;i<num;i++)
        {
            if (name[i])
            {
                if (name[i].match("dashboard"))
                {
                    $("#tmp"+i).attr("id",name[i]);
                    $("#tmp_t"+i).prepend("<span>"+ title_ary[name[i]] +"</span>");
                    $("#tmp_d"+i).attr("onclick","table_hidden('"+name[i]+"')");
                    if ($("#tmp_a"+i))
                    	$("#tmp_a"+i).attr("href",title[title_ary[name[i]]]);
                 }
            }else
            {
                $("#tmp"+i).attr("id","dashboard_"+i);
                $("#tmp_t"+i).prepend("<span>"+ title_ary["dashboard_"+i] +"</span>");
                $("#tmp_d"+i).attr("onclick","table_hidden('dashboard_"+i+"')");
                if ($("#tmp_a"+i))
                    $("#tmp_a"+i).attr("href",title[title_ary["dashboard_"+i]]);
            }
        }    
    });
    
    this.show=(function(o){alert(o)});

}

function refresh()
{
    var t = $("#sec").text();
    t--;
    if (t > 0)
    {
        $("#sec").text(t);
        setTimeout("refresh();",1000);
    }else if (t==0)
        show_table('dashboard_',11,'a');
} 

function show_table(oo,index,check)
{
    if (index > 0)
    {
        index--;
        if (check != 'a' || index == 0 || index == 1 || index == 4 || index == 5 || index == 9)
            Ajax(oo+index);
        show_table(oo,index,check);
    }else
    {
        $("#re_time").change();
        refresh();
    }
}

function Ajax(id)
{
    $.ajax({
        url:'dashboard.pl',
        cache:false,
        dataType: 'html',
        type:'GET',
        data: {id:id},
        error: function(xhr){ 
        },
        success: function(response) {
            $("#"+id).html(response);
            
            if ( id == 'dashboard_9')
            {
                var oTable =  $('#tables').dataTable({
                    "bPaginate": false,
                    "bInfo": false,
                    "aoColumns": [
                    	{ "sType": 'html' },
                    	{ "sType": 'string-case' },
                    	{ "sType": 'string-case' },
                    ]
            	});
	   	$("th").eq(1).click();
	    	$("th").eq(1).click();
	        $("#tables_filter").attr("style","display:none");
	        for (var x=0; x < $("#tables").children("tbody").children("tr").length; x++)
	            if (x > 2)
	                $("#tables").children("tbody").children("tr").eq(x).attr("style","display:none");
	    }else if (id == 'dashboard_1')
	    {
    		var status = new Array('cpu','mem','session');
       		for(var i=0;i<status.length;i++)
       		{
	            get_picture(status[i]);
	            $("#"+status[i]).parent("td").prev("td").attr("style","width:30%;align:left;");
	        }
	    }else if (id == 'dashboard_6')
	    {
	        for (var x = 1; x < $("#dashboard_6").find("tr").length;x++)
	    	    $("#dashboard_6").find("tr").eq(x).children("td").attr("style","width:50%");
	    }
        }
    });
}

jQuery.fn.dataTableExt.oSort['string-case-asc']  = function(x,y) {
    x = x.replace(" Kbps","");
    y = y.replace(" Kbps","");
    var ssv3 = x-y;
    return ssv3;
};

jQuery.fn.dataTableExt.oSort['string-case-desc'] = function(x,y) {
    x = x.replace(" Kbps","");
    y = y.replace(" Kbps","");var ssv3 = y-x;
    return ssv3;
};

function table_hidden(oo)
{
    
    if ($("#"+oo).attr("style") == "display:none;" || $("#"+oo).attr("style") == "display: none;")
        $("#"+oo).attr("style","display:block");
    else
        $("#"+oo).attr("style","display:none");
}

function get_picture(status)
{
	$.ajax({
	    url:'system_usage.pl',
    	    cache:false,
    	    dataType: 'html',
    	    type:'GET',
    	    data: {id:status},
    	    error: function(xhr){
    	    },
    	    success: function(response) {
		var dd = new Array();
		var yy = new Array();
    	        var data=[];
    	        yy=response.split(/--/);
    	        dd=yy[1].split(/ %/);
    	        for(var x=0;x<dd.length;x++)
    	            data.push(dd[x]);
        	creat_picture(data,status);
    	    }
        });
}

function creat_picture(data,name)
{
    $("#"+name).sparkline(data, {
        type: 'line',width: '100%'});
}

</script>
</html>                   
