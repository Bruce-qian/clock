#!/bin/bash
#Description
# this script will find pid and kill a process
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/clock
export PATH
echo 'kill'
kill -2 $(ps aux | grep 'clockback' | grep -v 'grep' | awk '{print $2}')
