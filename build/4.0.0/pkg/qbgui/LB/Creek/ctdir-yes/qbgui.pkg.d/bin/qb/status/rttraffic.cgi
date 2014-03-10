#!/usr/bin/perl  
use CGI;
require ("/usr/local/apache/qb/qbmod.cgi");

authenticate(action=>'RANDOMCHECK');

my $form = new CGI;

#---------------------------------------------------------------------------
#	variable convey to rate.cgi
#	$page_now => rate.cgi?page=$page_now (current page)
#	$acton => rate.cgi?action=$action ( action  is reset , sort or null )
#	$ispnum => rate.cgi?show=$ispnum ( per page show records )
#	$spool => rate.cgi?pool=$spool ( show pool) 
#---------------------------------------------------------------------------
my $page_now=$form->param('page_now');
my $action=$form->param('action');
my $page_pre=$page_now - 1;
my $page_next=$page_now + 1;
my $ispnum=$form->param('ispnum');
my $spool=$form->param('spool');

#per page show 10 ~ 100 records 
if ( $ispnum=~m/\D/ || $ispnum < 10 ) { $ispnum="10"; }
if ( $ispnum > 100 ) { $ispnum="100"; }



print "Content-type:text/html\n\n";
#page css
print qq(<html><head><link rel="stylesheet" href="../gui.css" type="text/css">);
print qq(<link rel="stylesheet" href="../jquery-ui-1.10.3.custom.css" />);
print qq(<script type="text/javascript" src="../jquery-1.10.2.js"></script>);
print qq(<script src="../highcharts.min.js"></script>);
print qq(<script src="../highcharts-more.js"></script>);
print qq(<script src="../exporting.js"></script>);
print qq(<style>);
print qq(.page {font-size:10px;color:#ffffff;text-decoration:none;word-spacing:2px;});
print qq(</style></head>);

print qq(<body style="margin:0;text-align:center" bgcolor="#336699">);
print qq(<DIV>);
print qq(<form name="rttform" method="post" action="rttraffic.cgi">);







print qq(<DIV>);
print qq(<div class="qbCopy" align="center" style="width:100%;"><table style="border:1px #FFFFFF solid;padding:5px;" ><tr>);
print qq(<th><div id="total_down" style="width: 340px; height: 300px;" ></div></th>);
print qq(<th><div id="total_up"   style="width: 340px; height: 300px;" ></div></th></tr>);
print qq(</table></div>);
print qq(<div align="center"><table><tr><td>);
print qq(<span style="width:100;color:white;font:12 Verdana;border:2px ridge white;filter:progid:DXImageTransform.Microsoft.Gradient(gradientType=0,startColorStr=white,endColorStr=green);background-image: -ms-linear-gradient(top, #FFFFFF 0%, #008000 100%);background: -moz-linear-gradient(center top , white, green) repeat scroll 0 0 transparent;background: -webkit-gradient(linear, left top, left bottom, from(white), to(green));"><b>INBOUND</b></span>);
print qq(<span style="width:100;color:white;font:12 Verdana;border:2px ridge white;filter:progid:DXImageTransform.Microsoft.Gradient(gradientType=0,startColorStr=white,endColorStr=purple);background-image: -ms-linear-gradient(top, white 0%, purple 100%);background: -moz-linear-gradient(center top , white, purple) repeat scroll 0 0 transparent;background: -webkit-gradient(linear, left top, left bottom, from(white), to(purple));"><b>OUTBOUND</b></span>);
print qq (</td></tr></table></div>);
print qq(<div id="graphspace" style="display: inline-block;">);
print qq (</div>);
print qq(<script></script>);
print qq(<DIV class="qbCopy">);
print qq(Auto Refresh Per&#32&#32);
print qq(<select class="qbopt" id="refreshtime">);
my @time=("9", "7", "5", "3");
foreach my $tm ( @time )
{
    print qq(<option value="$tm">$tm</option>);
}
print qq(</DIV>);
##JS
print << "QB_TRAFFIC";

<script language="javascript">

var myform;





//GraphCard
//GraphCard.set()
//GraphCard.show()
//GraphCard.del()


function graphcard(GraphMasterObj){

        this.tx = null;
        this.rx = null;
        this.RX = null;
        this.TX = null;
        this.DL = null;
        this.UL = null;
        this.name = null;
        this.alive = null;
        this.parent = GraphMasterObj;
        this.obj = document.createElement("FIELDSET");
        this.obj2 = document.createElement("TABLE");
        this.obj3 = document.createElement("LEGEND");
        this.nameobj = document.createElement("SPAN");
        this.nameobj.style.fontWeight = "bold";
        this.portobj = document.createElement("SPAN");
        this.gwayobj = document.createElement("SPAN");
        this.line0 = document.createElement("SPAN");
        this.line1 = document.createElement("SPAN");
        this.line2 = document.createElement("SPAN");
        this.line3 = document.createElement("SPAN");
        this.alink = document.createElement("a");
        this.latency = document.createElement("SPAN");
        this.pktloss = document.createElement("SPAN");
        
        //this.alink.setAttribute("style", "text-decoration:none");

        for(var i=0;i<4;i++){
                eval('this.line'+i).innerHTML = "&nbsp;";
                eval('this.line'+i).style.width = "0";
                eval('this.line'+i).style.fontSize = "8";
                eval('this.line'+i).style.height = "8";
                eval('this.line'+i).style.backgroundColor = (i&1?"pink":"lightgreen");
		if(navigator.userAgent.search("MSIE")> -1){
			if(navigator.userAgent.search("MSIE 10.0")> -1){
			var sttyle ="-ms-linear-gradient(top, white, "+(i>1?"purple":"green")+")";
				eval('this.line'+i).style.background=sttyle;
				eval('this.line'+i).style.display="block";
			}else{
			eval('this.line'+i).style.filter="progid:DXImageTransform.Microsoft.Gradient(gradientType=0,startColorStr=white,endColorStr="+(i>1?"purple":"green")+")";
			
			}
		}else{
			if(navigator.userAgent.search("Firefox")> -1){
			var sttyle ="-moz-linear-gradient(center top , white,"+ (i>1?"purple":"green")+") repeat scroll 0 0 transparent";
			eval('this.line'+i).style.background=sttyle;
			eval('this.line'+i).style.display="block";
			}else{
				var sttyle ="-webkit-gradient(linear, left top, left bottom, from(white), to("+(i>1?"purple":"green")+"))";
				eval('this.line'+i).style.background=sttyle;
				eval('this.line'+i).style.display="block";
			}
			}
        }

	this.obj3.style.color = "white";
        this.obj3.style.font = "12 Verdana";
	this.obj3.style.backgroundColor ="#336699";
        this.obj3.appendChild(this.nameobj);
        this.obj3.appendChild(document.createTextNode(" Interface: [ "));
        this.obj3.appendChild(this.portobj);
        this.obj3.appendChild(document.createTextNode(" ] GateWay: [ "));
        this.obj3.appendChild(this.gwayobj);
        this.obj3.appendChild(document.createTextNode(" ]"));
        this.obj3.appendChild(this.alink);
        this.obj3.appendChild(document.createTextNode(" Latency : [ "));
        this.obj3.appendChild(this.latency);
        this.obj3.appendChild(document.createTextNode(" ]"));
        this.obj3.appendChild(document.createTextNode(" Loss : [ "));
        this.obj3.appendChild(this.pktloss);
        this.obj3.appendChild(document.createTextNode(" ]"));
        this.obj.appendChild(this.obj3);


        this.obj2.cellSpacing = "1";
        this.obj2.cellPadding = "0";
        this.obj2.style.font = "9 Verdana";
        this.obj2.style.color = "white";

        with(this.obj2.insertRow(-1)){
                insertCell(-1);
                insertCell(-1).appendChild(this.line0);
                insertCell(-1);
                insertCell(-1).appendChild(this.line1);
        }
        with(this.obj2.insertRow(-1)){
                insertCell(-1);
                insertCell(-1).appendChild(this.line2);
                insertCell(-1);
                insertCell(-1).appendChild(this.line3);
        }

        for(i=0;i<2;i++){
                for(j=0;j<2;j++){
                        this.obj2.rows[i].cells[j<<1].width = "90";
                        this.obj2.rows[i].cells[j<<1].align = "right";
                        this.obj2.rows[i].cells[j<<1].style.paddingRight = "2";
                        this.obj2.rows[i].cells[(j<<1)+1].width = "120";
                        this.obj2.rows[i].cells[(j<<1)+1].style.background = "black";
                        this.obj2.rows[i].cells[(j<<1)+1].style.border = "2px ridge white";
                }
        }
        this.obj.appendChild(this.obj2);
}



graphcard.prototype.show=function show(){
       if(this.rx > this.DL * 1.1){
                this.rx = this.DL;
        }
       if(this.tx > this.UL * 1.1){
                this.tx = this.UL;
        }
        this.obj2.rows[0].setAttribute("onclick","window.open('speed_page.php?name="+this.name+"')");
        this.obj2.rows[0].cells[0].innerHTML = this.rx + "(Kb/s)";
        this.line0.style.width = this.DL? this.rx / this.DL * 100 + "%" :0;
        this.line0.innerHTML = this.DL? "&nbsp;":"";
        if(this.RX < 1048576){
        this.obj2.rows[0].cells[2].innerHTML = this.RX + "(KB)";
        }else{
        this.obj2.rows[0].cells[2].innerHTML = parseInt(this.RX/1024,10) + "(MB)";
        }
        this.line1.style.width = this.parent.RX_total ? this.RX / this.parent.RX_total * 100 + "%" : 0;
        this.line1.innerHTML = this.parent.RX_total ? "&nbsp;":"";

        this.obj2.rows[1].setAttribute("onclick","window.open('speed_page.php?name="+this.name+"')");
        this.obj2.rows[1].cells[0].innerHTML = this.tx + "(Kb/s)";
        this.line2.style.width = this.UL ? this.tx / this.UL * 100 + "%":0;
        this.line2.innerHTML = this.UL ? "&nbsp;":"";
	if(this.TX<1048576){
        this.obj2.rows[1].cells[2].innerHTML = this.TX + "(KB)";
	}else{
	this.obj2.rows[1].cells[2].innerHTML = parseInt(this.TX /1024,10)+ "(MB)";
	}
        this.line3.style.width = this.parent.TX_total ? this.TX / this.parent.TX_total * 100 + "%":0;
        this.line3.innerHTML = this.parent.TX_total ? "&nbsp;":"";

        
		if(navigator.userAgent.search("MSIE")> -1){
			if(navigator.userAgent.search("MSIE 10.0")> -1){
			var sttyle ="-ms-linear-gradient(top, yellow, red)";
			this.obj.style.background = this.alive?"":sttyle;
			this.obj.style.display = this.alive?"":"block";
			}else{
			this.obj.style.filter = this.alive?"":"progid:DXImageTransform.Microsoft.Gradient(gradientType=1,startColorStr=yellow,endColorStr=red)";
			
			
			}
		}else{
			if(navigator.userAgent.search("Firefox")> -1){
			var sttyle ="-moz-linear-gradient(center top , yellow,red) repeat scroll 0 0 transparent";
			this.obj.style.background = this.alive?"":sttyle;
			this.obj.style.display = this.alive?"":"block";
			}else{
				var sttyle ="-webkit-gradient(linear, left top, left bottom, from(yellow), to(red))";
				this.obj.style.background = this.alive?"":sttyle;
				this.obj.style.display = this.alive?"":"block";
			}
			}
        this.obj2.style.color = this.alive?"white":"black";
        this.obj3.style.color = this.alive?"white":"black";
}


graphcard.prototype.set=function set(name,port,gway,tx,rx,TX,RX,DL,UL,alive,remote,latency,pktloss){
	this.name = name;
        this.nameobj.innerHTML = name;
        this.portobj.innerHTML = port;
        this.gwayobj.innerHTML = gway;
        if ( alive == 1 && latency == 0)
        {
            latency = 1;
        }
        //else if ( alive == 0 )
        //{
        //    latency = 0;
        //}
        if ( latency > 300 ) 
        {
            this.latency.style.color = "red";
        }
        else
        {
            this.latency.style.color = "yellow";
        }
        if ( pktloss > 25 ) 
        {
            this.pktloss.style.color = "red";
        }
        else
        {
            this.pktloss.style.color = "yellow";
        }
        this.latency.innerHTML = latency + 'ms';
        this.pktloss.innerHTML = pktloss + '%';
        if (port.match("mpv") || port.match("tmv")) {
            var gotofunction = "javascript:openclient('" + remote + "')";
            this.alink.setAttribute("href", gotofunction);
            //this.alink.setAttribute('style', 'text-decoration:none; font-weight:bold');
            this.alink.innerHTML = " Remote: [ " + remote + " ]";
        } 

        this.tx = parseInt(tx);
        this.rx = parseInt(rx);
        this.TX = parseInt(TX);
        this.RX = parseInt(RX);
        this.DL = parseInt(DL);
        this.UL = parseInt(UL);

        this.alive = parseInt(alive);
}

function resetVolumn(){
        //var ispnum=document.getElementById('ispnum').value;
        graphIF.location.href='rate.cgi?action=reset&page=1&show=10';
}


function ShowByPool() {
        var bypool=document.getElementById('pool').value;
        
 	myform=window.document.forms[0];
	if (bypool == 'ID') {
    		myform.page_now.value = '1';
        	myform.action.value = '';
	}
	else if (bypool == 'Name') {
    
    		myform.page_now.value = '1';
        	myform.action.value = 'sort';
	}
	else {
    		myform.page_now.value = '';
        	myform.action.value = '';
	}
        myform.spool.value = bypool;
        myform.submit();
}

function ChangeISPnum() {
        myform=window.document.forms[0];
        var ispnum=document.getElementById('ispnum').value;
    	var action=document.getElementById('action').value;
    	
        myform.action.value = action;
    	myform.page_now.value = '1';
        myform.ispnum.value = ispnum;
        myform.submit();
}

//for pre next first last page 
function gotopage(num) {
        myform=window.document.forms[0];
        var action=document.getElementById('action').value;
        var ispnum=document.getElementById('ispnum').value;
        
        myform.action.value = action;
    	myform.page_now.value = num;
        myform.ispnum.value = ispnum;
        myform.submit();
}

//check button next and pre ( disable or enable )
function checkpage() {
        var total=document.getElementById('total').value;
	var page=document.getElementById('page_now').value;
	var PRE=document.getElementById('PRE');
	var NEXT=document.getElementById('NEXT');
	var FIRST=document.getElementById('FIRST');
	var LAST=document.getElementById('LAST');
	var pool=document.getElementById('spool').value;
	
	
	//document.getElementById(pool).selected = true;
 	
	if (!page)
		return;
	
	if (page == '1') {
		PRE.disabled = true;
		FIRST.disabled = true;
	}
		
	if (page == total) {
		LAST.disabled = true;
		NEXT.disabled = true;
	}
}

function openclient(ip) {
	var url='http://' + ip + ':4000';
        window.open(url);
}
                      

window.onload=checkpage;


</script>
<script language="javascript">
function graphmaster(element_id){

        var PA = document.all[element_id];
        if(!PA){
                return null;
        }
        while(PA.childNodes.length){
                PA.firstChild.removeNode(1);
        }

        this.cards = new Array();
        this.count = 0;
        this.obj = document.createElement("TABLE");
	this.obj.id = 'tbId';
        this.rx_total = 0;
        this.tx_total = 0;
        this.RX_total = 0;
        this.TX_total = 0;
        this.DL_total = 0;
        this.UL_total = 0;

        PA.appendChild(this.obj);
}
graphmaster.prototype.clear=function clear(){
	 this.count = 0;
	 
}

var tx0=0,rx0=0,TX0=0,RX0=0,DL0=0,UL0=0,agcount0=0,DL_t=0;UL_t=0;
graphmaster.prototype.add =function add(name,port,gway,tx,rx,TX,RX,DL,UL,alive,remote,latency,pktloss){

        if(this.count < this.cards.length){
                var GCARD = this.cards[this.count];
        }
        else{
                var GCARD = new graphcard(this);
                this.cards.push(GCARD);
                this.obj.insertRow(-1).insertCell(-1).appendChild(GCARD.obj);
        }
        GCARD.set(name,port,gway,tx,rx,TX,RX,DL,UL,alive,remote, latency,pktloss);
        this.count++;
		//Aggregated Speed value
		
		agcount0++;
		var poorid2 = document.getElementById('spool').value;
		if(poorid2 =="" || poorid2 =="ID"){
			if(port.search("mpv")<0 && port.search("tmv")<0){
			if(parseInt(rx) > DL * 1.1){
			rx = DL;
			}
			if(parseInt(tx) > UL * 1.1){
					tx = UL;
			}
			rx0+=parseInt(rx);
			tx0+=parseInt(tx);
			RX0+=parseInt(RX);
			TX0+=parseInt(TX);
			DL0+=parseInt(DL);
			UL0+=parseInt(UL);
			}
		}else{
		if(parseInt(rx) > DL * 1.1){
			rx = DL;
			}
			if(parseInt(tx) > UL * 1.1){
					tx = UL;
			}
		rx0+=parseInt(rx);
        tx0+=parseInt(tx);
        RX0+=parseInt(RX);
        TX0+=parseInt(TX);
        DL0+=parseInt(DL);
        UL0+=parseInt(UL);
		
		}
		
		
}

graphmaster.prototype.show= function show(){

        this.rx_total = 0;
        this.tx_total = 0;
        this.RX_total = 0;
        this.TX_total = 0;
        this.DL_total = 0;
        this.UL_total = 0;

        for(var i=0;i<this.count;i++){
                this.rx_total += this.cards[i].rx;
                this.tx_total += this.cards[i].tx;
                this.RX_total += this.cards[i].RX;
                this.TX_total += this.cards[i].TX;
                this.DL_total += this.cards[i].DL;
                this.UL_total += this.cards[i].UL;
        }
		
        for(i=0;i<this.count;i++){
                this.cards[i].show();
        }

        //balance
        while(this.count < this.cards.length){
                this.cards.pop();
                this.obj.rows[this.count].removeNode(1);
        }
		//show Aggregated Speed 
		toallvalue();
		//if(agcount0>1){
		//toallvalue();
		
		//}
		tx0=rx0=TX0=RX0=DL0=UL0=agcount0=0;
}

var myVar;
function refresh(){

	//var page=document.getElementById('page_now').value;
	//var action=document.getElementById('action').value;
        //var ispnum=document.getElementById('ispnum').value;
        var pool=document.getElementById('spool').value;
    	var refreshtime=document.getElementById('refreshtime');

        if ( pool == 'ID' ) {
		var page=document.getElementById('page_now').value;
        	var ispnum=document.getElementById('ispnum').value;
         	graphIF.location.href='rate.cgi?page=' + page + '&show=' + ispnum;
        } else if ( pool == 'Name' ){
		var page=document.getElementById('page_now').value;
        	var ispnum=document.getElementById('ispnum').value;
       	 	graphIF.location.href='rate.cgi?action=sort&page=' + page + '&show=' + ispnum;	
        } else
         	graphIF.location.href='rate.cgi?pool=' + pool;
        
        if(refreshtime)
             myVar = setTimeout("refresh();",parseInt(refreshtime.value)*1000);
		
		
}
function auto_refresh(){
    	var REF=document.getElementById('REF');
    	var refreshtimer=document.getElementById('refreshtime');
		
        if(REF.innerHTML!="STOP"){
                REF.innerHTML="STOP";
               setTimeout("refresh()",100);
	      
        }
        else{
                REF.innerHTML="AUTO";
                clearTimeout(myVar);
        }
}

function toallvalue(){

//if(document.getElementById('ttrowid')){
//document.getElementById('tbId').deleteRow(0);
//}
//var maindiv= document.getElementById('tbId').insertRow(0);
	//maindiv.id="ttrowid";
//var GCARD = new graphcard(this);
      //this.cards.push(GCARD);
	  
  //GCARD.obj.childNodes[0].outerHTML ='<legend style="color: white; font: 12px Verdana; background-color: rgb(51, 102, 153);"><span style="font-weight: bold;">Aggregated Speed</span></legend>';
  //var y=maindiv.insertCell(0).appendChild(GCARD.obj);
  //GCARD.parent.RX_total = RX0;
  //GCARD.parent.TX_total = TX0;
  var speed = new speed_meter();
  speed.set('10000','0','5000','8000','Kb/s','Aggregated Speed [Download]','total_down','2000','total_down',rx0,DL0);
  speed.creat();
  speed.set('10000','0','5000','8000','Kb/s','Aggregated Speed [Upload]','total_up','2000','total_up',tx0,UL0);
  speed.creat();
  //GCARD.set("Total_link","","",tx0,rx0,TX0,RX0,DL0,UL0,1,"", "");
  
  //GCARD.show();
  //y.innerHTML='<fieldset><legend style="color: white; font: 12px Verdana; background-color: rgb(51, 102, 153);"><span style="font-weight: bold;">Total_Link</span> Interface: [ <span>eth0</span> ] GateWay: [ <span>218.211.253.254</span> ]<a></a> Latency : [<span style="color: yellow;">42ms</span> ]</legend><table cellspacing="1" cellpadding="0" style="font: 9px Verdana; color: white;"><tbody><tr><td width="90" align="right" style="padding-right: 2px;">12(Kb/s)</td><td width="120" style="background: none repeat scroll 0% 0% black; border: 2px ridge white;"><span style="width: 0.342857%; font-size: 8px; height: 8px; background: -moz-linear-gradient(center top , white, green) repeat scroll 0px 0px transparent; display: block;">&nbsp;</span></td><td width="90" align="right" style="padding-right: 2px;">244374(KB)</td><td width="120" style="background: none repeat scroll 0% 0% black; border: 2px ridge white;"><span style="width: 95.8111%; font-size: 8px; height: 8px; background: -moz-linear-gradient(center top , white, green) repeat scroll 0px 0px transparent; display: block;">&nbsp;</span></td></tr><tr><td width="90" align="right" style="padding-right: 2px;">17(Kb/s)</td><td width="120" style="background: none repeat scroll 0% 0% black; border: 2px ridge white;"><span style="width: 2.125%; font-size: 8px; height: 8px; background: -moz-linear-gradient(center top , white, purple) repeat scroll 0px 0px transparent; display: block;">&nbsp;</span></td><td width="90" align="right" style="padding-right: 2px;">38675(KB)</td><td width="120" style="background: none repeat scroll 0% 0% black; border: 2px ridge white;"><span style="width: 64.5767%; font-size: 8px; height: 8px; background: -moz-linear-gradient(center top , white, purple) repeat scroll 0px 0px transparent; display: block;">&nbsp;</span></td></tr></tbody></table></fieldset>';
  
// var mainttable

}

function speed_meter()
{
    this.max='200';
    this.mix='0';
    this.max_color='150';
    this.mix_color='50';
    this.unit='bps/s';
    this.title='Speed';
    this.id='';
    this.time='1000';
    this.name='';
    this.num=0;

    this.set=(function(max,mix,max_color,mix_color,unit,title,id,time,name,num,total){
        this.max=max;
        this.mix=mix;
        this.max_color=max_color;
    	this.mix_color=mix_color;
        this.unit=unit;
        this.title=title;
        this.id=id;
        this.time=time;
        this.name=name;
        this.num=num;
        this.total=total;
    });

    this.creat=(function(){
       var id = this.id;
       var name = this.name;
       var num=this.num;
       var total=this.total*1024;
        \$("#"+id).highcharts({
            chart: {
                type: 'gauge',
                backgroundColor: "#336699",
                plotBackgroundColor: null,
                plotBackgroundImage: null,
                plotBorderWidth: 0,
                plotShadow: false
            },
            title: {
                text: this.title,
                style:{
                    color:"#FFFFFF"
                }
            },
    	    pane: {
    	        startAngle: -150,
    	        endAngle: 150,
    	        background: [{
    	            backgroundColor: {
    	                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
    	                stops: [
    	                    [0, '#FFF'],
    	                    [1, '#333']
    	                ]
    	            },
    	            borderWidth: 0,
    	            outerRadius: '109%'
    	        },
    	        {
    	            backgroundColor: {
    	            	linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
    	            	stops: [
    	                    [0, '#333'],
    	                    [1, '#FFF']
    	            	]
    	            },
    	            borderWidth: 1,
    	            outerRadius: '107%'
    	        },
    	        {
    	        },
    	        {
    	            backgroundColor: '#DDD',
    	            borderWidth: 0,
    	            outerRadius: '105%',
    	            innerRadius: '103%'
    	        }]
    	    },
    	    yAxis: {
    	        min: 0,
    	        max: total,
    	        minorTickInterval: 'auto',
    	        minorTickWidth: 1,
    	        minorTickLength: 10,
    	        minorTickPosition: 'inside',
    	        minorTickColor: '#666',
    	        tickPixelInterval: 30,
    	        tickWidth: 2,
    	        tickPosition: 'inside',
    	        tickLength: 10,
    	        tickColor: '#666',
    	        labels: {
    	            step: 2,
    	            rotation: 'auto'
    	        },
    	        title: {
    	            text: this.unit
    	        },
    	        plotBands: [{
    	            from: 0,
    	            to: total/2,
    	            color: '#55BF3B' // green
    	        },
    	        {
    	            from:total/2,
    	            to:(total/4)*3,
    	            color: '#DDDF0D' // yellow
    	        },
    	        {
    	            from:(total/4)*3,
    	            to:total,
    	            color: '#DF5353' // red
    	        }]
    	    },
    	    series: [{
    	        enableMouseTracking: false,
    	        data: [0],
    	        dataLabels: {
    	            formatter: function () {
    	   		var kmh = this.y;
    	                return kmh/1024;
    	            }
    	        }
    	    }]
    	},
        function (chart1) {
                //setInterval(function () {
                    var point = chart1.series[0].points[0];
                        point.update(Math.round(num*1024));
                    /*\$.get("speed_data.pl",{name:name,option:id},function(yy){
                        point.update(Math.round(yy));
                    }); 
                },1000);*/
        });
    });
}

</script>

QB_TRAFFIC

#JS

print qq(</select>);
print qq(seconds&#32&#32);
print qq(<button  type="button" ID=REF class="qb" style="font:9 Verdana;width:40;height:20" onclick="auto_refresh();">AUTO</button>);

print qq(&#32&#32);
print qq(<button ty pe="button" class="qb" style="font:9 Verdana;width:50;height:20" onclick="resetVolumn();">Reset</button>);
print qq(&#32&#32);

#count is numbers of isp
my $ispref=XMLread("/usr/local/apache/active/basic.xml");
my $isplist=$ispref->{isp};
my $count=0;
foreach my $isp ( @$isplist ) 
{ 
    if ( $isp->{iid} eq 'system' ) { next; }
    $count++; 
}
#total page
my $page=1;
while ( $count > 0 )
{
    $count -= $ispnum;
    $page++;
}
$page--;


#-----------------------------------------------------------
#	Select Show By Name , By ID or Pool 
#-----------------------------------------------------------
my %rtablehash=GETALLPOOL();

print qq(Show);
print qq(<select id="pool" class="qbopt"  onchange="ShowByPool();" style="font:9 Verdana;height:20;width:110">);
print qq(<option id="ID" value="ID">Links By Default</option>);
print qq(<option id="Name" value="Name">Links Alphabetically</option>);
print qq(<option id="DEAD" Value="DEAD">Links Down</option>);
print qq(<option id="WAN" Value="WAN">Physical Links</option>);

foreach $key (sort num_sort keys %rtablehash )
{
    print qq(<option id="$key" value="$key">Pool $key  $rtablehash{$key}</option>);
}

print qq(</select>);
print qq(</DIV>);


#only by ID and by Name need pre & next page 
if ( $page_now ne "" )
{
	print qq(<DIV class="qbCopy">);
	#print qq(<DIV class="body">);
	print qq(Show); 
	print qq(<input class="qb" id="ispnum" name="ispnum" style="WIDTH: 30px"  value="$ispnum" title="Records Range 10 - 100" onchange="ChangeISPnum();">);
	print qq(Records Per Page);

	print qq(<button class="qb" ID=FIRST style="font:9 Verdana;width:25;height:20" onclick="gotopage(1);">&lt&lt</button>);
	print qq(&#32&#32);
	print qq(<button class="qb" ID=PRE style="font:9 Verdana;width:25;height:20" onclick="gotopage($page_pre);">&lt</button>);
	print qq(</td>);
	print qq(&#32&#32\( $page_now&#32&#32 of &#32&#32 $page \)&#32&#32);
	print qq(&#32&#32);
	print qq(<button class="qb" ID=NEXT style="font:9 Verdana;width:25;height:20" onclick="gotopage($page_next);">&gt</button>);
	print qq(&#32&#32);
	print qq(<button class="qb" ID=LAST style="font:9 Verdana;width:25;height:20" onclick="gotopage($page);">&gt&gt</button>);
	print qq(</DIV>);
}

print qq(<iframe name="graphIF" src="rate.cgi?action=$action&page=$page_now&show=$ispnum&pool=$spool" style="display:none"></iframe>);

print qq(<input type="hidden" id="action" name="action" value="$action">);
print qq(<input type="hidden" id="page_now" name="page_now" value="$page_now">);
print qq(<input type="hidden" id="total" name="total" value="$page">);
print qq(<input type="hidden"  id="spool" name="spool" value="$spool">);

print qq(<script> var gmaster = new graphmaster('graphspace');var REF=document.getElementById('REF'); REF.click()</script>);

print qq(</form>);
print qq(</body>);
print qq(</html>);

sub num_sort { int($a) <=> int($b); }

sub GETALLPOOL
{
    my $rtables = XMLread('/usr/local/apache/active/rtable.xml');
    my $temptables=$rtables->{table};
    my %poolnote;
     
    foreach my $table ( @$temptables )
   {
    	if ( $table->{table_num} eq 'system' || $table->{table_num} > 52 || $table->{table_num} == 30 ) { next; }
    	$poolnote{ $table->{table_num} }=$table->{note};
    }
    return %poolnote;
}
#XMLread
1
