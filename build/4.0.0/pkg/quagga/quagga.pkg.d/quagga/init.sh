if [ ! -f /usr/sbin/zebra ];then
 ln -s /opt/qb/quagga/sbin/zebra /usr/sbin/ 
 ln -s /opt/qb/quagga/sbin/ripd /usr/sbin/ 
 ln -s /opt/qb/quagga/sbin/ospfd /usr/sbin/ 
 ln -s /mnt/extra/usr/lib/quagga /usr/lib/
fi

ln -s /opt/qb/quagga/init/zebra /etc/init.d/
ln -s /opt/qb/quagga/init/ripd /etc/init.d/
ln -s /opt/qb/quagga/init/ospfd /etc/init.d/
ln -s /opt/qb/quagga/etc/quagga /etc/
ln -s /opt/qb/quagga/etc/sysconfig/quagga /etc/sysconfig/quagga
echo "quagga:!!:15313::::::" >>/etc/shadow
echo "quagga:x:92:92:Quagga routing suite:/var/run/quagga:/sbin/nologin" >>/etc/passwd
echo "quaggavt:x:85:" >>/etc/group
echo "quagga:x:92:" >>/etc/group
mkdir /var/log/quagga
chmod 764  /var/log/quagga
chown quagga:quagga /var/log/quagga
mkdir /var/run/quagga
chmod 764  /var/run/quagga
chown quagga:quagga /var/run/quagga
