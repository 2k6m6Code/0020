#!/bin/bash
#set -x

ACTIVEBASICXML="/usr/local/apache/active/basic.xml"
Base_BW=32 #32Kbps
IspID=$1
Max_latency_user=$2

TargetIP=`grep iid=\"$IspID\" $ACTIVEBASICXML|sed -e "s/  <.*target=\"//"|sed -e "s/\".*//"|sed -e "s/\n//"`
Avg_Latency=0

#To get the Upper/Lower bound.
while test $Avg_Latency -lt $Max_latency_user
do
  if [ $Avg_Latency -lt $Max_latency_user ];then
  let Data_Size=$Base_BW*2000 #Bytes
  Last_Link_Speed=$Link_Speed
  Last_Min_Latency=$Min_Latency
  Last_Avg_Latency=$Avg_Latency
  Last_BW=$Base_BW
  BW_Result=`/sbin/bwping -b $Base_BW -s 1500  -v $Data_Size $TargetIP 2>/dev/null`
  Link_Speed=`echo $BW_Result|awk '{print $28}'`
  Min_Latency=`echo $BW_Result|awk '{print $32}'|awk '{FS="/"} {print $1}'`
  Max_Latency=`echo $BW_Result|awk '{print $32}'|awk '{FS="/"} {print $2}'`
  Avg_Latency=`echo $BW_Result|awk '{print $32}'|awk '{FS="/"} {print $3}'`
  #echo "Measure Result:Test_Speed= $Base_BW kbps; Link_Speed= $Link_Speed Kbps; Min_Latency= $Min_Latency ms; Max_Latency= $Max_Latency ms; Avg_Latency= $Avg_Latency ms"
  echo "ISP$IspID:Speed=$Link_Speed Kbps;Max_Latency=$Max_Latency ms;Avg_Latency=$Avg_Latency ms"
  let Base_BW=$Base_BW*2
  test $Link_Speed -eq 0 && break;
  fi
done

if [ $Last_Link_Speed ] && [ $Link_Speed ];then
MIN_test_BW=$Last_Link_Speed  #Lower bound
MAX_test_BW=$Link_Speed       #Max bound
subtract=11
while test $subtract -ge 10
do
  let test_BW=$MIN_test_BW+$MAX_test_BW
  let test_BW=$test_BW/2
  let Data_Size=$test_BW*2000 #Bytes
  Last_Link_Speed=$Link_Speed
  Last_Min_Latency=$Min_Latency
  Last_Avg_Latency=$Avg_Latency
  BW_Result=`/sbin/bwping -b $test_BW -s 1500  -v $Data_Size $TargetIP 2>/dev/null`
  Link_Speed=`echo $BW_Result|awk '{print $28}'`
  Min_Latency=`echo $BW_Result|awk '{print $32}'|awk '{FS="/"} {print $1}'`
  Max_Latency=`echo $BW_Result|awk '{print $32}'|awk '{FS="/"} {print $2}'`
  Avg_Latency=`echo $BW_Result|awk '{print $32}'|awk '{FS="/"} {print $3}'`
  #echo "Measure Result:Test_Speed= $test_BW kbps; Link_Speed= $Link_Speed Kbps; Min_Latency= $Min_Latency ms; Max_Latency= $Max_Latency ms; Avg_Latency= $Avg_Latency ms"
  echo "ISP$IspID:Speed=$Link_Speed Kbps;Max_Latency=$Max_Latency ms;Avg_Latency=$Avg_Latency ms"
  if [ $Avg_Latency -gt $Max_latency_user ];then
  MAX_test_BW=$Link_Speed
  else
  MIN_test_BW=$Link_Speed
  fi
  let subtract=$MAX_test_BW-$MIN_test_BW
  let BW_subtract=$Last_Link_Speed-$Link_Speed
  test $BW_subtract -le 0 && let BW_subtract=-$BW_subtract
  test $BW_subtract -le 3 && break; #If the value of user define latency is too big
done
fi
echo "Optimal:Speed=$Link_Speed Kbps;Max_Latency=$Max_Latency ms;Avg_Latency=$Avg_Latency ms"
echo "------------------------------------------------------------------------------------------"
