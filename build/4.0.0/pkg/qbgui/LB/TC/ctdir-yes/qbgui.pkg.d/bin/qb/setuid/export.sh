#! /bin/bash
# backup configuration shell script

CFGSETNAME_TO_BACKUP=$1
CFGSETNAME_TO_SAVEAS=$2

CUR_CONF_FILE=/usr/local/apache/active
EXPORT_CFG_DIR=/mnt/qb/conf/set

BAK_LOCAL_DIR=/tmp/bak
BAK_LOCAL_FILE=qbconf.bak


QB_EXPORT_DIR=/usr/local/apache/qb/export

DIAGNOSE=/var/log/diagnose.log

unalias cp
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

chmod 777 /tmp

if [ ! -d  $BAK_LOCAL_DIR ]
then
    echo "Backup configuration files ... "   
    mkdir -p $BAK_LOCAL_DIR 
fi


if [ -f $BAK_LOCAL_DIR/$BAK_LOCAL_FILE ]
then
    rm -f $BAK_LOCAL_DIR/$BAK_LOCAL_FILE 
fi


echo $(date -R) "Packaging the configuration files ..."

case "$CFGSETNAME_TO_BACKUP" in
active)  
    if [ -d  $CUR_CONF_FILE ]
    then
        cd $CUR_CONF_FILE
        rm -rf $(find . -name CVS)
        
        tar zcvf $BAK_LOCAL_FILE * >& /dev/null
        last_status=$?
        if [[ ${last_status} != '0' ]]
        then
            echo $(date -R) "ERROR: Fail to pack configuration files." | tee -a $DIAGNOSE
            exit ${last_status} 
        fi
        
        mv -f $BAK_LOCAL_FILE  $CFGSETNAME_TO_SAVEAS
        mv -f $CFGSETNAME_TO_SAVEAS $BAK_LOCAL_DIR/
    else
        echo $(date -R) "ERROR: Configuration Set NOT Found" | tee -a $DIAGNOSE
        exit 1
    fi
    ;;
*)  
    if [ -d $EXPORT_CFG_DIR/$CFGSETNAME_TO_BACKUP ]
    then
        cd $EXPORT_CFG_DIR/$CFGSETNAME_TO_BACKUP/ 
        rm -rf $(find . -name CVS)
        
        tar zcvf $BAK_LOCAL_FILE * >& /dev/null
        last_status=$?
        if [[ ${last_status} != '0' ]]
        then
            echo $(date -R) "ERROR: Fail to pack the configuration files." | tee -a $DIAGNOSE
            exit ${last_status} 
        fi
        
        mv -f $BAK_LOCAL_FILE  $CFGSETNAME_TO_SAVEAS
        mv -f $CFGSETNAME_TO_SAVEAS $BAK_LOCAL_DIR/
        
    else
        echo "ERROR: Configuration Set NOT Found"  | tee -a $DIAGNOSE
        exit 1
    fi
    ;;
esac

cd $BAK_LOCAL_DIR 

echo $(date -R) "Encrypting the configuration files ..."

echo $(date -R) "SUCCESS: Package Config. $CFGSETNAME_TO_BACKUP as $CFGSETNAME_TO_SAVEAS OK ..."

rm -rf $QB_EXPORT_DIR
mkdir -p  $QB_EXPORT_DIR

ln -s $BAK_LOCAL_DIR/$CFGSETNAME_TO_SAVEAS  $QB_EXPORT_DIR/$CFGSETNAME_TO_SAVEAS


