#set -x

mask_value=$1
systemip=$2
interface=$3
gateway=$4
status=$5

case $mask_value in
      24)
         mask='255.255.255.0'
	 ;;
      25)
         mask='255.255.255.128'
	 ;;
      26)
         mask='255.255.255.192'
	 ;;
      27)
         mask='255.255.255.224'
	 ;;
      28)
         mask='255.255.255.240'
	 ;;
      29)
         mask='255.255.255.248'
	 ;;
      30)
         mask='255.255.255.252'
	 ;;
      31)
         mask='255.255.255.254'
	 ;;
      32)
         mask='255.255.255.255'
	 ;;
esac
IPALIAS="/tmp/ipalias"

/sbin/ifconfig $interface $systemip netmask $mask broadcast $gateway $status
if [ ! -f $IPALIAS ]; then
    touch /tmp/ipalias
fi

grep -v "$interface" /tmp/ipalias >/tmp/_ipalias
cp -a /tmp/_ipalias /tmp/ipalias
rm -rf /tmp/_ipalias

if [ -f $IPALIAS ]; then
    echo "/sbin/ifconfig $interface $systemip netmask $mask broadcast $gateway $status">>/tmp/ipalias
fi

