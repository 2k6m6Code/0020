#! /bin/bash

PKGINFO_FILE=/mnt/conf/pkginfo 
TMP_PKGINFO_FILE=/tmp/pkginfo 

unalias rm

clear 

echo "Build /mnt/conf/pkginfo  ..... "
echo 

if [ -d /tmp/pkg ]
then
    rm -rf /tmp/pkg/*
else
    mkdir /tmp/pkg
fi

if [ -f $TMP_PKGINFO_FILE ];
then
    rm -f $TMP_PKGINFO_FILE 
fi

if [ -f $PKGINFO_FILE ];
then
    rm -f $PKGINFO_FILE 
fi

DOM_VERSION=$(ls /mnt/*.dom)
DOM_VERSION=$(basename $DOM_VERSION)

echo "DOM VERSION: $DOM_VERSION" >> $TMP_PKGINFO_FILE
echo "                         " >> $TMP_PKGINFO_FILE 

# 2005-0520 Hammer
if [ -f pkginfo ]; then
	cat pkginfo >> $TMP_PKGINFO_FILE 
	echo >> $TMP_PKGINFO_FILE 
fi


# build registry accrording to seiral.txt in every package

# uncompress package to read serial.txt

for file in $(ls *.pkg);
do
    echo "Build /mnt/conf/pkginfo according to $file " 
    echo   
 
    tar zxvfC $file /tmp/pkg >& /dev/null
    sync
     
    TMP_DIR=$(ls /tmp/pkg)

    if [ -z $TMP_DIR ]
    then
        echo "ERROR: Umcompress $PKG_FILE error "
        #exit 1
    fi

    if [ -f /tmp/pkg/$TMP_DIR/serial.txt ]
    then 
    	sed '/notes/,$d' /tmp/pkg/$TMP_DIR/serial.txt >> $TMP_PKGINFO_FILE 
    	echo "                         " >> $TMP_PKGINFO_FILE 
    fi
   
    rm -rf /tmp/pkg/* 
	
done

mv $TMP_PKGINFO_FILE $PKGINFO_FILE

sync
sync




