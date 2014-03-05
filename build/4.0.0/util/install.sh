#! /bin/sh

unalias rm
unalias cp

clear

TMP_DOM_DIR=/tmp/tmpupg/dom    #Brian 20090522 tmp directory is not enough,so change path to ramdisk for install process
#TMP_DOM_DIR=/tmp/dom

if [ ! -d $TMP_DOM_DIR ]
then
    mkdir $TMP_DOM_DIR 
fi

DOM_FILE=$(ls /mnt/*.dom)

echo
echo "Find $DOM_FILE "

cd /mnt

# Extract all package to $TMP_DOM_DIR

#tar zxfC $DOM_FILE /tmp/ >& /dev/null  
tar zxfC $DOM_FILE /tmp/tmpupg >& /dev/null #Brian 20090522 tmp directory is not enough,so change path to ramdisk for install process

cd $TMP_DOM_DIR 


# Extract conf.pkg to /mnt/conf

echo
echo "Extract conf.pkg to /mnt/conf "

tar zxfC $TMP_DOM_DIR/conf.pkg /mnt >& /dev/null

echo
echo "Extract function.pkg to /mnt/conf "
tar zxfC $TMP_DOM_DIR/function.pkg /mnt >& /dev/null

sync

# Process xml package   

echo
echo "Extract qbxml.pkg to /mnt/qb "

tar zxf $TMP_DOM_DIR/qbxml.pkg >& /dev/null
tar zxf $TMP_DOM_DIR/qbgui.pkg >& /dev/null
sync

XML_VERSION=$(cat ${TMP_DOM_DIR}/bin/XMLVERSION )

if [ -d /mnt/qb/conf ]
then
	rm -rf /mnt/qb
fi

mkdir /mnt/qb/
mkdir /mnt/qb/conf/
mkdir /mnt/qb/conf/set/

cp -R $TMP_DOM_DIR/xmltemplate/*.xml /mnt/qb/conf/ >& /dev/null

if [ ! -d /mnt/qb/conf/set/default ]
then
    mkdir /mnt/qb/conf/set/default
fi

cp -R $TMP_DOM_DIR/xmltemplate/$XML_VERSION/* /mnt/qb/conf/set/default/ >& /dev/null


if [ ! -d /mnt/qb/conf/set/boot ]
then
    mkdir /mnt/qb/conf/set/boot
fi

cp -R $TMP_DOM_DIR/xmltemplate/$XML_VERSION/* /mnt/qb/conf/set/boot/ >& /dev/null

sync


echo
echo "Build pkginfo in /mnt/conf "

$TMP_DOM_DIR/regpkg.sh

cp -f *.pkg /mnt

if [ -f linux ]
then
    cp -f linux     /mnt
fi

if [ ! -d /mnt/log ]
then
	mkdir /mnt/log
fi

  
sync
sync

echo 
echo "Install finish ..."
echo
echo "Please enter /mnt/qbkey ... "
echo



