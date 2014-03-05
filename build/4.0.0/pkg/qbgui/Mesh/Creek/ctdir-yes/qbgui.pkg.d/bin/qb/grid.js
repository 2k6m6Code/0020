/* for general purpose Select and Focus schema */

var sColor  =   "#66aadd";
var sfColor =   "#77bbee";
var fColor  =   "#3377aa";
var aColor  =   "#bb6600";
var afColor =   "#cc7711";
var asColor =   "#dd8822";

var lastSelected=null;

function initSelect(obj)
{
    switch ( obj.bgColor )
    {
        case aColor :
            obj.bgColor=asColor;
            break;
    
        default:
            obj.bgColor=sfColor;
    }

    lastSelected=obj;
}

function focusedColor(obj)
{


    switch ( obj.bgColor )
    {
        case sColor :
            obj.bgColor=sfColor;
            break;

        case sfColor :
            obj.bgColor=sfColor;
            break;

        case aColor :
            obj.bgColor=afColor;
            break;
         
        case asColor:
            break;   

        default:
            obj.bgColor=fColor;
    }
}


function blurColor(obj)
{
    switch ( obj.bgColor )
    {
        case sfColor :
            obj.bgColor=sColor;
            break;

        case sColor :
            alert(obj.bgColor);
            obj.bgColor=sColor;
            break;

        case asColor :
            break;    
        
        default:
            obj.bgColor=obj.getAttribute("originalcolor");
    }

}   

function selectedColor(obj)
{
    switch ( obj.bgColor )
    {
        case afColor :
            obj.bgColor=asColor;
            break;

        case aColor :
            obj.bgColor=asColor;
            break;

        case fColor:
            obj.bgColor=sfColor;
            break;
    
        default:
            obj.bgColor=sfColor;
    }
 
	if(lastSelected==obj)
	{
		lastSelected.bgColor=lastSelected.getAttribute("originalcolor");
		lastSelected=null;
		return;
	}
	if(lastSelected)
	{
		lastSelected.bgColor=lastSelected.getAttribute("originalcolor");
	}
	lastSelected=obj;
   
}


