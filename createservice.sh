#!/bin/bash
#Description:
# this script will create systemd service
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/clock
export PATH
dir=$(pwd)
echo -e "[Unit]
Description=clock service
[Service]
Type=simple
KillMode=none
ExecStart=/usr/bin/python3 ${dir}/bin/clockback.py
ExecStop=/bin/bash ${dir}/stop.sh
[Install]
WantedBy=multi-user.target" > /etc/systemd/system/clockd.service
chmod +x /etc/systemd/system/clockd.service
systemctl daemon-reload