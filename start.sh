#!/bin/bash
# Add this to cron
# PROJ_PATH = /home/pi/projcets/Album_Artwork_Display
# LOG_PATH  = $PROJ_PATH/logs
# @reboot $PROJ_PATH/start.sh > $LOG_PATH/Album-Display.log

DISPLAY=:0 xrandr --output HDMI-1 --rotate right
cd $PROJ_PATH
python album_display.py