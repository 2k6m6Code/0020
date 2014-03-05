set -x
QB_EXPORT_DIR=/usr/local/apache/qb/export

unalias cp
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

cd /root/.ssh/
cp id_rsa.pub qbkey
tar cf qbkey.tar qbkey
mcrypt qbkey.tar -p -k 42084021 >/dev/null 2>&1
mv qbkey.tar.bz2.nc qbkey.crt
chmod 644 qbkey.crt
mkdir $QB_EXPORT_DIR 
mv qbkey.crt $QB_EXPORT_DIR
rm -f qb*
echo $(date -R) "Download QB Managerment Key...";

