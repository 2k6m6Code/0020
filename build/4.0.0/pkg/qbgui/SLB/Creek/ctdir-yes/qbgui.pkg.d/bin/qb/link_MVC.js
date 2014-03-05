var myapp={};

myapp.Model = function(){
   var data='';
   var iid='';
   var num='';
   
   this.reNum = function(){
        return "Line"+num;
   }; 
   
   this.getData = function(x,n,d){
       $.get("link_data.pl",{iid:x,option:n,data:d},function(y){
           var tmp = new Array();
           tmp = y.split(/=/);
           data = tmp[0];
           num = tmp[1];
           num++;
           iid=x;
       });
   	$("#check_button").val(x);
   };
   
   this.build = function(x){
	var list = new Array();
	var lineCount = 1;
	var table='';
   	list = x.split(/:/);
   	for(var i =0; i < list.length;i++)	
   	{
   	    var data_tmp = new Array();
   	    data_tmp = list[i].split(/-/);
   	    if (data_tmp[0])
   	    {
   	    	var originalColor=(lineCount%2) ? ( '#556677' ) : ( '#334455' );
   	        table += '<tr bgcolor='+ originalColor +'>';
   	        table += '<td style="width:30%">Line'+data_tmp[0]+'</td>';
   	        table += '<td style="width:30%">'+data_tmp[1]+'</td>';
   	        table += '<td style="width:20%"><a onclick="myapp.view.presenter.edit(\''+data_tmp[0]+'\',\''+data_tmp[1]+'\');"><img src="image/edit.gif" border="0" style="cursor: pointer;"></a></td>';
   	        table += '<td style="width:20%"><input type="checkbox" name="tablestodel" value='+data_tmp[0]+'</td>';
   	        lineCount++;
   	    }
   	}
   	return table;
   };
  
   this.edit = function (x,y,z,k){
       $("#num").val(x);
       $("#name").val(y);
       $("#line").attr("disabled",z);
       if (k)
       {
           $("#setting").dialog( "open" );
           $("#line option[value="+iid+"]").attr("selected",true);
       }
   };
   
   this.div_init = function(x){
   	$( "#" + x).dialog({
   	    autoOpen: false,
   	    height: 400,
   	    width: 350,
   	    modal: true,
   	    buttons:{
   	        "Create": function() {
   	             var data = $("#num").val() + "," + $("#name").val() + "," + $("#line").val();
   	             myapp.view.presenter.option($("#line").val(),'save',data);
   	             $( this ).dialog( "close" );
   	             myapp.view.presenter.getModel().reset_page();
   	        },
   	        Cancel: function() {
   	            $( this ).dialog( "close" );
   	        }
   	    },
   	    close: function() {
   	    }
   	});
   };
   
   this.reset_page=function(){
       setTimeout(function(){$("input[name^='title']").eq(0).trigger("click");},500);
   };
   
   this.sendData = function(){
       return data;
   };
   
   this.button_CSS = function(x){
       $("input[name^='title']").prop("class","menu");
       x.prop("class","menu_down");
   };
   
   this.clear = function(){
       data = '';
   };
};

myapp.Presenter = function(){
    var model = null;
    this.init = function(){
        model=new myapp.Model();
        model.div_init("setting");
    };
    this.edit = function(x,y){
        if (x)
    	    model.edit(x,y,true,'1');
    	else
    	    model.edit(model.reNum(),'',false,null);
    };
    
    this.del = function(){
        var data='';
        for(var i = 0 ; i < $("input[name^='tablestodel']").length;i++)
        {
            if($("input[name^='tablestodel']").eq(i).prop("checked"))
                data+=$("input[name^='tablestodel']").eq(i).val()+',';
        }
        if (data == '')
        {
            alert("Please choose anyone!!");
            return;
    	}
    	model.getData($("#check_button").val(),'del',data);
   	model.reset_page();
    };
    
    this.option = function(x,y,d){
        if (y)
            model.getData(x,y,d);
        else
            model.getData(x,'option');
    };
    this.build = function(x){
    	model.build(x);
    };
    
    this.button = function(x){
        model.button_CSS(x);
    };
    
    this.getModel = function (){
        return model;
    };
};

myapp.view={
    $button_save: null,
    $button_option: null,
    $list: null,
    $check_del: null,
    presenter:null,
    init : function(){
   	this.presenter = new myapp.Presenter();
   	this.$button_add = $("#add");
   	this.$button_option = $("input[name^='title']");
   	this.$list = $("#list");
   	this.$check_del = $("#check_button");
   	this.presenter.init();
   	this.bindEvents();
   	$("input[name^='title']").eq(0).trigger("click");
    },
    bindEvents:function(){
        var view = this;
        var presenter = this.presenter;
        
        this.$check_del.click(function(){
            if ($(this).prop("checked"))
                $("input[name^='tablestodel']").prop("checked",true);
            else
                $("input[name^='tablestodel']").prop("checked",false);
        });
        
        this.$button_add.click(function(){
   	    myapp.view.presenter.edit();
            $( "#setting" ).dialog( "open" );
        });
        
        this.$button_option.click(function(){
            presenter.option($(this).val(),'');
            setTimeout(function(){
   	        $( "#list" ).html(presenter.getModel().build(presenter.getModel().sendData()));
   	    },500);
   	    presenter.getModel().clear();
   	    presenter.button($(this));
        });
    }
};



$(function(){
    myapp.view.init();
});

