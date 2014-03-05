#!/bin/sh

if [ $# -ne 1 ]; then
	echo "Usage : $0 <qbalancer-log-file>"
	exit 1
fi

LOG_FILE=$1
REPORT_FILE=$1.report

cat $LOG_FILE | grep -i qbserv | cut -d' ' -f6- > $REPORT_FILE


