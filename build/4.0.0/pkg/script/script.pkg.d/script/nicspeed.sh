#!/bin/bash
#set -x

ACTIVEBASICXML=/usr/local/apache/active/basic.xml
ACTIVEZONEXML=/usr/local/apache/active/zonecfg.xml
ETHTOOL="/sbin/ethtool"

if [ -f $ETHTOOL ];then

AllNic_WAN=`grep nic_speed $ACTIVEBASICXML|sed -e "s/  <isp.*nic=\"//"|sed -e "s/\".*//"`
AllNic_LAN=`grep nic_speed $ACTIVEZONEXML|sed -e "s/  <nat.*nic=\"//"|sed -e "s/\".*//"|grep -v ra`

for nicinfo in $AllNic_WAN
do
  case "$nicinfo" in ppp*) nicinfo=`grep nic=\"$nicinfo\" $ACTIVEBASICXML|sed -e "s/  <isp.*pppoeportdev=\"//"|sed -e "s/\".*//"`;; esac
  chk3g=`echo $nicinfo|grep -c "ttyUSB"`
  if [ $chk3g = '0' ];then
  NIC_Speed=`grep nic=\"$nicinfo\" $ACTIVEBASICXML|grep nic_speed|sed -e "s/  <isp.*nic_speed=\"//"|sed -e "s/\".*//"|head -n 1`
  case "$NIC_Speed" in
        Auto)
            chk=`$ETHTOOL $nicinfo|grep -c "Auto-negotiation: on"`
            if [ $chk = '0' ];then
            $ETHTOOL -s $nicinfo autoneg on
            fi
           ;;
       1000F)
            $ETHTOOL -s $nicinfo speed 1000 duplex full autoneg off
           ;;
        100F)
            $ETHTOOL -s $nicinfo speed 100 duplex full autoneg off
           ;;
        100H)
            $ETHTOOL -s $nicinfo speed 100 duplex half autoneg off
           ;;
         10F)
            $ETHTOOL -s $nicinfo speed 10 duplex full autoneg off
           ;;
         10H)
            $ETHTOOL -s $nicinfo speed 10 duplex half autoneg off
           ;;
           *)
           echo "Undefined NIC Speed!!!!" >>/mnt/log/link.log
           ;;
   esac
   fi
done

for nicinfo in $AllNic_LAN
do
  NIC_Speed=`grep nic=\"$nicinfo\" $ACTIVEZONEXML|grep nic_speed|sed -e "s/  <nat.*nic_speed=\"//"|sed -e "s/\".*//"|head -n 1`
  case "$NIC_Speed" in
        Auto)
            chk=`$ETHTOOL $nicinfo|grep -c "Auto-negotiation: on"`
            if [ $chk = '0' ];then
            $ETHTOOL -s $nicinfo autoneg on
            fi
           ;;
       1000F)
            $ETHTOOL -s $nicinfo speed 1000 duplex full autoneg off
           ;;
        100F)
            $ETHTOOL -s $nicinfo speed 100 duplex full autoneg off
           ;;
        100H)
            $ETHTOOL -s $nicinfo speed 100 duplex half autoneg off
           ;;
         10F)
            $ETHTOOL -s $nicinfo speed 10 duplex full autoneg off
           ;;
         10H)
            $ETHTOOL -s $nicinfo speed 10 duplex half autoneg off
           ;;
           *)
           echo "Undefined NIC Speed!!!!" >>/mnt/log/link.log
           ;;
   esac
done
fi
