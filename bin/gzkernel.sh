#!/bin/sh

date=`date +%Y%m%d`
tar zcvf /home/BACKUP/QBkernel.$date.tar.gz /home/QBPL/KERNEL
split --bytes=728760320 /home/BACKUP/QBkernel.$date.tar.gz /home/BACKUP/QBkernel.$date.
rm -rf /home/BACKUP/QBkernel.$date.tar.gz

