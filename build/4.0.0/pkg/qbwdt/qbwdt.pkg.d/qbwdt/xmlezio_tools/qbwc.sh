#!/bin/sh
EZIO_PRINT_DEFAULT="/opt/qb/qbwdt/ezio"
EZIO_PRINT="/opt/qb/qbwdt/ezio -c 1 -t "

ln_count=0

if [ $# -eq 1 ] ;then 
    infile=$1

    ### count lines of file.
    if [ -f $infile ] ;then 
            number_of_record=$(awk 'END { print NR }' <$infile)
	    ( $EZIO_PRINT "Total Sessions:[ $number_of_record ]"; sleep 60; $EZIO_PRINT_DEFAULT) &
    else
        echo "No such file!"
    fi
else
    echo "No parameter ! ($#)"
    echo "Usage: $0 <infile>"
    echo
    echo "To count lines of <infile>, even /proc/... files"
    echo
fi
