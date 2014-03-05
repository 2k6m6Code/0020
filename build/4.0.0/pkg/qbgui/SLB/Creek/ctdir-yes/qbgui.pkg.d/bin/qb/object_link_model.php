<?php

class action_1 { 

    private $_name = null;

    public function getTitle(){
        $f = fopen('/usr/local/apache/qbconf/basic.xml','r');
        
        $titlelist = array();
        
        while( $data = fgets($f))
        {
    	    preg_match('/ispname=\"(.*?)\"/s',$data,$data2);
    	    $data3=str_replace('ispname=','',$data2[0]);
    	    if (str_replace('"','',$data3) != '')
    	    {
    	        $titlelist[] = str_replace('"','',$data3);
    	        if ($this->_name == null)
    	        {
    	            preg_match('/iid=\"(.*?)\"/s',$data,$data21);
    	            $data31=str_replace('iid=','',$data21[0]);
    	            $data31=str_replace('"','',$data31);
    	            $this->_name = $data31;
    	        }
    	    }
    	}
    	fclose( $f );
    	
    	return $titlelist;
    }
    
    public function getList(){
        $f = fopen('/usr/local/apache/qbconf/rtable.xml','r');
        
        $titlelist = array();
        
        while( $data = fgets($f))
        {
    	    preg_match('/table_num=\"(.*?)\"/s',$data,$data2);
    	    $data3=str_replace('table_num=','',$data2[0]);
    	    $data3=str_replace('"','',$data3);
    	    if ( $data3 < 100 && $data3 != 30 && $data3 != 'system' && $data3 != '')
    	    {
    	        preg_match('/isp_num=\"(.*?)\"/s',$data,$aa);
    	        $bb=str_replace('isp_num=','',$aa[0]);
    	        $bb=str_replace('"','',$bb);
    	        if ($this->_name != $bb)
    	            continue;
    	        preg_match('/note=\"(.*?)\"/s',$data,$data21);
    	        $data31=str_replace('note=','',$data21[0]);
    	        $data31=str_replace('"','',$data31);
    	        $titlelist[$data3] = $data31;
    	    }
	}
	fclose( $f );   
	
	return $titlelist;
    }
    
    public function debug_1(){
        return $this->_name;
    
    }

}

?>
