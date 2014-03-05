#!/bin/bash

# QBALANCE Restore Configuration Service
# Argument and Parameter Definition
#set -x
TMP_UPLOAD_FILE="/tmp/tmpupg/upload.tmp"
FTP_CFGFILE="upload.tmp"
RES_LOCAL_DIR=/var/res
STR=$1
IMPORT_CFG_NAME=`echo "$STR" | awk -F',' '{print $1}'`
CHECK=`echo $STR | awk -F',' '{print $2}'`
if [ -n "$CHECK" ] ; then
    IMPORT_CFG_DIR=/mnt/qb/conf/cms/$CHECK/$IMPORT_CFG_NAME
else
    IMPORT_CFG_DIR=/mnt/qb/conf/set/$IMPORT_CFG_NAME
fi

DIAGNOSE=/var/log/diagnose.log

 

unalias cp
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

echo $(date -R) "Start uploading config pack" | tee -a $DIAGNOSE

#=============================================
# Step 1: recreate $RES_LOCAL_DIR
rm -rf $RES_LOCAL_DIR
mkdir -p $RES_LOCAL_DIR 

mv $TMP_UPLOAD_FILE  $RES_LOCAL_DIR 

cd $RES_LOCAL_DIR

#=============================================
# Step 2: untar Config pack
tar zxvf $FTP_CFGFILE >& /dev/null 

last_status=$?
if [[ ${last_status} != '0' ]]
then
    rm -rf ${RES_LOCAL_DIR} >& /dev/null
    echo $(date -R) "ERROR: Fail to extract config pack" | tee -a $DIAGNOSE
    echo "Please Try again !!" | tee -a $DIAGNOSE
    exit ${last_status}
else
    echo $(date -R) "SUCCESS: Extracting config package successfully" | tee -a $DIAGNOSE
fi


#=============================================
# Step 3: check if this is valid xml package
if [ ! -f basic.xml ]
then
    rm -rf ${RES_LOCAL_DIR} >& /dev/null
    echo $(date -R) "ERROR: Not a valid Config Set" | tee -a $DIAGNOSE
    echo "Please try to upload again" | tee -a $DIAGNOSE
    exit ${last_status}
else
    echo $(date -R) "SUCCESS: Validating config package successfully" | tee -a $DIAGNOSE
fi


#=============================================
# Step 4: remove downloaded Config Pack and remove any CVS directory if any exists
rm -f  $FTP_CFGFILE >& /dev/null 
rm -rf $(find . -name CVS)  


#=============================================
# Step 5: recreate $IMPORT_CFG_DIR
rm -rf $IMPORT_CFG_DIR
mkdir -p $IMPORT_CFG_DIR 


#=============================================
# Step 6: copy imported and untared xmls into $IMPORT_CFG_DIR
cp -rf *  $IMPORT_CFG_DIR >& /dev/null

last_status=$?
if [[ ${last_status} != '0' ]]
then
    echo $(date -R) "ERROR: Fail to extract config pack" | tee -a $DIAGNOSE
    rm -rf ${IMPORT_CFG__DIR} >& /dev/null
    rm -rf ${RES_LOCAL_DIR} >& /dev/null
    exit ${last_status}
else
    echo $(date -R) "SUCCESS: Creating config set $IMPORT_CFG_NAME successfully" | tee -a $DIAGNOSE
fi

sync
sync
sync

#=============================================
#last modified by Murphy : 2003.04.02 
# Step 7: Remove /var/res
#rm -rf ${RES_LOCAL_DIR} >& /dev/null

