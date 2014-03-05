#! /bin/sh

# REBOOT_OPTION
# 0: no reboot
# 1: reboot now

# REBOOT_OPT=$1

unalias cp

#TMP_DOM_DIR=/tmp/dom
TMP_DOM_DIR=/tmp/tmpupg/dom

if [ ! -d $TMP_DOM_DIR ]
then
    mkdir $TMP_DOM_DIR 
fi

DOM_FILE=$(ls /mnt/*.dom)

cd /mnt

# Extract all package to $TMP_DOM_DIR

#tar zxfC $DOM_FILE /tmp/tmp 
tar zxfC $DOM_FILE /tmp/tmpupg 

cd $TMP_DOM_DIR

tar zxfC $TMP_DOM_DIR/conf.pkg /mnt
sync

# Process xml package   

tar zxf $TMP_DOM_DIR/qbxml.pkg 
tar zxf $TMP_DOM_DIR/qbgui.pkg 
sync

XML_VERSION=$(cat ${TMP_DOM_DIR}/bin/XMLVERSION )

rm -rf /mnt/qb/conf/set/*

cp -R $TMP_DOM_DIR/xmltemplate/login.xml /mnt/qb/conf/ >& /dev/null
cp -R $TMP_DOM_DIR/xmltemplate/ha.xml /mnt/qb/conf/ >& /dev/null

cp -R $TMP_DOM_DIR/xmltemplate/$XML_VERSION/ /mnt/qb/conf/set/default
cp -R $TMP_DOM_DIR/xmltemplate/$XML_VERSION/ /mnt/qb/conf/set/boot

sync


$TMP_DOM_DIR/regpkg.sh

cp -f *.pkg /mnt
  
sync
sync

echo " REBOOT SYSTEM NOW  ..."

sleep 10

#reboot
/sbin/reboot -n
