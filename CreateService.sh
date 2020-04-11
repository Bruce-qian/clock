#!/bin/bash
#Description:
# this script will create systemd serverce
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/clock
export PATH
dir=$(pwd)
echo -e "[Unit]
Description=clock service
[Service]
Type=simple
ExecStart=/usr/bin/python3 ${dir}/bin/clockback.py
ExecStop=/bin/sh ~/clock/stop.sh
KillMode=process
[Install]
WantedBy=multi-user.target" > /etc/systemd/system/clockd.service
chmod +x /etc/systemd/system/clockd.service
systemctl daemon-reload