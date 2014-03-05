#!/bin/sh

TMP_DIR=/tmp/.tmp.$$
trap "rm -rf $TMP_DIR" 0 1 2 15

FLASH1_DIR=$1
FLASH2_DIR=$2

echo
echo "---> Comparing image.gz ..."
echo
cmp $FLASH1_DIR/image.gz $FLASH2_DIR/image.gz

echo
echo "---> Comparing *.pkg ..."
echo
FILE_LIST=`(cd $FLASH1_DIR; ls *.pkg)`
for FILE in $FILE_LIST; do
	rm -rf $TMP_DIR
	echo "comparing $FILE ..."
	TMP_DATA1_DIR=$TMP_DIR/data-1
	TMP_DATA2_DIR=$TMP_DIR/data-2
	mkdir -p $TMP_DATA1_DIR
	mkdir -p $TMP_DATA2_DIR
	tar xfzC $FLASH1_DIR/$FILE $TMP_DATA1_DIR
	tar xfzC $FLASH2_DIR/$FILE $TMP_DATA2_DIR
	diff -r $TMP_DATA1_DIR $TMP_DATA2_DIR
done

echo
echo "--> Comparing the kernel file (linux) ..."
echo
cmp $FLASH1_DIR/linux $FLASH2_DIR/linux

echo
echo "--> Comparing the whole flash ..."
echo
diff -r $FLASH1_DIR $FLASH2_DIR


