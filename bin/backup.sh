#!/bin/sh

rsync -avz -e ssh --delete /p1 /BACKUP/192.168.1.175
rsync -avz -e ssh --delete /p2 /BACKUP/192.168.1.175

