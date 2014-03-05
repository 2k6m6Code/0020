var myapp={};

myapp.Model = function(){
   
   this.query = function(op_file){
   	$("#query").attr('disabled', true);
  	$.get('fqdn_import.pl',{type:op_file},function(request){
  	    $("#list").html(request);
  	    $("#query").attr('disabled', false);
  	});
   };
   
   this.goback = function (){
       window.opener.location.replace('host.cgi?type=fqdn');
       window.close();
   };
};

myapp.Presenter = function(){
    var model = null;
    this.init = function(){
        model=new myapp.Model();
        model.query();
    };
    
    this.query = function(op_file){
        model.query(op_file);
    };
    
    this.goback = function(op_file){
        model.goback();
    };
    
};

myapp.view={
    $button_add: null,
    $input_checkbox: null,
    presenter:null,
    init : function(){
   	this.presenter = new myapp.Presenter();
   	this.$button_add = $("#query");
   	this.presenter.init();
   	this.bindEvents();
    },
    bindEvents:function(){
        var view = this;
        var presenter = this.presenter;
        
        this.$button_add.click(function(){
            var option = new Array();
            var box = $("input[type='checkbox']");
            for (x=0;x < box.length;x++)
                if(box.eq(x).prop('checked'))
                    option.push(box.eq(x).val());
            presenter.query(option.join());
            presenter.goback();
        });
    }
};



$(function(){
    myapp.view.init();
});

