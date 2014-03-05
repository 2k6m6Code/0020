#! /bin/sh
#set -x
AP_device=$1

 	    # Signal
 	    #
            #signal=`echo -e "at+CSQ\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^+CSQ|awk '{print $2}'|sed -e "s/,99//"`
            signal=`catty -r 0 -d /dev/$AP_device -b 460800 -w "AT+CSQ\r\n"|grep ^+CSQ|awk '{print $2}'|sed -e "s/,99//"`
            echo Signal:$signal > /tmp/MC8090_3G_info.$AP_device
            
            if [ "$signal" = "" ];then
            #echo -e "at+CSQ\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^+CSQ|awk '{print $2}'|sed -e "s/,99//"
            signal=`catty -r 0 -d /dev/$AP_device -b 460800 -w "AT+CSQ\r\n"|grep ^+CSQ|awk '{print $2}'|sed -e "s/,99//"`
            echo Signal:$signal > /tmp/MC8090_3G_info.$AP_device
            fi
            
            # ISP
            #
            #echo -e "at+COPS?\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^+COPS|sed -e "s/^+COPS.*,\"//"|sed -e "s/\".*//"|sed -e "s/^+COPS: //"
            #catty -r 0 -d /dev/$AP_device -b 460800 -w "AT+COPS?\r\n"|grep ^+COPS|sed -e "s/^+COPS.*,\"//"|sed -e "s/\".*//"|sed -e "s/^+COPS: //"
            isp=`catty -r 0 -d /dev/$AP_device -b 460800 -w "AT+COPS?\r\n" |grep -v "AT+COPS" |grep "COPS" |awk -F',' '{print $3}'`
            echo ISP:$isp >> /tmp/MC8090_3G_info.$AP_device
            
            # Cell ID
            #
            #echo -e "at\$cellinfo3G=1\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep CELLINFO3G|awk -F "," '{print $11}'
            #catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$cellinfo3G=1\r\n"|grep CELLINFO3G|awk -F "," '{print $11}'
            cell=`catty -r 0 -d /dev/$AP_device -b 460800 -w "AT\!GSMINFO?\r\n" |grep "Cell ID" |awk '{print $3}'`
            echo Cell_ID:$cell >> /tmp/MC8090_3G_info.$AP_device
            
#      band )
            #echo -e "at\$QAB\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^\$QAB|sed -e "s/^\$QAB.*:\"//"|sed -e "s/\"//"
            #catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$QAB\r\n"|grep ^\$QAB|sed -e "s/^\$QAB.*:\"//"|sed -e "s/\"//"
            band=`catty -r 0 -d /dev/$AP_device -b 460800 -w "AT\!GSTATUS?\r\n" |grep "WCDMA band" |awk '{print $3}'`
            echo Band:$band >> /tmp/MC8090_3G_info.$AP_device
            #;;
#      txrx )
            #catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$QTTR=2\r\n"|grep ^\$QTTR|sed -e "s/^\$QTTR://"|awk -F "," '{print $1 "','" $2}'
            #;;
#        tx )
            #echo -e "at\$QTTR=2\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^\$QTTR|sed -e "s/^\$QTTR://"|awk -F "," '{print $1}'
#            catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$QTTR=2\r\n"|grep ^\$QTTR|sed -e "s/^\$QTTR://"|awk -F "," '{print $1}'
#            ;;
#        rx )
            #echo -e "at\$QTTR=2\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^\$QTTR|awk -F "," '{print $2}'
#            catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$QTTR=2\r\n"|grep ^\$QTTR|awk -F "," '{print $2}'
#            ;;
      #get Ec/Io and RSCP
#  eciorscp )
            #echo -e "at\$cellinfo3G=1\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep CELLINFO3G|awk -F "," '{print $11}'
#            catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$cellinfo3G=2\r\n"|grep CELLINFO3G|awk -F "," '{print $3 "','" $4}'
