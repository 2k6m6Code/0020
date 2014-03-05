function title(sa)
{
    if (sa == "local_unit")
    {
	$("#ip_name").text(" Local ");
	$("td[class='bigtitle']").html("Local Traffic");
	$("#ip_option option").remove();
	$("#ip_option").append($("<option></option>").attr("value","-A srcip ").text("Src IP"));
	$("#ip_option").append($("<option></option>").attr("value","-A dstip ").text("Dst IP"));
	$("#ip_option").append($("<option></option>").attr("value","-A srcip4/24 ").text("Src Subnet"));
	$("#ip_option").append($("<option></option>").attr("value","-A dstip4/24 ").text("Dsr Subnet"));
    }
    else if (sa == "top_N")
    {
	$("#ip_name").text(" Top N of all Units ");
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("TopN Per Unit");
	$("#ip_option").append($("<option></option>").attr("value","").text("Units"));
    }
    else if (sa == "syn_flood")
    {
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("SYN Flood");
    }
    else if (sa == "port_scan")
    {
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("Port Scan");
    }
    else if (sa == "t_connect")
    {
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("TCP Connection Limit");
    }
    else if (sa == "u_connect")
    {
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("UDP Connection Limit");
    }
    else if (sa == "port")
    {
	$("#ip_option option").remove();
//	$("td[class='bigtitle']").html("Traffic Summary");
	$("td[class='bigtitle']").html("Service");
    }
    else if (sa == "in_dst")
    {
	$("#ip_name").text(" Inbound ");
	$("td[class='bigtitle']").html("Inbound Dst");
	$("#ip_option option").remove();
	$("#ip_option").append($("<option></option>").attr("value","-A proto,srcip").text("Dst IP"));
	$("#ip_option").append($("<option></option>").attr("value","-A proto,srcip4/24").text("Dst Subnet"));
    }
    else if (sa == "in_unit")
    {
	$("#ip_name").text(" Inbound ");
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("Inbound Unit");
	$("#ip_option").append($("<option></option>").attr("value","-A dstip").text("Inside Unit"));
	$("#ip_option").append($("<option></option>").attr("value","-A dstip").text("Outside Unit"));
    }
    else if (sa == "out_unit")
    {
	$("#ip_name").text(" Outbound ");
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("Outbound Unit");
	$("#ip_option").append($("<option></option>").attr("value","-A srcip").text("Inside Unit"));
	$("#ip_option").append($("<option></option>").attr("value","-A srcip").text("Outside Unit"));
    }
    else if (sa == "in_src")
    {
	$("#ip_name").html(" Inbound ");
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("Inbound Src");
	$("#ip_option").append($("<option></option>").attr("value","-A proto,dstip").text("Src IP"));
	$("#ip_option").append($("<option></option>").attr("value","-A proto,dstip4/24").text("Src Subnet"));
    }
    else if (sa == "out_dst")
    {
	$("#ip_name").text(" Outbound ");
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("Outbound Dst");
	$("#ip_option").append($("<option></option>").attr("value","-A proto,srcip").text("Dst IP"));
	$("#ip_option").append($("<option></option>").attr("value","-A proto,srcip4/24").text("Dst Subnet"));
    }
    else if (sa == "out_src")
    {
	$("#ip_name").html(" Outbound ");
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("Outbound Src");
	$("#ip_option").append($("<option></option>").attr("value","-A proto,dstip").text("Src IP"));
	$("#ip_option").append($("<option></option>").attr("value","-A proto,dstip4/24").text("Src Subnet"));
    }
    else if (sa == "bd_tr")
    {
        $("#ip_name").html(" BiDirection  ");
	$("#ip_option option").remove();
	$("td[class='bigtitle']").html("BiDirection Traffic");
	$("#ip_option").append($("<option></option>").attr("value","-B").text("IP"));
    }else if (sa == "query_host")
    {
        $("td[class='bigtitle']").html("Host Query");
        $("a[name='noquery']").attr("style","display:none");
   	$("select[name='noquery']").attr("style","display:none"); 
	$("#ip_option option").remove();
	$("#ip_option").append($("<option></option>").attr("value","-A proto,dstip").text("Group by outbound destination port"));
	$("#ip_option").append($("<option></option>").attr("value","-A proto,srcip").text("Group by inbound destination port"));
	$("#report_type option").val('6');
    }
}

function list_action (oo)
{
    if (oo.checked)
    {
        $("#proto").attr("disabled",true);
        $("#proto").attr("checked",false);
        $("#srcport").attr("disabled",true);
        $("#srcport").attr("checked",false);
        $("#src").attr("disabled",true);
        $("#src").attr("checked",false);
        $("#srcoption").attr("disabled",true);
        $("#srcoption").attr("checked",false);
        $("#dstport").attr("disabled",true);
        $("#dstport").attr("checked",false);
        $("#dst").attr("disabled",true);
        $("#dst").attr("checked",false);
        $("#dstoption").attr("disabled",true);
        $("#dstoption").attr("checked",false);
    }else
    {
        $("#proto").attr("disabled",false);
        $("#srcport").attr("disabled",false);
        $("#src").attr("disabled",false);
        $("#srcoption").attr("disabled",false);
        $("#dstport").attr("disabled",false);
        $("#dst").attr("disabled",false);
        $("#dstoption").attr("disabled",false);
    }
}

function port(oo)
{
   var id = $(oo).attr("id");
   if (oo.checked)
       $("#"+id+'sel').attr("disabled",false);
   else
       $("#"+id+'sel').attr("disabled",true);
}

function sele(oo)
{
    var id = $(oo).attr("id");
    if (oo.selectedIndex != 0)
        $("#"+id+'option').attr("disabled",false);
    else
        $("#"+id+'option').attr("disabled",true);
        
}


function today ()
{
    this.setYear = 1970;
    this.setMonth = 01;
    this.setDay = 01;
}

today.prototype.getYear = function getYear(){
    return this.setYear;
}

today.prototype.getMonth = function getMonth(){
    return this.setMonth;
}

today.prototype.getDay = function getDay(){
    return this.setDay;
}    
 
