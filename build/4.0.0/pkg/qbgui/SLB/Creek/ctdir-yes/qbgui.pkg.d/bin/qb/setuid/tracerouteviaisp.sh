#! /bin/bash
DIAGNOSE=/var/log/diagnose.log

FLOWMARK=$1
VIAISP=$2
OPTIONS=$3
unalias cp

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

#==================================================================
# 1.
if [[ $FLOWMARK != 'TOLAN' ]]
then
    echo "----------------------------------------------------------------------"
    iptables -t mangle -I OUTPUT -j MARK --set-mark $FLOWMARK

    iptables_result=$?

    if [[ ${iptables_result} != '0' ]]
    then
        echo $(date) "ERROR: Fail to prepare isp path via $VIAISP" | tee -a $DIAGNOSE
        exit ${iptables_result}
    else
        echo $(date) "SUCCESS: OK to  prepare isp path via $VIAISP" | tee -a $DIAGNOSE
    fi
fi

#==================================================================
# 2. 
echo "----------------------------------------------------------------------"
traceroute $OPTIONS

#==================================================================
# 3.
if [[ $FLOWMARK != 'TOLAN' ]]
then
    echo "----------------------------------------------------------------------"
    iptables -t mangle -D OUTPUT -j MARK --set-mark $FLOWMARK

    iptables_result=$?

    if [[ ${iptables_result} != '0' ]]
    then
        echo $(date) "ERROR: Fail to remove isp path via $VIAISP" | tee -a $DIAGNOSE
        exit ${iptables_result}
    else
        echo $(date) "SUCCESS: OK to remove isp path via $VIAISP" | tee -a $DIAGNOSE
    fi
    echo "----------------------------------------------------------------------"
fi
