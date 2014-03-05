<?php

class Controller{

    private $_action = 'index';
    
    private $_model = null;
    
    private $_view = null;
    
    public function __construct(){
    	if (isset($_GET['action']))
    	{
    	    $action = strtolower($_GET['action']);
    	    if (method_exists($this,$action))
    	        $this->_action = $action;
    	}
    	$this->init();	
    	call_user_func(array($this,$this->_action));
    }
    
    public function init(){
        require_once "object_link_model.php";
        $this->_model = new action_1();
        
        require_once "object_link_view.php";
        $this->_view = new View();
    }
    
    public function index(){
	$this->_view->newstitle = $this->_model->getTitle();
	$this->_view->newslist = $this->_model->getList();
	$this->_view->display('text.t');
    }
    
    public function viewflow_auth(){
	$this->_view->display('viewflow_auth.htm');
    }
    
    public function host_import(){
	$this->_view->display('host_import.htm');
    }
}

?>
