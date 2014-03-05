#!/bin/sh

ACTION=$*

case "$ACTION" in
	on)
	    rm /usr/local
	    ln -s /u1/Project.Q-Balancer/qbfs/usr/local /usr/local
	    ;;

	off)
	    rm /usr/local
	    ln -s /zone/usr/local /usr/local
	    ;;
	*)
	    echo "Usage : $0 [on|off]"
	    exit 1
	    ;;
esac

