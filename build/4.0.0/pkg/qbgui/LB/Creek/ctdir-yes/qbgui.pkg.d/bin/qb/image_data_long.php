<?php
$time_1 = explode(":",$_GET[option]);
for($k=0;$k < $time_1[1]; $k++)
{
    $traffic = null;
    $data = $time_1[0] - (86400 * $k);
    $date_format = date('Y/m/d',$data);
    $tmp_data = explode("/",$date_format);
    
    $data_1 = $tmp_data[0].$tmp_data[1].$tmp_data[2];
    exec("/bin/cat /mnt/tclog/total_$data_1",$traffic);

    $go = new box();
    foreach ($traffic as $value)
    {
        if ($value)
    	{
            $input = explode(",",$value);
            $time = explode("-:",$input[0]);
            for ($i=1;$i<count($input);$i++)
       	    {   
           	$name = explode("-",$input[$i]);
           	if ($name[0] != '')
           	    $total[$name[0]]+=$name[1];
            }
    	}
    }
    foreach ($total as $key => $dd)
    {
        $low=$go->input($date_format,$dd);
        $boxbig[$key][0].=$low.",";
    }
}
//echo $go->debug($boxbig);
foreach ($boxbig as $key => $value)
{
    $data_2.=$key."-:".$value[0].":";
}
//echo print_r($boxbig);
echo $go->debug($data_2);
class box 
{
   function input ($box,$str)
   {
       //$tmp_box=$box.",".$str;
       $tmp_box=$str;
       return $tmp_box;
   }
      
   function debug($obj)
   {
       var_dump($obj);
   }
}
/*
class box 
{
   var $bigbox=array();
   function input ($box,$str)
   {
       $tmp_box[]=$box;
       $tmp_box[]=$str;
       return $tmp_box;
   }
      
   function debug($obj)
   {
       var_dump($obj);
   }
}*/
?>
