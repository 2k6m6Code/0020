#!/bin/sh
#
# Generate the UPG file
#

#
# <VERSION> : 2.5.0, ...
# <BRAND>   : all, Deansoft, XRIO, ZeroOneTech
# <MODEL>   : all, 1610, 1611, ...
# 
if [ $# -ne 3 ]; then
	echo "Usage : $0 <VERSION> <BRAND> <MODEL>"
	exit 1
fi

#
# Main
#

QB_DIR=/u1/Project.Q-Balancer

VERSION=$1
BRAND=$2
MODEL=$3

VERSION=$1

echo
echo "Generating $VERSION UPG file of $BRAND $MODEL ..."

#--------------------------------------------------
rm -rf $UPG_DIR
mkdir -p $UPG_DIR

#=====================================================
# !! we have to get the CPUTYPE
CPUTYPE=""
present_dir=$PWD
cd $ROOT_DIR/$VERSION/$MODEL/
tar zxvf function.pkg
CPUTYPE=$(awk '/PLATFORM/ {print $2}' ./conf/registry)
CTDIR_ON=$(awk '/ENABLECTDIR/ {print $2}' ./conf/registry) ## for ctdir...nancy050106
ODM=$(awk '/MODEL/ {print $2}' ./conf/registry) ## for odm...nancy050223
rm -rf ./conf
cd $present_dir

#=====================================================
# step 1. copy qb model dependent PKGs  
cp -f $ROOT_DIR/$VERSION/$MODEL/*.pkg $UPG_DIR

last_status=$?
if [[ $last_status != '0' ]];
then
    echo 
    echo "ERROR: Fail to copy $ROOT_DIR/$VERSION/$MODEL/*.pkg to $UPG_DIR "
    echo
    exit 1
fi

#=====================================================
# step 2. copy hardware model dependent PKGs  
cp -f $ROOT_DIR/$VERSION/HW_DEP_PKG/$CPUTYPE/*.pkg $UPG_DIR 

last_status=$?
if [[ $last_status != '0' ]];
then
    echo 
    echo "ERROR: Fail to copy $ROOT_DIR/$VERSION/HW_DEP_PKG/$CPUTYPE/*.pkg to $UPG_DIR "
    echo
    exit 1
fi

if [[ $CTDIR_ON = '1' && -f $ROOT_DIR/$VERSION/HW_DEP_PKG/$CPUTYPE/modules.pkg.ctdir ]] ;then 
    cp -f $ROOT_DIR/$VERSION/HW_DEP_PKG/$CPUTYPE/modules.pkg.ctdir $UPG_DIR/modules.pkg
    
    last_status=$?
    if [[ $last_status != '0' ]];
    then
        echo 
        echo "ERROR: Fail to copy $ROOT_DIR/$VERSION/$MODEL/modules.pkg to $UPG_DIR "
        echo
        exit 1
    fi
fi ## for ctdir...nancy050106

#=====================================================
# step 3. copy qb model in-dependent PKGs  
cp -f $ROOT_DIR/$VERSION/RELEASE_PKG/*.sh $UPG_DIR 
cp -f $ROOT_DIR/$VERSION/RELEASE_PKG/*.pkg $UPG_DIR 

#
# 2005-0401 Hammer
#           Some platform-dependent pkg.
#
PLATFORM_DIR="$ROOT_DIR/$VERSION/RELEASE_PKG/PLATFORM-DEPENDENT/$CPUTYPE"
if [ -d $PLATFORM_DIR ]; then
    cp -f $PLATFORM_DIR/*.pkg $DOM_RELEASE_DIR/dom 
fi

last_status=$?
if [[ $last_status != '0' ]];
then
    echo 
    echo "ERROR: Fail to copy $ROOT_DIR/$VERSION/RELEASE_PKG/*.pkg to $UPG_DIR "
    echo
    exit 1
fi

if [[ $CTDIR_ON = '1' && -f $ROOT_DIR/$VERSION/RELEASE_PKG/qbbin.pkg.ctdir ]] ;then 
    cp -f $ROOT_DIR/$VERSION/RELEASE_PKG/qbbin.pkg.ctdir $UPG_DIR/qbbin.pkg

    last_status=$?
    if [[ $last_status != '0' ]];
    then
        echo 
        echo "ERROR: Fail to copy $ROOT_DIR/$VERSION/RELEASE_PKG/qbbin.pkg to $UPG_DIR"
        echo
        exit 1
    fi
fi ## for ctdir...nancy050106

if [[ ( $ODM = "BL10400" || $ODM = "BL10800" ) && -f $ROOT_DIR/$VERSION/RELEASE_PKG/qbcli.pkg.odm ]] ;then
    cp -f $ROOT_DIR/$VERSION/RELEASE_PKG/qbcli.pkg.odm $UPG_DIR/qbcli.pkg
    cp -f $ROOT_DIR/$VERSION/RELEASE_PKG/qbwdt.pkg.odm $UPG_DIR/qbwdt.pkg
    last_status=$?
    if [[ $last_status != '0' ]];
    then
        echo
        echo "ERROR: Fail to copy $ROOT_DIR/$VERSION/RELEASE_PKG/qbcli & qbwdt.pkg to $UPG_DIR"
        echo
        exit 1
    fi
fi ## for odm...nancy050223

#=====================================================
# step 4. copy the model of linux kernel to dom directory

if [ -d $ROOT_DIR/$VERSION/linux_kernel/$CPUTYPE ];
then
    echo "Linux Kernel : $CPUTYPE" 
    echo
    cp -f $ROOT_DIR/$VERSION/linux_kernel/$CPUTYPE/linux  $UPG_DIR/linux
fi


echo 
echo "Stage 3: copy $VERSION $MODEL package files to $UPG_DIR : OK"
echo


cd $UPG_ROOT_DIR

./build.sh $VERSION $MODEL $PRODUCT_ID


