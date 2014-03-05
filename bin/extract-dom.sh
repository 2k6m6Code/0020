#!/bin/sh
#
# To extract a DOM file to a new created sub-directory with the same
# DOM name.
#

if [ $# -ne 1 ]; then
	echo "Usage : $0 <upg-file>"
	exit 1
fi

QB_DIR=/u1/Project.Q-Balancer

PATH=$PATH:$QB_DIR/bin;		export PATH

DOM_FILE=$1

FILE_NAME=`basename $DOM_FILE`
LEN=`echo $FILE_NAME | wc -c | awk '{print $1}'`
P1=`expr $LEN - 5`
P2=`expr $LEN - 3`
P3=`expr $LEN - 1`
DOM_NAME=`echo $FILE_NAME | cut -c1-${P1}`
EXT_NAME=`echo $FILE_NAME | cut -c${P2}-${P3}`

if [ ! "x$EXT_NAME" = "xdom" ]; then
	echo "Error ! file extension has to be .dom !"
	exit 1
fi

rm -rf $DOM_NAME; mkdir $DOM_NAME

tar xfz $DOM_FILE -C $DOM_NAME

#
#
#
cd $DOM_NAME/dom
PKG_FILES=`ls *.pkg`
for PKG_FILE in $PKG_FILES; do
	extract-pkg.sh $PKG_FILE
done


