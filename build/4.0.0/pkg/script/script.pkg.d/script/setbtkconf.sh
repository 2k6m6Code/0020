#!/bin/bash

LEVEL=$1
MEASURETIME=$2
BTKCONFPATH=/opt/qb/bin/script/avg_mure.ini
BTKQBCONFPATH=/usr/local/apache/qbconf/avg_mure.ini

case "$LEVEL" in
   1)
     MICRO_ADJUST=1
     HISTORY_REVIEW=1
   ;;
   2)
     MICRO_ADJUST=1
     HISTORY_REVIEW=0
   ;;
   3)
     MICRO_ADJUST=0
     HISTORY_REVIEW=0
   ;;
esac
sed -e '{
        s/MICRO_ADJUST=.*/MICRO_ADJUST='$MICRO_ADJUST'/g
        s/HISTORY_REVIEW=.*/HISTORY_REVIEW='$HISTORY_REVIEW'/g
        s/INTER_MSASURE_TIME=.*/INTER_MSASURE_TIME='$MEASURETIME'/g
        }' $BTKCONFPATH > $BTKQBCONFPATH
#if [ "$?" != "1" ];then
#   /bin/chmod 777 $TEMPXML
#   /bin/cp -af $TEMPXML $BASICXML
#fi

