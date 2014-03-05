/usr/local/sbin/iptables -t nat -D PREROUTING -p udp --dport 53 -s 192.168.1.0/24 -m time --timestart 9:00 --timestop 18:00 --days Mon,Tue,Wed,Thu,Fri -j REDIRECT --to-port 2500
/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  -s 0.0.0.0/0 -m state --state NEW -j CTDIRMARK --set-mark_original 0xA81E2715
/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  -s 0.0.0.0/0 -m ctdirmark --mark_original 0xA81E2715 -j MARK --set-mark 0xA81E2715
/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  -s 192.168.1.0/24 -m state --state NEW -j CTDIRMARK --set-mark_original 0xA81E271F
/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  -s 192.168.1.0/24 -m ctdirmark --mark_original 0xA81E271F -j MARK --set-mark 0xA81E271F
/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  -s 0.0.0.0/0 -m state --state REPLY -m ctdirmark ! --mark_reply 0xA01E271A -j CTDIRMARK --set-mark_reply 0xA01E271A
/sbin/iptables -t mangle -D OUTPUT -p udp --dport 53  -s 0.0.0.0/0 -m ctdirmark --mark_reply 0xA01E271A -j MARK --set-mark 0xA01E271A
