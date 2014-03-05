#! /bin/bash

set -x

year=$1
month=$2
day=$3
hour=$4
min=$5
sec=$6

DIAGNOSE=/var/log/diagnose.log

unalias cp
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

# 1. ===============================================================
date -s $year/$month/$day >& /dev/null
date_status=$?

if [[ ${date_status} != '0' ]]
then
    echo $(date) "ERROR: Fail to Set Date" | tee -a $DIAGNOSE
    exit ${date_status}
else
    echo "Set Date Successfully" $(date) | tee -a $DIAGNOSE
fi

# 2. ===============================================================
date -s $hour:$min:$sec >& /dev/null
time_status=$?

if [[ ${time_status} != '0' ]]
then
    echo $(date) "ERROR: Fail to Set Time" | tee -a $DIAGNOSE
    exit ${time_status}
else
    echo $(date) "Set Time Successfully" | tee -a $DIAGNOSE
fi

# 3. ===============================================================
clock -w >& /dev/null
clock_status=$?

if [[ ${clock_status} != '0' ]]
then
    echo $(date) "ERROR: Fail to Set Timezone as $zonename" | tee -a $DIAGNOSE
    exit ${clock_status}
else
    echo $(date) "Write Clock to BIOS Successfully" | tee -a $DIAGNOSE
fi





