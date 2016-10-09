#!/bin/sh
export DISPLAY=:0.0
sleep 20
killall feh
feh -Y -x -q -D 10 -B black -F -Z -z -r /home/pi/pricing/activepricing/
