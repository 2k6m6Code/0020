#!/bin/bash
#Q-Balancer Upgrade Procedure 

#UPG_DIR=/var/upg
UPG_DIR=/tmp/tmpupg/upg
BAK_DIR=/mnt/bak
PKG_DIR=/mnt
CONF_DIR=/mnt/qb/conf
SYSCONF_DIR=/mnt/conf
DIAGNOSE=/var/log/diagnose.log

unalias cp

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin

export PATH

#=====================================================================================
# 1. Check if do_upgrade exists in UPG_DIR
if [ -f  $UPG_DIR/do_upgrade ]
then
    echo  "Checking components for upgrading  packages OK" | tee -a $DIAGNOSE 
else
    echo  "Phrase 1 Error: do_upgrade Not Ready" | tee -a $DIAGNOSE
    echo  "Please get Upgrade Package Again" | tee -a $DIAGNOSE
    exit 0 
fi


#=====================================================================================
# 2. Launch function upgrade procedure
cd $UPG_DIR
./do_upgrade
last_status=$?
if [[ $last_status != '0' ]]
then
    echo "Phrase 2 ERROR: Fail to upgrade Function Packages..." | tee -a $DIAGNOSE

    case $last_status in
             2 )
                 echo "Phrase 3 ERROR: Fail to get Hardware Information..." | tee -a $DIAGNOSE
                     ;; #  
             3 )
                 echo "Phrase 3 ERROR: Warranty expired..." | tee -a $DIAGNOSE
                     ;; #
             4 )
                 echo "Phrase 3 ERROR: Can't get the serial number..." | tee -a $DIAGNOSE
                     ;; #
             5 )
                 echo "Phrase 3 ERROR: Can't get the shipment date..." | tee -a $DIAGNOSE
                     ;; #
             esac
    echo "   Please contact the distributor!!!" | tee -a $DIAGNOSE
    exit $last_status
else
    echo "Packages Upgraded Successfully !" | tee -a $DIAGNOSE
    rm -rf $UPG_DIR/*.pkg
    rm -rf $UPG_DIR/linux
    rm -rf $UPG_DIR/*db
fi


#=====================================================================================
# 3. Check if it is Ready to Upgrade XML Config. Files in /mnt/qb/conf/set/*
if [ -f $UPG_DIR/xmlupgrade.pl ]
then
    echo "Functions to upgrade XML Ready" | tee -a $DIAGNOSE
else
    echo "Phrase 3 Error: xmlupgrade Not Ready !!" | tee -a $DIAGNOSE
    echo "Get Upgrade Package Again" | tee -a $DIAGNOSE
    exit 0;
fi


#=====================================================================================
# 4.  backup all conifg. set to  BAK_DIR 
if [ ! -d $BAK_DIR ]
then
    mkdir -p $BAK_DIR 
fi

cp -rf  $CONF_DIR/set/boot   $BAK_DIR 

last_status=$?
if [[ $last_status != '0' ]]
then
    #echo "Phrase 4 ERROR: Fail to Backup Boot Configuration !!!" | tee -a $DIAGNOSE
    echo "Retring ............................................." | tee -a $DIAGNOSE

             echo $(date) "CF full when upgrading firmware!!!" >>/mnt/error/issue.log
             du -h /mnt >>/mnt/error/issue.log
             ls -al /mnt >>/mnt/error/issue.log
             cat /dev/null >/mnt/log/runway.log
             cat /dev/null >/mnt/log/alert.log
             rm -f /mnt/log/bootlog
             rm -f /mnt/log/daemon.log
             rm -f /mnt/log/disk.log
             rm -f /mnt/log/panic.log
             rm -f /mnt/log/process.log
             rm -f /mnt/log/qbalance.log

     rm -rf  $CONF_DIR/set/boot
     cp -rf  $CONF_DIR/set/boot   $BAK_DIR 
     last_status=$?
     if [[ $last_status != '0' ]]
     then
         #echo "Phrase 4-1 ERROR: Fail to Backup Boot Configuration again!!!" | tee -a $DIAGNOSE
         exit $last_status
     else
         echo "Configuration Sets Backedup Successfully !!" | tee -a $DIAGNOSE
     fi
else
    echo "Configuration Sets Backedup Successfully !!" | tee -a $DIAGNOSE
fi


#=====================================================================================
# 5. Launch XML upgrade process
./xmlupgrade.pl
last_status=$?
if [[ $last_status != '0' ]]
then
    echo "Phrase 5 ERROR: Fail to Upgrade Configuration Sets" | tee -a $DIAGNOSE
    echo "Recover  previous Version ..." | tee -a $DIAGNOSE
    cp -f $BAK_DIR/registry $SYSCONF_DIR/registry 
    cp -f $BAK_DIR/*.pkg $BAK_DIR/linux $PKG_DIR
    cp -R -f  $BAK_DIR/set  $CONF_DIR
    last_status=$?
    if [[ $last_status != '0' ]]
    then
        echo "Phrase 6 ERROR: Fail to Recover Original Configuration Sets" | tee -a $DIAGNOSE
        exit $last_status
    else
        echo "Original Configuration Sets Recovered Completely !!" | tee -a $DIAGNOSE
    fi
    sync #20130419 To prevent DOM/CF become readonly
    exit $last_status
else
    echo "Configuration Sets Upgraded OK!" | tee -a $DIAGNOSE
    echo "Please restart Q-Balancer !" | tee -a $DIAGNOSE
    sync #20130419 To prevent DOM/CF become readonly
fi

reEnableHA=`grep "ENABLEHA" /opt/qb/registry|sed -e "s/ENABLEHA //"|sed 's/\n//g'`
if [[ $reEnableHA == '1' ]]
then
	/usr/local/apache/qb/setuid/enableha.pl
fi
