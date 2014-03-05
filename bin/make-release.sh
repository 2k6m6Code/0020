#!/bin/sh
#set -x
#
# To generate the release (DOM/UPG) file.
#
# <VERSION> : 2.5.0, ...
# <BRAND>   : all, Deansoft, XRIO, ZeroOneTech
# <MODEL>   : all, 1610, 1611, ...
# 
# What is a DOM file : a tgz file
#	./dom
#	    ./pkginfo
#	    ./linux
#	    ./regpkg.sh
#
#	    ./image.gz		(??? in DOM ??? not included for now ???)
#
#	    ./afs.pkg
#	    ./conf.pkg
#	    ./crond.pkg
#	    ./dhcpd.pkg
#	    ./function.pkg
#	    ./mod2622.pkg
#	    ./modules.pkg
#	    ./qbapps.pkg
#	    ./qbbin.pkg
#	    ./qbbrg.pkg
#	    ./qbcli.pkg
#	    ./qbgui.pkg
#	    ./qbwdt.pkg
#	    ./qbxml.pkg
#	    ./script.pkg
#	    ./snmpd.pkg
#           20061221 Brian add:
#           ./ddns.pkg
#           ./dhcpcd.pkg
#           ./pppoe.pkg
#           ./layer7.pkg
#           #./zebra.pkg
#           ./squid.pkg
#           #./qbtoolib.pkg
#           ./analyweb.pkg
#           20091019 Luke add: 
#           ./ipsec.pkg 

# What is a UPG file : an encrypted tgz file
#	./pkginfo
#	./linux
#	./regpkg.sh
#
#	./checksum.md5		(only in UPG)
#	./do_upgrade		(only in UPG)
#	./install.sh		(only in UPG)
#	./xmlupgrade.pl		(only in UPG)
#
#	./afs.pkg
#	./conf.pkg
#	./crond.pkg
#	./dhcpd.pkg
#	./function.pkg
#	./mod2622.pkg
#	./modules.pkg
#	./qbapps.pkg
#	./qbbin.pkg
#	./qbbrg.pkg
#	./qbcli.pkg
#	./qbgui.pkg
#	./qbwdt.pkg
#	./qbxml.pkg
#	./script.pkg
#	./snmpd.pkg
#       20061221 Brian add:
#       ./ddns.pkg
#       ./dhcpcd.pkg
#       ./pppoe.pkg
#       ./layer7.pkg
#       #./zebra.pkg
#       ./squid.pkg
#       #./qbtoolib.pkg
#       ./analyweb.pkg
#
#       20091019 Luke add: 
#      ./ipsec.pkg
#	20130306 shane add:
#	./4to6.pkg 

YYYY_MMDD_HHNN_SS=`date +%Y-%m%d-%H%M-%S`
QB_DIR=/Q-Balancer-0020
PATH=$PATH:$QB_DIR/bin;		export PATH

TMP_DIR=$QB_DIR/tmp/.tmp.$$
trap "rm -rf $TMP_DIR" 0 1 2 15

#if [ $# -ne 4 ]; then
if [ $# -ne 4 ] && [ $# -ne 5 ]; then
	echo "Usage : $0 <VERSION> <BRAND> <MODEL> <TYPE:LB/SG> <Eval:Eval_num>"
	exit 1
fi

# ----------------------------------------------------------------------
# 1. For each package in <src-dir>, generates its pkg file in <dst-dir>.
#    And, append it's serial.txt info to <pkginfo-file>.
#
# 2. The package in <src-dir> might be :
#	1) a directory : <pkg-name>.pkg.d
#	2) a file      : <pkg-name>.pkg
#
# pack_pkg()
# 	Usage : pack_pkg <src-dir> <dst-dir> <pkginfo-file>
#
#
pack_pkg() {
	if [ $# -ne 3 ]; then
	    echo "Usage : pack_pkg <src-dir> <dst-dir> <pkginfo-file>"
	    exit 1
	fi

	X_SRC_DIR=$1
	X_DST_DIR=$2
	X_PKGINFO_FILE=$3

	X_TMP_SERIAL_FILE="`dirname $X_PKGINFO_FILE`/serial.txt"
	X_PKG_LIST=`ls $X_SRC_DIR`
	for X_PKG in $X_PKG_LIST; do
	    X_PKG_NAME=`echo $X_PKG | cut -d. -f1`
	    case "$X_PKG" in
		*.pkg.d)
		    if [ -f ${X_PKG_NAME}.pkg ]; then
			# Use *.pkg directly if both *.pkg and *.pkg.d exists.
			continue
		    fi

		    (cd $X_SRC_DIR/$X_PKG; \
			#make-pkg.sh $X_DST_DIR/$X_PKG_NAME.pkg .; \
                        make-pkg.sh $X_DST_DIR/$X_PKG_NAME.pkg . $IS_ENABLE_VMWARE; \
			X_THIS_SERIAL_FILE=`find . -name serial.txt -print`; \
			if [ ! -z "$X_THIS_SERIAL_FILE" ]; then
			    cp -a $X_THIS_SERIAL_FILE $X_TMP_SERIAL_FILE; \
			fi; \
			)
		    ;;

		*.pkg)
		    (cd $X_SRC_DIR; \
			cp -a $X_PKG $X_DST_DIR; \
			mkdir xx; \
			cd xx; tar xfz ../$X_PKG; \
			X_THIS_SERIAL_FILE=`find . -name serial.txt -print`; \
			if [ ! -z "$X_THIS_SERIAL_FILE" ]; then
			    cp -a $X_THIS_SERIAL_FILE $X_TMP_SERIAL_FILE; \
			fi; \
			cd ..; rm -rf xx \
			)
		    ;;

		*)
		    ;;
	    esac

	    # retrieve the notes from the serial.txt of each pkg.
	    if [ ! -z "$X_THIS_SERIAL_FILE" ]; then
	        sed '/notes/,$d' $X_TMP_SERIAL_FILE >> $X_PKGINFO_FILE
	        echo "                         " >> $X_PKGINFO_FILE
	    fi

	    rm -f $X_TMP_SERIAL_FILE
	done
}

# ----------------------------------------------------------------------

#
# Main
#

VERSION=$1
BRAND=$2
MODEL=$3
TYPE=$4
EVAL=$5

UTIL_DIR=$QB_DIR/build/$VERSION/util

BRAND_DIR=$QB_DIR/build/$VERSION/spec/$TYPE/$BRAND

mkdir -p $TMP_DIR/dom
PKGINFO_FILE=$TMP_DIR/dom/pkginfo

#
# Determine the model list ($MODEL_LIST) to be released.
#
if [ "x$MODEL" = "x" ]; then
	MODEL_LIST=`ls $BRAND_DIR`
else
	MODEL_DIR=$BRAND_DIR/$MODEL
	if [ -d $MODEL_DIR ]; then
	    MODEL_LIST="$MODEL"
	else
	    echo "This BRAND/MODEL ($BRAND/$MODEL) is not defined yet !"
	    exit 1
	fi
fi

#
# History information for each releases.
#
IS_RELEASE_TXT_READY=0
INFO_DIR=$QB_DIR/build/$VERSION/info
RELEASE_HISTORY_DIR=$INFO_DIR/history.d
LAST_RELEASE_TXT_FILE=$RELEASE_HISTORY_DIR/release.txt.last
THIS_RELEASE_TXT_FILE=$INFO_DIR/release.txt
if [ ! -f $THIS_RELEASE_TXT_FILE ]; then
	echo "ERROR ! No release-note file is found ($THIS_RELEASE_TXT_FILE) !"
	echo "        Please write the release-not file first !"
	exit
fi

if [ ! -f $LAST_RELEASE_TXT_FILE ]; then
	IS_RELEASE_TXT_READY=1
else
	diff $LAST_RELEASE_TXT_FILE $THIS_RELEASE_TXT_FILE > /dev/null 2>&1
	if [ $? -eq 0 ]; then
	    # Yes, the same. The release-note file is not revised.
	    IS_RELEASE_TXT_READY=0
	else
	    # No, different. The release-note file is already revised.
	    IS_RELEASE_TXT_READY=1
	fi
fi


#
# Patch information :
#
# 1. Prompt the user whether this is a new (update) release.
#	1.1 A new release :
#		Some modifications is done for this release.
#		This 
#
#	1.2 'Not' A new release :
#		No any modification was done since last release.
#		Only packing operation is done.
#
# 2.
#
#
PATCH_NO_FILE=$QB_DIR/build/$VERSION/info/.patch-no
if [ ! -f $PATCH_NO_FILE ]; then
	echo "0" > $PATCH_NO_FILE
fi

PATCH_NO=`head -1 $PATCH_NO_FILE`

IS_NEW_RELEASE=n

echo "Last Patch-no is : $PATCH_NO"
echo -n "Is this a new patch (modification) release (y/n) ? "
read ANS
if [ "x$ANS" = "xy" ]; then
	if [ "x$IS_RELEASE_TXT_READY" = "x0" ]; then
	    echo "ERROR ! The release.txt file is not updated for new release !"
	    echo "        Please update the release.txt file first !"
	    exit 1
	fi
	
	echo "Confirmed ! This will be a new patch release."
	PATCH_NO=`expr $PATCH_NO + 1`
	echo $PATCH_NO > $PATCH_NO_FILE
	echo "A new patch-no will be given."
	IS_NEW_RELEASE=y

else
	if [ "x$IS_RELEASE_TXT_READY" = "x1" ]; then
	    echo "ERROR ! The release-note file is already updated/available !"
	    echo "        Is this a new release ?!"
	    exit 1
	fi

	echo "Confirmed ! This is NOT a new patch release."
	echo "The patch-no is kept still."
fi

PATCH_NO=`printf "%04d" $PATCH_NO`
echo "This patch-no : ($PATCH_NO)"

#
# Make release for each model, one by one.
#
for MODEL in $MODEL_LIST; do

	MODEL_DIR=$BRAND_DIR/$MODEL

	REGISTRY_FILE=$MODEL_DIR/function.pkg.d/conf/registry
	if [ ! -f $REGISTRY_FILE ]; then
	    echo "ERROR ! This model is NOT registered yet !"
	    exit 1
	fi

        IS_ENABLE_VMWARE=$(awk '/^ENABLEVM/ {print $2}' $REGISTRY_FILE)

	#
	# There are MANY pkg files for each model release. They are
	# all saved in a directory for each model/release.
	#
	if [ $EVAL ]; then
	RELEASE_NAME=$BRAND-$MODEL-${VERSION}-$TYPE-${PATCH_NO}-$EVAL
        else
	RELEASE_NAME=$BRAND-$MODEL-${VERSION}-$TYPE-${PATCH_NO}
        fi
	RELEASE_PKG_DIR=$QB_DIR/release/pkg/$VERSION/all/$RELEASE_NAME
	mkdir -p $RELEASE_PKG_DIR

	#
	# There is only ONE dom/upg file for each model release. Each
	# is saved in a single file (*.dom/*.upg) for each model/release.
	#
	RELEASE_DOM_DIR=$QB_DIR/release/dom
	RELEASE_UPG_DIR=$QB_DIR/release/upg
	RELEASE_DOM_FILE=$RELEASE_DOM_DIR/$VERSION/all/$RELEASE_NAME.dom
	RELEASE_UPG_FILE=$RELEASE_UPG_DIR/$VERSION/all/$RELEASE_NAME.upg
	RELEASE_TGZ_FILE=$RELEASE_UPG_DIR/$VERSION/all/$RELEASE_NAME.tgz

	if [ -f $RELEASE_DOM_FILE ]; then
	    echo
	    echo "WARNING ! An existing release (DOM) is already exist !"
	    echo "Press CTRL-C to abort, or ENTER to overwrite  !"
	    echo
	    read ANS
	fi

	if [ -f $RELEASE_UPG_FILE ]; then
	    echo
	    echo "WARNING ! An existing release (UPG) is already exist !"
	    echo "Press CTRL-C to abort, or ENTER to overwrite  !"
	    echo
	    read ANS
	fi

	#
	# $PLATFORM
	# $PLATFORM_DIR
	# $KERNEL_DIR
	# $KERNEL_FILE
	#
	PLATFORM=$(awk '/^PLATFORM/ {print $2}' $REGISTRY_FILE)
	PLATFORM_DIR=$QB_DIR/build/$VERSION/platform/$PLATFORM
	KERNEL_DIR=$PLATFORM_DIR/kernel
	KERNEL_FILE=$KERNEL_DIR/linux

	if [ ! -d $PLATFORM_DIR ]; then
	    echo "ERROR ! platform ($PLATFORM) NOT available yet !"
	    exit 1
	fi

	if [ ! -f $KERNEL_FILE ]; then
	    echo "ERROR ! kernel file ($KERNEL_FILE) not found !"
	    exit 1
	fi

	#
	# $NUMOFPORT
	#
	NUMOFPORT=$(awk '/^NUMOFPORT/ {print $2}' $REGISTRY_FILE)

	#
	# Create a new pkginfo file with header.
	#	"DOM VERSION: 24215030.dom"
	#
	rm -f $PKGINFO_FILE
        
	if [ $EVAL ]; then
	echo "VERSION DETAIL : $BRAND-$MODEL-$VERSION-$TYPE-$PATCH_NO-$EVAL" > $PKGINFO_FILE
        else
	echo "VERSION DETAIL : $BRAND-$MODEL-$VERSION-$TYPE-$PATCH_NO" > $PKGINFO_FILE
        fi
	#
	# Now, begin the release work.
	#
	echo
	if [ $EVAL ]; then
	echo "Generating $VERSION DOM/UPG file for $BRAND-$TYPE-$MODEL-$EVAL ..."
        else
	echo "Generating $VERSION DOM/UPG file for $BRAND-$TYPE-$MODEL ..."
	fi
	#
	# 1. Prepare kernel file.
	#    'kernel' file is platform-dependent.
	#
	cp -aH $KERNEL_FILE $TMP_DIR/dom


	#
	# 2.1 packages in spec.
	#     e.g. conf.pkg, functions.pkg
	#
	SRC_DIR=$QB_DIR/build/$VERSION/spec/$TYPE/$BRAND/$MODEL
	pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE
	
	#
	# 2.2 packages commonly used in all models.
	#
	PKG_LIST="crond dhcpd qbapps qbbrg qbwdt script ddns dhcpcd pppoe layer7 radius squid pptpclt pptpser ipsec hsdpa qblogin xl2tp 3proxy sslvpn quagga"

	ENABLEANALYSER=$(awk '/^ENABLEANALYSER/ {print $2}' $REGISTRY_FILE)
        if [ "x$ENABLEANALYSER" = "x1" ]; then
	    PKG_LIST="$PKG_LIST analyweb"		
	fi

        #For vmware
        if [ "$IS_ENABLE_VMWARE" = "1" ]; then
	    PKG_LIST="$PKG_LIST vmconf"		
        fi

        #For sslvpn client
#	if [ "$TYPE" = "SG" ] || [ "$TYPE" = "Mesh" ] ; then
#	    PKG_LIST="$PKG_LIST sslportal"		
#	fi

        #For Wireless AP
	ENABLEWIRELESS=$(awk '/^ENABLEWIRELESS/ {print $2}' $REGISTRY_FILE)
	if [ "$ENABLEWIRELESS" = "1" ]; then
	    PKG_LIST="$PKG_LIST wireless"		
	fi

	for PKG_NAME in $PKG_LIST; do

           SRC_DIR=$QB_DIR/build/$VERSION/pkg/$PKG_NAME        
	   pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE
	done

	ENABLESNMP55=$(awk '/^ENABLESNMP55/ {print $2}' $REGISTRY_FILE)
        #
        #.a snmpd.pkg
        # 

        if [ "$ENABLESNMP55" = "1" ]; then
             SRC_DIR=$QB_DIR/build/$VERSION/pkg/snmpd/net-snmp55
        else
           SRC_DIR=$QB_DIR/build/$VERSION/pkg/snmpd
        fi

            pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE

        #
        #2.2.a afs.pkg
        # 

       if [ "$IS_ENABLE_VMWARE" != "1" ]; then
        #if [ "x$MODEL" = "x2710" ]; then
        #    SRC_DIR=$QB_DIR/build/$VERSION/pkg/afs/2710
#
#        elif [ "x$MODEL" = "x3000" ]; then
#            SRC_DIR=$QB_DIR/build/$VERSION/pkg/afs/2710
#
#        else
           SRC_DIR=$QB_DIR/build/$VERSION/pkg/afs
#        fi

            pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE
        fi

	#
	# 2.3 mod2421.pkg (platform-dependent)
	#
	SRC_DIR=$QB_DIR/build/$VERSION/pkg/mod2622/$PLATFORM
	pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE
	
	#4to6.pkg
	#
	SRC_DIR=$QB_DIR/build/$VERSION/pkg/4to6/ctdir-yes
	pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE
	
	#
	# 2.4 qbgui.pkg (brand-dependent, ctdir-dependent, evaluation-dependent)
	#
	IS_ENABLE_CTDIR=$(awk '/^ENABLECTDIR/ {print $2}' $REGISTRY_FILE)
	case "$PLATFORM" in
	    *eval)
		if [ "x$IS_ENABLE_CTDIR" = "x1" ]; then
		    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbgui/$TYPE/$BRAND/eval/ctdir-yes
		else
		    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbgui/$TYPE/$BRAND/eval/ctdir-no
		fi
		;;
	    *)
		if [ "x$IS_ENABLE_CTDIR" = "x1" ]; then
		    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbgui/$TYPE/$BRAND/ctdir-yes
		else
		    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbgui/$TYPE/$BRAND/ctdir-no
		fi
		;;
	esac

	pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE


	#
	# 2.4.1 qbcli.pkg (brand-dependent)
	#
       if [ "$IS_ENABLE_VMWARE" != "1" ]; then
	case "$BRAND" in
	    Deansoft)
		    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbcli/$BRAND
		;;
	    *)
		    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbcli
		;;
	esac
       else
           SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbcli/vmconsole
       fi

	pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE

	#
	# 2.5 modules.pkg (platform-dependent, ctdir-dependent)
	#
	if [ "x$IS_ENABLE_CTDIR" = "x1" ]; then
	    SRC_DIR=$QB_DIR/build/$VERSION/pkg/modules/$TYPE/$PLATFORM/ctdir-yes
	else
	    SRC_DIR=$QB_DIR/build/$VERSION/pkg/modules/$TYPE/$PLATFORM/ctdir-no
	fi
	pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE

	#
	# 2.6 qbbin.pkg (ctdir-dependent)
	#
	IS_ENABLE_CTDIR=$(awk '/^ENABLECTDIR/ {print $2}' $REGISTRY_FILE)
	case "$PLATFORM" in
	    *eval)
		if [ "x$IS_ENABLE_CTDIR" = "x1" ]; then
		    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbbin/eval/ctdir-yes
		else
		    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbbin/eval/ctdir-no
		fi
		;;
	    *)
		if [ "x$IS_ENABLE_CTDIR" = "x1" ] && [ "$IS_ENABLE_VMWARE" != "1" ]; then
                   #if [ "x$MODEL" = "x2710" ]; then
                   #      SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbbin/2710
                   #else
		         SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbbin/ctdir-yes/$TYPE
                   #fi
                elif [ "$IS_ENABLE_VMWARE" = "1" ]; then
                    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbbin/vmware
		else
		    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbbin/ctdir-no
		fi
		;;
	esac

#echo "\$SRC_DIR=[$SRC_DIR]"

#                if [ "x$IS_ENABLE_CTDIR" = "x1" ]; then
#                    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbbin/ctdir-yes
#                else
#                    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbbin/ctdir-no
#                fi

        pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE

	#
	# 2.7 qbxml.pkg (port-dependent).
	#
	if [ $NUMOFPORT -gt 3 ]; then
	    #SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbxml/more-than-3-ports
	    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbxml/more-than-3-ports/$BRAND
	else
	    SRC_DIR=$QB_DIR/build/$VERSION/pkg/qbxml/3-ports
	fi
	pack_pkg $SRC_DIR $RELEASE_PKG_DIR $PKGINFO_FILE


	#
	# 3. Prepare other utility files.
	#
	cp -a $UTIL_DIR/regpkg.sh $TMP_DIR/dom
        #20100507 Brian To add a time stamp 
        DATE=`date +"%Y-%m-%d"`
        echo
	echo "Adding local time stamp:$DATE ..."
        echo $DATE >$TMP_DIR/dom/release
        mcrypt $TMP_DIR/dom/release -k 2k6m6$  > /dev/null 2>&1
        rm -f $TMP_DIR/dom/release
        mv -f $TMP_DIR/dom/release.nc $TMP_DIR/dom/release.dat
        echo

	if [ "x$IS_NEW_RELEASE" = "xy" ]; then
	    #
	    # 4. history.txt
	    #    Put this release-note file into history directory.
	    #    Append this release file into history file.
	    #
	    HISTORY_RELEASE_TXT_FILE=$RELEASE_HISTORY_DIR/release.txt.$VERSION-$PATCH_NO

	    #
	    # Generate release.txt.$VERSION-$PATCH_NO iff it's a new release.
	    #
	    cp -a $THIS_RELEASE_TXT_FILE $HISTORY_RELEASE_TXT_FILE

	    #
	    # Re-generate release.txt.last (symbolic link)
	    # iff it's a new release.
	    #
	    rm -f $LAST_RELEASE_TXT_FILE
	    ln -s $HISTORY_RELEASE_TXT_FILE $LAST_RELEASE_TXT_FILE

	    #
	    # Update the history.txt file iff it's a new release.
	    #
	    HISTORY_TXT_FILE=$RELEASE_HISTORY_DIR/history.txt
	    mv $HISTORY_TXT_FILE $HISTORY_TXT_FILE.old
	    echo >> $HISTORY_TXT_FILE
	    echo "======== `date` ========" >> $HISTORY_TXT_FILE
	    echo "Version : ${VERSION}-${PATCH_NO}" >> $HISTORY_TXT_FILE
	    echo >> $HISTORY_TXT_FILE
	    cat $THIS_RELEASE_TXT_FILE >> $HISTORY_TXT_FILE
	    cat $HISTORY_TXT_FILE.old >> $HISTORY_TXT_FILE

	    rm -f $HISTORY_TXT_FILE.old
	    cp -a $HISTORY_TXT_FILE $TMP_DIR/dom
	fi

	#
	# 5. Generate DOM file.
	#
	cp -a $RELEASE_PKG_DIR/*.pkg $TMP_DIR/dom
	(cd $TMP_DIR; tar cfz $RELEASE_DOM_FILE ./dom)

	#
	# 6. Generate UPG file.
	#    In ./dom, add in some extra files.
	#
	#	./do_upgrade		(only in UPG)
	#	./install.sh		(only in UPG)
	#	./xmlupgrade.pl		(only in UPG)
	#
	#    Generate checksum.md5 file.
	#	./checksum.md5		(only in UPG)
	#
	cp -a $UTIL_DIR/do_upgrade $TMP_DIR/dom
	cp -a $UTIL_DIR/install.sh $TMP_DIR/dom
	cp -a $UTIL_DIR/xmlupgrade.pl $TMP_DIR/dom
	cp -a $UTIL_DIR/*db $TMP_DIR/dom
        cp -a $UTIL_DIR/doupgrade.sh $TMP_DIR/dom
	(cd $TMP_DIR/dom; \
		rm -f checksum.md5; \
		md5sum * > checksum.md5; \
		tar cfz $RELEASE_TGZ_FILE .; \
		mcrypt $RELEASE_TGZ_FILE -k 42084021 > /dev/null 2>&1; \
		#mcrypt --nolock $RELEASE_TGZ_FILE -k 42084021 > /dev/null 2>&1; \
		rm -f $RELEASE_TGZ_FILE; \
		mv $RELEASE_TGZ_FILE.nc $RELEASE_UPG_FILE; \
		chmod a+r $RELEASE_UPG_FILE \
	)

	#
	# pkginfo file :
	#
	#DOM VERSION: 24215030.dom
	#
	#[CONF.PKG]
	#version = 2.5.0
	#serial = 2720
	#[/CONF.PKG]
	#
	#serial = 1   Thu Apr 27 18:25:41 CST 2004
	#component= DHCPD.PKG
	#version=2.5.0
	#
	#[FUNCTION.PKG]
	#version = 2.5.0
	#serial = 2720
	#[/FUNCTION.PKG]
	#
	#serial = 3   Mon Feb 21 17:39:12 CST 2005
	#component= MODULES.PKG.CTDIR
	#PIV: recompile qbkflow & qbkf_timeout of MAX_Gateway.
	#------------------------------------------------
	#serial = 2   Mon Feb 21 17:38:35 CST 2005
	#component= MODULES.PKG.CTDIR
	#PIV: recompile qbkflow & qbkf_timeout of MAX_Gateway.
	# ...
	#

	#
	# ???
	# ??? present_dir=$PWD
	# ??? cd $DOM_RELEASE_DIR/dom/
	# ??? $DOM_RELEASE_DIR/dom/regpkg.sh
	# ??? cd $present_dir
	# ??? cp -f /mnt/conf/pkginfo $DOM_RELEASE_DIR/dom
	# ???
	#

	#
	sync
done
#rm -rf $TMP_DIR
echo "New DOM file : $RELEASE_DOM_FILE"
echo "New UPG file : $RELEASE_UPG_FILE"

