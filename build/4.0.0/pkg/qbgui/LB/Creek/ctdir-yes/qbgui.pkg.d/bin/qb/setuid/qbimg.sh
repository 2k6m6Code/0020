#!/bin/bash
# QBALANCE Remote Upgrade Service
# Argument and Parameter Definition
TMP_UPLOAD_FILE=/tmp/tmpupg/image.tmp
set -x
# TMPUPGFILE will be located in /mnt/bak so we will face the 8.3 filename restriction
# after mcrypt this, the filename will be changed to $TMPUPGFILE.dc, which is what we shoule take care
TMPUPGFILE=upgrade 

UPGFILENAME=upgrade.tgz
BAK_LOCAL_DIR=/tmp/tmpupg/bak
DIAGNOSE=/var/log/diagnose.log

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin

export PATH

#========================================================================
# motivation 1. because ramdisk is always not enough
#               so we want to use DOM space to store upgrade.tgz
#               we prepare /mnt/bak directory for this
# movitivation 2. we will also backup some pkg(s)  here
#========================================================================
if [ ! -d  $BAK_LOCAL_DIR ]
then
    mkdir -p $BAK_LOCAL_DIR 
fi

#========================================================================
# 0. Call /opt/qb/bin/script/qbmond.sh with the R_LEVERL option '0' to 
#    delete upnecessary log files to get enough space for downloading upgrade upg file
#========================================================================
echo "Warning !! This procedure will delete all log files ..." 
/opt/qb/bin/script/qbmon.sh 0

echo "Processing Upgrade Service .... " | tee  -a $DIAGNOSE
rm -rf $BAK_LOCAL_DIR\/*
#=========================================================================
# 1. Extracting Image file 
#========================================================================
echo "Phase 1 : Extracting Image file ..."
rm -rf /mnt/bak/*
tar zxfC $TMP_UPLOAD_FILE /mnt/bak/ >& /dev/null
last_status=$?
if [[ $last_status != '0' ]]
then
    rm -f $TMP_UPLOAD_FILE
    echo $(date) "ERROR: Fail to extract upgrade image package" | tee -a $DIAGNOSE
    rm -f /mnt/bak/*
    exit $last_status
else
    echo $(date) "Image package extracted OK!" | tee -a $DIAGNOSE
fi
sync
rm -f $TMP_UPLOAD_FILE

#=========================================================================
# 2. Decrypt the upgraded image file
#=========================================================================

# Get image file name.
  for i in /mnt/bak/*.100; do
  [ ! -f $i ] && continue
  TMPIMGFILE=$i
  done
  case "$TMPIMGFILE" in
        /mnt/bak/libimage.100)
                                     echo "Phase 2 : Trying decryption ..."
                                     echo $(date) "Decryption OK!" | tee -a $DIAGNOSE
                                     echo "Phase 3 : Relocate image file ..."
                                     echo $(date) "Relocate image file OK!" | tee -a $DIAGNOSE
                                     mv -f /mnt/bak/*.ifo /mnt/conf/
                                     echo  $(date) "Upgrade [ Software Image ] OK!" | tee -a $DIAGNOSE
                                     echo  "$(date) Upgrade [ Software Image ] OK!" >/var/log/runway.log
                                     #echo  $(date) "Please reboot QB!!!"
                                     sync
                                     ;;
        /mnt/bak/fsimage.100)
                                     echo "Phase 2 : Trying decryption ..."
                                     mv /mnt/bak/fsimage.100 $BAK_LOCAL_DIR/image.gz.nc
                                     mcrypt $BAK_LOCAL_DIR/image.gz.nc -u -d -k qbfsimage~!
                                     decrypt_result=$?
                                     if [[ $decrypt_result != '0' ]]
                                     then
                                          echo $(date) "Decryption fail: Fail to process decryption" | tee -a $DIAGNOSE
                                          rm -rf $BAK_LOCAL_DIR/image.gz.nc
                                          exit $decrypt_result
                                     else
                                          echo $(date) "Decryption OK!" | tee -a $DIAGNOSE
                                     fi
                                     echo "Phase 3 : Relocate image file ..."
                                     mv -f /mnt/bak/*.ifo /mnt/conf/
                                     mv -f $BAK_LOCAL_DIR/image.gz /mnt/
                                     relocate_result=$?
                                     if [[ $relocate_result != '0' ]]
                                     then
                                           echo $(date) "Relocate image file fail: The CF space is not enough!!!" | tee -a $DIAGNOSE
                                           rm -rf $BAK_LOCAL_DIR/image.gz
                                           exit $relocate_result
                                      else
                                           sync
                                           echo $(date) "Relocate image file OK!" | tee -a $DIAGNOSE
                                      fi
                                     echo  $(date) "Upgrade [ Filesystem Image ] OK!" | tee -a $DIAGNOSE
                                     echo  "$(date) Upgrade [ Filesystem Image ] OK!" >/var/log/runway.log
                                     #echo  $(date) "Please reboot QB!!!"
                                     sync
                                     ;;
  esac                                      
exit 0
if [ $TMPIMGFILE = "$BAK_LOCAL_DIR/dom.100" ]
then
echo "Phase 2 : Trying decryption ..."
mv $BAK_LOCAL_DIR/dom.100 $BAK_LOCAL_DIR/dom
rm -f /mnt/*.dom
mcrypt $BAK_LOCAL_DIR/dom -d -u -k 42084021
decrypt_result=$?
if [[ $decrypt_result != '0' ]]
then
    echo $(date) "Decryption fail: Fail to process decryption" | tee -a $DIAGNOSE
    rm -rf $BAK_LOCAL_DIR/dom
    exit $decrypt_result
else
    echo $(date) "Decryption OK!" | tee -a $DIAGNOSE
fi
echo "Phase 3 : Relocate DOM file ..."
mv $BAK_LOCAL_DIR/dom.dc /mnt/upgrade.dom
relocate_result=$?
if [[ $relocate_result != '0' ]]
then
    echo $(date) "Relocate image file fail: Fail to process Relocation" | tee -a $DIAGNOSE
    rm -rf $BAK_LOCAL_DIR/dom
    exit $relocate_result
else
    echo $(date) "Relocate DOM file OK!" | tee -a $DIAGNOSE
fi
echo  $(date) ".....Upgrade DOM file OK! !!! .....Please reboot QB!!!" | tee -a $DIAGNOSE
sync
fi

