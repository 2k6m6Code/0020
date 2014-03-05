//////////////////////////////
//daslt_rttraffic.js 2004/03/30
//////////////////////////////

//////////////////////////////
//Variable
//////////////////////////////

var sltObj;	//ActiveX Scriptlet Object
var DAVC;	//Direct Animation Viewer Control Object
var m;		//Direct Animation Library Object
var userData;		//userDataObj
var daColorArr;		//DAColor Array
var daFillImageHash;	//DA FillImage hash (implement with new Object())
var daDefaultFont;	//DAFont
var daMbNode;		//DAModifiableBehavior Array (implement with new Array())
var daMbNodeIndex;	//number
var isModify;
var dataMode;
var daRadius;
var a2r = Math.PI / 180;

//////////////////////////////
//Scriptlet function
//////////////////////////////

function sltInit(sObj){

	//assign dhtml object to variable
	sltObj = sObj;

	DAVC = document.all["oDAViewerControl"];
	m = DAVC.pixelLibrary;
	dataMode = "RXTX";
	daRadius = 80;

	sltObj.style.width = sltObj.clientWidth;
	sltObj.style.height = sltObj.clientHeight;
	DAVC.style.width = 540;	//sltObj.style.pixelWidth-20;
	DAVC.style.height = 350;//sltObj.style.pixelHeight;

	//initial variable
	userData = new userDataObj();
	daMbNode = new Array();

	daDefaultFont = m.defaultFont.size(12).Family("Verdana").color(m.WHITE);
	daColorArr = new Array();
	sltObj.setColor(0,243,170,228);
	sltObj.setColor(1,255,182,110);
	sltObj.setColor(2,255,255,110);
	sltObj.setColor(3,127,255,127);
	sltObj.setColor(4,127,194,255);
	sltObj.setColor(5,127,136,255);
	sltObj.setColor(6,202,0,208);

	
	//Initial DAViewerControl
	DAVC.Image = DrawMain();
	DAVC.Start();
	
	return sltObj;
}

function sltShow(){
	
	infoUpdate();
	
	DrawImage();
	isModify=false;
	return sltObj;
}
function sltSetRadius(r){
	daRadius = r;
	return sltObj;
}
function sltSetDataMode(type){
	switch(type){
	case "rx":
	case "tx":
	case "rxtx":
	case "RX":
	case "TX":
	case "RXTX":
		dataMode = type;
		break;
	default:
		dataMode = "rx";
		break;
	}
	return sltObj;
}

function sltSetColor(name){
	switch(name){
	case "background":document.body.style.background = arguments[1];break;
	default:daColorArr[name] = m.colorRgb255(parseInt(arguments[1]),parseInt(arguments[2]),parseInt(arguments[3]));break;
	}
	return sltObj;
}

function sltClear(){
	isModify=true;
	userData.clear();
	return sltObj;
}

function sltSetData(){
	isModify=true;
	userData.add(arguments);
	return sltObj;
}

function CreateScriptlet(){
	
	this.show = sltShow;
	this.init = sltInit;
	this.clear = sltClear;
	this.add = sltSetData;
	this.setColor = sltSetColor;
	this.setDataMode = sltSetDataMode;
	this.setRadius = sltSetRadius;
}

var public_description = new CreateScriptlet();

//////////////////////////////
//Object's Construstor Functions
//////////////////////////////

function userDataObj(){
	this.data = new Array();
}
function userDataObj.prototype.add(dataArr){
	this.data.push(new DrawData(dataArr));
}
function userDataObj.prototype.clear(){
	this.data = new Array();
}

function DrawData(dataArr){
	var tmp;
	this.name	= dataArr[0];
	this.port	= isNaN(tmp=parseInt(dataArr[1]))?0:tmp;
	this.gateway	= dataArr[2];
	this.tx		= isNaN(tmp=parseFloat(dataArr[3]))?0:tmp;
	this.rx		= isNaN(tmp=parseFloat(dataArr[4]))?0:tmp;
	this.TX		= isNaN(tmp=parseFloat(dataArr[5]))?0:tmp;
	this.RX		= isNaN(tmp=parseFloat(dataArr[6]))?0:tmp;
	this.DL		= isNaN(tmp=parseFloat(dataArr[7]))?Number.POSITIVE_INFINITY:tmp;
	this.UL		= isNaN(tmp=parseFloat(dataArr[8]))?Number.POSITIVE_INFINITY:tmp;
	this.alive	= isNaN(tmp=parseInt(dataArr[9]))?0:tmp;
	this.rxtx = this.rx + this.tx;
	this.RXTX = this.RX + this.TX;
	this.percent = 0;
	this.sAngle = 0;
	this.eAngle = 0;
}
DrawData.prototype.max = 0;


function infoUpdate(){
	
	//Calculate the total of RX & TX
	DrawData.prototype.max = 0;
	
	for(var i=0;i<userData.data.length;i++){
		if(userData.data[i][dataMode]==0)
			continue;
		DrawData.prototype.max += userData.data[i][dataMode];
	}
	var N2A = 360 / DrawData.prototype.max;	//number to angle
	var angle = 0;
	for(var i=0;i<userData.data.length;i++){
		if(userData.data[i][dataMode]==0)
			continue;
		userData.data[i].percent = parseInt(userData.data[i][dataMode] * 100 / DrawData.prototype.max);
		userData.data[i].sAngle = angle;
		userData.data[i].eAngle = angle += userData.data[i][dataMode] * N2A;
	}
}

//////////////////////////////
//DirectAnimation Functions
//////////////////////////////

//Scriptlet.set(name,port,gw,tx,rx,TX,RX,DL,UL,alive);

function DrawMain(){

	var i;
	var index;
	daMbNodeIndex=0;
	
	var imgArr = new Array(m.EmptyImage);

	for(i=0;i<userData.data.length;i++){
		imgArr.unshift(drawRecord(i));
	}

	var mb1 = daMbNode[daMbNodeIndex++]= m.ModifiableBehavior( m.OverlayArray(imgArr));

	return mb1;
}
function DrawImage(){

	var i,index;
	daMbNodeIndex=0;

	var imgArr = new Array(m.EmptyImage);
	
	for(i=0;i<userData.data.length;i++){
		if(userData.data[i][dataMode]==0)
			continue;
		imgArr.unshift(drawRecord(i));
	}
	if(DrawData.prototype.max==0)
		imgArr.unshift(m.StringImage("Zero Traffic Count",daDefaultFont));
	
	daMbNode[daMbNodeIndex++].SwitchTo(m.OverlayArray(imgArr));
}

function drawRecord(index){
		
	//pie
	var b1 = drawPie(index);
	
	//line
	var b2 = drawLine(index);
	
	//number
	var b3 = drawText(index);

	return m.OverlayArray([b1,b2,b3]);
}

function drawPie(index){
	
	return m.PieDegrees(
		90-userData.data[index].sAngle,90-userData.data[index].eAngle,daRadius<<1,daRadius<<1
		).Fill(m.defaultLineStyle,m.solidColorImage(daColorArr[index%7]));
}

function drawLine(index){
	
	var a = ( userData.data[index].sAngle + userData.data[index].eAngle ) / 2;
	
	var p1 = m.Point2((daRadius+0)*Math.sin(a*a2r),-(daRadius+0)*Math.cos(a*a2r));
	var p2 = m.Point2((daRadius+20)*Math.sin(a*a2r),-(daRadius+20)*Math.cos(a*a2r));
	var p3 = m.Point2((daRadius+20)*Math.sin(a*a2r)>=0?daRadius*1.35:-daRadius*1.35,-(daRadius+20)*Math.cos(a*a2r));
	
	return m.Concat(m.Line(p1,p2),m.Line(p2,p3)).Draw(m.defaultLineStyle);
}

function drawText(index){
	
	var a = ( userData.data[index].sAngle + userData.data[index].eAngle ) / 2;
	var b1 = m.StringImage(userData.data[index].name+" ("+userData.data[index].percent+"%)",daDefaultFont).Transform(m.Translate2((daRadius+20)*Math.sin(a*a2r)>=0?daRadius*1.75:-daRadius*1.75,-(daRadius+20)*Math.cos(a*a2r)));
	
	return b1;
}