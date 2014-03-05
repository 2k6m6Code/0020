#!/bin/sh

QB1_DIR=$1
QB2_DIR=$2

FILE_LIST=`(cd $QB1_DIR/mnt; ls *.pkg linux)`

for FILE in $FILE_LIST; do
	echo "comparing $FILE ..."
	cmp $QB1_DIR/mnt/$FILE $QB2_DIR/mnt/$FILE
done

