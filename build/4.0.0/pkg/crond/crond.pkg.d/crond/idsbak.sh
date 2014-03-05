#! /bin/sh

unalias cp

CHK_FLAG="TRUE"

COUNT=0;

while [ "$CHK_FLAG" != "FALSE" ]
do
    if [ -f /mnt/$COUNT.tgz ];
    then
        COUNT=$(($COUNT+1))
        VAL=$COUNT    
    else
        if [ $COUNT = 0 ];
        then
            VAL=0
        fi 
        CHK_FLAG="FALSE" 
    fi

done

cd /var/log/snort

free >& mem

tar zcvf $VAL.tgz alert 

mv $VAL.tgz /mnt
sync

#cp -f /dev/null /var/log/snort/alert
#cp -f /dev/null /var/log/snort/scan.log




