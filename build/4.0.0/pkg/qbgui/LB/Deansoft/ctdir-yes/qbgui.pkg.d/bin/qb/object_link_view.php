<?php
class View{

    private $_var = array();
    
    public function __set($name,$value){
        $this->_var[$name] = $value;
    }
    
    public function __get($name){
         return isset($this->_var[$name]) ? $this->_var[$name] : null;
    }
    
    public function display($name){
        include $name;
    }
    
    public function show_data(){
        $xml .='<div style="width:100%;"><table width="100%" border="1">';
        $xml .='<tr bgcolor="#332211"><td style="width:30%;">Link ID</td><td style="width:30%">Link Name</td>';
        $xml .='<td style="width:20%">Edit</td><td style="width:20%"><a href="javascript:myapp.view.presenter.del()"><img border="0" title="Delete Selected Links" src="image/del.gif"></a><input id="check_button" type="checkbox" title="select or deselect all items"></td></tr>';
        $xml .='</table></div><table id="list" width="100%" border="1"></table>';
        
        return $xml;
    }
    
    public function show_select(){
        foreach($this->newstitle as $val)
        {
            $xml .='<option value='.$val.'>'.$val.'</option>';
        }
        return $xml;
    }
}
?>
