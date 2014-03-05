#!/bin/sh

date=`date +%Y%m%d`
tar zcvf /u1/QBbackup.$date.tar.gz /u1/Project.Q-Balancer
split --bytes=728760320 /u1/QBbackup.$date.tar.gz /u1/QBbackup.$date.
rm -rf /u1/QBbackup.$date.tar.gz

