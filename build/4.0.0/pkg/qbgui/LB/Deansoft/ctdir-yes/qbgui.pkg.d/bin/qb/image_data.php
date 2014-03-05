<?php
$time = $_GET[option];
//$time = "20131007";
exec("/bin/cat /mnt/tclog/total_$time",$traffic);

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
           $low=$go->input($time[1],$name[1]);
           $boxbig[$name[0]][0].=$low.",";
       }
    }
    
}
foreach ($boxbig as $key => $value)
{
    if ($key != '' && $value != '')
        $data.=$key."-:".$value[0].":";
}

//echo print_r($boxbig);
echo $go->debug($data);
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
