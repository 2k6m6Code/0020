#set -x

#limit_time=`date -d '30 min'`
#limit_time_s=`date --date="$limit_time" +%s`


limit_time_s=$1


now_time_s=`date +%s`
The_remaining_time_s=`expr $limit_time_s - $now_time_s`
The_remaining_time_min=`expr $The_remaining_time_s / 60`
echo $The_remaining_time_min
