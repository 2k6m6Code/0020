//////////////////////////////
//daslt_rttraffic.js 2004/03/30
//////////////////////////////

//////////////////////////////
//Variable
//////////////////////////////

var sltObj;	//ActiveX Scriptlet Object
var sltScroll;	//ActiveX Srcollbar Object
var DAVC;	//Direct Animation Viewer Control Object
var m;		//Direct Animation Library Object
var userData;		//userDataObj
var daColorHash;	//DAColor hash (implement with new Object())
var daFillImageHash;	//DA FillImage hash (implement with new Object())
var daDefaultFont;	//DAFont
var daMbNode;		//DAModifiableBehavior Array (implement with new Array())
var daMbNodeIndex;	//number
var graphLines;		//number
var isModify;


//////////////////////////////
//Scriptlet function
//////////////////////////////

function sltInit(sObj){

	//assign dhtml object to variable
	sltObj = sObj;
	sltScroll = document.all["oScroll"];
	DAVC = document.all["oDAViewerControl"];
	m = DAVC.pixelLibrary;

	sltObj.style.width = sltObj.clientWidth;
	sltObj.style.height = sltObj.clientHeight;
	DAVC.style.width = 540;	//sltObj.style.pixelWidth-20;
	DAVC.style.height = 370;//sltObj.style.pixelHeight;

	sltScroll.attachEvent('change',sltObj.show);

	//initial variable
	userData = new userDataObj();
	daMbNode = new Array();
	polyLines = 90;
	daDefaultFont = m.defaultFont.size(11).Family("Verdana").color(m.WHITE);

	daFillImageHash = new Object();
	daFillImageHash["skin_die"] = 
		m.GradientPolygon(
			new Array(m.Point2(0,0),m.Point2(520,0),m.Point2(520,70),m.Point2(0,70)),
			new Array(m.YELLOW,m.RED,m.RED,m.YELLOW)
		);
	daColorHash = new Object();
	sltObj.setColor("outline",255,0,128);
	sltObj.setColor("inline",100,255,100);
	sltObj.setColor("outpoly",255,0,128);
	sltObj.setColor("inpoly",100,255,100);
	sltObj.setColor("default",128,128,128);
	daColorHash["fullcolor"] = m.colorHslAnim(m.localtime,m.DANumber(1),m.DANumber(0.5));
	


	//Initial DAViewerControl
	DAVC.Image = DrawMain().Transform(m.Translate2(-DAVC.style.pixelWidth/2,-DAVC.style.pixelHeight/2));
	DAVC.Start();
	
	return sltObj;
}

function sltShow(){
	
	if(isModify)
		infoUpdate();
	
	DrawImage();
	isModify=false;
	return sltObj;
}

function sltSetColor(name){
	switch(name){
	case "background":document.body.style.background = arguments[1];break;
	default:daColorHash[name] = m.colorRgb255(parseInt(arguments[1]),parseInt(arguments[2]),parseInt(arguments[3]));break;
	}
	switch(name){
	case "inline":
	case "outline":
		daFillImageHash[name] = m.GradientPolygon(
			new Array(m.Point2(0,0),m.Point2(150,0),m.Point2(150,8),m.Point2(0,8)),
			new Array(m.WHITE,m.WHITE,daColorHash[name],daColorHash[name]));
		break;
	case "inpoly":
	case "outpoly":
		daFillImageHash[name] = m.GradientPolygon(
			new Array(m.Point2(0,0),m.Point2(180,0),m.Point2(180,20),m.Point2(0,20)),
			new Array(m.WHITE,m.WHITE,daColorHash[name],daColorHash[name]));
		break;
	case "default":
		daFillImageHash[name+"line"]=m.GradientPolygon(
			new Array(m.Point2(0,0),m.Point2(150,0),m.Point2(150,8),m.Point2(0,8)),
			new Array(m.WHITE,m.WHITE,daColorHash[name],daColorHash[name]));
		daFillImageHash[name+"poly"] = m.GradientPolygon(
			new Array(m.Point2(0,0),m.Point2(180,0),m.Point2(180,20),m.Point2(0,20)),
			new Array(m.WHITE,m.WHITE,daColorHash[name],daColorHash[name]));
		break;
	default:break;
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
	this.graph;
	this.setGraph();
}
DrawData.prototype.RXM=0;
DrawData.prototype.TXM=0;
DrawData.prototype.polyData = new Object();

function DrawData.prototype.setGraph(){
	
	var p;
	if(typeof(p=this.polyData[this.name])=="undefined"){
		p = this.polyData[this.name] = new Object();
		p.rx = new Array();
		p.tx = new Array();
		for(var i=0;i<polyLines;i++)
			p.rx[i] = p.tx[i] = 0;
	}
	p.rx.push(this.rx);
	p.rx.shift()
	p.tx.push(this.tx);
	p.tx.shift();
	this.graph = p;
}
function infoUpdate(){
	
	sltScroll.Max = userData.data.length < 4 ? 0 : userData.data.length - 4;
	
	var from = userData.data.length ? sltScroll.value+1 : 0;
	var to = sltScroll.Max - sltScroll.value > 0 ? sltScroll.value+4 : userData.data.length ;
	
	sltScroll.title = from + " ~ " + to + " of " + userData.data.length;
	sltScroll.LargeChange = 4;
	
	//Calculate the total of RX & TX
	DrawData.prototype.RXM = 0;
	DrawData.prototype.TXM = 0;
	for(var i=0;i<userData.data.length;i++){
		DrawData.prototype.RXM += userData.data[i].RX;
		DrawData.prototype.TXM += userData.data[i].TX;
		if(userData.data[i].graph.rx[polyLines-1]>userData.data[i].DL)
			userData.data[i].graph.rx[polyLines-1] = userData.data[i].DL;
		if(userData.data[i].graph.tx[polyLines-1]>userData.data[i].UL)
			userData.data[i].graph.tx[polyLines-1] = userData.data[i].UL;
	}
}


//////////////////////////////
//DirectAnimation Functions
//////////////////////////////


//Scriptlet.set(name,port,gw,tx,rx,TX,RX,DL,UL,alive);

function DrawMain(){
	
	var i;
	var index;
	var top=10;
	daMbNodeIndex=0;
	
	var imgArr = new Array();
	
	imgArr.unshift(drawNotice(true).Transform(m.Translate2(10,top)));
	
	top+=40;
	
	for(i=0;i<4;i++){
		//drawRecord
		index = i<userData.data.length?i:-1;
		imgArr.unshift(drawRecord(true,index).Transform(m.Translate2(10,top)));
		top+=80;
	}
	
	return m.OverlayArray(imgArr);
}
function DrawImage(){

	var i,index;
	daMbNodeIndex=0;
	
	drawNotice(false);
	
	for(i=sltScroll.value;i<4+sltScroll.value;i++){
		index = i<userData.data.length?i:-1;
		drawRecord(false,index);
	}

}

function drawNotice(init){

	var w = 520;
	var h = 30;
	
	var b1 = m.RoundRect(50,8,5,5).Fill(m.defaultLineStyle.color(m.Silver),daFillImageHash["inline"].Transform(m.Translate2(-75,-4)));
	var b2 = m.RoundRect(50,8,5,5).Fill(m.defaultLineStyle.color(m.Silver),daFillImageHash["outline"].Transform(m.Translate2(-75,-4)));

	if(!init){
		daMbNode[daMbNodeIndex++].SwitchTo(b1);
		daMbNode[daMbNodeIndex++].SwitchTo(b2);
		return false;
	}
	
	var mb1 =(daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b1)).Transform(m.Translate2(25+20,4+10));
	var mb2 =(daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b2)).Transform(m.Translate2(25+150,4+10));
	var b3 = m.StringImage("InBound",daDefaultFont).Transform(m.Translate2(100,18));
	var b4 = m.StringImage("OutBound",daDefaultFont).Transform(m.Translate2(235,18));
	var b5 = m.RoundRect(w,h,20,20).Draw(m.defaultLineStyle.color(m.white)).Transform(m.Translate2(w/2,h/2));
	
	return m.OverlayArray([mb1,mb2,b3,b4,b5]);
}

function drawRecord(init,index){
	
	var b1 = drawSkin(init,index);
	var b2 = drawTitle(init,index);
	var b3 = drawLine(init,index,"rx");	//rx
	var b4 = drawLine(init,index,"tx");	//tx
	var b5 = drawLine(init,index,"RX");	//RX
	var b6 = drawLine(init,index,"TX");	//TX
	var b7 = drawPoly(init,index,"rx");
	var b8 = drawPoly(init,index,"tx");

	if(!init)return false;

	b3 = b3.Transform(m.Translate2(10,20));
	b4 = b4.Transform(m.Translate2(10,45));
	b5 = b5.Transform(m.Translate2(360,20));
	b6 = b6.Transform(m.Translate2(360,45));
	b7 = b7.Transform(m.Translate2(170,20));
	b8 = b8.Transform(m.Translate2(170,45));

	return m.OverlayArray([b1,b2,b3,b4,b5,b6,b7,b8].reverse());
}



function drawSkin(init,index){

	var w = 520;
	var h = 70;
	var s = 25;
	
	var field1=2;
	if(index != -1){
		field1 = userData.data[index].alive;
	}

	if(!drawSkin.fillImage)
		drawSkin.fillImage = new Array(
			m.SolidColorImage(m.colorRgb255(255,255,0)),
			m.SolidColorImage(m.colorRgb255(148,239,237)),
			m.SolidColorImage(daColorHash["default"])
		);
	if(!drawSkin.color)
		drawSkin.color = new Array(
			m.colorRgb255(255,0,0),
			m.white,
			daColorHash["default"]
		);
	
	
	var b1 = m.PolyLine(new Array(
		m.Point2(0,0),
		m.Point2(s*3/4,0),
		m.Point2(0,s*3/4),
		m.Point2(0,0)
		)).Fill(m.defaultLineStyle.color(drawSkin.color[field1]),drawSkin.fillImage[field1]);

	var b2 = m.PolyLine(new Array(
		m.Point2(s,0),
		m.Point2(w,0),
		m.Point2(w,h),
		m.Point2(0,h),
		m.Point2(0,s),
		m.Point2(s,0)
		));
	if(field1==0)
		b2 = b2.Fill(m.defaultLineStyle.color(drawSkin.color[field1]),daFillImageHash["skin_die"]);
	else
		b2 = b2.Draw(m.defaultLineStyle.color(drawSkin.color[field1]));

	if(!init){
		daMbNode[daMbNodeIndex++].SwitchTo(b1);
		daMbNode[daMbNodeIndex++].SwitchTo(b2);
		return false;
	}

	var mb1 = daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b1);
	var mb2 = daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b2);
	
	return m.OverlayArray([mb1,mb2]);
}
drawSkin.fillImage;
drawSkin.fillImage2;
drawSkin.color;

function drawTitle(init,index){
	
	var field1="";
	var field2="";
	var field3="";
	
	if(index != -1){
		field1 = userData.data[index].name;
		field2 = userData.data[index].port;
		field3 = userData.data[index].gateway;
	}
	
	var b1 = m.StringImage(field1,daDefaultFont);
	var b2 = m.StringImage(field2,daDefaultFont);
	var b3 = m.StringImage(field3,daDefaultFont);

	if(!init){
		daMbNode[daMbNodeIndex++].SwitchTo(b1);
		daMbNode[daMbNodeIndex++].SwitchTo(b2);
		daMbNode[daMbNodeIndex++].SwitchTo(b3);
		return false;
	}
	
	var mb1 = ( daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b1) ).Transform(m.Translate2(10+50,15));
	var mb2 = ( daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b2) ).Transform(m.Translate2(20+200,15));
	var mb3 = ( daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b3) ).Transform(m.Translate2(55+310,15));
	var b4 = m.StringImage("Interface : Port",daDefaultFont).Transform(m.Translate2(50+100,15));
	var b5 = m.StringImage("Gateway :",daDefaultFont).Transform(m.Translate2(35+240,15));
	
	return m.OverlayArray([mb1,mb2,mb3,b4,b5]);
}


function drawLine(init,index,type){

	var w = 150;
	var h = 8;
	var s = 8;

	var percent;
	var value;
	var max;
	var cname;

	switch((init||index==-1)?"":type){
	case "rx":
		value = userData.data[index].rx;
		max = userData.data[index].DL;
		cname=userData.data[index].alive?"inline":"defaultline";
		break;
	case "tx":
		value = userData.data[index].tx;
		max = userData.data[index].UL;
		cname=userData.data[index].alive?"outline":"defaultline";
		break;
	case "RX":
		value = userData.data[index].RX;
		max = userData.data[index].RXM;
		cname=userData.data[index].alive?"inline":"defaultline";
		break;
	case "TX":
		value = userData.data[index].TX;
		max = userData.data[index].TXM;
		cname=userData.data[index].alive?"outline":"defaultline";
		break;
	default:
		value = 0;
		max = 0;
		cname="defaultline";
	break;
	}

	percent = parseFloat(value/max);
	if(isNaN(percent))percent=0;
	if(percent>1)percent=1;
	var b1 = m.PolyLine(new Array(
		m.Point2(s,0),
		m.Point2((w-s)*percent+s,0),
		m.Point2((w-s)*percent,h),
		m.Point2(0,h),
		m.Point2(s,0)
		)).Fill(
			m.defaultLineStyle,
			daFillImageHash[cname]
		);
	var b2 = m.StringImage(value,daDefaultFont);
	var b3 = m.StringImage(max,daDefaultFont);

	if(!init){
		daMbNode[daMbNodeIndex++].SwitchTo(b1);
		daMbNode[daMbNodeIndex++].SwitchTo(b2);
		daMbNode[daMbNodeIndex++].SwitchTo(b3);
		return false;
	}
	var mb1 = ( daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b1) );
	var mb2 = ( daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b2) ).Transform(m.Translate2((w-10)/4,h+12));
	var mb3 = ( daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b3) ).Transform(m.Translate2((w-10)*3/4,h+12));

	var unit;
	switch(type){
	case "rx":unit="Kbps";break;	//rx
	case "tx":unit="Kbps";break;	//tx
	case "RX":unit="KB";break;	//RX
	case "TX":unit="KB";break;	//TX
	default:break;
	}
	
	var b4 = m.PolyLine(new Array(
		m.Point2(s,0),
		m.Point2(w,0),
		m.Point2(w-s,h),
		m.Point2(0,h),
		m.Point2(s,0)
		)).Fill(m.defaultLineStyle,m.solidColorImage(m.BLACK));

	var b5 = m.PolyLine(new Array(
		m.Point2(s,0),
		m.Point2(w,0),
		m.Point2(w-s,h),
		m.Point2(0,h),
		m.Point2(s,0)
		)).Draw(m.defaultLineStyle.width(1).color(m.Silver));

	var b6 = m.StringImage("/",daDefaultFont).Transform(m.Translate2((w-10)/2,h+12))
	var b7 = m.StringImage(unit,daDefaultFont).Transform(m.Translate2(w-10,h+12))

	return  m.OverlayArray([b7,mb3,b6,mb2,b5,mb1,b4]);
}


function drawPoly(init,index,type){
	
	var w = 180;
	var h = 20;
	
	var lineArr = new Array();
	var posdx = 2;//w / polyLines;
	var posx = 1;//posdx / 2;
	var maxBound;
	var cname;
	var graphArr;
	var v2p;

	switch((init||index==-1)?"":type){
	case "rx":
		graphArr = userData.data[index].graph.rx;
		maxBound = userData.data[index].DL;
		cname=userData.data[index].alive?"inpoly":"defaultpoly";
		break;
	case "tx":
		graphArr = userData.data[index].graph.tx;
		maxBound = userData.data[index].UL;
		cname=userData.data[index].alive?"outpoly":"defaultpoly";
		break;
	default:
		cname="defaultpoly";
	break;
	}
	
	if((init||index==-1)){
		var b1 = m.EmptyImage;
	}
	else{
		v2p = h / maxBound;	//value to percent
		lineArr.push(m.Point2(posx,h));
		for(var i=0;i<polyLines;i++){
			lineArr.push(m.Point2(posx,h-graphArr[i]*v2p));
			posx += posdx;
		}
		lineArr.push(m.Point2(posx-posdx,h));
		lineArr.push(m.Point2(posdx/2,h));
		var b1 = m.PolyLine(lineArr).Fill(m.defaultLineStyle.color(m.BLACK),daFillImageHash[cname]);
	}

	if(!init){
		daMbNode[daMbNodeIndex++].SwitchTo(b1);
		return false;
	}
	
	var mb1 = daMbNode[daMbNodeIndex++] = m.ModifiableBehavior(b1);
	
	var b2 = m.PolyLine(new Array(
		m.Point2(0,0),
		m.Point2(w,0),
		m.Point2(w,h),
		m.Point2(0,h),
		m.Point2(0,0)
		)).Fill(m.defaultLineStyle,m.solidColorImage(m.BLACK));
	
	var b3 = m.PolyLine(new Array(
		m.Point2(0,0),
		m.Point2(w,0),
		m.Point2(w,h),
		m.Point2(0,h),
		m.Point2(0,0)
		)).Draw(m.defaultLineStyle.color(m.Silver));
	
	return m.OverlayArray([b3,mb1,b2]);
}
