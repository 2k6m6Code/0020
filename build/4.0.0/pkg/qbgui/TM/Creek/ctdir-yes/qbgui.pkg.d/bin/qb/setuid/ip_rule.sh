#set -x

action=$1
alias_ip=$2
isp_iid=$3

table_num=$((100+$isp_iid))
    
/sbin/ip rule $action from $alias_ip table $table_num prio 30000

