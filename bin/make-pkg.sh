#! /bin/bash
#
#
#set -x
QB_DIR=/u1/Project.Q-Balancer
PATH=$PATH:$QB_DIR/bin;		export PATH

#if [ $# -ne 2 ]; then
#	echo "Usage : $0 <PKG_FILE> <PKG_DIR>"
#	exit 1
#fi

PKG_FILE=$1
PKG_NAME=`basename $1 | cut -d. -f1`
PKG_DIR=$2
PKG_VMWARE=$3

if [ ! -d $PKG_DIR ]; then
	echo "ERROR! Package directory ($PKG_DIR) is not found !"
	exit 1
fi

case "$PKG_NAME" in
	qbgui)
	    (cd $PKG_DIR/bin; \
	        # Generate qbui.tar; \
	        tar cf qbui.tar ./qb; \
	        # Generate qbui.100; \
	        mcrypt qbui.tar -p -k 42084021_qb30 > /dev/null 2>&1; \
	        rm -f qbui.tar; \
	        mv -f qbui.tar.bz2.nc qbui.100; \
	    )

	    (cd $PKG_DIR; \
		tar cfz $PKG_FILE . --exclude ./bin/qb)

	    rm -f $PKG_DIR/*/qbui.100
	    ;;

	qbbin)
	    #
	    # Create qbserv.100.
	    #
	    (cd $PKG_DIR/bin; \
	        # Generate qbserv.100 (bzip2 in the same time); \
	        mcrypt qbserv -p -k 42084021_qb30 > /dev/null 2>&1; \
	        rm -f qbserv.bz2; \
	        mv -f qbserv.bz2.nc qbserv.100; \
                rm -f ckmd5; \
                md5sum qbrunway > ckmd5; \
	    )

	    (cd $PKG_DIR; \
		tar cfz $PKG_FILE . --exclude ./bin/qbserv)

	    #
	    # qbserv.100 was created during make-pkg.sh.
	    # It is supposed to be removed after make-pkg.sh.
	    #
	    rm -f $PKG_DIR/*/qbserv.100
	    ;;

       qblogin)
           (cd $PKG_DIR; \
               tar cf qblogin.tar .; \
               # Generate qbui.tar; \
               mcrypt qblogin.tar -p -k 42084021_qb30 > /dev/null 2>&1; \
               #chmod 644 qblogin.tar.*; \
               mv  qblogin.tar.bz2.nc $PKG_FILE;
           )
           ;;

	script)
	    #
	    # Create script.pkg
	    #
	     cd $PKG_DIR; tar cfz $PKG_FILE .
             if [ "$PKG_VMWARE" = "1" ];then
             mcrypt $PKG_FILE -k 2k6m6ej3zp4
             mv -f $PKG_FILE.nc $PKG_FILE
             fi
	    ;;

	function)
	    #
	    # Create function.pkg
	    #
	     cd $PKG_DIR; tar cfz $PKG_FILE .
             if [ "$PKG_VMWARE" = "1" ];then
             mcrypt $PKG_FILE -k pkg2k6m6ej3zp4function
             mv -f $PKG_FILE.nc $PKG_FILE
             fi
	    ;;

	*)
	    (cd $PKG_DIR; tar cfz $PKG_FILE .)
	    ;;

esac



