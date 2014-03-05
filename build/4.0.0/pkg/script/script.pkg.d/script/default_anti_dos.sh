#!/bin/bash
#/usr/local/sbin/iptables -t filter -F FORWARD
#/usr/local/sbin/iptables -t filter -A FORWARD -p tcp --syn -m fuzzy --lower-limit 1500 --upper-limit 2000 -j DROP
