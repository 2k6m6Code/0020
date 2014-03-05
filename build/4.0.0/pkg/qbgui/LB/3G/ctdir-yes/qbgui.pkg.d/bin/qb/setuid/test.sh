#set -x
QB_HOME_DIR=/opt/qb
QBREG_FILE=$QB_HOME_DIR/registry
MAXISP=$(awk "/^MAXISP/ {print \$2}"  $QBREG_FILE)
ACTIVEBASICXML=/usr/local/apache/active/basic.xml
#random=$(( $RANDOM % $MAXISP ))
echo $(date) "QB Link check...">/mnt/log/bootlog
for (( random=0; random<=$MAXISP; random=random+1 ))
do

 mpvgw=`grep nic=\"mpv$random\" $ACTIVEBASICXML|sed -e "s/  <isp.*gateway=\"//"|sed -e "s/\".*//"`
 if [ "$mpvgw" != "" ];then
 ping $mpvgw -c 1
 pingresult=$?
  if [ $pingresult = '1' ] ;then
  echo "Link is down!"
  continue
  fi
  /sbin/wget http://$mpvgw:4000/clean/cleandiagnose.htm --connect-timeout=1 --tries=1 -O /tmp/chk_file
  testresult=$?
  if [ $testresult = '1' ] ;then
  echo "Find a strange link:mpv$random" >>/mnt/log/link.log
  /sbin/ifconfig mpv$random down
  #/usr/local/sbin/iptables -D FORWARD -p tcp --tcp-flags SYN,RST SYN -m gw --gw $mpvgw -j TCPMSS --set-mss 1550
  #/usr/local/sbin/iptables -A FORWARD -p tcp --tcp-flags SYN,RST SYN -m gw --gw $mpvgw -j TCPMSS --set-mss 1550
  sync #20130419 To prevent DOM/CF become readonly
  fi
 fi

done
