#!/bin/bash
# QBALANCE Remote Upgrade Service
# Argument and Parameter Definition
#set -x
TMP_UPLOAD_FILE=/tmp/tmpupg/upload.tmp

# TMPUPGFILE will be located in /mnt/bak so we will face the 8.3 filename restriction
# after mcrypt this, the filename will be changed to $TMPUPGFILE.dc, which is what we shoule take care
TMPUPGFILE=upgrade 

UPGFILENAME=upgrade.tgz
#UPG_LOCAL_DIR=/var/upg
UPG_LOCAL_DIR=/tmp/tmpupg/upg
BAK_LOCAL_DIR=/mnt/bak
LOG_LOCAL_DIR=/mnt/log
DIAGNOSE=/var/log/diagnose.log
KEYFILE=/mnt/conf/qbkey

unalias cp

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

#=========================================================================
# 1. Refresh old content in UPG_LOCAL_DIR
#========================================================================
echo "Processing Upgrade Service .... " | tee  -a $DIAGNOSE

rm -rf $UPG_LOCAL_DIR
mkdir -p $UPG_LOCAL_DIR 
rm -rf $BAK_LOCAL_DIR/*   #Brian 20080918 To prevent CF/DOM become full and cause upgrade fail.
ORG_VER=`grep "VERSION DETAIL" /mnt/conf/pkginfo|awk -F ":" '{print $2}'|sed 's/\n//g'`
echo $(date -R) "Upgrade firmware from $ORG_VER ." >>$LOG_LOCAL_DIR/user.log
# !! Important,  for the sake of preventing ramdisk from being overflow
#    we have to move the uploaded upgrade package to DOM
mv -f $TMP_UPLOAD_FILE  $BAK_LOCAL_DIR/$TMPUPGFILE
sync

cd $BAK_LOCAL_DIR

#=========================================================================
# 2. Decrypt the upgrade files in $BAK_LOCAL_DIR
#=========================================================================

#========================================================================
echo "Phase 1 : Trying free-license decryption ..."
mcrypt -d ${TMPUPGFILE} -k 42084021
decrypt_result=$?
if [[ $decrypt_result != '0' ]]
then
    #Brian 20131213 If upgrade fail,delete the logs.
    mv $LOG_LOCAL_DIR/user.log /tmp/
    rm -rf $LOG_LOCAL_DIR/*
    rm -f /mnt/Fail_*
    mv -f /tmp/user.log $LOG_LOCAL_DIR/

    #Try again
    mcrypt -d ${TMPUPGFILE} -k 42084021
    decrypt_result=$?
    if [[ $decrypt_result != '0' ]]
    then
         echo $(date -R) "free-license decryption fail: Fail to process free-license decryption" | tee -a $DIAGNOSE
    
         #==============================================================
         echo "Phase 2 : Trying registered-license decryption ..."
         mcrypt -d ${TMPUPGFILE} -f $KEYFILE
         decrypt_result=$?
         if [[ $decrypt_result != '0' ]]
         then
             echo $(date -R) "registered-license decryption fail: Fail to process registered-license decryption" | tee -a $DIAGNOSE
             exit $decrypt_result
         fi
     fi

fi
rm -rf $TMPUPGFILE 
mv -f ${TMPUPGFILE}.dc  $BAK_LOCAL_DIR/$UPGFILENAME
sync

#=========================================================================
# 3. Extracting $UPGFILENAME 
#========================================================================
tar zxfC $BAK_LOCAL_DIR/$UPGFILENAME $UPG_LOCAL_DIR  >& /dev/null

last_status=$?
if [[ $last_status != '0' ]]
then
    rm -rf $UPG_LOCAL_DIR
    echo $(date -R) "ERROR: Fail to extract upgrade package" | tee -a $DIAGNOSE
    exit $last_status
else
    echo $(date -R) "Upgrade package extracted OK!" | tee -a $DIAGNOSE
fi

# if we do not want to keep the upgrade file , just remove the leading '#' in the next line
#rm -f $UPGFILENAME 

sync


#=========================================================================
# 4. Processing md5 checksum 
#========================================================================
cd $UPG_LOCAL_DIR

md5sum -c --status checksum.md5 

last_status=$?
if [[ $last_status != '0' ]]
then
    rm -rf $UPG_LOCAL_DIR
    echo $(date -R) "ERROR: Upgrade Packages Checksum Error." | tee -a $DIAGNOSE
    exit $last_status
else
    echo $(date -R) "Upgrade Packages Checksum OK!" | tee -a $DIAGNOSE
fi

#=========================================================================
# 5. #20070425 Brian Check CPU PLATFORM 
#========================================================================
QBREG_FILE_TMP="/tmp/function/conf/registry"
QBREG_FILE="/opt/qb/registry"
C_TYPE="PLATFORM"
ENABLEVM=$(awk  "/ENABLEVM/ { print \$2 }" $QBREG_FILE)
mkdir /tmp/function
if [ "$ENABLEVM" = "1" ]
then
    cp -a $UPG_LOCAL_DIR/function.pkg /tmp/function.pkg.nc
    /usr/bin/mcrypt -d /tmp/function.pkg.nc -k pkg2k6m6ej3zp4function >/dev/null 2>&1
    tar zxfC /tmp/function.pkg /tmp/function
else
    tar zxfC $UPG_LOCAL_DIR/function.pkg /tmp/function
fi

#tar zxfC $UPG_LOCAL_DIR/function.pkg /tmp/function
CPU_TYPE=$(awk  "/$C_TYPE/ { print \$2 }" $QBREG_FILE)
CPU_TYPE_TMP=$(awk  "/$C_TYPE/ { print \$2 }" $QBREG_FILE_TMP)
last_status=$?
if [[ $last_status != '0' ]]
then
    echo $(date -R) "ERROR: Check Function Package Error." | tee -a $DIAGNOSE
    exit $last_status
else
    echo $(date -R) "Check Function Package OK!" | tee -a $DIAGNOSE
    if [ $CPU_TYPE = $CPU_TYPE_TMP ]
    then
        echo $(date -R) "Check CPU Type OK!" | tee -a $DIAGNOSE
    else
        rm -rf $UPG_LOCAL_DIR
        echo $(date -R) "Check CPU Type Error!" | tee -a $DIAGNOSE
        exit 1
    fi
fi
#rm -rf /tmp/function

#=========================================================================
# 5.1 #20090710 Brian Check original version
#========================================================================
C_TYPE="VERSION"
VERSION_ORG=$(awk  "/$C_TYPE/ { print \$2 }" $QBREG_FILE)
VERSION_NEW=$(awk  "/$C_TYPE/ { print \$2 }" $QBREG_FILE_TMP)
last_status=$?
if [[ $last_status != '0' ]]
then
    echo $(date -R) "ERROR: Get New Version Detail Error." | tee -a $DIAGNOSE
    exit $last_status
else
    echo $(date -R) "Get New Version Detail OK!" | tee -a $DIAGNOSE
    if [ $VERSION_ORG = $VERSION_NEW ]
    then
        echo $(date -R) "Check Version Detail OK!" | tee -a $DIAGNOSE
    else
        rm -rf $UPG_LOCAL_DIR
        echo $(date -R) "Check Version Detail Error!" | tee -a $DIAGNOSE
        exit 1
    fi
fi
rm -rf /tmp/function

#=========================================================================
# 6. backup /mnt/*.pkg and linux to /mnt/bak
#========================================================================
#20090319 copy *.pkg to $BAK_LOCAL_DIR will waste disk space
#cp -f /mnt/*.pkg $BAK_LOCAL_DIR
cp -f /mnt/linux $BAK_LOCAL_DIR
cp -f /mnt/conf/registry $BAK_LOCAL_DIR

sync
sync
sync

echo  $(date -R) "Ready to Launch Upgrade Procedure !!! " | tee -a $DIAGNOSE

