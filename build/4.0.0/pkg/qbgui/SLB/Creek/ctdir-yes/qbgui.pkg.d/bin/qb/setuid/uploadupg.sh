#!/bin/bash
num=$1
echo "Select $num"
rm -f /tmp/$num/*.upg
mv /tmp/tmpupg/*.upg /tmp/$num
rm -f /tmp/tmpupg/*.upg
