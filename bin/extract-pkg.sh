#!/bin/sh
#
# To extract a .pkg file to a new created sub-directory with the same
# pkg name.
#

if [ $# -lt 1 ]; then
	echo "Usage : $0 <pkg-file> ..."
	exit 1
fi

PKG_FILE_LIST=$*

for PKG_FILE in $PKG_FILE_LIST; do
	FILE_NAME=`basename $PKG_FILE`
	LEN=`echo $FILE_NAME | wc -c | awk '{print $1}'`
	P1=`expr $LEN - 5`
	P2=`expr $LEN - 3`
	P3=`expr $LEN - 1`
	PKG_NAME=`echo $FILE_NAME | cut -c1-${P1}`
	EXT_NAME=`echo $FILE_NAME | cut -c${P2}-${P3}`

	PKG_DIR=$PKG_NAME.pkg.d

	if [ ! "x$EXT_NAME" = "xpkg" ]; then
	    echo "Error ! file extension has to be .pkg !"
	    exit 1
	fi

	rm -rf $PKG_DIR; mkdir $PKG_DIR

	tar xfz $PKG_FILE -C $PKG_DIR

	#
	#
	#
	if [ "x$PKG_NAME" = "xqbgui" ]; then
	    (cd $PKG_DIR/bin; \
	        mv qbui.100 qbui.tar.gz2.nc; \
    	        mcrypt qbui.tar.gz2.nc -d -k 42084021_qb30 > /dev/null 2>&1; \
    	        #mcrypt qbui.tar.gz2.nc -d -k 42084021 > /dev/null 2>&1; \
	        rm -f qbui.tar.gz2.nc; \
	        tar xfj qbui.tar.gz2; \
	        rm -f qbui.tar.gz2; \
	    )
	elif [ "x$PKG_NAME" = "xqbbin" ]; then
	    (cd $PKG_DIR/bin; \
	        mv qbserv.100 qbserv.bz2.nc; \
    	        mcrypt qbserv.bz2.nc -d -k 42084021_qb30 > /dev/null 2>&1; \
    	        #mcrypt qbserv.bz2.nc -d -k 42084021 > /dev/null 2>&1; \
	        rm -f qbserv.bz2.nc; \
	        bunzip2 qbserv.bz2; \
	    )
	fi
done



