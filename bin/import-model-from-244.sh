#!/bin/sh

QB_DIR=/u1/Project.Q-Balancer

if [ $# -lt 3 ]; then
	echo
	echo "Usage : $0 <VERSION> <BRAND> <MODEL1> <MODEL2> ..."
	echo
	echo "        <VERSION> : 2.5.0"
	echo "        <BRAND>   : Deansoft, XRIO, ZeroOneTech"
	echo "        <MODEL>   : 1610, 1611, ..."
	exit 1
fi

VERSION=$1
BRAND=$2
shift; shift
MODEL_LIST=$*

echo
echo " NOTE : Only function.pkg and conf.pkg will be imported (as spec) !!!"
echo

for MODEL in $MODEL_LIST; do

	FROM_DIR=192.168.5.244:/home/QBPL/DOM/$VERSION/$MODEL
	SPEC_DIR=$QB_DIR/build/$VERSION/spec/$BRAND/$MODEL

	if [ -d $SPEC_DIR ]; then
	    echo
	    echo "INFO : Model ($MODEL) was already imported from 244 host."
	    continue
	fi

	mkdir $SPEC_DIR

	#
	# To transfer model-dependent PKG (function.pkg, conf.pkg).
	#
	echo
	echo "... going to transfer files of model ($MODEL) from host 244 "
	echo
	scp -pr $FROM_DIR/[cf]*.pkg $SPEC_DIR

	cd $SPEC_DIR

	#
	# Import/create :
	#   .../products/brands/imported-from-244/models/$MODEL/function.pkg.d
	#
	(tar xfz ./function.pkg; \
	    mkdir function.pkg.d; \
	    mv conf function.pkg.d; \
	    rm -rf ./function.pkg)

	#
	# Import/create :
	#   .../products/brands/imported-from-244/models/$MODEL/conf.pkg.d
	#
	(tar xfz ./conf.pkg; \
	    mkdir conf.pkg.d; \
	    mv conf conf.pkg.d; \
	    rm -rf ./conf.pkg)

	echo
	echo "... complete to transfer files of model ($MODEL) from host 244 "
	echo
	echo " NOTE : Remember to add 'BRAND $BRAND' into the registry file."
	echo

done


