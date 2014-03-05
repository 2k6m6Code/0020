if [ ! -d /root/.ssh ]; then
    mkdir /root/.ssh
fi
#cat /tmp/tmpupg/upload.tmp >> /root/.ssh/authorized_keys 
cd /tmp/tmpupg/
rm -f /tmp/tmpupg/qb*
mv upload.tmp qbkey.bz2
cp -a qbkey.bz2 /mnt/conf/
if [ -f qbkey.bz2 ]; then
    mcrypt qbkey.bz2 -d -k 42084021 >/dev/null 2>&1
else
    echo "Error: Upload fail!!"
fi
tar jxf qbkey.bz2.dc
cat qbkey >> /root/.ssh/authorized_keys
rm -f /tmp/tmpupg/qb*
echo $(date -R) "Upload QB Managerment Key...";
sync && sync
