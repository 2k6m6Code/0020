#!/bin/sh
name=$1
echo reset > /proc/net/ipt_account/$name
