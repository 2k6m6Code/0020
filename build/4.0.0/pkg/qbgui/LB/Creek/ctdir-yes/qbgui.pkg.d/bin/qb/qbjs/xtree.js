var basepath = window.location.href.replace(/[^/]+$/gi,"");

function xTree(tCont,xTreeSrc){

	var oCont = document.all[tCont];

	//clear oCont's child

	while(oCont.childNodes.length)
		oCont.firstChild.parentNode.removeChild(oCont.firstChild);//oCont.firstChild.removeNode(1);

	//if xTreeSrc is NULL, get one from Tag
	if(typeof(xTreeSrc)!="string")
		xTreeSrc = oCont.getAttribute("xTreeSrc");

	if(xTreeSrc == "")
        {
            var lang=getcookie('language');
            var english_only=getcookie('english_only');
            var menutree="";

            if ( english_only == "true" )  
                menutree="english_only"; 
            else
                if ( typeof(lang) != "string" )  
                    menutree='english'; 
                else
                    menutree=lang;

            xTreeSrc=menutree + '.xml';
        }

	//if xTreeSrc is NULL, do not thing
	if(typeof(xTreeSrc)!="string")
		return false;
		
	//load xml
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
	    xmlhttp = new XMLHttpRequest();
	 }else{
	    xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function(){if(xmlhttp.readyState!=4)return false;xTreeBuild(tCont,xmlhttp.responseXML)};
	xmlhttp.open("GET",'xtree.cgi?name='+xTreeSrc,true);
	xmlhttp.send();
}

function xTreeBuild(tCont,oXml){

	var oCont = document.all[tCont];

	if(oXml.childNodes.length!=2){
		oCont.innerHTML = xTreeParseXml(tCont,oXml.childNodes[0]);
	}else{
	
	oCont.innerHTML = xTreeParseXml(tCont,oXml.childNodes[1]);
	}
}

function xTreeParseXml(tCont,root){

	var oCont = document.all[tCont];

	var text="";

	var tm_target=oCont.getAttribute("xTreeTarget");
	
	var i,j,tmp;
	
	var oLI,oOL,oA;
	var myName,myUrl,subroot,myTitle,myScript,myXmlSrc;
	for(i=0;i<root.childNodes.length;i++){
	if (root.nodeType==1){

		myName = myUrl = subroot = myTitle = myXmlSrc=myScript="";

		for(j=0;j<root.childNodes[i].childNodes.length;j++){
		if(root.childNodes[i].childNodes[j].nodeType!=1){continue;}
		if(root.childNodes[i].nodeType==1){
			if (navigator.userAgent.search("MSIE") >-1)
			{// code for IE
				if(navigator.userAgent.search("MSIE 10.0") >-1){
				tmp = root.childNodes[i].childNodes[j].textContent;
				}else{
				
				tmp = root.childNodes[i].childNodes[j].text;
				}
				
			 }else{
				tmp = root.childNodes[i].childNodes[j].textContent;
			} 			
			switch(root.childNodes[i].childNodes[j].tagName){
			case "name":myName=tmp;break;
			case "title":myTitle=tmp;break;
			case "script":myScript=tmp;break;
			case "xml":myXmlSrc=tmp;break;
			case "link":myUrl=tmp;break;
			case "child":subroot=root.childNodes[i].childNodes[j];break;
			default:break;
			}
			
		}//if root.childNodes[i].nodeType==1
		}

		if(myUrl)myUrl=basepath+myUrl;
		if(myXmlSrc)myXmlSrc=basepath+myXmlSrc;


		if(!myName)continue;
		
		oLI = document.createElement("LI");
		oA = document.createElement("A");
		oLI.style.listStyle = "circle";
		oLI.style.listStylePosition="inside";
		oLI.style.border="0 solid white";
		oLI.style.cursor="default";
		oLI.style.width="auto";
		//oLI.onclick = "tm_LIclick(this)";
		oLI.setAttribute("onclick", "javascript:tm_LIclick(this);");
		oLI.title = myTitle;
		oA.href = myUrl;
		if (myName == "ViewFlow")
		    oA.target = "_blank";
		else
                    oA.target = tm_target;
		//oA.onclick = (myXmlSrc?"xTree('"+tCont+"','"+myXmlSrc+"');":"")+(myScript?myScript:"")+(myUrl?"":";return false");
		var oAclick =(myXmlSrc?"xTree('"+tCont+"','"+myXmlSrc+"');":"")+(myScript?myScript:"")+(myUrl?"":";return false");
		oA.setAttribute("onclick","javascript:"+ oAclick+";");
		
			if (navigator.userAgent.search("MSIE") >-1)
			{// code for IE
				oA.innerText = myName;
				
			 }else{
				oA.textContent = myName;
			}
		
		oLI.innerHTML = (myUrl||myXmlSrc||myScript?oA.outerHTML:myName);
				
		//oLI.onmouseover = tm_LImouseover(this);
		//oLI.onmouseout = tm_LImouseout(this);
		oLI.setAttribute("onmouseover", "javascript:tm_LImouseover(this);");
		oLI.setAttribute("onmouseout", "javascript:tm_LImouseout(this);");

		if(!subroot){
			text += oLI.outerHTML+"\n";
			continue;
		}

		oLI.style.listStyle = "disc";
		oLI.style.listStylePosition="inside";
		text += oLI.outerHTML+"\n";
		
		oOL = document.createElement("OL");
		oOL.style.display="none";
		oOL.style.margin="0 0 0 0";
		oOL.style.padding="0 0 0 30";
		oOL.innerHTML = xTreeParseXml(tCont,subroot);
		
		text += oOL.outerHTML+"\n";
	}//if nodeType==1
	}


	return text;
}

function tm_LIclick(oLI){

if(oLI.nextSibling.nodeType !=1){
	if(oLI.nextSibling.nextSibling.nodeName=="LI"){return false;}
	}else{
	if(oLI.nextSibling.nodeName=="LI"){return false;}
	}
	var olnode = document.getElementsByTagName('ol');
	for(var hh = 0;hh<olnode.length;hh++){
	olnode[hh].style.display="none";
	if( olnode[hh].previousSibling.nodeType !=1 ){
	olnode[hh].previousSibling.previousSibling.style.listStyle = "disc";
	olnode[hh].previousSibling.previousSibling.style.listStylePosition= "inside";
	}else{
	olnode[hh].previousSibling.style.listStyle = "disc";
	olnode[hh].previousSibling.style.listStylePosition= "inside";
	}
	}
	if(oLI.nextSibling.nodeType!=1  && oLI.nextElementSibling.nodeName=="OL"){
		if(oLI.nextElementSibling.style.display=="none" ){
		oLI.style.listStyle = "circle";
		oLI.style.listStylePosition="inside";
		oLI.nextElementSibling.style.display="block";
		}else{
		oLI.style.listStyle = "disc";
		oLI.style.listStylePosition="inside";
		oLI.nextElementSibling.style.display="none";
		
		}
	}

	if(!oLI.nextSibling || oLI.nextSibling.tagName!="OL")
		return false;
	if(oLI.nextSibling.style.display!="block"){
		oLI.style.listStyle = "circle";
		oLI.nextSibling.style.display="block";
	}
	else{
		oLI.style.listStyle = "disc";
		oLI.nextSibling.style.display="none";
	}
}tm_LIclick.last=null;
function tm_LImouseover(oLI){
	oLI.style.backgroundColor="#999999";
	oLI.style.borderColor="#555555";
}
function tm_LImouseout(oLI){
	oLI.style.backgroundColor="";
	oLI.style.borderColor="";
}
